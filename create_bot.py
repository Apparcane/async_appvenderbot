import logging
import pyowm
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *

logging.basicConfig(level=logging.INFO)
owm = pyowm.OWM(owm_token)
bot = Bot(token = bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class States(StatesGroup):
    city = State()
    anime_page = State() 