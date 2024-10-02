from bot_token import API_TOKEN, obj_to_json

from telebot import TeleBot
from telebot.handler_backends import ContinueHandling


bot = TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):

    print(message)
    print(type(message))
    print(message.content_type)
    print(message.id)
    print(message.message_id)
    print(message.from_user)
    print(message.date)
    print(message.chat)
    print(message.sender_chat)
    # ...
    print(message.text)
    print(message.entities)
    print(message.audio)
    print(message.document)
    print(message.photo)
    print(message.sticker)
    print("-------------------")
    print(f'Message json欄位內容如下......{type(message.json)}')
    # print(message.json)
    print(f'message_id = {message.json["message_id"]}')
    print(f'from       = {message.json["from"]}')
    print(f'chat       = {message.json["chat"]}')
    print(f'date       = {message.json["date"]}')
    print(f'text       = {message.json["text"]}')
    print(f'entities   = {message.json["entities"]}')

    bot.send_message(message.chat.id, 'Hello World!')
    bot.send_message(message.chat.id, 'Hello World1!')
    return ContinueHandling()

@bot.message_handler(commands=['start'])
def start2(message):
    """
    This handler comes after the first one, but it will never be called.
    But you can call it by returning ContinueHandling() in the first handler.

    If you return ContinueHandling() in the first handler, the next
    registered handler with appropriate filters will be called.
    """
    bot.send_message(message.chat.id, 'Hello World2!')

bot.infinity_polling()