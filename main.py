import os
import requests
import time
from telegram import Bot

# Точка входа
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_TO_CHECK = os.getenv("URL_TO_CHECK")
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))

site_down = False
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_message(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        print(f"Ошибка при отправке: {e}")

def check_site():
    global site_down
    while True:
        try:
            response = requests.get(URL_TO_CHECK, timeout=10)
            status = response.status_code

            if status == 500:
                if not site_down:
                    site_down = True
                    message = '❗️Paperform упал — ошибка 500'
                    send_message(message)
            else:
                if site_down:
                    site_down = False
                    message = '✅Paperform работает'
                    send_message(message)

        except requests.RequestException:
            if not site_down:
                site_down = True
                message = '❗️Paperform недоступен'
                send_message(message)

        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == '__main__':
    check_site()
