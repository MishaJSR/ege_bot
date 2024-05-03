from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_task, orm_transport_base
from keyboards.user.reply_user import start_kb
from keyboards.admin.reply_admin import start_kb, answers_kb_end, about_kb, answers_kb, \
    answer_kb, back_kb, chapter_kb, exam_kb
from handlers.admin.states import Admin_state

admin_add_task_router = Router()


@admin_add_task_router.message(F.text == 'Добавить задание')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer('Выберите раздел подготовки', reply_markup=exam_kb())
    await state.set_state(Admin_state.exam)


@admin_add_task_router.message(F.text == 'Update tables')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        await orm_transport_base(session)
    except:
        await message.answer('Error')
    await message.answer('Successfully')


@admin_add_task_router.message(Admin_state.exam)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.data = Admin_state.default_data.copy()
    Admin_state.data['exam'] = message.text
    await message.answer('Выберите модуль', reply_markup=chapter_kb())
    await state.set_state(Admin_state.chapter)


@admin_add_task_router.message(Admin_state.chapter)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.data['chapter'] = message.text
    await message.answer('Напишите название подраздела', reply_markup=back_kb())
    await state.set_state(Admin_state.under_chapter)


@admin_add_task_router.message(Admin_state.under_chapter)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.data['under_chapter'] = message.text
    await message.answer('Напишите условие задания', reply_markup=back_kb())
    await state.set_state(Admin_state.description)


@admin_add_task_router.message(Admin_state.description)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.data['description'] = message.text
    await message.answer('Напишите вариант ответа', reply_markup=back_kb())
    await state.set_state(Admin_state.answers)


@admin_add_task_router.message(Admin_state.answers)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.data['answers'] = ''
    Admin_state.data['answers'] = message.text
    await message.answer('Введите следующий вариант ответа', reply_markup=answers_kb())
    await state.set_state(Admin_state.answers_swap)


@admin_add_task_router.message(Admin_state.answers_swap)
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


@admin_add_task_router.message(Admin_state.answers_checker)
async def fill_admin_state(message: types.Message, state: FSMContext):
    if message.text == 'Подтвердить':
        await message.answer('Введите ответ на вопрос', reply_markup=answer_kb())
        await state.set_state(Admin_state.answer)
    else:
        Admin_state.data['answers'] = ''
        await state.set_state(Admin_state.answers_swap)
        await message.answer('Заново', reply_markup=answers_kb())


@admin_add_task_router.message(Admin_state.answer)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.data['answer'] = message.text
    await message.answer('Введите обьяснение', reply_markup=about_kb())
    await state.set_state(Admin_state.about)


@admin_add_task_router.message(Admin_state.about)
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


@admin_add_task_router.message(Admin_state.check_info)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text == 'Подтвердить':
        try:
            await orm_add_task(session, Admin_state.data)
            await message.answer('Успешное добавление', reply_markup=start_kb())
        except:
            await message.answer('Неудачное добавление', reply_markup=start_kb())
        await state.set_state(Admin_state.start)
