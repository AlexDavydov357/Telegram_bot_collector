import logging
from aiogram import Bot, Dispatcher
import config

# Configure logging
logging.basicConfig(level=logging.INFO,
                    filename="botlog.log",
                    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    datefmt='%H:%M:%S',
                    )

# проверяем наличие токена
if not config.token:
    exit("Токен не найден")

# init
bot = Bot(token=config.token, parse_mode="HTML")
dp = Dispatcher(bot)
