from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardBuilder

main_but = ['История ЕГЭ', 'Общество ЕГЭ', 'История ОГЭ', 'Общество ОГЭ']


def start_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Начать подготовку')
    test_kb.button(text='Информация о боте')
    test_kb.button(text='Оплата')
    test_kb.button(text='Поддержка')
    test_kb.adjust(2, 2)
    return test_kb.as_markup()

def subj_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for but in main_but:
        test_kb.button(text=but)
        test_kb.adjust(1, 2, 2)
    return test_kb.as_markup()


def chapters_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for but in data:
        test_kb.button(text=but)
        test_kb.adjust(1, 1)
    return test_kb.as_markup()


def prepare_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Теория')
    test_kb.button(text='Практика')
    test_kb.adjust(1, 2)
    return test_kb.as_markup()





del_keyboard = ReplyKeyboardRemove()
