import os

from aiogram.filters import Command, StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from dotenv import find_dotenv, load_dotenv
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ContentType

from database.orm_query import orm_add_task, get_all_users
from keyboards.user.reply import start_kb
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.admin.reply_admin import start_kb, back_kb, exam_kb, chapter_kb, answers_kb, answers_kb_end, about_kb, \
    answer_kb, restart_answer_kb, reset_kb

admin_private_router = Router()
load_dotenv(find_dotenv())
admin = int(os.getenv('ADMIN_ID'))


class Admin_state(StatesGroup):
    start = State()
    exam = State()
    chapter = State()
    under_chapter = State()
    description = State()
    answers_checker = State()
    answers = State()
    answers_swap = State()
    answer = State()
    about = State()
    check_info = State()
    save_in_db = State()
    texts = {
        'Admin_state:start': ['Начало работы', start_kb],
        'Admin_state:exam': ['Выбор части', exam_kb],
        'Admin_state:chapter': ['Выбор модуля', chapter_kb],
        'Admin_state:under_chapter': ['Введите подмодуль', back_kb],
        'Admin_state:description': ['Введите условие задания', back_kb],
        'Admin_state:answers': ['Введите ответы', restart_answer_kb],
        'Admin_state:answers_swap': ['Введите вариант ответа', answers_kb_end],
        'Admin_state:answer': ['Введите ответ на задание', answer_kb],
        'Admin_state:about': ['Введите пояснение', about_kb],
        'Admin_state:check_info': ['Проверка', answers_kb_end],
        'Admin_state:save_in_db': ['Начало работы', start_kb],
    }
    default_data = {
        'exam': None,
        'chapter': None,
        'under_chapter': None,
        'description': None,
        'answers': '',
        'answer_mode': 'Квиз',
        'updated': '2024-03-19 11:44:19',
        'answer': None,
        'about': " ",
        'addition': ' ',
    }
    data = {}


class AdminStateSender(StatesGroup):
    text_state = State()
    image_state = State()
    confirm_state = State()
    texts = {
        'AdminStateSender:text_state': 'Выбор текста',
        'AdminStateSender:image_state': 'Выбор изображения',
        'AdminStateSender:confirm_state': 'Подтверждение',
    }
    text = ''
    photo = None


@admin_private_router.message(Command('admin'))
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Привет админ', reply_markup=start_kb())
    await state.set_state(Admin_state.start)


@admin_private_router.message(StateFilter('*'), Command("назад"))
@admin_private_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == Admin_state.start:
        await message.answer('Предыдущего шага нет, или введите название товара или напишите "отмена"')
        return

    previous = None
    for step in Admin_state.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n{Admin_state.texts[previous.state][0]}",
                                 reply_markup=Admin_state.texts[previous.state][1]())
            return
        previous = step


@admin_private_router.message(F.text == 'Отправить рассылку')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Напишите текст рассылки', reply_markup=reset_kb())
    await state.set_state(AdminStateSender.text_state)


@admin_private_router.message(AdminStateSender.text_state)
async def fill_admin_state(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.set_state(Admin_state.start)
        await message.answer(f"Ок, вы вернулись к прошлому шагу", reply_markup=start_kb())
    else:
        AdminStateSender.text = message.text
        await message.answer(text='Отправьте изображение')
        await state.set_state(AdminStateSender.image_state)


@admin_private_router.message(F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    await message.answer_photo(caption=AdminStateSender.text, photo=message.photo[-1].file_id,
                               reply_markup=answers_kb_end())
    AdminStateSender.photo = message.photo[-1].file_id
    await state.set_state(AdminStateSender.confirm_state)


@admin_private_router.message(AdminStateSender.confirm_state)
async def process_photo(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text == 'Подтвердить':
        res = await get_all_users(session)
        await message.answer(text="Начало рассылки")
        for user in res:
            await message.bot.send_photo(chat_id=user._mapping['user_id'], photo=AdminStateSender.photo, caption=AdminStateSender.text)
        await message.answer(text="Рассылка завершена")
    else:
        await message.answer(text="Ошибка рассылки")
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


# @admin_private_router.message(F.text == 'Закончить ввод')
# async def fill_admin_state(message: types.Message, state: FSMContext):
#     await message.answer('Конецdd', reply_markup=answers_kb())
#     await state.set_state(Admin_state.answer)


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
