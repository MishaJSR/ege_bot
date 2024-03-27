from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task
from sqlalchemy import select, update


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


async def orm_get_modules_task(session: AsyncSession, target_exam=None, target_module=None, target_prepare=None,
                               target_under_prepare=None):
    if target_prepare == 'Практика':
        query = select(Task).where((Task.exam == target_exam) & (Task.chapter == target_module) & (Task.under_chapter == target_under_prepare))
        result = await session.execute(query)
        return result.fetchall()


async def orm_get_prepare_module(session: AsyncSession, module=None, exam=None):
    query = select(Task.under_chapter).where((Task.chapter == module) & (Task.exam == exam)).distinct()
    result = await session.execute(query)
    return result
