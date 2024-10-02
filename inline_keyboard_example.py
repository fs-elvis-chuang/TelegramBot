from bot_token import API_TOKEN


# This example show how to use inline keyboards and process button presses
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = API_TOKEN

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def gen_markup() -> InlineKeyboardMarkup:
    """
    建立鍵盤並將此鍵盤回傳
    :return: 鍵盤markup
    """
    # 1. 建立Keyboard
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    # 2. 添加按鈕
    markup.add(InlineKeyboardButton("🆗Yes", callback_data="cb_yes"),    # 按鈕1： a. 設定按鈕標題 b.當使用者按選該按鈕，則callback傳遞data名稱"cb_yes"
               InlineKeyboardButton("No", callback_data="cb_no")         # 按鈕2： a. 設定按鈕標題 b.當使用者按選該按鈕，則callback傳遞data名稱
               )

    print(f'InlineKeyboardMarkup= {markup}')
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(f'callback_query()所獲得的{type(call)} = {call}')
    print(f'CallbackQuery ID= {call.id}')
    print(f'CallbackQuery from_user= {call.from_user}')
    print(f'CallbackQuery message= {call.message}')
    print(f'CallbackQuery message.from_user= {call.message.from_user}')
    print(f'CallbackQuery message.chat= {call.message.chat}')
    print(f'CallbackQuery message.text= {call.message.text}')
    print(f'***CallbackQuery data= {call.data}')
    print(f'CallbackQuery json= {call.json}')
    # print(f'CallbackQuery json.message.chat= {call.json.message.chat}')
    # print(f'CallbackQuery json.message.reply_markup= {call.json.message.reply_markup}')
    # print(f'CallbackQuery json.message.text= {call.message.text}')
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(
        message.chat.id,                # 傳送的對象 chat.id
        # "Yes/no?\n123\n456",                      # 傳送的文字內容
        "期",  # 傳送的文字內容
        reply_markup=gen_markup()
    )

bot.infinity_polling()