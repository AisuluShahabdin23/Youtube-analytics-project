import os
import json

import requests
from googleapiclient.discovery import build

API_KEY = os.getenv('YOUTUBE_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        self.__channel_id = channel_id
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        info_channel = json.dumps(channel, indent=2, ensure_ascii=False)
        info_channel_json = json.loads(info_channel)
        self.title = info_channel_json['items'][0]['snippet']['title']
        self.description = info_channel_json['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subs_count = info_channel_json['items'][0]['statistics']['subscriberCount']
        self.video_count = info_channel_json['items'][0]['statistics']['videoCount']
        self.view_count = info_channel_json['items'][0]['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с API вне класса"""
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        return youtube

    @property
    def channel_id(self):
        """Свойство для обращения к приватному атрибуту __channel_id"""
        return self.__channel_id

    def printj(self: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(self, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        Channel.printj(channel)

    def to_json(self, file_name: str) -> None:
        """Запись информации о канале в file_name.json"""
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        with open(file_name, 'w') as json_file:
            json.dump(channel, json_file, ensure_ascii=False)

    def __str__(self) -> str:
        return f'{self.title} ({self.url})'

    def __add__(self, other) -> int:
        """Сложение классов по количеству подписчиков"""
        return int(self.subs_count) + int(other.subs_count)

    def __sub__(self, other) -> int:
        """Разность классов по количеству подписчиков"""
        return int(self.subs_count) - int(other.subs_count)

    def __gt__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        return int(self.subs_count) > int(other.subs_count)

    def __ge__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        return int(self.subs_count) >= int(other.subs_count)

    def __lt__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        return int(self.subs_count) < int(other.subs_count)

    def __le__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        return int(self.subs_count) <= int(other.subs_count)
