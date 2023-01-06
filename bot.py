# -*- coding: utf-8 -*-
# coding: utf-8
import re
import copy
import requests
import sys
import traceback
import json
import time
from os.path import exists
import logging
import os
import math
import threading
from threading import Timer
import random
import pymysql
import datetime
import telebot
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram import exceptions
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
#from tortoise.query_utils import Q #unvalid from tortoise update
from tortoise.expressions import F, Q
from aiogram.contrib.middlewares.logging import LoggingMiddleware


# Здесь игровые штуки
import logger
import engine as db

kakushigoto = 702528084
devChat = -1001364436303
owner = ['702528084']
devs = ['702528084']
tradeChat = -1001317123616
godEyeChat = -1001361746905
leadersChannel = -1001597665166
main_chat = -1001345068459
logging.basicConfig(level=logging.INFO, filename='toh.log')
bot = Bot(token='')
logBot = Bot(token='')
secondLogBot = Bot(token='')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


#Подхват файлов
print("Подключение плагинов...")
game_plugins = [ f[:-3] for f in os.listdir('game') if f.endswith('.py') ]
for plugin in game_plugins:
    try:
        exec(open("./game/" + plugin + ".py", encoding="utf-8").read())
        print ("Подключен " + plugin)
    except Exception as e:
        print("Ошибка подключения " + plugin) 
        print(str(e))
# !
try:
    exec(open("./main.py", encoding="utf-8").read())
except Exception as e:
    print(e)
print("Всё запущено.")



async def databasetimer():
    if not db.database.is_closed():
        db.database.close()
        db.database.connect()
        print("DB conn restart")
    await asyncio.sleep(3600)
    await databasetimer()

if __name__ == "__main__":
    executor.start_polling(dp)
