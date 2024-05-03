import emoji
from aiogram.filters import StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import random
import logging

from database.orm_query import orm_get_modules_task, orm_get_prepare_module
from keyboards.user.inline_user import get_inline
from keyboards.user.reply_user import start_kb, prepare_kb, subj_kb, module_kb, train_kb, under_prepare_kb, main_but, \
    modules, teor, next_kb
from sqlalchemy.ext.asyncio import AsyncSession

user_task_router = Router()


class UserTaskState(StatesGroup):
    start_choose = State()
    subj_choose = State()
    module_choose = State()
    under_prepare_choose = State()
    prepare_choose = State()
    train_choose = State()
    next_choose = State()
    texts = {
        'UserTaskState:start_choose': ['Выберите задание', start_kb],
        'UserTaskState:subj_choose': ['Выбираем предметы', subj_kb],
        'UserTaskState:module_choose': ['Выбрана подготовка', module_kb],
        'UserTaskState:under_prepare_choose': ['Выбрана подготовка', under_prepare_kb],
        'UserTaskState:prepare_choose': ['Выбрана подготовка', prepare_kb],
        'UserTaskState:train_choose': ['Выбрана подготовка', train_kb],
        'UserTaskState:next_choose': ['Выбрана подготовка', train_kb],
    }


@user_task_router.message(StateFilter('*'), F.text == emoji.emojize(':left_arrow:') + ' Назад')
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    print("Назад")
    current_state = await state.get_state()

    previous = None
    async for step in get_generator(UserTaskState.__all_states__):
        if step.state == current_state:
            await state.set_state(previous)
            data = await state.get_data()
            if previous.state == 'UserTaskState:under_prepare_choose':
                await message.answer(f"Вы вернулись к прошлому шагу",
                                     reply_markup=UserTaskState.texts[previous.state][1](data['under_prepare']))
            elif previous.state == 'UserTaskState:train_choose':
                await message.answer(f"Вы вернулись к прошлому шагу",
                                     reply_markup=UserTaskState.texts['UserTaskState:prepare_choose'][1]())
                await state.set_state(UserTaskState.prepare_choose)
                logging.info(previous.state)
            elif previous.state == 'UserTaskState:start_choose':
                await message.answer(f"Вы вернулись в главное меню",
                                     reply_markup=UserTaskState.texts[previous.state][1]())
                logging.info(previous.state)
            else:
                await message.answer(f"Вы вернулись к прошлому шагу",
                                     reply_markup=UserTaskState.texts[previous.state][1]())
            return
        previous = step


@user_task_router.message(UserTaskState.subj_choose, F.text)
async def start_subj_choose(message: types.Message, state: FSMContext):
    if message.text not in main_but:
        await message.answer(f'Ошибка ввода')
        return
    data = await state.get_data()
    data['subj'] = message.text
    await state.set_data(data)
    await message.answer(f'Выберите раздел для подготовки', reply_markup=module_kb())
    await state.set_state(UserTaskState.module_choose)  #


