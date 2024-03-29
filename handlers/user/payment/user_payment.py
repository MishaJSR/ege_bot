import emoji
from aiogram.filters import CommandStart, StateFilter, or_f, Command
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from common.functions import check_subscribe
from database.orm_query import orm_get_modules_task, orm_get_prepare_module, add_user, check_new_user, set_sub_orm, \
    check_sub_orm
from keyboards.user.reply_user import train_kb, pay_var, sub_var
from keyboards.user.reply_user import start_kb, prepare_kb, subj_kb, module_kb, train_kb, under_prepare_kb, main_but, \
    start_but, modules, teor, payment_kb, payment_var_kb
from sqlalchemy.ext.asyncio import AsyncSession

user_payment_router = Router()


class UserPaymentState(StatesGroup):
    start_choose = State()
    sub_process = State()
    pay_process = State()

    texts = {
        'UserPaymentState:start_choose': start_kb,
        'UserPaymentState:sub_process': payment_kb,
        'UserPaymentState:pay_choose': payment_var_kb,
    }
    data = 0


@user_payment_router.message(or_f(StateFilter(UserPaymentState.pay_process), StateFilter(UserPaymentState.sub_process)), F.text == emoji.emojize(':left_arrow:') + ' Назад')
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    previous = None
    for step in UserPaymentState.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            if previous.state == 'UserPaymentState:start_choose':
                await message.answer(f"Вы вернулись в главное меню после оплаты", reply_markup=start_kb())
            else:
                await message.answer(f"Вы вернулись к прошлому шагу",
                                     reply_markup=UserPaymentState.texts[previous.state]())
            return
        previous = step


@user_payment_router.message(UserPaymentState.sub_process, F.text)
async def start_subj_choose(message: types.Message, state: FSMContext):
    if message.text not in sub_var:
        await message.answer('Ошибка ввода')
        return
    UserPaymentState.data = 0
    if 'мес' in message.text:
        UserPaymentState.data = int(message.text[0])
    else:
        UserPaymentState.data = 12
    await message.answer(f'Выберите вариант оплаты', reply_markup=payment_var_kb())
    await state.set_state(UserPaymentState.pay_process)


@user_payment_router.message(UserPaymentState.pay_process, F.text)
async def start_subj_choose(message: types.Message, state: FSMContext, session: AsyncSession,):
    if message.text not in pay_var:
        await message.answer('Ошибка ввода')
        return
    if await check_subscribe(message, session, message.from_user.id, show=False):
        await message.answer(f'У Вас уже есть подписка', reply_markup=start_kb())
        await state.set_state(UserPaymentState.start_choose)
        return
    else:
        await message.answer(f'Проводим оплату ...')
        try:
            await set_sub_orm(session, message.from_user.id, UserPaymentState.data)
            await message.answer(f'Оплата прошла успешно', reply_markup=start_kb())
        except:
            await message.answer(f'Ошибка проведении подписки, обратитесь в поддержку', reply_markup=start_kb())
        # момент оплаты
        await state.set_state(UserPaymentState.start_choose)
