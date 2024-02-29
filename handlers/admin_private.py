import os

from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from dotenv import find_dotenv, load_dotenv
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import start_kb, del_keyboard, history_kb, subj_kb

admin_private_router = Router()
load_dotenv(find_dotenv())
admin = int(os.getenv('ADMIN_ID'))


class AddTask(StatesGroup):
    subj = State()
    exam = State()
    chapter = State()
    description = State()
    answer_mode = State()
    answer = State()
    texts = {
        'AddTask:subj': 'Введите предмет заново',
        'AddTask:exam': 'Введите экзамен заново',
        'AddTask:chapter': 'Введите главу заново',
        'AddTask:description': 'Введите описание задания заново',
        'AddTask:answer_mode': 'Введите режим ответа заново',
    }


@admin_private_router.message(StateFilter(None), F.chat.id == admin, F.text == 'Добавить задание')
async def fill_task(message: types.Message, state: FSMContext):
    await message.answer('Привет админ) \nВведите предмет', reply_markup=del_keyboard)
    await state.set_state(AddTask.subj)

@admin_private_router.message(StateFilter('*'), Command("назад"))
@admin_private_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddTask.subj:
        await message.answer('Предыдущего шага нет, или введите название товара или напишите "отмена"')
        return

    previous = None
    for step in AddTask.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n{AddTask.texts[previous.state]}")
            return
        previous = step


@admin_private_router.message(StateFilter('*'), F.chat.id == admin, Command('отмена'))
@admin_private_router.message(StateFilter('*'), F.chat.id == admin, F.text.casefold() == 'отмена')
async def fill_task(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer('Действия отменены')




@admin_private_router.message(AddTask.subj, F.chat.id == admin, F.text)
async def fill_task(message: types.Message, state: FSMContext):
    await state.update_data(subj=message.text)
    await message.answer('Введите экзамен')
    await state.set_state(AddTask.exam)


@admin_private_router.message(AddTask.exam, F.chat.id == admin, F.text)
async def fill_task(message: types.Message, state: FSMContext):
    await state.update_data(exam=message.text)
    await message.answer('Введите главу')
    await state.set_state(AddTask.chapter)


@admin_private_router.message(AddTask.chapter, F.chat.id == admin, F.text)
async def fill_task(message: types.Message, state: FSMContext):
    await state.update_data(chapter=message.text)
    await message.answer('Введите описание')
    await state.set_state(AddTask.description)


@admin_private_router.message(AddTask.description, F.chat.id == admin, F.text)
async def fill_task(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Введите режим ответа\n1 - цифра\n2 - слова')
    await state.set_state(AddTask.answer_mode)


@admin_private_router.message(AddTask.answer_mode, F.chat.id == admin, F.text)
async def fill_task(message: types.Message, state: FSMContext):
    await state.update_data(answer_mode=message.text)
    await message.answer('Введите ответ')
    await state.set_state(AddTask.answer)


@admin_private_router.message(AddTask.answer, F.chat.id == admin, F.text)
async def fill_task(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)
    await message.answer('Задание добавлено')
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()

