from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import PyQt5.Qt

from widgets.list import list_item
from widgets.list import simple_item
import requests

class PopularListItem(QWidget):
    def __init__(self):
        super().__init__()
        list_item.Ui_Form().setupUi(self)

        self.url = None

        self.thumbnailLabel = self.findChild(QLabel, 'thumbnailLabel')
        self.mangaNameLabel = self.findChild(QLabel, 'mangaNameLabel')
        self.lastChapterLabel = self.findChild(QLabel, 'lastChapterLabel')
        self.viewsLabel = self.findChild(QLabel, 'viewsLabel')
        self.descriptionLabel = self.findChild(QLabel, 'descriptionLabel')

    def setThumbnail(self, raw_data : bytes) -> None:
        if raw_data == None:
            return

        image = QImage()
        image.loadFromData(raw_data)

        pixmap = QPixmap.fromImage(image)
        
        size = self.thumbnailLabel.sizeHint()

        self.thumbnailLabel.setPixmap(pixmap.scaled(48, 81, Qt.KeepAspectRatio))

    def mangaTitle(self) -> str:
        return self.mangaNameLabel.text()

    def setMangaTitle(self, manga_title : str) -> None:
        self.mangaNameLabel.setText(manga_title)

    def lastChapter(self) -> str:
        return self.lastChapterLabel.text()

    def setLastChapter(self, last_chapter : str) -> None:
        self.lastChapterLabel.setText(last_chapter)

    def views(self) -> str:
        return self.viewsLabel.text()

    def setViews(self, views : str) -> None:
        self.viewsLabel.setText(views)

    def description(self) -> str:
        return self.lastChapterLabel.text()

    def setDescription(self, description : str) -> None:
        word_list = description.split(' ')
        self.descriptionLabel.setText(word_list[0] + ' ' + word_list[1] + ' ...')
        self.descriptionLabel.setToolTip(description)

class SimpleListItem(QWidget):
    def __init__(self):
        super().__init__()
        simple_item.Ui_Form().setupUi(self)

        self.url = None
        self.title = self.findChild(QLabel, 'mangaLabel')
        self.chapter = self.findChild(QLabel, 'chapterLabel')

    def setTitle(self, title: str) -> None:
        self.title.setText(title)

    def title(self) -> str:
        return self.title.title()

    def setChapter(self, chapter: str) -> None:
        self.chapter.setText(chapter)

    def chapter(self) -> str:
        return self.chapter.chapter()