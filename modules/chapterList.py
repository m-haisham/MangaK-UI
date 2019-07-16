import requests
from requests.exceptions import MissingSchema, InvalidSchema, InvalidURL

from bs4 import BeautifulSoup
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ChapterListLoader(QObject):

    finished = pyqtSignal()
    valid_url = pyqtSignal(bool)
    title = pyqtSignal(str)
    maximum = pyqtSignal(int)
    progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.manga_link =''
        self.loaded_list = []

    def load(self):
        r = None
        try:
            r = requests.get(self.manga_link)
        except InvalidURL and InvalidSchema and MissingSchema:
            self.valid_url.emit(False)
            return
        else:
            self.valid_url.emit(True)

        soup = BeautifulSoup(r.content, "html.parser")
        chapterbox = soup.find_all(class_="chapter-list")
        rows = chapterbox[0].find_all(class_="row")
        title = soup.find(class_="manga-info-text").find("h1").text
        self.title.emit(title)
        self.maximum.emit(len(rows))

        count = 0
        self.loaded_list = []
        for i in range(len(rows) - 1, -1, -1):
            self.loaded_list.append({
                'name': rows[i].find('a', href=True).text,
                'href': rows[i].find('a', href=True)['href']
            })
            count += 1
            self.progress.emit(count)

        self.finished.emit()