from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import emoji

start_but = ['Начать подготовку', 'Оплата подписки', 'Проверить подписку']
main_but = ['Основная часть', 'Планы', 'Признаки', '23 задание', '25 задание']
modules = ['Человек и общество', 'Экономика', 'Социальные отношения', 'Политика', 'Право']
teor = ['Теория', 'Практика']


def start_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    for el in start_but:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def subj_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=emoji.emojize(':left_arrow:') + ' Назад')
    for but in main_but:
        test_kb.button(text=but)
    test_kb.adjust(1, 2, 2)
    return test_kb.as_markup(resize_keyboard=True)


def chapters_kb(data=None):
    test_kb = ReplyKeyboardBuilder()

    test_kb.button(text=emoji.emojize(':left_arrow:') + ' Назад')
    for but in data:
        test_kb.button(text=but)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def module_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=emoji.emojize(':left_arrow:') + ' Назад')
    for el in modules:
        test_kb.button(text=f'{el}')
    test_kb.adjust(1, 2)
    return test_kb.as_markup(resize_keyboard=True)


def under_prepare_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=emoji.emojize(':left_arrow:') + ' Назад')
    for el in data:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def prepare_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=emoji.emojize(':left_arrow:') + ' Назад')
    for but in teor:
        test_kb.button(text=but)
    test_kb.adjust(1, 2)
    return test_kb.as_markup(resize_keyboard=True)


def train_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=emoji.emojize(':left_arrow:') + ' Назад')
    # test_kb.adjust(1, 2)
    return test_kb.as_markup(resize_keyboard=True)


def quiz_kb(data_mass=None, sizes: tuple[int] = (1,)):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text=emoji.emojize(':left_arrow:') + ' Назад')
    text_des, but_text, answer = data_mass
    butns = but_text.split(", ")
    for ind, el in enumerate(butns):
        test_kb.button(text=f'{el}')
    test_kb.adjust(1, 2)
    return test_kb.as_markup(resize_keyboard=True)


del_keyboard = ReplyKeyboardRemove()
