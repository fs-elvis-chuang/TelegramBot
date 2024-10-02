from bot_token import API_TOKEN


# This example show how to write an inline mode telegram bot use pyTelegramBotAPI.
import logging
import sys
import time

import telebot
from telebot import types

bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.ERROR)

# 測試方式
# 在輸入訊息欄： 輸入 @follow_suit_bot
# 1. 如果沒有後面參數則會出現 【default】按鈕選項
# 2. 如果輸入text  【default】按鈕選項


@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        print(f'------------------------------------1')
        r = types.InlineQueryResultArticle('1', 'Result1', types.InputTextMessageContent('hi_1'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('hi_2'))
        print(r, r2)
        bot.answer_inline_query(inline_query.id, [r, r2])
        print(f'End of query_text')
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: query.query == 'photo1')
def query_photo(inline_query):
    try:
        print(f'------------------------------------2')
        r = types.InlineQueryResultPhoto('1',
                                         'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/kitten.jpg',
                                         'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/kitten.jpg',
                                         input_message_content=types.InputTextMessageContent('hi photo1 111'),                                                  # 當使用者選中該項目，只會顯示此字串
                                         )
        r2 = types.InlineQueryResultPhoto('2',                                                                                                                  # id
                                          'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg',          # photo url
                                          'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg',          # photo thumbnail， 後面參數就必須過指定的方式
                                          caption= 'Caption 標題',
                                          show_caption_above_media=True,
                                          )

        bot.answer_inline_query(inline_query.id, [r, r2], cache_time=1)
        print(f'End of query_photo')
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: query.query == 'video')
def query_video(inline_query):
    try:
        print(f'------------------------------------3')
        r = types.InlineQueryResultVideo('1',
                                         'https://github.com/eternnoir/pyTelegramBotAPI/blob/master/tests/test_data/test_video.mp4?raw=true',
                                         'video/mp4',
                                         'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg',
                                         'Title---標題'
                                         )
        bot.answer_inline_query(inline_query.id, [r])
        print(f'End of query_video')
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: len(query.query) == 0)
def default_query(inline_query):
    try:
        print(f'------------------------------------0')
        print(f'inline_query= {inline_query}')
        r = types.InlineQueryResultArticle('1',
                                           'default',
                                           types.InputTextMessageContent('你選擇了 default')
                                           )
        if bot.answer_inline_query(inline_query.id, [r]):
            print(f'回傳為真')
        else:
            print(f'回傳為False')
        print(f'End of default_query')

    except Exception as e:
        print(e)


def main_loop():
    bot.infinity_polling()
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)