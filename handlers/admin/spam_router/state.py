from aiogram.fsm.state import StatesGroup, State


class AdminSpamState(StatesGroup):
    send_photo = State()
    send_text = State()
    send_button_text = State()
    send_button_link = State()
    show_post = State()
    photo = None
    text = None
    button_text = None
    button_link = None
    markup = None

