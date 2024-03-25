import emoji
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.orm_query import orm_get_modules_task, orm_add_task, orm_get_prepare_module
from keyboards.reply import start_kb, chapters_kb, prepare_kb, subj_kb, module_kb, train_kb, quiz_kb, under_prepare_kb, main_but
from sqlalchemy.ext.asyncio import AsyncSession

user_private_router = Router()


class UserState(StatesGroup):
    start_choose = State()
    subj_choose = State()
    module_choose = State()
    under_prepare_choose = State()
    prepare_choose = State()
    train_choose = State()
    texts = {
        'UserState:start_choose': ['Выберите задание', start_kb],
        'UserState:subj_choose': ['Выбираем предметы', subj_kb],
        'UserState:module_choose': ['Выбрана подготовка', module_kb],
        'UserState:under_prepare_choose': ['Выбрана подготовка', under_prepare_kb],
        'UserState:prepare_choose': ['Выбрана подготовка', prepare_kb],
        'UserState:train_choose': ['Выбрана подготовка', train_kb],
    }
    data = {
        'subj': None,
        'module': None,
        'under_prepare': [],
        'under_prepare_choose': None,
        'prepare': None,
    }
    question_data = []
    now_question = []
    last_kb = None


# async def check_input(message: types.Message, state):
#     if message.md_text not in state.available_params:
#         await message.answer(f'Ошибка ввода')
#         return False
#     else:
#         return True


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    text = 'Привет дорогой друг ' + emoji.emojize(':cat_with_wry_smile:') + '\nВыбери к чему ты бы хотел подготовиться'
    await message.answer(text, reply_markup=start_kb())
    await state.set_state(UserState.start_choose)
    UserState.last_kb = start_kb()


@user_private_router.message(StateFilter('*'), F.text == emoji.emojize(':left_arrow:') + ' Назад')
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    print("Назад")
    current_state = await state.get_state()

    if current_state == UserState.start_choose:
        await message.answer('Предыдущего шага нет, или введите название товара или напишите "отмена"',
                             reply_markup=start_kb())
        return

    previous = None
    for step in UserState.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            if previous.state == 'UserState:under_prepare_choose':
                await message.answer(f"Ок, вы вернулись к прошлому шагу",
                                     reply_markup=UserState.texts[previous.state][1](UserState.data['under_prepare']))
            else:
                await message.answer(f"Вы вернулись к прошлому шагу", reply_markup=UserState.texts[previous.state][1]())
            # await message.answer(f"Ок, вы вернулись к прошлому шагу \n{UserState.texts[previous.state]}",
            #                      reply_markup=UserState.texts[previous.state][1]())
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
    # if not await check_input(message, UserState):
    #     return
    await message.answer(f'Выберите задание к которому Вы бы хотели подготовиться', reply_markup=subj_kb())
    await state.set_state(UserState.subj_choose)


@user_private_router.message(UserState.subj_choose, F.text)
async def start_subj_choose(message: types.Message, state: FSMContext):
    if message.text not in main_but:
        await message.answer(f'Ошибка ввода')
        return
    UserState.data['subj'] = message.text
    await message.answer(f'Выберите модуль для подготовки', reply_markup=module_kb())
    await state.set_state(UserState.module_choose)  #


@user_private_router.message(UserState.module_choose)
async def start_module_choose(message: types.Message, session: AsyncSession, state: FSMContext):
    UserState.data['module'] = message.text
    try:
        res = await orm_get_prepare_module(session, module=UserState.data['module'], exam=UserState.data['subj'])
        UserState.data['under_prepare'] = []
        for task in res:
            UserState.data['under_prepare'].append(task._data[0])
    except Exception as e:
        await message.answer(
            f'Ошибка: \n{str(e)}'
        )
    await message.answer(f'Выберите подраздел', reply_markup=under_prepare_kb(data=UserState.data['under_prepare']))
    await state.set_state(UserState.under_prepare_choose)

@user_private_router.message(UserState.under_prepare_choose)
async def start_under_choose(message: types.Message, session: AsyncSession,  state: FSMContext):
    UserState.data['under_prepare_choose'] = message.text

    await message.answer(f'Выберите вариант подготовки', reply_markup=prepare_kb())
    await state.set_state(UserState.prepare_choose)


@user_private_router.message(UserState.prepare_choose)
async def start_prepare_choose(message: types.Message, session: AsyncSession, state: FSMContext):
    UserState.data['prepare'] = message.text
    try:
        res = await orm_get_modules_task(session,
                                         target_exam=UserState.data['subj'],
                                         target_module=UserState.data['module'],
                                         target_prepare=UserState.data['prepare'],
                                         target_under_prepare=UserState.data['under_prepare_choose'])
        for task in res:
            UserState.question_data.append({
                'description': task._data[0].description,
                'answers': task._data[0].answers,
                'answer': task._data[0].answer,
                'about': task._data[0].about,
                'answer_mode': task._data[0].answer_mode,
                'addition': task._data[0].addition})
            # chapter_but.append(fields.chapter)
    except Exception as e:
        await message.answer(
            f'Ошибка: \n{str(e)}'
        )
    if len(UserState.question_data) == 0:
        await message.answer('Задания еще не добавлены в бота')
    else:
        await cut_stare_and_prepare_answers(message, UserState, state)


@user_private_router.message(UserState.train_choose, F.text)
async def start_train_choose(message: types.Message, session: AsyncSession, state: FSMContext):
    await answer_checker(message, UserState)
    if len(UserState.question_data) == 0:
        await message.answer(f'Вопросы закончились', reply_markup=prepare_kb())
        await state.set_state(UserState.prepare_choose)
    else:
        await cut_stare_and_prepare_answers(message, UserState, state)


async def cut_stare_and_prepare_answers(message, UserState, state):
    UserState.now_question = UserState.question_data[-1]
    UserState.question_data.pop()
    task_to_show = ''
    if UserState.now_question['answer_mode'] == "Квиз":
        task_to_show += UserState.now_question['description'] + '\n' + '\n'
        answer_arr = UserState.now_question['answers'].split("` ")
        for ind, txt in enumerate(answer_arr):
            task_to_show += f'{ind + 1}: {txt}' + '\n'
    await message.answer(task_to_show)
    await message.answer('Введите правильные ответы в формате 135', reply_markup=train_kb())
    await state.set_state(UserState.train_choose)


async def answer_checker(message, UserState):
    if UserState.now_question['answer_mode'] == 'Квиз':
        answer_user = sorted([int(ans) for ans in message.text])
        answer_list = sorted([int(ans) for ans in str(UserState.now_question['answer'])])
    else:
        answer_user = [int(ans) for ans in message.text]
        answer_list = [int(ans) for ans in str(UserState.now_question['answer'])]
    if answer_list == answer_user:
        await message.answer(f'Правильно')
    else:
        await message.answer(f'Ошибка\nПравильные ответы: {UserState.now_question["answer"]}\n'
                             f'Пояснение: {str(UserState.now_question["about"])}')
