import os
from aiogram.filters import Command, StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_task, get_all_users, find_task, delete_task
from keyboards.user.reply import start_kb
from keyboards.admin.reply_admin import start_kb, back_kb, exam_kb, chapter_kb, answers_kb, answers_kb_end, about_kb, \
    answer_kb, reset_kb, send_img_kb
from handlers.admin.states.states import Admin_state, AdminStateSender, AdminStateDelete

admin_private_router = Router()
load_dotenv(find_dotenv())
admin = int(os.getenv('ADMIN_ID'))


@admin_private_router.message(Command('admin'))
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Привет админ', reply_markup=start_kb())
    await state.set_state(Admin_state.start)


@admin_private_router.message(StateFilter('*'), Command("назад"))
@admin_private_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == Admin_state.start:
        await message.answer('Предыдущего шага нет')
        return

    previous = None
    for step in Admin_state.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n{Admin_state.texts[previous.state][0]}",
                                 reply_markup=Admin_state.texts[previous.state][1]())
            return
        previous = step


@admin_private_router.message(F.text == 'Отмена')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Вы вернулись в основное меню', reply_markup=start_kb())
    await state.set_state(Admin_state.start)


@admin_private_router.message(F.text == 'Отправить рассылку')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Напишите текст рассылки', reply_markup=reset_kb())
    await state.set_state(AdminStateSender.text_state)


@admin_private_router.message(AdminStateSender.text_state)
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminStateSender.text = message.text
    await message.answer(text='Отправьте изображение', reply_markup=send_img_kb())
    await state.set_state(AdminStateSender.image_state)


@admin_private_router.message(AdminStateSender.image_state)
async def process_photo(message: types.Message, state: FSMContext):
    await message.answer_photo(caption=AdminStateSender.text, photo=message.photo[-1].file_id,
                               reply_markup=answers_kb_end())
    AdminStateSender.photo = message.photo[-1].file_id
    await message.answer(text='Все верно?')
    await state.set_state(AdminStateSender.confirm_state)


@admin_private_router.message(AdminStateSender.confirm_state)
async def process_photo(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text == 'Подтвердить':
        res = await get_all_users(session)
        await message.answer(text="Начало рассылки")
        for user in res:
            await message.bot.send_photo(chat_id=user._mapping['user_id'], photo=AdminStateSender.photo,
                                         caption=AdminStateSender.text)
        await message.answer(text="Рассылка завершена")
    else:
        await message.answer(text="Ошибка рассылки")
    await state.set_state(Admin_state.start)


@admin_private_router.message(F.text == 'Удалить задание')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer('Введите часть из описания задания', reply_markup=reset_kb())
    await state.set_state(AdminStateDelete.find_key)


@admin_private_router.message(AdminStateDelete.find_key)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await find_task(session, message.text)
        if len(res) == 0:
            await message.answer('Ничего не нашлось, попробуйте еще раз')
            await state.set_state(Admin_state.find_key)
            return
        for ind, el in enumerate(res):
            AdminStateDelete.data.append(el._data[0].description)
            await message.answer(f'{ind}: {el._data[0].description}\n')
    except:
        await message.answer('Ошибка поиска', reply_markup=start_kb())
        await state.set_state(Admin_state.start)
        return
    await message.answer('Введите номер задания который вы хотите удалить', reply_markup=reset_kb())
    await state.set_state(AdminStateDelete.confirm_delete)


@admin_private_router.message(AdminStateDelete.confirm_delete)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        des_del = AdminStateDelete.data[int(message.text)]
        await delete_task(session, des_del)
    except:
        await message.answer('Ошибка удаления', reply_markup=start_kb())
        await state.set_state(Admin_state.start)
        return
    await message.answer('Задание удалено', reply_markup=start_kb())
    await state.set_state(Admin_state.start)


@admin_private_router.message(F.text == 'Добавить задание')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer('Выберите раздел подготовки', reply_markup=exam_kb())
    await state.set_state(Admin_state.exam)


@admin_private_router.message(Admin_state.exam)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.data = Admin_state.default_data.copy()
    Admin_state.data['exam'] = message.text
    await message.answer('Выберите модуль', reply_markup=chapter_kb())
    await state.set_state(Admin_state.chapter)


@admin_private_router.message(Admin_state.chapter)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.data['chapter'] = message.text
    await message.answer('Напишите название подмодуля', reply_markup=back_kb())
    await state.set_state(Admin_state.under_chapter)


@admin_private_router.message(Admin_state.under_chapter)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.data['under_chapter'] = message.text
    await message.answer('Напишите условие задания', reply_markup=back_kb())
    await state.set_state(Admin_state.description)


@admin_private_router.message(Admin_state.description)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.data['description'] = message.text
    await message.answer('Напишите вариант ответа', reply_markup=back_kb())
    await state.set_state(Admin_state.answers)


@admin_private_router.message(Admin_state.answers)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.data['answers'] = ''
    Admin_state.data['answers'] = message.text
    await message.answer('Введите следующий вариант ответа', reply_markup=answers_kb())
    await state.set_state(Admin_state.answers_swap)


@admin_private_router.message(Admin_state.answers_swap)
async def fill_admin_state(message: types.Message, state: FSMContext):
    if message.text == 'Закончить ввод':
        mass = Admin_state.data['answers'].split('` ')
        await message.answer('Вы ввели:')
        for ind, el in enumerate(mass):
            await message.answer(f'{ind + 1}. {el}')
        await message.answer('Все правильно?', reply_markup=answers_kb_end())
        await state.set_state(Admin_state.answers_checker)
    else:
        Admin_state.data['answers'] += '` ' + message.text
        await message.answer('Введите следующий вариант ответа', reply_markup=answers_kb())
        await state.set_state(Admin_state.answers_swap)


@admin_private_router.message(Admin_state.answers_checker)
async def fill_admin_state(message: types.Message, state: FSMContext):
    if message.text == 'Подтвердить':
        await message.answer('Введите ответ на вопрос', reply_markup=answer_kb())
        await state.set_state(Admin_state.answer)
    else:
        Admin_state.data['answers'] = ''
        await state.set_state(Admin_state.answers_swap)
        await message.answer('Заново', reply_markup=answers_kb())


@admin_private_router.message(Admin_state.answer)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.data['answer'] = message.text
    await message.answer('Введите обьяснение', reply_markup=about_kb())
    await state.set_state(Admin_state.about)


@admin_private_router.message(Admin_state.about)
async def fill_admin_state(message: types.Message, state: FSMContext):
    if message.text == 'Оставить пустым':
        Admin_state.data['about'] = ''
    else:
        Admin_state.data['about'] = message.text
    await message.answer('Вы ввели:\n')
    for key, el in Admin_state.data.items():
        await message.answer(f'{key}: {el}\n')
    await message.answer('Все правильно?', reply_markup=answers_kb_end())
    await state.set_state(Admin_state.check_info)


@admin_private_router.message(Admin_state.check_info)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text == 'Подтвердить':
        try:
            await orm_add_task(session, Admin_state.data)
            await message.answer('Успешное добавление', reply_markup=start_kb())
        except:
            await message.answer('Неудачное добавление', reply_markup=start_kb())
        await state.set_state(Admin_state.start)
