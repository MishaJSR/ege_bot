from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from keyboards.reply import main_but, modules
import emoji


def start_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Добавить задание')
    test_kb.button(text='Удалить задание')
    test_kb.button(text='Изменить задание')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def exam_kb(data=main_but):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for el in data:
        test_kb.button(text=el)
    test_kb.adjust(1, 2)
    return test_kb.as_markup(resize_keyboard=True)


def chapter_kb(data=modules):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for el in data:
        test_kb.button(text=el)
    test_kb.adjust(1, 2)
    return test_kb.as_markup(resize_keyboard=True)


def answers_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Закончить ввод')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def answers_kb_end():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Подтвердить')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def answer_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    return test_kb.as_markup(resize_keyboard=True)

def restart_answer_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Начать снова')
    return test_kb.as_markup(resize_keyboard=True)


def about_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Оставить пустым')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def back_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)
