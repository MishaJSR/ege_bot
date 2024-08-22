import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, ChatMemberUpdatedFilter, KICKED, Command
from aiogram.types import ChatMemberUpdated

from handlers.user.state import UserState
from handlers.user.utils import *
from keyboards.user.inline_user import get_inline_channel, get_inline_about
from keyboards.user.reply_user import *
from utils.common.static_user import *

user_private_router = Router()


#
# @user_private_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
# async def user_blocked_bot(event: ChatMemberUpdated):
#     data = {
#         "user_id": 548349299
#     }
#     res = await UserRepository().update_fields(data=data)
#

@user_private_router.message(Command("test"))
async def user_blocked_bot(message: types.Message, state: FSMContext):
    data = {
        "user_id": 548349299
    }
    res = await UserRepository().u(data=data)
    print(res)


@user_private_router.message(StateFilter(UserState), F.text == BACK_BUTTON)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == UserState.start:
        await message.answer('Предыдущего шага нет')
        return

    if current_state == UserState.answer_mode:
        await message.answer("Вы вернулись к прошлому шагу")
        UserState.index_now_under_chapter = 0
        await go_to_under_chapters(message=message, user_state=UserState)
        await state.set_state(UserState.under_chapter)
        return

    if current_state == UserState.under_chapter:
        res = await message.bot.get_chat_member(chat_id='@humanitiessociety', user_id=message.from_user.id)
        if res.status.value not in ['member', 'creator']:
            await message.answer(TEXT_NOT_SUBSCRIBE_CHANNEL, reply_markup=get_inline_channel())
            return
        await message.answer("Вы вернулись к прошлому шагу")
        await message.answer(TEXT_CHAPTER, reply_markup=chapter_kb(data=UserState.list_of_chapters))
        await state.set_state(UserState.chapter)
        return

    previous = None
    for step in UserState.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому шагу")
            await message.answer(f"{UserState.texts[previous.state][0]}",
                                 reply_markup=UserState.texts[previous.state][1]())
            return
        previous = step


@user_private_router.message(CommandStart())
async def user_start(message: types.Message, state: FSMContext):
    username = await check_user(user_id=message.from_user.id)
    if username:
        await message.answer(f"Привет {username}")
    else:
        await add_new_user(
            user_id=message.from_user.id,
            username=message.from_user.full_name,
        )
        await message.answer(f"Привет {message.from_user.full_name}")
    await message.answer(GREETING, reply_markup=start_user_kb())
    await state.set_state(UserState.start)


@user_private_router.message(UserState.start, F.text)
async def user_press_start_train(message: types.Message, state: FSMContext):
    await message.answer(TEXT_MAIN_CHAPTER, reply_markup=main_chapter_kb())
    await state.set_state(UserState.main_chapter)


@user_private_router.message(UserState.main_chapter, F.text)
async def user_press_main_chapter(message: types.Message, state: FSMContext):
    UserState.list_of_chapters = await get_all_chapters()
    await message.answer(TEXT_CHAPTER, reply_markup=chapter_kb(data=UserState.list_of_chapters))
    await state.set_state(UserState.chapter)


@user_private_router.message(UserState.chapter, F.text)
async def user_press_chapter(message: types.Message, state: FSMContext):
    res = await message.bot.get_chat_member(chat_id='@humanitiessociety', user_id=message.from_user.id)
    if res.status.value not in ['member', 'creator']:
        await message.answer(TEXT_NOT_SUBSCRIBE_CHANNEL, reply_markup=get_inline_channel())
        return
    if message.text not in UserState.list_of_chapters:
        await message.answer(DONT_UNDERSTAND)
        return
    UserState.list_of_under_chapters = await get_all_under_chapters(chapter=message.text)
    UserState.list_of_under_chapters = split_array(UserState.list_of_under_chapters, 6)
    await go_to_under_chapters(message=message, user_state=UserState)
    await state.set_state(UserState.under_chapter)


@user_private_router.message(UserState.under_chapter, F.text == RETURN_BUTTON)
async def user_press_under_chapter_return(message: types.Message):
    UserState.index_now_under_chapter -= 1
    await update_under_chapters(message=message, user_state=UserState)


@user_private_router.message(UserState.under_chapter, F.text == MORE_BUTTON)
async def user_press_under_chapter_more(message: types.Message):
    UserState.index_now_under_chapter += 1
    await update_under_chapters(message=message, user_state=UserState)


@user_private_router.message(UserState.under_chapter, F.text)
async def user_press_under_chapter(message: types.Message, state: FSMContext):
    if message.text not in UserState.list_of_under_chapters[UserState.index_now_under_chapter]:
        await message.answer(DONT_UNDERSTAND)
        return
    UserState.select_under_chapter = message.text
    await message.answer(TEXT_ANSWER_MODE, reply_markup=answer_mode_kb())
    await state.set_state(UserState.answer_mode)


@user_private_router.message(UserState.answer_mode, F.text)
async def user_press_answer_mode(message: types.Message, state: FSMContext):
    if message.text not in answer_mode_list:
        await message.answer(DONT_UNDERSTAND)
        return
    if message.text == answer_mode_list[0]:
        await message.answer(DONT_UNDERSTAND)
        return
    else:
        UserState.questions = await get_questions(under_chapter=UserState.select_under_chapter)
        await message.answer(TEXT_INTRODUCE_TEST, reply_markup=ready_test_kb())
        await state.set_state(UserState.answer_prepare)


@user_private_router.message(UserState.answer_prepare, F.text == TEXT_READY_TEST)
async def user_press_ready_to_test(message: types.Message, state: FSMContext):
    await message.answer(TEXT_START_TEST, reply_markup=ReplyKeyboardRemove())
    await send_question(message=message, user_state=UserState, state=state)
    await state.set_state(UserState.answers_checker)


@user_private_router.message(UserState.answers_checker, F.text != NEXT_BUTTON)
async def user_first_test(message: types.Message):
    if not message.text.isdigit():
        await message.answer(DONT_UNDERSTAND)
        await message.answer(SHORT_INTRODUCE_TEST)
        return
    if sorted(list(message.text)) == sorted(list(UserState.now_question.answer)):
        await message.answer(SUCCESS_TEST, reply_markup=next_kb(), parse_mode="Markdown")
    else:
        text_to_send = f"{NOT_SUCCESS_TEST}{UserState.now_question.answer}\n\n"
        await message.answer(text_to_send, reply_markup=next_kb(), parse_mode="Markdown")
    if UserState.now_question.about:
        mess = await message.answer(SHOW_ABOUT_TEXT, reply_markup=get_inline_about())
        UserState.last_message_id = mess.message_id


@user_private_router.message(UserState.answers_checker, F.text == NEXT_BUTTON)
async def user_press_next_test(message: types.Message, state: FSMContext):
    if UserState.last_message_id:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=UserState.last_message_id)
    UserState.last_message_id = None
    await send_question(message=message, user_state=UserState, state=state)


@user_private_router.callback_query(lambda call: call.data == CALLBACK_SHOW_ABOUT)
async def check_button(call: types.CallbackQuery):
    await call.message.delete()
    UserState.last_message_id = None
    await call.answer("Пояснение")
    await call.message.answer(f"{ABOUT_TEST}{UserState.now_question.about}", parse_mode="Markdown")
