import sys

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.codec import MKCodec
from modules.chapterList import ChapterListLoader
from ui.search import ThreadedSearch
from ui.mangaLoading import ThreadedMangaLoad

class Ui(QMainWindow, ThreadedSearch, ThreadedMangaLoad):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('dialogs/main.ui', self)

        self.stack = self.findChild(QStackedWidget, 'dynamicStack')

        self.navigation = {
            'search': self.findChild(QPushButton, 'searchNavButton'),
            'direct': self.findChild(QPushButton, 'directNavButton'),
            'browser': self.findChild(QPushButton, 'viewFunButton')
        }
        
        self.navigation['search'].clicked.connect(lambda : self.stack.setCurrentIndex(0))
        self.navigation['direct'].clicked.connect(lambda : self.stack.setCurrentIndex(1))

        self.search = {
            'input': self.findChild(QLineEdit, 'searchInputBox'),
            'search_button': self.findChild(QPushButton, 'mangaSearchButton'),
            'table': self.findChild(QTableWidget, 'searchResultTable'),
            'progress_bar': self.findChild(QProgressBar, 'searchProgressBar'),
            'next_button': self.findChild(QPushButton, 'searchNextButton')
        }

        self.search['progress_bar'].hide()
        self.search['search_button'].clicked.connect(self._search)
        self.search['next_button'].clicked.connect(self._search_to_manga_download)

        self.direct = {
            'input': self.findChild(QLineEdit, 'directDownloadInput'),
            'next_button': self.findChild(QPushButton, 'directNextButton'),
            'error_label': self.findChild(QLabel, 'directDownloadErrorLabel')
        }

        self.direct['next_button'].clicked.connect(lambda : self.load_manga(self.direct['input'].text()))

        self.download = {
            'title': self.findChild(QLabel, 'mangaTitle'),
            'select_all': self.findChild(QPushButton, 'selectAllMangaButton'),
            'inverse': self.findChild(QPushButton, 'inverseSelectedMangaButton'),
            'list': self.findChild(QListWidget, 'chapterListWidget'),
            'progress_bar': self.findChild(QProgressBar, 'mangaDataLoadProgressBar'),
            'download_button': self.findChild(QPushButton, 'selectedMangaDownloadButton')
        }

        self.download['progress_bar'].hide()
        self.download['select_all'].clicked.connect(self.select_all)
        self.download['inverse'].clicked.connect(self.inverse_all)

        self.progress = {
            'total_label': self.findChild(QLabel, 'totalDownloadProgressLabel'),
            'total_progress': self.findChild(QProgressBar, 'totalDownloadProgressBar'),

            'chapter_label': self.findChild(QLabel, 'chapterDownloadProgressLabel'),
            'chapter_progress': self.findChild(QProgressBar, 'chapterDownloadProgressBar'),

            'page_label': self.findChild(QLabel, 'pageDownloadProgressLabel'),
            'page_progress': self.findChild(QProgressBar, 'pageDownloadProgressBar'),
        }

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()
