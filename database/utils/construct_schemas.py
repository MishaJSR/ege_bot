from typing import Optional

from pydantic import conint, BaseModel


class ConstructUser(BaseModel):
    user_id: conint(strict=True, gt=0)
    username: str
    is_subscribe: bool
    points: Optional[int] = 0


class ConstructTask(BaseModel):
    chapter: str
    under_chapter: str
    description: str
    answer_mode: str
    answers: str
    answer: str
    about: Optional[str] = None
    addition: Optional[str] = None


class ConstructTheory(BaseModel):
    under_chapter: str
    photo_id: Optional[str] = None
    text: str
    message_id: Optional[int] = None


class ConstructUserProgress(BaseModel):
    chapter: str
    under_chapter: str
    user_id: Optional[int]
    question_id: Optional[int]
    is_pass: bool

