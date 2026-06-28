import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(
        url,
        data=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"Telegram Error : {response.text}"
        )

    return response.json()
