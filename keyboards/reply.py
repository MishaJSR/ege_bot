from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_but = ['История ЕГЭ', 'Общество ЕГЭ', 'История ОГЭ', 'Общество ОГЭ']


def get_pool(kb: ReplyKeyboardBuilder):
    return [text.text for text in kb.as_markup().keyboard[0]]


def start_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Начать подготовку')
    test_kb.button(text='Информация о боте')
    test_kb.button(text='Оплата')
    test_kb.button(text='Поддержка')
    pool = get_pool(test_kb)
    test_kb.adjust(2, 2)
    return test_kb.as_markup(), pool


def subj_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for but in main_but:
        test_kb.button(text=but)
    pool = get_pool(test_kb)
    test_kb.adjust(1, 2, 2)
    return test_kb.as_markup(), pool


def chapters_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for but in data:
        test_kb.button(text=but)
    pool = get_pool(test_kb)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(), pool


def prepare_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Теория')
    test_kb.button(text='Практика')
    pool = get_pool(test_kb)
    test_kb.adjust(1, 2)
    return test_kb.as_markup(), pool


del_keyboard = ReplyKeyboardRemove()
