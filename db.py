import os
from datetime import datetime
import psycopg2
from dotenv import load_dotenv
import logging

load_dotenv()


class PostgresTable:
    def __init__(self):
        """
        Парматры для подключения к бд.
        """

        self.database = os.environ['DATABASE']
        self.user = os.environ['USER']
        self.password = os.environ['PASSWORD']
        self.host = os.environ['HOST']
        self.port = os.environ['PORT']

    def insert_data(self, rows, usd):
        """
        Вставляет новые данные в базу данных.

        :param rows: список строк
        :param usd: курс доллара
        :return: None
        """
        connection = psycopg2.connect(
            database="postgres",
            user='postgres',
            password='password',
            host='localhost',
            port='5432'
        )
        cursor = None
        try:
            cursor = connection.cursor()
            for row in rows:
                rub = usd * int(row[2])
                row.append(rub)
                mysql_insert_query = f"""INSERT INTO home_orders(num, order_num, cost_usd, delivery_time, cost_rub) VALUES {tuple(row)}"""
                cursor.execute(mysql_insert_query)
                connection.commit()

        except Exception as e:
            logging.warning(f" Error while connecting: insert_data-  {e}")

        finally:
            if connection:
                cursor.close()
                connection.close()

    def update_data(self, rows, usd):
        """
        Обновляет существующие данные в базе данных.

        :param rows: список строк
        :param usd: курс доллара
        :return: None
        """
        connection = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        cursor = None
        try:
            cursor = connection.cursor()
            for row in rows:
                rub = usd * row[2]
                sql_update_query = f"""
                UPDATE home_orders 
                SET order_num={row[1]}, cost_usd={row[2]}, delivery_time='{datetime.strftime(row[3], '%d.%m.%Y')}', cost_rub={rub} 
                WHERE num ={row[0]}"""
                cursor.execute(sql_update_query)
                connection.commit()


        except Exception as e:
            logging.warning(f" Error while connecting: update_data-  {e}")

        finally:
            if connection:
                cursor.close()
                connection.close()

    def delete_data(self):
        """
        Удаляет все данные из базы данных.
        """
        connection = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        cursor = None
        try:
            mysql_delete_query = f"DELETE from home_orders  "
            cursor = connection.cursor()
            cursor.execute(mysql_delete_query)
            connection.commit()


        except Exception as e:
            logging.warning(f" Error while connecting: delete_data-  {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def get_data(self, query):
        """
        Возвращает данные из бд по sql запросу.
        """
        connection = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        cursor = None
        try:
            if connection:
                cursor = connection.cursor()
                cursor.execute(query)
                records = cursor.fetchall()
                return records

        except Exception as e:
            logging.warning(f" Error while connecting: get_data-  {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def insert_query(self, query):
        """
        Выполняет любой переданные sql запрос.

        :param query: sql запрос
        :return: Список полученных по запросу строк в бд.
        """
        print(query)
        connection = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        cursor = None
        try:
            if connection:
                mysql_delete_query = f"{query} "
                cursor = connection.cursor()
                cursor.execute(mysql_delete_query)
                connection.commit()
                records = cursor.fetchall()
                return records


        except Exception as e:
            logging.warning(f" Error while connecting: insert_query-  {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()
