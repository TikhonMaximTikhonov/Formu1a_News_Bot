# coding: utf-8

import telebot
from os import environ
from database import DataBase

bot = telebot.TeleBot(environ.get("TOKEN"))


def create_markup(main_buttons_data):
    markup = telebot.types.ReplyKeyboardMarkup(True)
    for button_data in main_buttons_data:
        markup.row(telebot.types.KeyboardButton(button_data))
    return markup


@bot.message_handler(content_types=["text"],
                     func=lambda message: message.text == "Подписаться")
@bot.message_handler(commands=["start"])
def on(message):
    if data_base.create_user(message.from_user.id) is False:
        data_base.subscribe(message.from_user.id)
    bot.send_message(message.from_user.id, "Вы успешно подписались на новости",
                     reply_markup=create_markup(["Отписаться"]))


@bot.message_handler(content_types=["text"],
                     func=lambda message: message.text == "Отписаться")
def off(message):
    data_base.unsubscribe(message.from_user.id)
    bot.send_message(message.from_user.id, "Вы успешно отписались от новостей",
                     reply_markup=create_markup(["Подписаться"]))


if __name__ == '__main__':
    data_base = DataBase("database.db")
    bot.polling()
