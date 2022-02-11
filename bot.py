import requests
import datetime
import json
import logging
import pyowm
import asyncio

from config import bot_token, owm_token
from IndividualID import *
from markups import *
from ongoing import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)
owm = pyowm.OWM(owm_token)
bot = Bot(token = bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class States(StatesGroup):
    city = State()
    anime_page = State() 

@dp.message_handler(commands=["start", "go"])
async def start_command(message: types.Message):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")
    await message.answer("Привет!")

    copy = 0
    with open('./json/data.json', 'r+', encoding = 'utf-8') as data_file:   
        users = json.load(data_file)

    if users != {}:
        for p in users['user']:
            index = p['nums'] + 1

        for p in users['user']:
            if message.chat.id == p['chat_id']:
                copy = 1
                break

        if copy == 0:
            with open('./json/data.json', 'w+', encoding = 'utf-8') as data_file:
                users['user'].append({
                    'nums' : index,
                    'username' : message.from_user.username,
                    'chat_id' : message.chat.id,
                    'first_name' : message.from_user.first_name,
                    'last_name' : message.from_user.last_name
                })

                json.dump(users, data_file, indent = 4)            

    else:
        with open('./json/data.json', 'w+', encoding = 'utf-8') as data_file:
            users['user'].append({
                'nums' : 1,
                'username' : message.from_user.username,
                'chat_id' : message.chat.id,
                'first_name' : message.from_user.first_name,
                'last_name' : message.from_user.last_name
            })

            json.dump(users, data_file, indent = 4)

@dp.message_handler(commands=['settings'])
async def settings(message: types.Message):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")
    await message.answer("Меня может редактировать только мой создатель!!")

@dp.message_handler(commands=['commands'])
async def commands(message: types.Message):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")
    await message.answer("У меня присутствуют такие команды как:\n1)/start\n2)/settings\n3)/help\n4)/weather\n5)/ongoing")

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")
    await message.answer("Я <b>Пинки</b>, бот созданный одним человеком)\nСписок команд: /commands", parse_mode='HTML')

@dp.message_handler(commands=['weather'])
async def weather(message):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")
    await States.city.set()
    await message.answer("Введи название своего города пожалуйста.\nВведи 'отмена' - для отмены команды.")
    
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')

@dp.message_handler(state=States.city)
async def get_weather(message: types.Message, state: FSMContext):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")

    async with state.proxy() as town:
        town['city'] = message.text

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={town['city']}&appid={owm_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
            f"***Хорошего дня!***"
            )

    except:
        await message.answer("\U00002620 Проверьте название города \U00002620")

    await state.finish()

@dp.message_handler(commands=['ongoing'])
async def ongoing_commands(message):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")  
    await States.anime_page.set()
    await message.answer("Введине номер страницы 1-8.\nВведи 'отмена' - для отмены команды.")

@dp.message_handler(state=States.anime_page)
async def choose_page(message: types.Message, state: FSMContext):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n") 
    
    async with state.proxy() as page:
        page['anime_page'] = message.text
    
    try:
        answer = ''
        for i in ongoing(int(page['anime_page'])):
            answer = str(answer) + str(i) + str('\n')

        await message.answer(answer)
    except:
        await message.answer("К сожалению нет страницы с таким номером.")
    
    await state.finish()

@dp.message_handler()
async def talk(message):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")

    if "привет" in (str.lower(message.text)) or "ку" in (str.lower(message.text)) or "куку" in (str.lower(message.text)) or "hello" in (str.lower(message.text)):
        if message.from_user.id == CreatorId:
            await message.answer("Я рада видеть вас создатель))")
        else:
            await message.answer(f"Привет {message.from_user.first_name}!")

    elif "я" in (str.lower(message.text)) and "твой" in (str.lower(message.text)) and "создатель" in (str.lower(message.text)):
        if message.from_user.id == CreatorId:
            await message.answer("Я рада видеть своего создателя))")
        else:
            await message.answer("Не ври мне!!!")

    elif "пока" in (str.lower(message.text)):
        await message.answer("Удачи тебе!")

    elif "как дела" in (str.lower(message.text)) or "как ты" in (str.lower(message.text)):
        await message.answer("У меня всё отлично)\nА ты как?", reply_markup=sentimentMenu)

    elif "ты работаешь" in (str.lower(message.text)):
        await message.answer("Я рада что могу функционировать правильно))")

    elif "ты бот" in (str.lower(message.text)):
        await message.answer("Я и обидется могу!")

    elif "ты не бот" in (str.lower(message.text)):
        await message.answer("Я рада что меня считают человеком)")

    elif "кто ты" in (str.lower(message.text)) or "ты кто" in (str.lower(message.text)):
        await message.answer("Я <b>Пинки</b>))", parse_mode='HTML')

    elif "ля ты крыса" in (str.lower(message.text)):
        await message.answer("А может ты крыса?")

    elif "онгоинг" in (str.lower(message.text)):
        await message.answer("Показать список аниме онгоингов?", reply_markup=anime)

    else:
        await message.answer("Я не знаю что ответить...")

@dp.callback_query_handler(text_contains="sentiment")
async def sentiments(call: types.CallbackQuery):
    try:
        if call.data == 'sentimentGood':
            await bot.send_message(call.message.chat.id, "Вот и хорошо)")

        elif call.data == 'sentimentBad':
            await bot.send_message(call.message.chat.id, "Бывает и хуже)")
        
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="У меня всё отлично)\nА ты как?", reply_markup=None)
    except Exception as e:
        print(repr(e))

@dp.callback_query_handler(text_contains="anime")
async def anime_list(call: types.CallbackQuery):
    try:
        if call.message:
            if call.data == 'animeAll':
                await bot.send_message(call.message.chat.id, "Одну секунду ...")

                answer = ''
                clock = 0

                for i in ongoing_all(1):
                    answer = str(answer) + str(i) + str('\n')
                    clock = clock + 1
                    if clock % 11 == 0:
                        await bot.send_message(call.message.chat.id, answer)
                        clock = 1
                        answer = ''
                        await asyncio.sleep(2)

                await bot.send_message(call.message.chat.id, answer)

            elif call.data == 'animeChoose':
                await States.anime_page.set()
                await bot.send_message(call.message.chat.id, "Введине номер страницы 1-8.\nВведи 'отмена' - для отмены команды.")

            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Показать список аниме онгоингов?", reply_markup=None)

    except Exception as e:
        print(repr(e))

if __name__ == "__main__":
    executor.start_polling(dispatcher = dp)