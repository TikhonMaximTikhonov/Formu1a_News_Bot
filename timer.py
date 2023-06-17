import telebot
from time import sleep
from datetime import datetime
from os import environ

from bs4 import BeautifulSoup as BS
import requests

from database import DataBase

bot = telebot.TeleBot(environ.get("TOKEN"))


def timer():
    while True:
        parser = BS(requests.get("https://www.f1news.ru/").text, "lxml")

        all_news = []
        for news in parser.findAll("div", {"class": "b-news-list__info"}):
            if ":" in news.findNext("a", {"class": "news_date b-news-list__date"}).text:
                all_news.append(news)

        if len(all_news) < data_base.len_news():
            data_base.del_news()

        database_news = data_base.return_news()
        for news in all_news:
            if news.a.text not in database_news:
                data_base.create_news(news.a.text)

                url = "https://www.f1news.ru" + news.a.get("href")
                parser = BS(requests.get(url).text, "lxml").find("div", {"class": "widget post"})
                message_data = [f"<b>{parser.find('h1').text}</b>\n\n"]
                for line in parser.findAll("p"):
                    if "strong" in str(line):
                        new_line = f"<i>{line.text}</i>\n\n"
                    else:
                        new_line = f"{line.text}\n\n"
                    if (len(message_data[-1] + new_line) > 1024 and len(message_data) == 1) or len(
                            message_data[-1] + new_line) > 4096:
                        message_data.append("")
                    message_data[-1] += new_line
                link = f"\n<b>Ссылка на источник: {url}</b>"
                if (len(message_data[-1] + new_line) > 1024 and len(message_data) == 1) or len(
                        message_data[-1] + new_line) > 4096:
                    message_data.append("")
                message_data[-1] += link

                image = "https:" + parser.find("img").get("src")
                print(image, len(message_data))
                for user_id in data_base.return_users():
                    bot.send_photo(user_id, image, message_data[0], parse_mode='html')
                    for message in message_data[1::]:
                        bot.send_message(user_id, message, parse_mode='html')
        sleep(300)
        print("Обновление данных " + str(datetime.now()))


if __name__ == '__main__':
    data_base = DataBase("database.db")
    timer()
