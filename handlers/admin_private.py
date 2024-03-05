import os

from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from dotenv import find_dotenv, load_dotenv
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import start_kb, del_keyboard, history_kb, subj_kb
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task

admin_private_router = Router()
load_dotenv(find_dotenv())
admin = int(os.getenv('ADMIN_ID'))




class Tasks(StatesGroup):
    subj = State()
    exam = State()
    chapter = State()
    description = State()
    answer_mode = State()
    answer = State()
    texts = {
        'Tasks:subj': 'Введите предмет заново',
        'Tasks:exam': 'Введите экзамен заново',
        'Tasks:chapter': 'Введите главу заново',
        'Tasks:description': 'Введите описание задания заново',
        'Tasks:answer_mode': 'Введите режим ответа заново',
    }


@admin_private_router.message(StateFilter(None), F.text == 'Добавить задание')
async def fill_Tasks(message: types.Message, state: FSMContext):
    await message.answer('Привет админ) \nВведите предмет', reply_markup=del_keyboard)
    await state.set_state(Tasks.subj)


@admin_private_router.message(StateFilter('*'), Command("назад"))
@admin_private_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == Tasks.subj:
        await message.answer('Предыдущего шага нет, или введите название товара или напишите "отмена"')
        return

    previous = None
    for step in Tasks.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n{Tasks.texts[previous.state]}")
            return
        previous = step


@admin_private_router.message(StateFilter('*'), Command('отмена'))
@admin_private_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def fill_Tasks(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer('Действия отменены')


@admin_private_router.message(Tasks.subj, F.text)
async def fill_Tasks(message: types.Message, state: FSMContext):
    await state.update_data(subj=message.text)
    await message.answer('Введите экзамен')
    await state.set_state(Tasks.exam)


@admin_private_router.message(Tasks.exam, F.text)
async def fill_Tasks(message: types.Message, state: FSMContext):
    await state.update_data(exam=message.text)
    await message.answer('Введите главу')
    await state.set_state(Tasks.chapter)


@admin_private_router.message(Tasks.chapter, F.text)
async def fill_Tasks(message: types.Message, state: FSMContext):
    await state.update_data(chapter=message.text)
    await message.answer('Введите описание')
    await state.set_state(Tasks.description)


@admin_private_router.message(Tasks.description, F.text)
async def fill_Tasks(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Введите режим ответа\n1 - цифра\n2 - слова')
    await state.set_state(Tasks.answer_mode)


@admin_private_router.message(Tasks.answer_mode, F.text)
async def fill_Tasks(message: types.Message, state: FSMContext):
    await state.update_data(answer_mode=message.text)
    await message.answer('Введите ответ')
    await state.set_state(Tasks.answer)


@admin_private_router.message(Tasks.answer, F.text)
async def fill_Tasks(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(answer=message.text)
    await message.answer('Задание добавлено')
    data = await state.get_data()
    obj = Task(
        subj=data['subj'],
        exam=data['exam'],
        chapter=data['chapter'],
        description=data['description'],
        answer_mode=data['answer_mode'],
        answer=data['answer']
    )
    session.add(obj)
    await session.commit()
    await message.answer(str(data))
    await state.clear()
