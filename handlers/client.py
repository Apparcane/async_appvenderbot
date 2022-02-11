from handlers.callback_query import sentiments, anime_list
from config import CreatorId
from functions.markups import sentimentMenu, anime

from aiogram import Dispatcher, types

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

def register_handlers_clients(dp: Dispatcher):
    dp.register_message_handler(talk, content_types=['text'])