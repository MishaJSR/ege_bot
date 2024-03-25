import os

from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from dotenv import find_dotenv, load_dotenv
from aiogram.fsm.state import StatesGroup, State

from database.orm_query import orm_add_task
from keyboards.reply import start_kb, del_keyboard
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task
admin_private_router = Router()
load_dotenv(find_dotenv())
admin = int(os.getenv('ADMIN_ID'))




class Tasks_state(StatesGroup):
    subj = State()
    exam = State()
    chapter = State()
    description = State()
    answer_mode = State()
    answer = State()
    texts = {
        'Tasks_state:subj': 'Введите предмет заново',
        'Tasks_state:exam': 'Введите экзамен заново',
        'Tasks_state:chapter': 'Введите главу заново',
        'Tasks_state:description': 'Введите описание задания заново',
        'Tasks_state:answer_mode': 'Введите режим ответа заново',
    }


@admin_private_router.message(StateFilter(None), F.text == 'Добавить задание')
async def fill_Tasks_state(message: types.Message, state: FSMContext):
    await message.answer('Привет админ) \nВведите предмет', reply_markup=del_keyboard)
    await state.set_state(Tasks_state.subj)


@admin_private_router.message(StateFilter('*'), Command("назад"))
@admin_private_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == Tasks_state.subj:
        await message.answer('Предыдущего шага нет, или введите название товара или напишите "отмена"')
        return

    previous = None
    for step in Tasks_state.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n{Tasks_state.texts[previous.state]}")
            return
        previous = step


@admin_private_router.message(StateFilter('*'), Command('отмена'))
@admin_private_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def fill_Tasks_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer('Действия отменены')


@admin_private_router.message(Tasks_state.subj, F.text)
async def fill_Tasks_state(message: types.Message, state: FSMContext):
    await state.update_data(subj=message.text)
    await message.answer('Введите экзамен')
    await state.set_state(Tasks_state.exam)


@admin_private_router.message(Tasks_state.exam, F.text)
async def fill_Tasks_state(message: types.Message, state: FSMContext):
    await state.update_data(exam=message.text)
    await message.answer('Введите главу')
    await state.set_state(Tasks_state.chapter)


@admin_private_router.message(Tasks_state.chapter, F.text)
async def fill_Tasks_state(message: types.Message, state: FSMContext):
    await state.update_data(chapter=message.text)
    await message.answer('Введите описание')
    await state.set_state(Tasks_state.description)


@admin_private_router.message(Tasks_state.description, F.text)
async def fill_Tasks_state(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Введите режим ответа\n1 - цифра\n2 - слова')
    await state.set_state(Tasks_state.answer_mode)


@admin_private_router.message(Tasks_state.answer_mode, F.text)
async def fill_Tasks_state(message: types.Message, state: FSMContext):
    await state.update_data(answer_mode=message.text)
    await message.answer('Введите ответ')
    await state.set_state(Tasks_state.answer)


@admin_private_router.message(Tasks_state.answer, F.text)
async def fill_Tasks_state(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    try:
        await orm_add_task(session, data)
        await message.answer('Задание добавлено')
    except Exception as e:
        await message.answer(
            f'Ошибка: \n{str(e)}'
        )
    await state.clear()



