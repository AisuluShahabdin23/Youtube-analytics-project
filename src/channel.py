import os
import json

import requests
from googleapiclient.discovery import build

API_KEY = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=API_KEY)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        url = "https://www.youtube.com/channel/"
        response = requests.get(url, headers={'id': self.channel_id})
        data = json.loads(response.text)
        print(data)
