import sys
sys.path.append(".")
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN_API

storage = MemoryStorage()

bot = Bot(TOKEN_API)
dp = Dispatcher(bot=bot, storage=storage)