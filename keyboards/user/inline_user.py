from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.common.static_text import *
from utils.common.static_url import url_of_channel


def get_inline_channel():
    builder = InlineKeyboardBuilder()
    builder.button(text=LABEL_CHANNEL_BUTTON, url=url_of_channel)
    return builder.as_markup()


def get_inline_about():
    builder = InlineKeyboardBuilder()
    builder.button(text=SHOW_ABOUT_INLINE, callback_data=CALLBACK_SHOW_ABOUT)
    return builder.as_markup()
