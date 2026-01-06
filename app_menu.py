from logger import create_logger
import json

"""Модуль меню"""


def render_menu(menu_key: str):
    try:
        with open("menu_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        menu = config["MENU_CONFIG"].get(menu_key)
        if not menu:
            raise KeyError(f"Меню '{menu_key}' не найдено!!!")

        print("\n" + "=" * 40)
        print(menu["title"])
        print("=" * 40)
        for k, v in menu["items"].items():
            print(f"{k}. {v}")

    except Exception as e:
        create_logger().exception(e)
        print(f"Неожиданная ошибка: {e}")

# def main_menu():
#     """Главное меню приложения."""
#     create_logger().info("Открыто главное меню")
#     menu_items = {
#         1: "Сотрудники",
#         2: "Проекты",
#         0: "Выход"
#     }
#
#     print("\n" + "=" * 40)
#     print("УПРАВЛЕНИЕ СОТРУДНИКАМИ И ПРОЕКТАМИ")
#     print("=" * 40)
#
#     for k, v in menu_items.items():
#         print(f"{k}. {v}")
#
#     try:
#         choice_menu = int(input("\nВведите номер пункта: "))
#         if choice_menu in menu_items:
#             print(f"Вы выбрали: {menu_items[choice_menu]}")
#             return choice_menu
#         else:
#             print("Ошибка! Нет такого пункта меню.")
#             return None
#     except ValueError as e:
#         create_logger().error(e)
#         print("Ошибка!")
#         return None
#
#
# def workers_menu():
#     """Меню сотрудников"""
#     create_logger().info("Открыто меню сотрудников")
#     menu_items = {
#         1: "Показать сотрудников",
#         2: "Добавить сотрудника",
#         3: "Удалить сотрудника",
#         4: "Добавить отработанные часы",
#         5: "Рассчитать зарплату сотрудника",
#         0: "Вернуться в главное меню"
#     }
#
#     print("\n" + "=" * 40)
#     print("УПРАВЛЕНИЕ СОТРУДНИКАМИ")
#     print("=" * 40)
#
#     for k, v in menu_items.items():
#         print(f"{k}. {v}")
#     try:
#         choice_menu = int(input("\nВведите номер пункта: "))
#         if choice_menu in menu_items:
#             print(f"Вы выбрали: {menu_items[choice_menu]}")
#             return choice_menu
#         else:
#             print("Ошибка! Нет такого пункта меню.")
#             return None
#     except ValueError:
#         print("Ошибка! Введите число от 0 до 5.")
#         return None
#
#
# def projects_menu():
#     """Меню проектов"""
#     create_logger().info("Открыто меню проектов")
#     menu_items = {
#         1: "Список проектов",
#         2: "Детали проекта",
#         3: "Добавить проект",
#         0: "Вернуться в главное меню"
#     }
#
#     print("\n" + "=" * 40)
#     print("УПРАВЛЕНИЕ ПРОЕКТАМИ")
#     print("=" * 40)
#
#     for k, v in menu_items.items():
#         print(f"{k}. {v}")
#     try:
#         choice_menu = int(input("\nВведите номер пункта: "))
#         if choice_menu in menu_items:
#             print(f"Вы выбрали: {menu_items[choice_menu]}")
#             return choice_menu
#         else:
#             print("Ошибка! Нет такого пункта меню.")
#             return None
#     except ValueError:
#         print("Ошибка! Введите число от 0 до 3.")
#         return None
