import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from database.models import UserRepository, TheoryRepository


async def check_theory(under_chapter):
    theory_field = ["id"]
    theory_filter = {
        "under_chapter": under_chapter
    }
    theory = await TheoryRepository().get_all_by_fields(data=theory_field, field_filter=theory_filter)
    return theory


async def delete_theory(under_chapter):
    theory_filter = {
        "under_chapter": under_chapter
    }
    await TheoryRepository().delete_fields(delete_filter=theory_filter)