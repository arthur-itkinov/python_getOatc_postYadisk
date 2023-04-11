
import requests
import datetime
import openpyxl
import os
from dateTimeConversion import dateTimeConversion
import yadisk
import shutil
import telebot


now = datetime.datetime.now()
today = datetime.datetime.now()
delta = datetime.timedelta(days=30)
dateback = today - delta
dayback = dateback.strftime("%d")
monthback = dateback.strftime("%m")
yearback = dateback.strftime("%Y")
full_day = dateback.strftime("%d-%m-%Y")
full_time_day = dateback.strftime("%d-%m-%Y %H:%M:%S")
id = ''


# TODO отправка в телеграм
token_telegram = ''  # сюда вставить токен телеграм
bot = telebot.TeleBot(token_telegram)
chat_id = ''  # сюда вставить chatId


def send_message_telegram(text):
    bot.send_message(chat_id, text)

# TODO загрузка информации по разговорам


def getRecord(id):
    if id == '':
        url = 'https://cloudpbx.beeline.ru/apis/portal/records?dateFrom={yearback}-{monthback}-{dayback}T00%3A00%3A59.000Z&dateTo={yearback}-{monthback}-{dayback}T23%3A59%3A59.000Z'.format(
            yearback=yearback, monthback=monthback, dayback=dayback)

    else:
        url = 'https://cloudpbx.beeline.ru/apis/portal/records?id={id}&dateFrom={yearback}-{monthback}-{dayback}T00%3A00%3A59.000Z&dateTo={yearback}-{monthback}-{dayback}T23%3A59%3A59.000Z'.format(
            id=id, yearback=yearback, monthback=monthback, dayback=dayback)
    headers = {'X-MPBX-API-AUTH-TOKEN': ''}  # сюда вставить токен оатс билайна
    abonents = requests.get(url, headers=headers)
    if abonents:
        recordId = add_record_in_excel(abonents.json())
        if recordId != '':
            if id != recordId:
                id = recordId
                getRecord(id)
            else:
                return
        else:
            return
    else:
        send_message_telegram(
            f'запрос на получение записей от {yearback}-{monthback}-{dayback} не сработал')
        return


# TODO создание excel file


def crate_excel_file():
    book = openpyxl.Workbook()
    sheet = book.active
    sheet['A1'] = 'ID звонка'
    sheet['B1'] = 'PHONE'
    sheet['C1'] = 'Направление'
    sheet['D1'] = 'Дата'
    sheet['E1'] = 'USERID'
    sheet['F1'] = 'Телефон сотрудника'
    sheet['G1'] = 'Имя сотрудника'
    sheet['H1'] = 'Имя файла'
    book.save(f'{dayback}-{monthback}-{yearback}.xlsx')
    book.close()

# TODO загрузка mp3


def fileLoad(idfile, firstname, phone):

    url = f'https://cloudpbx.beeline.ru/apis/portal/v2/records/{idfile}/download'
    headers = {'X-MPBX-API-AUTH-TOKEN': ''}  # сюда вставить токен оатс билайна
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(f'{idfile}-{firstname}-{phone}.mp3', 'wb') as f:
            f.write(response.content)
            f.closed
    return f'{idfile} {firstname} {phone}.mp3'

# TODO добавление записей в эксель


def add_record_in_excel(abonents):
    recordId = ''
    fn = f'{dayback}-{monthback}-{yearback}.xlsx'
    wb = openpyxl.load_workbook(fn)
    ws = wb['Sheet']
    for abonent in abonents:
        recordId = abonent['id']
        ws.append([abonent['id'], abonent['phone'],
                   abonent['direction'], dateTimeConversion(abonent['date']),
                   abonent['abonent']['userId'],
                   abonent['abonent']['phone'],
                   abonent['abonent']['firstName'],
                   fileLoad(abonent['id'], abonent['abonent']['firstName'], abonent['phone'])])
    wb.save(fn)
    wb.close()
    return recordId


def start():
    if not os.path.isdir(f"{dayback}-{monthback}-{yearback}"):
        os.mkdir(f"{dayback}-{monthback}-{yearback}")
    os.chdir(f"{dayback}-{monthback}-{yearback}")
    crate_excel_file()
    getRecord(id)


start()
