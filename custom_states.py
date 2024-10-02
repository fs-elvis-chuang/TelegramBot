from bot_token import API_TOKEN

import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.storage import StateMemoryStorage

# Initialize the bot
state_storage = StateMemoryStorage()  # don't use this in production; switch to redis
bot = telebot.TeleBot(API_TOKEN, state_storage=state_storage, use_class_middlewares=True)


# Define states
class MyStates(StatesGroup):
    name = State()
    age = State()
    color = State()
    hobby = State()


# Start command handler
@bot.message_handler(commands=["start"])
def start_ex(message: types.Message, state: StateContext):

    # 設定目前進入 name state
    state.set(MyStates.name)

    bot.send_message(message.chat.id, "Hello! What is your first name?", reply_to_message_id=message.message_id)
    print(f'@start: message.message_id = {message.message_id}')


# Cancel command handler
@bot.message_handler(state="*", commands=["cancel"])
def any_state(message: types.Message, state: StateContext):
    state.delete()
    bot.send_message(message.chat.id,"Your information has been cleared. Type /start to begin again.", reply_to_message_id=message.message_id)
    print(f'@cancel: message.message_id = {message.message_id}')


# Handler for name input
@bot.message_handler(state=MyStates.name)
def name_get(message: types.Message, state: StateContext):

    # 設定目前進入 age state
    state.set(MyStates.age)

    bot.send_message(message.chat.id, "How old are you?", reply_to_message_id=message.message_id)
    # 等待回應

    # 等到使用者輸入訊息後會回到這裡
    state.add_data(name=message.text)
    print(f'@age: message.message_id = {message.message_id}')


# Handler for age input
@bot.message_handler(state=MyStates.age, is_digit=True)
def ask_color(message: types.Message, state: StateContext):

    state.set(MyStates.color)
    state.add_data(age=message.text)

    # Define reply keyboard for color selection
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    colors = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange", "Other"]
    buttons = [types.KeyboardButton(color) for color in colors]
    keyboard.add(*buttons)

    bot.send_message(
        message.chat.id,
        "What is your favorite color? Choose from the options below.",
        reply_markup=keyboard,
        reply_to_message_id=message.message_id,
    )


# Handler for color input
@bot.message_handler(state=MyStates.color)
def ask_hobby(message: types.Message, state: StateContext):
    state.set(MyStates.hobby)
    state.add_data(color=message.text)

    # Define reply keyboard for hobby selection
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    hobbies = ["Reading", "Traveling", "Gaming", "Cooking"]
    buttons = [types.KeyboardButton(hobby) for hobby in hobbies]
    keyboard.add(*buttons)

    bot.send_message(message.chat.id,"What is one of your hobbies? Choose from the options below.", reply_markup=keyboard, reply_to_message_id=message.message_id)


# Handler for hobby input
@bot.message_handler(
    state=MyStates.hobby, text=["Reading", "Traveling", "Gaming", "Cooking"]
)
def finish(message: types.Message, state: StateContext):
    with state.data() as data:
        name = data.get("name")
        age = data.get("age")
        color = data.get("color")
        hobby = message.text  # Get the hobby from the message text

        # Provide a fun fact based on color
        color_facts = {
            "Red": "Red is often associated with excitement and passion.",
            "Green": "Green is the color of nature and tranquility.",
            "Blue": "Blue is known for its calming and serene effects.",
            "Yellow": "Yellow is a cheerful color often associated with happiness.",
            "Purple": "Purple signifies royalty and luxury.",
            "Orange": "Orange is a vibrant color that stimulates enthusiasm.",
            "Other": "Colors have various meanings depending on context.",
        }
        color_fact = color_facts.get(
            color, "Colors have diverse meanings, and yours is unique!"
        )
        # https://core.telegram.org/bots/api#markdownv2-style
        msg = (
            f"<i>Thank you for sharing! Here is a summary of your information:</i>\n"
            f"<u>First Name: {name}</u>\n"
            f"<b>Age: {age}</b>\n"
            f"<s>Favorite Color</s>: {color} <strike>Favorite Color</strike> <del>Favorite Color</del>\n"   # 刪除線
            f"<code>Fun Fact about your color</code>: {color_fact}\n"           # 程式碼
            f"<code>Fun <u>Fact</u> about your color</code>: {color_fact}\n"    # 程式碼，底線無效
            f"<pre>Favorite Hobby: {hobby}</pre>❤️\n"
            f'<a href="http://www.google.com/">超連結到Google</a>\n'
            f'<code>程式碼、程式碼、程式碼、程式碼、程式碼、程式碼、程式碼、程式碼、程式碼、程式碼、程式碼、程式碼、程式碼、</code>\n'
            f'<b><i>粗斜字體</i></b>\n'
            f'<tg-spoiler>不要劇透</tg-spoiler>\n'
            f'<a href="tg://user?id=6812403854">inline mention of a user用戶資訊</a>\n'   # 顯示用戶資訊
            f'😊😍💕❤️😶😶😶直接使用\n'
            f'<tg-emoji emoji-id="5368324170671202286">123456👍</tg-emoji>\n'
            # f'<tg-emoji emoji-id="5368324170671202286">9876543210</tg-emoji>\n' # 這樣不會顯示
            f'<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>\n'
            f'<blockquote>1. Block quotation started\n2. Block quotation continued\n3. The last line of the block quotation</blockquote>'
            # 可捲動的引用
            f'<blockquote expandable>1.Expandable block quotation started\n2. Expandable block quotation continued\n3. Expandable block quotation continued\n4. Hidden by default part of the block quotation started\nExpandable block quotation continued\nThe last line of the block quotation</blockquote>'
        )

    bot.send_message(
        message.chat.id, msg, parse_mode="html", reply_to_message_id=message.message_id
    )
    state.delete()


# Handler for incorrect age input
@bot.message_handler(state=MyStates.age, is_digit=False)
def age_incorrect(message: types.Message):
    bot.send_message(
        message.chat.id,
        "Please enter a valid number for age.",
        reply_to_message_id=message.message_id,
    )


# Add custom filters
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())

# necessary for state parameter in handlers.
from telebot.states.sync.middleware import StateMiddleware

bot.setup_middleware(StateMiddleware(bot))

# Start polling
bot.infinity_polling()