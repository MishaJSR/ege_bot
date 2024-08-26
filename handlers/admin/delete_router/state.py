from aiogram.fsm.state import StatesGroup, State


class AdminDeleteState(StatesGroup):
    select_chapter = State()
    select_under_chapter = State()
    confirm_under_chapter = State()
    list_of_chapters = []
    choose_under_chapter = None
