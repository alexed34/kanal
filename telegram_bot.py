import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_telegram(text: str):
    """
    Отправляем сообщения в телеграм
    :param text: текст для отправки
    :return:
    """
    # token = "5306353744:AAFA31eStWeN9-qAObU-_SxPIjV1k_Le_Y0"
    token = os.environ['TOKEN']
    url = "https://api.telegram.org/bot"
    channel_id = os.environ['CHANEL_ID']
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text,
        "parse_mode": 'html'
    })

    if r.status_code != 200:
        raise Exception("post_text error")


