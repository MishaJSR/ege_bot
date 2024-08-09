from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_markup_kb(text=None, url=None):
    builder = InlineKeyboardBuilder()
    builder.button(text=text, url=url)
    return builder.as_markup()
