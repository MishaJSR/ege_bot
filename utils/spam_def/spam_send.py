import asyncio
import datetime
import logging
import os

from aiogram.types import InputMediaPhoto, FSInputFile

from database.models import TheoryRepository
from utils.common.static_url import image_chat_id


async def send_remind(bot):
    logging.info("I start")
    await asyncio.sleep(5)
    while True:
        logging.info("I circle")
        try:
            theory_field = ["photo_id", "message_id"]
            photos = await TheoryRepository().get_all_by_fields(data=theory_field)
            for el in photos:
                if el.photo_id:
                    await bot.forward_message(chat_id=image_chat_id,
                                              from_chat_id=image_chat_id,
                                              message_id=el.message_id)
                await asyncio.sleep(3)
        except Exception as e:
            logging.info(e)
        finally:
            logging.info("I wait")
            await asyncio.sleep(20000)
