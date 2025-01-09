import requests


class TelegramBot:
    def __init__(self, token: str, chat: str):
        self.chat = chat
        self.url = f"https://api.telegram.org/bot{token}"

    def send_message(self, message: str):
        data = {'chat_id': self.chat, 'text': message, 'parse_mode': 'Markdown'}
        requests.post(
            url=f"{self.url}/sendMessage",
            headers={'Content-Type': 'application/json'},
            params=data,
            timeout=120)