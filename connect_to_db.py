import logging
import sqlite3
from logger import create_logger
"""Модуль для подключения к БД. Изначально реализовал на постгре но позже, для наглядности, переделал на лайт."""

#

# def connect_to_db():
#     try:
#         connect = psycopg2.connect("dbname=postgres",
#                                    user="postgres",
#                                    password="postgres",
#                                    host="localhost",
#                                    port="5432"
#                                    )
#         print("Successfully connected to PostgreSQL")
#         return connect
#     except psycopg2.OperationalError:
#         print("Database connection failed.")
#         return None
#
#
# conn = connect_to_db()
def connect_to_db():
    create_logger().info("Подключение к базе данных.")
    try:
        with sqlite3.connect('db/my_app.db') as connection:
            print("Подключение к базе данных завершено.")
            create_logger().info("Подключение к базе данных завершено.")
            return connection
    except sqlite3.Error as error:
        create_logger().error(error)
        print(f"Произошла ошибка подключения - {error}")
