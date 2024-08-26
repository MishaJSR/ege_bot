from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utils.common.static_admin import *

start_kb_menu = [BUTTON_MENU1, BUTTON_MENU2, BUTTON_MENU3]


def start_kb():
    test_kb = ReplyKeyboardBuilder()
    for el in start_kb_menu:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def confirm_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=BUTTON_CONFIRM)
    test_kb.button(text=BUTTON_NOT_CONFIRM)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def next_post_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=BUTTON_END_POST)
    test_kb.button(text=BUTTON_NEXT_POST)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def skip_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=BUTTON_BACK)
    test_kb.button(text=BUTTON_SKIP)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def back_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=BUTTON_BACK)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)
