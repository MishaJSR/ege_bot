import emoji
from aiogram.filters import CommandStart, StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.orm_query import orm_get_modules_task, orm_get_prepare_module, add_user, check_new_user
from keyboards.user.reply_user import start_kb, prepare_kb, subj_kb, module_kb, train_kb, under_prepare_kb, main_but, \
    start_but, modules, teor
from sqlalchemy.ext.asyncio import AsyncSession

user_task_router = Router()


class UserTaskState(StatesGroup):
    start_choose = State()
    subj_choose = State()
    module_choose = State()
    under_prepare_choose = State()
    prepare_choose = State()
    train_choose = State()
    texts = {
        'UserTaskState:start_choose': ['Выберите задание', start_kb],
        'UserTaskState:subj_choose': ['Выбираем предметы', subj_kb],
        'UserTaskState:module_choose': ['Выбрана подготовка', module_kb],
        'UserTaskState:under_prepare_choose': ['Выбрана подготовка', under_prepare_kb],
        'UserTaskState:prepare_choose': ['Выбрана подготовка', prepare_kb],
        'UserTaskState:train_choose': ['Выбрана подготовка', train_kb],
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





@user_task_router.message(StateFilter('*'), F.text == emoji.emojize(':left_arrow:') + ' Назад')
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    print("Назад")
    current_state = await state.get_state()

    previous = None
    for step in UserTaskState.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            if previous.state == 'UserTaskState:under_prepare_choose':
                await message.answer(f"Вы вернулись к прошлому шагу",
                                     reply_markup=UserTaskState.texts[previous.state][1](UserTaskState.data['under_prepare']))
            elif previous.state == 'UserTaskState:start_choose':
                await message.answer(f"Вы вернулись в главное меню",
                                     reply_markup=UserTaskState.texts[previous.state][1]())
                print(previous.state)
            else:
                await message.answer(f"Вы вернулись к прошлому шагу", reply_markup=UserTaskState.texts[previous.state][1]())
            # await message.answer(f"Ок, вы вернулись к прошлому шагу \n{UserTaskState.texts[previous.state]}",
            #                      reply_markup=UserTaskState.texts[previous.state][1]())
            return
        previous = step


# @user_task_router.message(UserTaskState.start_choose, F.text != '/admin')
# async def start_func(message: types.Message, state: FSMContext):
#     if message.text not in ['Начать подготовку']:
#         await message.answer(f'Ошибка ввода')
#         return
#     await message.answer(f'Выберите задание к которому Вы бы хотели подготовиться', reply_markup=subj_kb())
#     await state.set_state(UserTaskState.subj_choose)


@user_task_router.message(UserTaskState.subj_choose, F.text)
async def start_subj_choose(message: types.Message, state: FSMContext):
    if message.text not in main_but:
        await message.answer(f'Ошибка ввода')
        return
    UserTaskState.data['subj'] = message.text
    await message.answer(f'Выберите модуль для подготовки', reply_markup=module_kb())
    await state.set_state(UserTaskState.module_choose)  #


@user_task_router.message(UserTaskState.module_choose)
async def start_module_choose(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text not in modules:
        await message.answer(f'Ошибка ввода')
        return
    UserTaskState.data['module'] = message.text
    try:
        res = await orm_get_prepare_module(session, module=UserTaskState.data['module'], exam=UserTaskState.data['subj'])
        UserTaskState.data['under_prepare'] = []
        for task in res:
            UserTaskState.data['under_prepare'].append(task._data[0])
    except Exception as e:
        await message.answer(
            f'Ошибка: \n{str(e)}'
        )
    await message.answer(f'Выберите подраздел', reply_markup=under_prepare_kb(data=UserTaskState.data['under_prepare']))
    await state.set_state(UserTaskState.under_prepare_choose)


@user_task_router.message(UserTaskState.under_prepare_choose)
async def start_under_choose(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text not in UserTaskState.data['under_prepare']:
        await message.answer(f'Ошибка ввода')
        return
    UserTaskState.data['under_prepare_choose'] = message.text
    await message.answer(f'Выберите вариант подготовки', reply_markup=prepare_kb())
    await state.set_state(UserTaskState.prepare_choose)


@user_task_router.message(UserTaskState.prepare_choose)
async def start_prepare_choose(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text not in teor:
        await message.answer(f'Ошибка ввода')
        return
    UserTaskState.data['prepare'] = message.text
    try:
        res = await orm_get_modules_task(session,
                                         target_exam=UserTaskState.data['subj'],
                                         target_module=UserTaskState.data['module'],
                                         target_prepare=UserTaskState.data['prepare'],
                                         target_under_prepare=UserTaskState.data['under_prepare_choose'])
        for task in res:
            UserTaskState.question_data.append({
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
    if len(UserTaskState.question_data) == 0:
        await message.answer('Задания еще не добавлены в бота')
    else:
        await cut_stare_and_prepare_answers(message, UserTaskState, state)


@user_task_router.message(UserTaskState.train_choose, F.text)
async def start_train_choose(message: types.Message, session: AsyncSession, state: FSMContext):
    await answer_checker(message, UserTaskState)
    if len(UserTaskState.question_data) == 0:
        await message.answer(f'Вопросы закончились', reply_markup=prepare_kb())
        await state.set_state(UserTaskState.prepare_choose)
    else:
        await cut_stare_and_prepare_answers(message, UserTaskState, state)


async def cut_stare_and_prepare_answers(message, UserTaskState, state):
    UserTaskState.now_question = UserTaskState.question_data[-1]
    UserTaskState.question_data.pop()
    task_to_show = ''
    if UserTaskState.now_question['answer_mode'] == "Квиз":
        task_to_show += UserTaskState.now_question['description'] + '\n' + '\n'
        answer_arr = UserTaskState.now_question['answers'].split("` ")
        for ind, txt in enumerate(answer_arr):
            task_to_show += f'{ind + 1}: {txt}' + '\n'
    await message.answer(task_to_show, reply_markup=train_kb())
    await state.set_state(UserTaskState.train_choose)


async def answer_checker(message, UserTaskState):
    if message.text.isdigit():
        if UserTaskState.now_question['answer_mode'] == 'Квиз':
            answer_user = sorted([int(ans) for ans in message.text])
            answer_list = sorted([int(ans) for ans in str(UserTaskState.now_question['answer'])])
        if answer_list == answer_user:
            await message.answer(f'Правильно')
        else:
            await message.answer(f'*Ошибка*\nПравильные ответы: {UserTaskState.now_question["answer"]}\n'
                                 f'\n*Пояснение*: {str(UserTaskState.now_question["about"])}', parse_mode="Markdown")
    else:
        await message.answer(f'*Ошибка*\nПравильные ответы: {UserTaskState.now_question["answer"]}\n'
                             f'\n*Пояснение*: {str(UserTaskState.now_question["about"])}', parse_mode="Markdown")
