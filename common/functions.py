import calendar
from datetime import datetime

from database.orm_query import check_sub_orm


async def check_subscribe(message, session, userid, show=True):
    res = await check_sub_orm(session, userid)
    if res[0]._data[0].is_subscribe:
        if show:
            await message.answer(f'Пользователь: {res[0]._data[0].username}\n'
                             f'Подписка активна до: {str(res[0]._data[0].day_end_subscribe)[:10]}')
        return True
    else:
        if show:
            await message.answer(f'Пользователь: {res[0]._data[0].username}\n'
                             f'Подписка не активна')
        return False


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)#