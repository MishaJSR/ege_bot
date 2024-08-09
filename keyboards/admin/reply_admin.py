from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb_menu = ['Добавить / Изменить теорию', 'Отправить рассылку']


def start_kb():
    test_kb = ReplyKeyboardBuilder()
    for el in start_kb_menu:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)
