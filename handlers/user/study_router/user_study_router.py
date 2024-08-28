import re

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter

from handlers.user.state import UserState
from handlers.user.study_router.state import UserStudyState
from handlers.user.utils import *
from keyboards.user.inline_user import get_inline_channel, get_inline_about
from keyboards.user.reply_user import *
from utils.common.static_url import channel
from utils.common.static_user import *

user_study_router = Router()


@user_study_router.message(StateFilter(UserStudyState), F.text == BACK_BUTTON)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    print(current_state)

    if current_state == UserStudyState.main_chapter:
        await state.set_state(UserState.start)
        await message.answer(GREETING, reply_markup=start_user_kb())
        return

    if current_state == UserStudyState.answer_mode:
        await message.answer("Вы вернулись к прошлому шагу")
        UserStudyState.index_now_under_chapter = 0
        await go_to_under_chapters(message=message, user_state=UserStudyState)
        await state.set_state(UserStudyState.under_chapter)
        return

    if current_state == UserStudyState.under_chapter:
        res = await message.bot.get_chat_member(chat_id=channel, user_id=message.from_user.id)
        if res.status.value not in ['member', 'creator']:
            await message.answer(TEXT_NOT_SUBSCRIBE_CHANNEL, reply_markup=get_inline_channel())
            return
        await message.answer("Вы вернулись к прошлому шагу")
        await message.answer(TEXT_CHAPTER, reply_markup=chapter_kb(data=UserStudyState.list_of_chapters))
        await state.set_state(UserStudyState.chapter)
        return

    previous = None
    for step in UserStudyState.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому шагу")
            await message.answer(f"{UserStudyState.texts[previous.state][0]}",
                                 reply_markup=UserStudyState.texts[previous.state][1]())
            return
        previous = step





@user_study_router.message(UserStudyState.main_chapter, F.text)
async def user_press_main_chapter(message: types.Message, state: FSMContext):
    UserStudyState.list_of_chapters = await get_all_chapters()
    await message.answer(TEXT_CHAPTER, reply_markup=chapter_kb(data=UserStudyState.list_of_chapters))
    await state.set_state(UserStudyState.chapter)


@user_study_router.message(UserStudyState.chapter, F.text)
async def user_press_chapter(message: types.Message, state: FSMContext):
    res = await message.bot.get_chat_member(chat_id=channel, user_id=message.from_user.id)
    if res.status.value not in ['member', 'creator']:
        await message.answer(TEXT_NOT_SUBSCRIBE_CHANNEL, reply_markup=get_inline_channel())
        return
    if message.text not in UserStudyState.list_of_chapters:
        await message.answer(DONT_UNDERSTAND)
        return
    UserStudyState.list_of_under_chapters = await get_all_under_chapters(chapter=message.text)
    UserStudyState.list_of_under_chapters = split_array(UserStudyState.list_of_under_chapters, 6)
    await go_to_under_chapters(message=message, user_state=UserStudyState)
    await state.set_state(UserStudyState.under_chapter)


@user_study_router.message(UserStudyState.under_chapter, F.text == RETURN_BUTTON)
async def user_press_under_chapter_return(message: types.Message):
    UserStudyState.index_now_under_chapter -= 1
    await update_under_chapters(message=message, user_state=UserStudyState)


@user_study_router.message(UserStudyState.under_chapter, F.text == MORE_BUTTON)
async def user_press_under_chapter_more(message: types.Message):
    UserStudyState.index_now_under_chapter += 1
    await update_under_chapters(message=message, user_state=UserStudyState)


@user_study_router.message(UserStudyState.under_chapter, F.text)
async def user_press_under_chapter(message: types.Message, state: FSMContext):
    if message.text not in UserStudyState.list_of_under_chapters[UserStudyState.index_now_under_chapter]:
        await message.answer(DONT_UNDERSTAND)
        return
    UserStudyState.select_under_chapter = message.text
    await message.answer(TEXT_ANSWER_MODE, reply_markup=answer_mode_kb())
    await state.set_state(UserStudyState.answer_mode)


@user_study_router.message(UserStudyState.answer_mode, F.text)
async def user_press_answer_mode(message: types.Message, state: FSMContext):
    if message.text not in answer_mode_list:
        await message.answer(DONT_UNDERSTAND)
        return
    if message.text == answer_mode_list[0]:
        await send_theory(message, UserStudyState)
        await message.answer(END_THEORY, reply_markup=answer_mode_kb())
        await state.set_state(UserStudyState.answer_mode)
    else:
        UserStudyState.questions = await get_questions(under_chapter=UserStudyState.select_under_chapter)
        await message.answer(TEXT_INTRODUCE_TEST, reply_markup=ready_test_kb())
        await state.set_state(UserStudyState.answer_prepare)


@user_study_router.message(UserStudyState.answer_prepare, F.text == TEXT_READY_TEST)
async def user_press_ready_to_test(message: types.Message, state: FSMContext):
    await message.answer(TEXT_START_TEST, reply_markup=ReplyKeyboardRemove())
    await send_question(message=message, user_state=UserStudyState, state=state)
    await state.set_state(UserStudyState.answers_checker)


@user_study_router.message(UserStudyState.answers_checker, F.text != NEXT_BUTTON)
async def user_first_test(message: types.Message):
    if not message.text.isdigit():
        await message.answer(DONT_UNDERSTAND)
        await message.answer(SHORT_INTRODUCE_TEST)
        return
    if sorted(list(message.text)) == sorted(list(UserStudyState.now_question.answer)):
        await update_progress(status=True, message=message, now_question=UserStudyState.now_question)
        await message.answer(SUCCESS_TEST, reply_markup=next_kb(), parse_mode=ParseMode.HTML)
    else:
        await update_progress(status=False, message=message, now_question=UserStudyState.now_question)
        text_to_send = f"{NOT_SUCCESS_TEST}{UserStudyState.now_question.answer}\n\n"
        await message.answer(text_to_send, reply_markup=next_kb(), parse_mode=ParseMode.HTML)
    if UserStudyState.now_question.about:
        mess = await message.answer(SHOW_ABOUT_TEXT, reply_markup=get_inline_about())
        UserStudyState.last_message_id = mess.message_id


@user_study_router.message(UserStudyState.answers_checker, F.text == NEXT_BUTTON)
async def user_press_next_test(message: types.Message, state: FSMContext):
    if UserStudyState.last_message_id:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=UserStudyState.last_message_id)
    UserStudyState.last_message_id = None
    await send_question(message=message, user_state=UserStudyState, state=state)


@user_study_router.callback_query(lambda call: call.data == CALLBACK_SHOW_ABOUT)
async def check_button(call: types.CallbackQuery):
    await call.message.delete()
    UserStudyState.last_message_id = None
    await call.answer("Пояснение")
    about = UserStudyState.now_question.about
    try:
        if UserStudyState.now_question.about[:2] == "1.":
            result = re.split(r'\s*\d+\.\s*', UserStudyState.now_question.about.strip())[1:]
            for index, line in enumerate(result):
                result[index] = f"{index+1}. {line}"
            about = "\n".join(result)
    except Exception as e:
        logging.info(e)
        logging.info(f"Error in about {UserStudyState.now_question.about}")
        about = UserStudyState.now_question.about
    await call.message.answer(f"{ABOUT_TEST}{about}", parse_mode=ParseMode.HTML)