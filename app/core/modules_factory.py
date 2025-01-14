from redis.asyncio import Redis
from openai import OpenAI

from app.core.config import config, redis_config, tg_conf, smc_config
from utils import telegram_bot
from utils.smc_driver import SMCDriver

# -------- Initialize REDIS connection --------------------
redis_db = Redis(
    host=redis_config.REDIS_HOST,
    port=redis_config.REDIS_PORT,
    username=redis_config.REDIS_USER,
    password=redis_config.REDIS_PASSWORD,
)

# -------- Initialize OpenAI --------------------
openai_client = OpenAI(api_key=config.OPENAI_API_KEY)

# -------- Initialize Telegram Bot --------------------
tg_bot = telegram_bot.TelegramBot(token=tg_conf.TG_TOKEN, chat=tg_conf.TG_CHAT_ID)

# -------- Initialize SMC Driver --------------------
smc_driver = SMCDriver(web_provider=smc_config.WEB3_PROVIDER, contract_address=smc_config.CONTRACT_ADDRESS, prize_key=smc_config.PRIZE_ADDRESS_PRIVATE_KEY)
