import os
from dataclasses import dataclass
from typing import Optional
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


@dataclass
class DbConfig:

    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    # For SQLAlchemy
    def construct_sqlalchemy_url(self, driver="asyncpg", host=None, port=None) -> str:
        from sqlalchemy.engine.url import URL

        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    @staticmethod
    def from_env():
        host = os.getenv("DB_HOST")
        password = os.getenv("POSTGRES_PASSWORD")
        user = os.getenv("POSTGRES_USER")
        database = os.getenv("POSTGRES_DB")
        port = os.getenv("DB_PORT", 5432)
        return DbConfig(
            host=host, password=password, user=user, database=database, port=port
        )


@dataclass
class TgBot:

    token: str
    admin_ids: list[int]
    use_redis: bool

    @staticmethod
    def from_env():
        token = os.getenv("TOKEN")
        admin_ids = [int(os.getenv("ADMIN_ID"))]
        use_redis = bool(os.getenv("USE_REDIS"))
        return TgBot(token=token, admin_ids=admin_ids, use_redis=use_redis)


@dataclass
class RedisConfig:

    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str]

    def dsn(self) -> str:
        """
        Constructs and returns a Redis DSN (Data Source Name) for this database configuration.
        """
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"

    @staticmethod
    def from_env():
        """
        Creates the RedisConfig object from environment variables.
        """
        redis_pass = os.getenv("REDISPASSWORD")
        redis_port = int(os.getenv("REDISPORT"))
        redis_host = os.getenv("REDISHOST")

        return RedisConfig(
            redis_pass=redis_pass, redis_port=redis_port, redis_host=redis_host
        )


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous
    db: Optional[DbConfig] = None
    redis: Optional[RedisConfig] = None


def load_config(path: str = None) -> Config:
    """
    This function takes an optional file path as input and returns a Config object.
    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    # Create an Env object.
    # The Env object will be used to read environment variables.

    return Config(
        tg_bot=TgBot.from_env(),
        db=DbConfig.from_env(),
        redis=RedisConfig.from_env(),
        misc=Miscellaneous(),
    )

