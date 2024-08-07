from typing import Optional

from pydantic import BaseConfig, conint, BaseModel


class GetDictUser(BaseModel):
    user_id: conint(strict=True, gt=0)
    username: str
    user_class: str
    user_tag: Optional[str] = '@'
    user_become_children: Optional[bool] = False
    parent_id: Optional[int] = None
    progress: Optional[int] = 0
    name_of_user: Optional[str] = None
    stop_spam: Optional[bool] = False
    user_block_bot: Optional[bool] = False
    id_last_block_send: Optional[int] = 0
    is_subscribe: Optional[bool] = False
    phone_number: Optional[str] = None
    user_callback: Optional[str] = None
    points: Optional[int] = 0

    def get_dictionary_add(self) -> dict:
        return self.dict()
