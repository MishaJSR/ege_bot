from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.orm_query import orm_get_chapters
from keyboards.reply import start_kb, chapters_kb, prepare_kb, subj_kb
from sqlalchemy.ext.asyncio import AsyncSession

user_private_router = Router()


#


class UserState(StatesGroup):
    start_choose = State()
    subj_choose = State()
    chapter_choose = State()
    prepare_choose = State()
    texts = {
        'UserState:start_choose': 'Начало работы',
        'UserState:subj_choose': 'Выбираем предметы',
        'UserState:chapter_choose': 'Выбор главы',
        'UserState:prepare_choose': 'Выбрана подготовка',
    }
    kb = {
        'Начало работы': start_kb,
        'Выбираем предметы': subj_kb,
        'Выбор главы': chapters_kb,
        'Выбрана подготовка': prepare_kb,
    }
    last_data = None
    available_params = None


async def check_input(message: types.Message, state):
    if message.md_text not in state.available_params:
        await message.answer(f'Ошибка ввода')
        return False
    else:
        return True


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    await message.answer('Вы запустили бота', reply_markup=start_kb()[0])
    await state.set_state(UserState.start_choose)
    UserState.last_kb, UserState.available_params = start_kb()


@user_private_router.message(StateFilter('*'), F.text == "Назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    print("Назад")
    current_state = await state.get_state()

    if current_state == UserState.start_choose:
        await message.answer('Предыдущего шага нет, или введите название товара или напишите "отмена"',
                             reply_markup=start_kb()[0])
        return

    previous = None
    for step in UserState.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n{UserState.texts[previous.state]}",
                                 reply_markup=UserState.kb[UserState.texts[previous.state]](data=UserState.last_data)[
                                     0])
            UserState.available_params = UserState.kb[UserState.texts[previous.state]](data=UserState.last_data)[1]
            return
        previous = step


@user_private_router.message(Command('about'))
async def start_about(message: types.Message):
    await message.answer('Это бот для подготовки к ЕГЭ')


@user_private_router.message(or_f(Command('payment'), F.text.lower().contains('оплата')))
async def payment(message: types.Message):
    await message.answer('Этот сервис ожидает подключения')


@user_private_router.message(F.text, F.text.lower().contains('привет'))
async def hello_filter(message: types.Message):
    await message.answer('Привет)')


@user_private_router.message(UserState.start_choose, )
async def start_func(message: types.Message, state: FSMContext):
    if not await check_input(message, UserState):
        return
    await message.answer(f'Выберите вариант подготовки', reply_markup=subj_kb()[0])
    UserState.available_params = subj_kb()[1]
    await state.set_state(UserState.subj_choose)


@user_private_router.message(UserState.subj_choose)
async def start_subj(message: types.Message, session: AsyncSession, state: FSMContext):
    if not await check_input(message, UserState):
        return
    chapter_but = []
    subj_text, exam_text = message.text.split(" ")
    try:
        res = await orm_get_chapters(session, target_subj=subj_text, target_exam=exam_text)
        for task in res:
            fields = task._data[0]
            chapter_but.append(fields.chapter)
        if len(res) > 0:
            await message.answer(f'Выберите главу', reply_markup=chapters_kb(chapter_but)[0])
            UserState.available_params = chapters_kb(chapter_but)[1]
            UserState.last_data = chapter_but
            await state.set_state(UserState.chapter_choose)
        else:
            await message.answer(f'Модуль в процессе разработки', reply_markup=start_kb()[0])
    except Exception as e:
        await message.answer(
            f'Ошибка: \n{str(e)}'
        )


@user_private_router.message(UserState.chapter_choose)
async def start_filter(message: types.Message, session: AsyncSession, state: FSMContext):
    if not await check_input(message, UserState):
        return
    await message.answer(f'Выберите режим подготовки', reply_markup=prepare_kb()[0])
    UserState.available_params = prepare_kb()[1]
    await state.set_state(UserState.prepare_choose)
