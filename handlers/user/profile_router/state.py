from aiogram.fsm.state import StatesGroup, State

from keyboards.user.reply_user import *


class UserProfileState(StatesGroup):
    start = State()
    chapter = State()
    under_chapter = State()

    list_of_chapters = []
    list_of_under_chapters = []
    index_now_under_chapter = 0
    select_under_chapter = None