import emoji
from aiogram.filters import Command, or_f, StateFilter, CommandStart
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import check_new_user, add_user
from handlers.user.user_task_router import user_task_router, UserTaskState
from handlers.user.payment.user_payment import user_payment_router, UserPaymentState
from keyboards.user.inline_user import get_inline
from keyboards.user.reply_user import start_kb, start_but, subj_kb

user_private_router = Router()
user_private_router.include_routers(user_payment_router, user_task_router)


class UserState(StatesGroup):
    start_user = State()
    payment_user = State()
    user_task = State()
    data = {
        'subj': None,
        'module': None,
        'under_prepare': [],
        'under_prepare_choose': None,
        'prepare': None,
    }


@user_private_router.message(StateFilter('*'), CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        userid, username = message.from_user.id, message.from_user.username
        res = await check_new_user(session, userid)
        if len(res) == 0:
            await add_user(session, userid, username)
    except:
        return
    text = f'Привет {message.from_user.username} ' + emoji.emojize(
        ':cat_with_wry_smile:') + '\nВыбери к чему ты бы хотел подготовиться'
    await message.answer(text, reply_markup=start_kb())
    await state.set_state(UserState.start_user)
    UserTaskState.last_kb = start_kb()


@user_private_router.message(or_f(UserState.start_user, UserTaskState.start_choose, UserPaymentState.start_choose),
                             F.text)
async def start_subj_choose(message: types.Message, state: FSMContext):
    if message.text not in start_but:
        await message.answer(f'Ошибка ввода')
        return
    if message.text == 'Начать подготовку':
        try:
            res = await message.bot.get_chat_member(chat_id='-1002022380565', user_id=message.from_user.id)
            if res.status.value not in ['member', 'creator']:
                raise Exception()
            await message.answer(f'Выберите задание к которому Вы бы хотели подготовиться', reply_markup=subj_kb())
            await state.set_state(UserTaskState.subj_choose)
        except:
            await message.answer('Вы не подписаны на канал', reply_markup=get_inline())
            return
    if message.text == 'Проверить подписку':
        await message.answer(f'Проверяем ...')
        try:
            res = await message.bot.get_chat_member(chat_id='-1002022380565', user_id=message.from_user.id)
            if res.status.value not in ['member', 'creator']:
                raise Exception()
        except:
            await message.answer(f'Подписки нет')
            return
        await message.answer(f'Подпискa есть')


@user_private_router.message(Command('about'))
async def start_about(message: types.Message):
    await message.answer('Это бот для подготовки к ЕГЭ')
