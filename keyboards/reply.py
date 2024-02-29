from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='История'),
            KeyboardButton(text='Общество'),
        ],
        [
            KeyboardButton(text='О нас'),
            KeyboardButton(text='Оплата'),
        ]
    ],
    resize_keyboard=True,
)

del_keyboard = ReplyKeyboardRemove()

subj_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ЕГЭ'),
        ],
        [
            KeyboardButton(text='ОГЭ'),
        ],
    ],
    resize_keyboard=True,
)

history_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Teма 1'),
        ],
        [
            KeyboardButton(text='Teма 2'),
        ],
        [
            KeyboardButton(text='Teма 3'),
        ],
        [
            KeyboardButton(text='Teма 4'),
        ],
        [
            KeyboardButton(text='Teма 1'),
        ],
        [
            KeyboardButton(text='Teма 2'),
        ],
        [
            KeyboardButton(text='Teма 3'),
        ],
        [
            KeyboardButton(text='Teма 4'),
        ]
    ],
    resize_keyboard=True,
)
