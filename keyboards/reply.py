from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='История', ),
            KeyboardButton(text='Общество'),
        ],
        [
            KeyboardButton(text='О нас'),
            KeyboardButton(text='Оплата'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Что вас интересует?'
)

del_keyboard = ReplyKeyboardRemove()