@user_task_router.message(UserTaskState.module_choose)
async def start_module_choose(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text not in modules:
        await message.answer(f'Ошибка ввода')
        return
    try:
        res = await message.bot.get_chat_member(chat_id='@humanitiessociety', user_id=message.from_user.id)
        if res.status.value not in ['member', 'creator']:
            raise Exception()
    except:
        await message.answer('Вы не подписаны на канал', reply_markup=get_inline())
        await message.answer('После подписки вы сможете продолжить работу', reply_markup=start_kb())
        await state.set_state(UserTaskState.start_choose)
        return
    data = await state.get_data()
    data['module'] = message.text
    await state.set_data(data)
    try:
        res = await orm_get_prepare_module(session, module=data['module'], exam=data['subj'])
        under_prepare_data = []
        for task in res:
            under_prepare_data.append(task._data[0])
        data = await state.get_data()
        data['under_prepare'] = under_prepare_data
        await state.set_data(data)
    except Exception as e:
        await message.answer(
            f'Ошибка: \n{str(e)}'
        )
        return
    await message.answer(f'Выберите подраздел', reply_markup=under_prepare_kb(data=data['under_prepare']))
    await state.set_state(UserTaskState.under_prepare_choose)


@user_task_router.message(UserTaskState.under_prepare_choose)
async def start_under_choose(message: types.Message, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    if message.text not in data['under_prepare']:
        await message.answer(f'Ошибка ввода')
        return
    data = await state.get_data()
    data['under_prepare_choose'] = message.text
    await state.set_data(data)
    await message.answer(f'Выберите вариант подготовки', reply_markup=prepare_kb())
    await state.set_state(UserTaskState.prepare_choose)


@user_task_router.message(UserTaskState.prepare_choose)
async def start_prepare_choose(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text not in teor:
        await message.answer(f'Ошибка ввода')
        return
    data = await state.get_data()
    data['prepare'] = message.text
    await state.set_data(data)
    try:
        res = await orm_get_modules_task(session,
                                         target_exam=data['subj'],
                                         target_module=data['module'],
                                         target_prepare=data['prepare'],
                                         target_under_prepare=data['under_prepare_choose'])

        question_data = [{
            'description': task._data[0].description,
            'answers': task._data[0].answers,
            'answer': task._data[0].answer,
            'about': task._data[0].about,
            'answer_mode': task._data[0].answer_mode,
            'addition': task._data[0].addition
        } for task in res]
        data = await state.get_data()
        data['question_data'] = question_data
        await state.set_data(data)
    except Exception as e:
        await message.answer(
            f'Ошибка: \n{str(e)}'
        )
    if len(data['question_data']) == 0:
        await message.answer('Задания еще не добавлены в бота')
    else:
        await cut_stare_and_prepare_answers(message, state)


@user_task_router.message(UserTaskState.train_choose, F.text)
async def start_train_choose(message: types.Message, state: FSMContext):
    await answer_checker(message, state)
    data = await state.get_data()
    if len(data['question_data']) == 0:
        await message.answer(f'Вопросы закончились', reply_markup=prepare_kb())
        await state.set_state(UserTaskState.prepare_choose)
    else:
        await state.set_state(UserTaskState.next_choose)


@user_task_router.message(UserTaskState.next_choose, F.text)
async def start_train_choose(message: types.Message, state: FSMContext):
    if message.text == 'Следующий ' + emoji.emojize(':right_arrow:'):
        await cut_stare_and_prepare_answers(message, state)
    else:
        await message.answer(f'Ошибка ввода', reply_markup=prepare_kb())
        await state.set_state(UserTaskState.prepare_choose)


async def cut_stare_and_prepare_answers(message, state):
    data = await state.get_data()
    data['now_question'] = random.choice(data['question_data'])
    data['question_data'].remove(data['now_question'])
    task_to_show = ''
    if data['now_question']['answer_mode'] == "Квиз":
        task_to_show += data['now_question']['description'] + '\n' + '\n'
        answer_arr = data['now_question']['answers'].split("` ")
        for ind, txt in enumerate(answer_arr):
            task_to_show += f'{ind + 1}. {txt}' + '\n'
    await state.set_data(data)
    await message.answer(task_to_show, reply_markup=train_kb())
    await state.set_state(UserTaskState.train_choose)


async def handle_correct_answer(message):
    await message.answer(f'Правильно')


async def handle_wrong_answer(message, correct_answers, explanation=""):
    if len(explanation) > 3:
        await message.answer(f'*Ошибка*\nПравильные ответы: {correct_answers}\n'
                             f'\n*Пояснение*: \n{explanation}', parse_mode="Markdown", reply_markup=next_kb())
    else:
        await message.answer(f'*Ошибка*\nПравильные ответы: {correct_answers}\n', parse_mode="Markdown",
                             reply_markup=next_kb())


async def answer_checker(message, state):
    data = await state.get_data()

    if message.text.isdigit():
        answer_user = sorted([int(ans) for ans in message.text])
        answer_list = sorted([int(ans) for ans in str(data['now_question']['answer'])])

        if data['now_question']['answer_mode'] == 'Квиз' and answer_list == answer_user:
            await handle_correct_answer(message, data['now_question']['answer'])
        else:
            await handle_wrong_answer(message, data['now_question']['answer'], data['now_question']['about'])
    else:
        await handle_wrong_answer(message, data['now_question']['answer'], data['now_question']['about'])


async def get_generator(arr: list):
    for item in arr:
        yield item
