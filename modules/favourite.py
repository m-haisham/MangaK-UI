import os
import json
import requests

from PyQt5.QtCore import *
from bs4 import BeautifulSoup
from requests.exceptions import InvalidURL, InvalidSchema, MissingSchema

from modules.settings import Settings


class Favourite(QObject):
    on_maximum = pyqtSignal(int)
    on_progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self):
        super(Favourite, self).__init__()

        self.loaded = []

    def load(self):

        data = Favourite.load_favourites()

        # if no data exit
        if data is None:
            self.finished.emit()
            return

        self.on_maximum.emit(len(data))
        self.loaded.clear()

        count = 0
        for _slice in data:

            url = _slice['manga']['url']
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')

            last_chapter_recorded = _slice['lastChapter']['name']
            updated_names, updated_urls = Favourite.get_updated_chapters(url, soup=soup,
                                                                         last_recorded_url=_slice['lastChapter']['url'])

            self.loaded.append({
                'title': self.get_name(_slice['manga']['url'], soup),
                'url': url,
                'chapter': last_chapter_recorded,
                'status': 'No updates' if len(updated_names) <= 0 else f'{len(updated_names)}'
            })
            count += 1
            self.on_progress.emit(count)

        self.finished.emit()

    @staticmethod
    def get_updated_chapters(url: str, *, soup: BeautifulSoup = None, last_recorded_url: str = None) -> tuple:
        """ Get tuple (names, links) of updated chapters """
        if last_recorded_url is not None and type(last_recorded_url) != str:
            raise TypeError("'last_recorded' must be of type str")
        if type(url) != str:
            raise TypeError("'url' must be of type str")

        # if last chapter is None get the last chapter
        if last_recorded_url is None:
            data = Favourite.load_favourites()

            # if no data exit
            if data is None:
                return tuple()

            for piece in data:
                if piece['manga']['url'] == url:
                    last_recorded_url = piece['lastChapter']['url']
                    break

        if soup is not None:
            if type(soup) != BeautifulSoup:
                raise TypeError("'soup' must be of type Beautiful soup")
        else:
            r = None
            try:
                r = requests.get(url)
            except InvalidURL or InvalidSchema or MissingSchema:
                return tuple()
            soup = BeautifulSoup(r.content, 'html.parser')

        rows = soup.find_all(class_="chapter-list")[0].find_all(class_="row")

        names = []
        updated = []
        for row in rows:
            href = row.find('a', href=True)['href']
            if href == last_recorded_url:
                break
            else:
                names.append(row.find('a', href=True).text)
                updated.append(href)

        return names, updated

    @staticmethod
    def load_favourites() -> list:
        """ Load favourites from json to list """
        # if favourites doesnt exist
        if not os.path.exists(Settings.favourite_data_file):
            return list()

        # load data
        data = None
        with open(Settings.favourite_data_file, 'r') as f:
            data = json.load(f)

        return data

    @staticmethod
    def is_favourite(url: str) -> bool:
        if type(url) != str:
            raise TypeError("'url' must be of type str")

        data = Favourite.load_favourites()

        # if no data exit
        if data is None:
            return False

        for piece in data:
            if piece['manga']['url'] == url:
                return True

        return False

    def get_name(self, url, soup: BeautifulSoup = None):
        """ Get name from url """

        if soup is not None:
            if type(soup) != BeautifulSoup:
                raise TypeError("'soup' must be of type Beautiful soup")
        else:
            r = None
            try:
                r = requests.get(url)
            except InvalidURL or InvalidSchema or MissingSchema:
                return list()
            soup = BeautifulSoup(r.content, 'html.parser')

        return soup.find(class_="manga-info-text").find("h1").text
