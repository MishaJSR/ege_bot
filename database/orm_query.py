import calendar
import datetime
import sqlite3

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task, Users
from sqlalchemy import select, delete, update
import pandas as pd
import subprocess



async def orm_transport_base(session: AsyncSession):
    conn = sqlite3.connect('database.db')

    # Запрос данных из базы данных в виде DataFrame
    df = pd.read_sql_query("SELECT * FROM task", conn)
    df = df.drop('id', axis=1)
    conn.close()
    for index, row in df.iterrows():
        obj = Task(
            exam=row['exam'],
            chapter=row['chapter'],
            under_chapter=row['under_chapter'],
            description=row['description'],
            answer_mode=row['answer_mode'],
            answers=row['answers'],
            answer=row['answer'],
            about=row['about'],
            addition=row['addition']
        )
        pass
        session.add(obj)
        await session.commit()





async def orm_add_task(session: AsyncSession, data: dict):
    obj = Task(
        exam=data['exam'],
        chapter=data['chapter'],
        under_chapter=data['under_chapter'],
        description=data['description'],
        answer_mode=data['answer_mode'],
        answers=data['answers'],
        answer=data['answer'],
        about=data['about'],
    )
    session.add(obj)
    await session.commit()


async def check_new_user(session: AsyncSession, user_id: int):
    query = select(Users.user_id).where(Users.user_id == user_id)
    result = await session.execute(query)
    return result.all()


async def check_sub_orm(session: AsyncSession, user_id: int):
    query = select(Users).where(Users.user_id == user_id)
    result = await session.execute(query)
    return result.all()


async def set_sub_orm(session: AsyncSession, user_id: int, months):
    new_date = add_months(datetime.datetime.now(), months)
    query = update(Users).where(Users.user_id == user_id).values(is_subscribe=True, day_end_subscribe=new_date)
    await session.execute(query)
    await session.commit()


async def add_user(session: AsyncSession, user_id: int, username: str):
    if not username:
        username = ')'
    obj = Users(
        user_id=user_id,
        username=username
    )
    session.add(obj)
    await session.commit()


async def get_all_users(session: AsyncSession):
    query = select(Users.user_id)
    result = await session.execute(query)
    return result.all()


async def find_task(session: AsyncSession, text: int):
    query = select(Task).where(Task.description.like(f'%{text}%'))
    result = await session.execute(query)
    return result.all()


async def delete_task(session: AsyncSession, description: int):
    query = delete(Task).where(Task.description == description)
    await session.execute(query)
    await session.commit()


async def orm_get_modules_task(session: AsyncSession, target_exam=None, target_module=None, target_prepare=None,
                               target_under_prepare=None):
    if target_prepare == 'Практика':
        query = select(Task).where(
            (Task.exam == target_exam) & (Task.chapter == target_module) & (Task.under_chapter == target_under_prepare))
        result = await session.execute(query)
        return result.fetchall()


async def orm_get_prepare_module(session: AsyncSession, module=None, exam=None):
    query = select(Task.under_chapter).where((Task.chapter == module) & (Task.exam == exam)).distinct()
    result = await session.execute(query)
    return result


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
