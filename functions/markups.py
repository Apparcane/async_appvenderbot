from os import name
from subprocess import call
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

sentimentMenu = InlineKeyboardMarkup(row_width=2)
btnGood = InlineKeyboardButton(text="Отлично!", callback_data="sentimentGood")
btnBad = InlineKeyboardButton(text="Так себе.", callback_data="sentimentBad")

sentimentMenu.insert(btnGood)
sentimentMenu.insert(btnBad)

anime = InlineKeyboardMarkup(row_width=2)
btnAll = InlineKeyboardButton("Все", callback_data='animeAll')
btnChoose = InlineKeyboardButton("Ввести значение", callback_data='animeChoose')

anime.insert(btnAll)
anime.insert(btnChoose)