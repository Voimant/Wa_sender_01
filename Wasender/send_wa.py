import datetime

import pandas as pd
from aiogram import Bot
from tqdm import tqdm
import time
from whatsapp_api_client_python import API
from config import TOKEN_WA, INST, TOKEN_TG
import csv

greenAPI = API.GreenApi(INST, TOKEN_WA)
bot = Bot(token=TOKEN_TG)


def save_report(number):
    """Отчет об неотправленых сообщениях, ДАТА И НОМЕР ТЕЛЕФОНА"""
    try:
        x = datetime.date.today()
        with open('report.txt', 'a') as f:
            f.write(f'\n{str(x)} ----- {str(number)}')
    except Exception as er:
        print(er)

def save__send_report(number):
    """Отчет об отправленых сообщениях, ДАТА И НОМЕР ТЕЛЕФОНА"""
    try:
        x = datetime.date.today()
        with open('send_report.txt', 'a') as f:
            f.write(f'\n{str(x)} ----- {str(number)}')
    except Exception as er:
        print(er)


def sender_list_number(text):
    """
    Функция отправляет раз в 1 минуту сообщение по базе list_number
    count счетчик сообщений, когда доходит до 480 уходит в слип на 8 часов.
    минута 60
    час 3600
    8 часов 28800 ( секунд)
    8 часов 480 (минут)
    :param text: текст сообщения
    :return:
    """
    df = pd.read_csv('Wasender/numbers.csv')
    print(df)
    numb_list = df['numbers'].to_list()
    count = 0
    for number in tqdm(numb_list, ncols=50, ascii=True, desc="Обработка файлов"):
        if count < 480:
            send_numbers = pd.read_csv('insert_numbs.csv')
            send_numbers_list = send_numbers['n'].to_list()
            print(send_numbers_list)
            if number not in send_numbers_list:
                notif = greenAPI.serviceMethods.checkWhatsapp(f'{number}')
                if notif.code == 200:
                    try:
                        df = pd.DataFrame({'numbers': [number]})
                        result = greenAPI.sending.sendMessage(f'{number}@c.us', text)
                        df.to_csv('insert_numbs.csv', mode='a', index=False, header=False)
                    except Exception as err:
                        with open('report_erros.txt', 'a') as file:
                            file.write(f'{str(err)} ----{datetime.date.today()}')
                        print(err)
                else:
                    save_report(number)
            else:
                continue
            count += 1
            time.sleep(60)
        elif count >= 480:
            count = 0
            #time.sleep(1)
            time.sleep(28800)
            continue
    df.to_csv('numers_1.csv', mode='w', index=False, header=False)
    new_list = pd.read_csv('insert_numbs.csv')
    cond = new_list['n'].to_list()
    print(new_list)
    print(cond)
    new_list = new_list[new_list.n.isin(cond) == False]
    new_list.to_csv('insert_numbs.csv', index=False)


def sender_list_with_pict(text):
    """
    Функция отправляет раз в 1 минуту сообщение по базе list_number
    count счетчик сообщений, когда доходит до 480 уходит в слип на 8 часов.
    минута 60
    час 3600
    8 часов 28800 ( секунд)
    8 часов 480 (минут)
    :param text: текст сообщения
    :return:
    """
    df = pd.read_csv('Wasender/numbers.csv')
    print(df)
    numb_list = df['numbers'].to_list()
    count = 0
    for number in tqdm(numb_list, ncols=50, ascii=True, desc="Обработка файлов"):
        if count < 480:
            send_numbers = pd.read_csv('Wasender/insert_numbs.csv')
            send_numbers_list = send_numbers['n'].to_list()
            print(send_numbers_list)
            if number not in send_numbers_list:
                df = pd.DataFrame({'numbers': [number]})
                notif = greenAPI.serviceMethods.checkWhatsapp(f'{number}')
                if notif.code == 200:
                    try:
                        save__send_report(f'\n{number} --- {datetime.date.today()}')
                        greenAPI.sending.sendFileByUpload(f'{number}@c.us', "send_photo.jpg", "send_photo.jpg", text)
                        df.to_csv('insert_numbs.csv', mode='a', index=False, header=False)
                    except Exception as err:
                        with open('report_erros.txt', 'a') as file:
                            file.write(f'{str(err)} ----{datetime.date.today()}')
                        print(err)
                else:
                    save_report(number)
            else:
                continue
            count += 1
            time.sleep(60)
        elif count >= 480:
            count = 0
            time.sleep(28800)
            continue
        new_list = pd.read_csv('insert_numbs.csv')
        cond = new_list['n'].to_list()
        print(new_list)
        print(cond)
        new_list = new_list[new_list.n.isin (cond) == False]
        new_list.to_csv('insert_numbs.csv', index=False)


def sender_list_with_video(text):
    """
    Функция отправляет раз в 1 минуту сообщение по базе list_number
    count счетчик сообщений, когда доходит до 480 уходит в слип на 8 часов.
    минута 60
    час 3600
    8 часов 28800 ( секунд)
    8 часов 480 (минут)
    :param text: текст сообщения
    :return:
    """
    df = pd.read_csv('Wasender/numbers.csv')
    print(df)
    numb_list = df['numbers'].to_list()
    count = 0
    for number in tqdm(numb_list, ncols=50, ascii=True, desc="Обработка файлов"):
        if count < 480:
            send_numbers = pd.read_csv('Wasender/insert_numbs.csv')
            send_numbers_list = send_numbers['n'].to_list()
            print(send_numbers_list)
            path_video = "/home/voimant/Рабочий стол/work/Wa_vosmetics/send_video.mp4"
            if number not in send_numbers_list:
                notif = greenAPI.serviceMethods.checkWhatsapp(f'{number}')
                if notif.code == 200:
                    df = pd.DataFrame({'numbers': [number]})
                    try:
                        greenAPI.sending.sendFileByUpload(f'{number}@c.us', path_video, "send_video.mp4", text)
                        df.to_csv('insert_numbs.csv', mode='a', index=False, header=False)
                    except Exception as err:
                        with open('report_erros.txt', 'a') as file:
                            file.write(f'{str(err)} ----{datetime.date.today()}')
                        print(err)
                else:
                    save_report(number)
            else:
                continue
            count += 1
            time.sleep(60)
        elif count >= 480:
            count = 0
            time.sleep(28800)
            continue
        new_list = pd.read_csv('insert_numbs.csv')
        cond = new_list['n'].to_list()
        print(new_list)
        print(cond)
        new_list = new_list[new_list.n.isin (cond) == False]
        new_list.to_csv('insert_numbs.csv', index=False)
