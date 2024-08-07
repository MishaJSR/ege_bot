from typing import Optional

from pydantic import BaseConfig, conint, BaseModel, field_validator, root_validator


class ConstructUser(BaseModel):
    user_id: conint(strict=True, gt=0)
    username: str
    is_subscribe: bool


class ConstructTask(BaseModel):
    chapter: str
    under_chapter: str
    description: str
    answer_mode: str
    answers: str
    answer: str
    about: Optional[str] = None
    addition: Optional[str] = None
