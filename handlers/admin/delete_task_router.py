from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import find_task, delete_task
from keyboards.user.reply_user import start_kb
from keyboards.admin.reply_admin import start_kb, reset_kb
from handlers.admin.states import Admin_state, AdminStateDelete

admin_delete_task_router = Router()


@admin_delete_task_router.message(F.text == 'Удалить задание')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer('Введите часть из описания задания', reply_markup=reset_kb())
    await state.set_state(AdminStateDelete.find_key)


@admin_delete_task_router.message(AdminStateDelete.find_key)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await find_task(session, message.text)
        if len(res) == 0:
            await message.answer('Ничего не нашлось, попробуйте еще раз')
            await state.set_state(Admin_state.find_key)
            return
        for ind, el in enumerate(res):
            AdminStateDelete.data.append(el._data[0].description)
            await message.answer(f'{ind}: {el._data[0].description}\n')
    except:
        await message.answer('Ошибка поиска', reply_markup=start_kb())
        await state.set_state(Admin_state.start)
        return
    await message.answer('Введите номер задания который вы хотите удалить', reply_markup=reset_kb())
    await state.set_state(AdminStateDelete.confirm_delete)


@admin_delete_task_router.message(AdminStateDelete.confirm_delete)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        des_del = AdminStateDelete.data[int(message.text)]
        await delete_task(session, des_del)
    except:
        await message.answer('Ошибка удаления', reply_markup=start_kb())
        await state.set_state(Admin_state.start)
        return
    await message.answer('Задание удалено', reply_markup=start_kb())
    await state.set_state(Admin_state.start)
