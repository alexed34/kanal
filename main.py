import time
from datetime import datetime, date
from typing import List

import gspread
import requests
from db import PostgresTable
from xml.etree import ElementTree
from telegram_bot import send_telegram
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(filename='log.txt', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



def get_datas_to_googlesheet(file_json) -> List:
    """
    Получает все записи из гугл таблицы

    :param file_json: файл с ключами для подключения
    :return: Список кортежей с записями
    """
    gp = gspread.service_account(filename=file_json)
    gsheet = gp.open('test1')
    wsheet = gsheet.worksheet("sh1")
    return wsheet.get_all_values()


def check_delivery_date(datas_googlesheet: List) -> None:
    """
    Отправляет сообщения по датам срок поставки которых прошел.

    :param datas_googlesheet: записи из гугл таблицы
    :return: None
    """
    orders_and_date = [(line[0], datetime.strptime(line[3], '%d.%m.%Y').date()) for line in datas_googlesheet[1:]]
    orders_and_date = sorted(orders_and_date, key=lambda x: x[1])
    date_now = date.today()
    for order in orders_and_date:
        if order[1] < date_now:
            send_telegram(f"Дата прошла, номер заказа {order[1]}")
            logging.warning('telegran')
            



def check_data_googlesheet(datas_from_db: List, datas_googlesheet: List):
    """
    Сравнивает записи из таблицы с записями из базы данных. И находит записи которые надо обновить или добавить.

    :param datas_from_db: Записи из базы данных совподающие по полю num с записями из гугл таблица
    :param datas_googlesheet: Записи из гугл таблицы
    :return: dates_for_update - список записей которые надо обновить, dates_for_insert - список записей которые надо добавить
    """
    dates_for_update, dates_for_insert = [], []
    num_for_db = [line[0] for line in datas_from_db]
    dict_datas_from_db = {line[0]: line for line in datas_from_db}
    for data in datas_googlesheet[1:]:
        num = int(data[0])
        if num in num_for_db:
            data_db = dict_datas_from_db[num]
            data = (int(data[0]), int(data[1]), int(data[2]), datetime.strptime(data[3], '%d.%m.%Y').date())
            if data_db[:-1] != data:
                dates_for_update.append(data)
        else:
            dates_for_insert.append(data)
    return dates_for_update, dates_for_insert


def get_dollar_exchange_rate() -> float:
    """
    Получить курс доллара с сайта центробанка.

    :return: число
    """
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp?')
    tree = ElementTree.fromstring(response.content).findall('./')
    usd = '0,0'
    for i in tree:
        if i.attrib['ID'] == 'R01235':
            usd = i.findall('./')[4].text
            break
    return float(usd.replace(',', '.'))


if __name__ == "__main__":
    load_dotenv()
    db = PostgresTable()
    file_json = os.environ['PATH_TO_FILE_JSON']
    usd = get_dollar_exchange_rate()
    while True:
        datas_googlesheet = get_datas_to_googlesheet(file_json)
        check_delivery_date(datas_googlesheet)
        nums_line_googleshit = [line[0] for line in datas_googlesheet[1:]]
        datas_from_db = db.get_data(f"select * from home_orders WHERE num in {tuple(nums_line_googleshit)}")
        dates_for_update, dates_for_insert = check_data_googlesheet(datas_from_db, datas_googlesheet)
        if dates_for_update:
            db.update_data(dates_for_update, usd)
        if dates_for_insert:
            db.insert_data(dates_for_insert, usd)
        time.sleep(60)
        one_day = time.time() % 86400
        if 0 <= one_day < 60:
            usd = get_dollar_exchange_rate()
