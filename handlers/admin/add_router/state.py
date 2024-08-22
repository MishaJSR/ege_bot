from aiogram.fsm.state import StatesGroup, State


class AdminAddState(StatesGroup):
    send_photo = State()
    send_text = State()
    confirm_post = State()
    select_post_action = State()
    select_chapter = State()
    select_under_chapter = State()
    confirm_under_chapter = State()
    list_of_chapters = []
    chapter = None
    under_chapter = None
    photo = None
    text = None
    posts_list = []

