from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_but = ['Основная часть', 'Планы', 'Признаки', '23 задание', '25 задание']
modules = ['Модуль 1', 'Модуль 2', 'Модуль 3', 'Модуль 4', 'Модуль 5']


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
    for el in modules:
        test_kb.button(text=f'{el}')
    test_kb.adjust(1, 2)
    return test_kb.as_markup()




del_keyboard = ReplyKeyboardRemove()
