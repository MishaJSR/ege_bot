from aiogram.fsm.state import StatesGroup, State

from keyboards.user.reply_user import *


class UserState(StatesGroup):
    start = State()
    main_chapter = State()
    chapter = State()
    under_chapter = State()
    answer_mode = State()
    answer_prepare = State()
    answers_checker = State()

    theory_mode = State()

    texts = {
        'UserState:start': [GREETING, start_user_kb],
        'UserState:main_chapter': [TEXT_MAIN_CHAPTER, main_chapter_kb],
        'UserState:chapter': [TEXT_CHAPTER, start_user_kb],
        'UserState:under_chapter': [TEXT_UNDER_CHAPTER, start_user_kb],
        'UserState:answer_mode': [TEXT_ANSWER_MODE, answer_mode_kb],
        'UserState:answer_prepare': [TEXT_INTRODUCE_TEST, ready_test_kb],
        'UserState:answers_checker': [TEXT_START_TEST, ReplyKeyboardRemove()],

    }
    list_of_chapters = []
    list_of_under_chapters = []
    index_now_under_chapter = 0
    questions = []
    select_under_chapter = None
    now_question = []
    last_message_id = None
