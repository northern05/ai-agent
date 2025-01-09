import redis
from web3 import Web3, HTTPProvider
from openai import OpenAI

from app.core.config import config, redis_config, tg_conf
from utils import telegram_bot

redis_db = redis.Redis(
    host=redis_config.REDIS_HOST,
    port=redis_config.REDIS_PORT,
    username=redis_config.REDIS_USER,
    password=redis_config.REDIS_PASSWORD,
)
web3 = Web3(HTTPProvider(config.WEB3_PROVIDER))

openai_client = OpenAI(api_key=config.OPENAI_API_KEY)

# -------- Initialize Telegram Bot --------------------
tg_bot = telegram_bot.TelegramBot(token=tg_conf.TG_TOKEN, chat=tg_conf.TG_CHAT_ID)