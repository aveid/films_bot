from decouple import config
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import random

from film_names import films

bot = telebot.TeleBot(config("TOKEN"))


@bot.message_handler(commands=["start", "привет"])
def get_hello(message):
    text = f"Привет {message.from_user.username}!!! \n" \
           f"Добро пожаловать выберите жанр который вас интересует:"
    murkup = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in films:
        button = KeyboardButton(i.get("genre"))
        murkup.add(button)
    bot.send_message(message.chat.id, text, reply_markup=murkup)


#
# @bot.message_handler(content_types=["text"])
# def get_films(message):
#     markup = InlineKeyboardMarkup(row_width=2)
#     for i in films:
#         if i.get("genre") == message.text:
#             my_film = random.choice(i.get("films"))
#             print(my_film)
#             button2 = InlineKeyboardButton(text=my_film.get('title'), url=my_film.get('link'))
#             markup.add(button2)
#             text = f"<b>Я рекомендую вам фильм {my_film.get('title')} c рейтингом {my_film.get('rating')} " \
#                 f"перейдите по ссылке приятного просмотра!!!</b>"
#         else:
#             text = "Фильмов этого жанра мы не нашли!"
#     bot.reply_to(message, text, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=["text"])
def get_films(message):
    markup = InlineKeyboardMarkup(row_width=2)
    for i in films:
        if i.get("genre") == message.text:
            for film in i.get("films"):
                button = InlineKeyboardButton(text=film.get('title'), callback_data=film.get('title'))
                markup.add(button)
            text = "Можете выбрать фильм который по душе:)"
        else:
            text = "Фильмов этого жанра мы не нашли!"
    bot.reply_to(message, text, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(lambda call: True)
def handler_call_data(call):
    markup = InlineKeyboardMarkup(row_width=2)
    photo1 = open("images/avatars-000437845644-c65edy-t500x500.jpeg", 'rb')
    for i in films:
        for j in i.get("films"):
            if j.get("title") == call.data:
                button = InlineKeyboardButton(text=j.get('title'), url=j.get('link'))
                markup.add(button)
                text = f"Фильм: {j.get('title')}\nРейтинг: {j.get('rating')}\nПриятного просмотра!"
                photo1 = open(j.get('image'), "rb")
    bot.send_photo(call.message.chat.id, photo1)
    bot.send_message(call.message.chat.id, text, reply_markup=markup)


bot.polling()
