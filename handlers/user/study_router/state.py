from aiogram.fsm.state import StatesGroup, State

from keyboards.user.reply_user import *


class UserStudyState(StatesGroup):
    main_chapter = State()
    chapter = State()
    under_chapter = State()
    answer_mode = State()
    answer_prepare = State()
    answers_checker = State()

    theory_mode = State()

    texts = {
        'UserStudyState:main_chapter': [TEXT_MAIN_CHAPTER, main_chapter_kb],
        'UserStudyState:chapter': [TEXT_CHAPTER, start_user_kb],
        'UserStudyState:under_chapter': [TEXT_UNDER_CHAPTER, start_user_kb],
        'UserStudyState:answer_mode': [TEXT_ANSWER_MODE, answer_mode_kb],
        'UserStudyState:answer_prepare': [TEXT_INTRODUCE_TEST, ready_test_kb],
        'UserStudyState:answers_checker': [TEXT_START_TEST, ReplyKeyboardRemove()],

    }
    list_of_chapters = []
    list_of_under_chapters = []
    index_now_under_chapter = 0
    questions = []
    select_under_chapter = None
    now_question = []
    last_message_id = None
