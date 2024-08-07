from aiogram.fsm.state import StatesGroup, State
from keyboards.admin.reply_admin import start_kb, back_kb, exam_kb, chapter_kb, answers_kb, answers_kb_end, about_kb, \
    answer_kb, restart_answer_kb, reset_kb


class Admin_state(StatesGroup):
    start = State()
    exam = State()
    chapter = State()
    under_chapter = State()
    description = State()
    answers_checker = State()
    answers = State()
    answers_swap = State()
    answer = State()
    about = State()
    check_info = State()
    save_in_db = State()
    texts = {
        'Admin_state:start': ['Начало работы', start_kb],
        'Admin_state:exam': ['Выбор части', exam_kb],
        'Admin_state:chapter': ['Выбор модуля', chapter_kb],
        'Admin_state:under_chapter': ['Введите подмодуль', back_kb],
        'Admin_state:description': ['Введите условие задания', back_kb],
        'Admin_state:answers': ['Введите ответы', restart_answer_kb],
        'Admin_state:answers_swap': ['Введите вариант ответа', answers_kb_end],
        'Admin_state:answer': ['Введите ответ на задание', answer_kb],
        'Admin_state:about': ['Введите пояснение', about_kb],
        'Admin_state:check_info': ['Проверка', answers_kb_end],
        'Admin_state:save_in_db': ['Начало работы', start_kb],
    }
    default_data = {
        'exam': None,
        'chapter': None,
        'under_chapter': None,
        'description': None,
        'answers': '',
        'answer_mode': 'Квиз',
        'updated': '2024-03-19 11:44:19',
        'answer': None,
        'about': " ",
        'addition': ' ',
    }
    data = {}


class AdminStateSender(StatesGroup):
    text_state = State()
    image_state = State()
    confirm_state = State()
    texts = {
        'AdminStateSender:text_state': 'Выбор текста',
        'AdminStateSender:image_state': 'Выбор изображения',
        'AdminStateSender:confirm_state': 'Подтверждение',
    }
    text = ''
    photo = None


class AdminStateDelete(StatesGroup):
    find_key = State()
    choose_task= State()
    confirm_delete = State()
    texts = {
        'AdminStateDelete:find_key': 'Ввод описания',
        'AdminStateDelete:choose_task': 'Выбор задания для удаления',
        'AdminStateDelete:confirm_delete': 'Подтверждение',
    }
    data = []

