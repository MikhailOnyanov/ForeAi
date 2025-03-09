import logging
import requests

from constants import TELEGRAM_API_KEY, MAX_SYM, FORE_AI_BACKEND_API

import telebot
from telebot import types


bot = telebot.TeleBot(TELEGRAM_API_KEY)


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)


def get_message_from_ai_model(message):
    api = FORE_AI_BACKEND_API
    logger.debug(api)
    response = requests.get(api, params={"message": message})
    logger.debug(response)
    return response.text


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Adding new button
        btn0 = types.KeyboardButton("Задать вопрос ai помощнику Fore ")
        markup.add(btn0)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup)  # Bot response

    else:
        nearest_answer = get_message_from_ai_model(message.text)
        if len(nearest_answer) > MAX_SYM:
            for x in range(0, len(nearest_answer), MAX_SYM):
                bot.reply_to(message, text=nearest_answer[x:x + MAX_SYM])
        else:
            bot.reply_to(message, text=nearest_answer)

        # bot.send_message(message.from_user.id,
        #                  f'Ответ векторной базы данных: {nearest_answer}',
        #                  parse_mode='Markdown')

def run():
    bot.polling(non_stop=True, interval=0) # Required for running bot
