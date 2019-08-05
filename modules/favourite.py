import os
import json
import requests

from PyQt5.QtCore import *
from bs4 import BeautifulSoup
from requests.exceptions import InvalidURL, InvalidSchema, MissingSchema

from modules.settings import Settings

class Favourite(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super(Favourite, self).__init__()

        self.loaded = []

    def load(self):
        # if favourites doesnt exist
        if not os.path.exists(Settings.favourite_data_file):
            self.finished.emit()
            return

        # load data
        data = None
        with open(Settings.favourite_data_file, 'r') as f:
            data = json.load(f)

        # if no data exit
        if data is None:
            self.finished.emit()
            return

        self.loaded.clear()
        for _slice in data:
            last_chapter_recorded = _slice['lastChapter']['name']
            self.loaded.append({
                'title': self.get_name(_slice['manga']['url']),
                'url': _slice['manga']['url'],
                'chapter': last_chapter_recorded,
                'status': 'available'
            })

        self.finished.emit()

    def get_name(self, url):
        """ Get name from url """
        r = None
        try:
            r = requests.get(url)
        except InvalidURL or InvalidSchema or MissingSchema:
            return
        soup = BeautifulSoup(r.content, "html.parser")
        return soup.find(class_="manga-info-text").find("h1").text