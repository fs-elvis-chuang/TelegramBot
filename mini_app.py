from bot_token import API_TOKEN


# The source of the "https://pytelegrambotminiapp.vercel.app"
# can be found in https://github.com/eternnoir/pyTelegramBotAPI/tree/master/examples/mini_app_web

from telebot import TeleBot
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

BOT_TOKEN = API_TOKEN
WEB_URL = "https://pytelegrambotminiapp.vercel.app"
WEB_URL1 = "https://www.google.com.tw"

bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    # 1. 建立reply_keyboard
    reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_keyboard_markup.row(KeyboardButton("【Reply】按鈕", web_app=WebAppInfo(WEB_URL)))

    # 2. 建立inline keyboard
    inline_keyboard_markup = InlineKeyboardMarkup()
    inline_keyboard_markup.row(InlineKeyboardButton('【Inline】按鈕', web_app=WebAppInfo(WEB_URL1)))

    bot.reply_to(message, "Click 【inline】 button to start Google", reply_markup=inline_keyboard_markup)
    bot.reply_to(message, "Click 【reply】 button to start MiniApp", reply_markup=reply_keyboard_markup)

@bot.message_handler(content_types=['web_app_data'])
def web_app(message):
    print(f'Web 回傳回來的訊息 is "{message.web_app_data.data}"')
    bot.reply_to(message, f'Web 回傳回來的訊息 is "{message.web_app_data.data}"')

bot.infinity_polling()