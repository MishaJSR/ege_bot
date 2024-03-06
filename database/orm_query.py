from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task
from sqlalchemy import select, update


async def orm_add_task(session: AsyncSession, data: dict):
    obj = Task(
        subj=data['subj'],
        exam=data['exam'],
        chapter=data['chapter'],
        description=data['description'],
        answer_mode=data['answer_mode'],
        answer=data['answer']
    )
    session.add(obj)
    await session.commit()


async def orm_get_chapters(session: AsyncSession, target_subj=None, target_exam=None):
    query = select(Task).where((Task.subj == target_subj) & (Task.exam == target_exam))
    result = await session.execute(query)
    return result.fetchall()


