import calendar
import datetime
import logging
import sqlite3

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task, Users
from sqlalchemy import select, delete, update
import pandas as pd
import re
import subprocess



async def orm_transport_base(session: AsyncSession):
    query = delete(Task)
    await session.execute(query)
    await session.commit()
    conn = sqlite3.connect('database.db')

    # Запрос данных из базы данных в виде DataFrame
    df = pd.read_sql_query("SELECT * FROM task", conn)
    df = df.drop('id', axis=1)
    conn.close()
    for index, row in df.iterrows():
        obj = Task(
            exam=str(row['exam']),
            chapter=str(row['chapter']),
            under_chapter=str(row['under_chapter']),
            description=str(row['description']),
            answer_mode=str(row['answer_mode']),
            answers=str(row['answers']),
            answer=str(row['answer']),
            about=str(row['about']),
        )
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
    target_module = remove_emojis(target_module)[1:]
    if target_prepare == 'Практика':
        query = select(Task).where(
            (Task.exam == target_exam) & (Task.chapter == target_module) & (Task.under_chapter == target_under_prepare))
        result = await session.execute(query)
        return result.fetchall()


async def orm_get_prepare_module(session: AsyncSession, module=None, exam=None):
    module = remove_emojis(module)[1:]
    query = select(Task.under_chapter).where((Task.chapter == module) & (Task.exam == exam)).distinct()
    result = await session.execute(query)
    return result


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

def remove_emojis(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002500-\U00002BEF"  # chinese char
                           u"\U00002702-\U000027B0"
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U0001f926-\U0001f937"
                           u"\U00010000-\U0010ffff"
                           u"\u2640-\u2642"
                           u"\u2600-\u2B55"
                           u"\u200d"
                           u"\u23cf"
                           u"\u23e9"
                           u"\u231a"
                           u"\ufe0f"  # dingbats
                           u"\u3030"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)