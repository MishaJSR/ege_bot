from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline():
    builder = InlineKeyboardBuilder()
    builder.button(text='Школа гуманитариев|Общество ЕГЭ', callback_data='ss', url='https://t.me/humanitiessociety')
    return builder.as_markup()
