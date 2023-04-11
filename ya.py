import yadisk
import datetime

import os
import shutil
import telebot

now = datetime.datetime.now()
today = datetime.datetime.now()
delta = datetime.timedelta(days=30)
dateback = today - delta
dayback = dateback.strftime("%d")
monthback = dateback.strftime("%m")
yearback = dateback.strftime("%Y")

y = yadisk.YaDisk(
    token="")  # сюда вставить токен яндекс диска


token = ''  # сюда вставить токен телеграмма
bot = telebot.TeleBot(token)
chat_id = ''  # сюда вставить chatId telegram


def send_message_telegram(path):
    if y.exists(f'{path}'):
        text = f"Записи разговоров за {dayback}-{monthback}-{yearback} загружены в каталог ЯДиск/OATC/{dayback}-{monthback}-{yearback}"
        bot.send_message(chat_id, text)
    else:
        text = f"Записи разговоров за {dayback}-{monthback}-{yearback} НЕ загружены"
        bot.send_message(chat_id, text)


# создаю папку на яндекс диске в папке OATC
y.mkdir(f'OATC/{dayback}-{monthback}-{yearback}')
# прохожусь по файлам папки с файлами и отправляю в соответствеющую папку на яндекс диске.
directory = f'{dayback}-{monthback}-{yearback}'


def send_file_yadisk():
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if os.path.isfile(file):
            y.upload(file, f'/OATC/{dayback}-{monthback}-{yearback}/{file}')
    send_message_telegram(
        f'/OATC/{dayback}-{monthback}-{yearback}/')
    shutil.rmtree(f'{dayback}-{monthback}-{yearback}')


send_file_yadisk()
