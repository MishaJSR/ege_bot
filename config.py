import os
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import URL

load_dotenv(find_dotenv())


@dataclass
class TgConfig:
    token: str
    admin_ids: Optional[list[int]]
    use_redis: bool

    @staticmethod
    def from_env():
        token = os.getenv("TOKEN")
        admin_list = os.getenv('ADMIN_IDS').split(", ")
        admin_ids = [int(ad_id) for ad_id in admin_list]
        use_redis = os.getenv("USE_REDIS") == 'True'
        return TgConfig(token=token, admin_ids=admin_ids, use_redis=use_redis)


@dataclass
class RedisConfig():
    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str]

    def dsn(self) -> str:
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"

    @staticmethod
    def from_env():
        redis_pass = os.getenv("REDISPASSWORD")
        redis_port = int(os.getenv("REDISPORT"))
        redis_host = os.getenv("REDISHOST")
        return RedisConfig(redis_pass=redis_pass, redis_port=redis_port, redis_host=redis_host)


class DbConfig:
    @staticmethod
    def get_url() -> str:
        url = URL.create(
            drivername=f"postgresql+asyncpg",
            host=os.getenv("DB_HOST"),
            password=os.getenv("POSTGRES_PASSWORD"),
            username=os.getenv("POSTGRES_USER"),
            database=os.getenv("POSTGRES_DB"),
            port=int(os.getenv("DB_PORT")),
        ).render_as_string(hide_password=False)
        return url


@dataclass
class Config:
    tg_bot: TgConfig
    redis: Optional[RedisConfig] = None


def load_config() -> Config:
    return Config(
        tg_bot=TgConfig.from_env(),
        redis=RedisConfig.from_env(),
    )
