import requests
from django.conf import settings


def send_to_telegram(message):
    """Таска отправки сообщения в телеграмм"""

    if settings.BOT_TOKEN and settings.CHAT_IDS:
        url = f'https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage'
        for chat_id in settings.CHAT_IDS:
            try:
                requests.post(url, {'chat_id': chat_id, 'text': message})
            except Exception as e:
                print('Send telegram exception\n', str(e))
