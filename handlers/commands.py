import requests
import json
import datetime

from create_bot import *
from handlers.callback_query import *

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

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

async def settings(message: types.Message):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")
    await message.answer("Меня может редактировать только мой создатель!!")

async def commands(message: types.Message):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")
    await message.answer("У меня присутствуют такие команды как:\n1)/start\n2)/settings\n3)/help\n4)/weather\n5)/ongoing")

async def help(message: types.Message):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")
    await message.answer("Я <b>Пинки</b>, бот созданный одним человеком)\nСписок команд: /commands", parse_mode='HTML')

async def weather(message):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")
    await States.city.set()
    await message.answer("Введи название своего города пожалуйста.\nВведи 'отмена' - для отмены команды.")

async def cancel_handler(message: types.Message, state: FSMContext):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')

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

async def ongoing_commands(message):
    print(f"Id: {message.from_user.id}\nName: {message.from_user.first_name}\nText: {message.text}\n")  
    await States.anime_page.set()
    await message.answer("Введине номер страницы 1-8.\nВведи 'отмена' - для отмены команды.")

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

def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start", "go"])
    dp.register_message_handler(settings, commands=["settings"])
    dp.register_message_handler(commands, commands=["commands"])
    dp.register_message_handler(help, commands=["help"])
    dp.register_message_handler(weather, commands=["weather"])
    dp.register_message_handler(cancel_handler, state='*', commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(get_weather, state=States.city)
    dp.register_message_handler(ongoing_commands, commands=['ongoing'])
    dp.register_message_handler(choose_page, state=States.anime_page)