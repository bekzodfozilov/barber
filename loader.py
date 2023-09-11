import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
s = MemoryStorage()
UABarbershop = Dispatcher(bot, storage=s)