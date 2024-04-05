from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline():
    builder = InlineKeyboardBuilder()
    builder.button(text='Ссылка на канал', callback_data='ss', url='https://t.me/+YwRdC0S_lQdlYzhi')
    return builder.as_markup()
