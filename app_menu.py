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
        print(f"Ошибка: {e}")
