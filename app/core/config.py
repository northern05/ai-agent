import os

from pydantic_settings import BaseSettings

COOKIE_SESSION_ID_KEY: str = os.environ.get("COOKIE_SESSION_ID_KEY", "agent-session-id")


class Config(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    APP_DOMAIN: str = "localhost"
    WEB3_PROVIDER: str = "localhost"
    OPENAI_API_KEY: str = ""


class RedisSettings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = ""
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""
    REDIS_URL: str = f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
    print(REDIS_URL)


class TelegramSettings(BaseSettings):
    TG_TOKEN: str = ""
    TG_CHAT_ID: str = ""


class DBSettings(BaseSettings):
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_PW: str = ""

    SQLALCHEMY_DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    db_echo: bool = False


class SuperadminSettings(BaseSettings):
    SUPERADMIN_WALLET_ADDRESS: str = ""


config = Config()
tg_conf = TelegramSettings()
db_config = DBSettings()
redis_config = RedisSettings()
superadmin_settings = SuperadminSettings()
