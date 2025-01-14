import os

from pydantic_settings import BaseSettings

COOKIE_SESSION_ID_KEY: str = os.environ.get("COOKIE_SESSION_ID_KEY", "agent-session-id")


class Config(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    APP_DOMAIN: str = "api.agent.zpoken.dev"
    WEB3_PROVIDER: str = "https://1rpc.io/sepolia"
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")


class RedisSettings(BaseSettings):
    REDIS_HOST: str = os.environ.get('REDIS_HOST')
    REDIS_PORT: str = os.environ.get('REDIS_PORT')
    REDIS_USER: str = os.environ.get('REDIS_USER')
    REDIS_PASSWORD: str = os.environ.get('REDIS_PASSWORD')
    REDIS_URL: str = f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
    print(REDIS_URL)


class TelegramSettings(BaseSettings):
    TG_TOKEN: str = ""
    TG_CHAT_ID: str = ""


class DBSettings(BaseSettings):
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_PW: str = os.environ.get("DB_PW")

    SQLALCHEMY_DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    db_echo: bool = False


class SMCSettings(BaseSettings):
    WEB3_PROVIDER: str = "https://1rpc.io/sepolia"
    CONTRACT_ADDRESS: str = os.environ.get("CONTRACT_ADDRESS", "0xE2ed2a7BeE11e2C936b7999913E3866D4cfc4f8E")
    PRIZE_ADDRESS_PRIVATE_KEY: str = os.environ.get("PRIZE_ADDRESS_PRIVATE_KEY")

class SuperadminSettings(BaseSettings):
    SUPERADMIN_WALLET_ADDRESS: str = ""


config = Config()
tg_conf = TelegramSettings()
db_config = DBSettings()
redis_config = RedisSettings()
superadmin_settings = SuperadminSettings()
smc_config = SMCSettings()
