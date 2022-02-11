from create_bot import *
from functions.ongoing import *
import asyncio
from aiogram import Dispatcher, types

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

def register_handlers_commands(dp: Dispatcher):
    dp.register_callback_query_handler(sentiments, text_contains="sentiment")
    dp.register_callback_query_handler(anime_list, text_contains="anime")