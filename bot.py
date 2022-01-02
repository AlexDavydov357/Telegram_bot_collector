import message_handler
from aiogram import executor
from dispatcher import dp
from db_command import BotDB

BotDB = BotDB('data_from_bot.db')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
