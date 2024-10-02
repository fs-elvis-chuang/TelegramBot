from bot_token import API_TOKEN


#!/usr/bin/python

# This is an example file to create 【quiz polls=測試民調】
import telebot
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=["poll"])
def create_poll(message):
    bot.send_message(message.chat.id, "English Article Test")   # 標題
    answer_options = ["a", "an", "the", "-"]                    # 0 1 2 3

    bot.send_poll(
        chat_id=message.chat.id,
        question="We are going to '' park.",                    # 題目
        options=answer_options,
        type="quiz",
        correct_option_id=2,
        is_anonymous=False,
    )


@bot.poll_answer_handler()
def handle_poll(poll):
    # This handler can be used to log User answers and to send next poll
    print(f'poll= {poll}')
    pass


bot.infinity_polling()