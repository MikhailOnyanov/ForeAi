import logging
import requests

from constants import TELEGRAM_API_KEY, MAX_SYM, FORE_AI_BACKEND_API

import telebot
from telebot import types

bot = telebot.TeleBot(TELEGRAM_API_KEY)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

EXCEPTION_TEXT = f"Не могу обработать запрос :( \nСейчас сервис недоступен" \
                 f"😢, но мы делаем всё, чтобы восстановить его работу! ⚙️"


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Активировать тестовый период")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)


def get_message_from_ai_model(message) -> str | None:
    logger.info(f"Sending query {message} to {FORE_AI_BACKEND_API}")
    try:
        response = requests.get(FORE_AI_BACKEND_API, params={"message": message})
        logger.debug(f"Response from service: {response}, {response.status_code}, {response.text}")
        if response.status_code == 500:
            logger.warning(f"Message service returned 500, raising exception")
        elif response.status_code == 200:
            return response.text
        else:
            logger.warning(f"Message service returned {response.status_code}, raising exception")
    except Exception as ex:
        logger.exception(ex)


@bot.message_handler(func=lambda message: message.text == "👋 Активировать тестовый период", content_types=['text'])
def handle_test_period_activation(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Adding new button
    btn0 = types.KeyboardButton("Меню")
    markup.add(btn0)
    bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup)  # Bot response


@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    try:
        nearest_answer = get_message_from_ai_model(message.text)
        prepared = nearest_answer.strip('\"').replace("\\n", "\n")
        if len(nearest_answer) > MAX_SYM:
            for x in range(0, len(nearest_answer), MAX_SYM):
                bot.reply_to(message, text=prepared[x:x + MAX_SYM])
        else:
            bot.reply_to(message, text=prepared)
    except Exception as ex:
        bot.reply_to(message, text=EXCEPTION_TEXT)
        logger.exception(ex)


def run():
    logger.info("BOT IS UP")
    bot.polling(non_stop=True, interval=0)  # Required for running bot


run()
