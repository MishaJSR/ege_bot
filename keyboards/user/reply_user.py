from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import emoji

from utils.common.static_user import *

start_but = [BUTTON_START_PREPARE_1, BUTTON_START_PREPARE_2]
start_profile = [BUTTON_MORE_STATISTIC, BUTTON_ABOUT_LEVEL]
main_but = [BUTTON_MAIN_CHAPTER]
answer_mode_list = ['Теория', 'Практика']


def start_user_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    for el in start_but:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def start_profile_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=BACK_BUTTON)
    for el in start_profile:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def main_chapter_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=BACK_BUTTON)
    for but in main_but:
        test_kb.button(text=but)
    test_kb.adjust(1, 2, 2)
    return test_kb.as_markup(resize_keyboard=True)


def chapter_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=BACK_BUTTON)
    for but in data:
        test_kb.button(text=but)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def under_chapter_kb(data=None, is_more=False, is_return=False):
    test_kb = ReplyKeyboardBuilder()
    if is_return:
        test_kb.button(text=RETURN_BUTTON)
    else:
        test_kb.button(text=BACK_BUTTON)
    for but in data:
        test_kb.button(text=but)
    if is_more:
        test_kb.button(text=MORE_BUTTON)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def answer_mode_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=BACK_BUTTON)
    for but in answer_mode_list:
        test_kb.button(text=but)
    test_kb.adjust(1, 2)
    return test_kb.as_markup(resize_keyboard=True)


def ready_test_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=BACK_BUTTON)
    test_kb.button(text=TEXT_READY_TEST)
    # test_kb.adjust(1, 2)
    return test_kb.as_markup(resize_keyboard=True)


def next_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=BACK_BUTTON)
    test_kb.button(text=NEXT_BUTTON)
    return test_kb.as_markup(resize_keyboard=True)


def back_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=BACK_BUTTON)
    return test_kb.as_markup(resize_keyboard=True)
