import sys

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.chapterList import ChapterListDownloader, ChapterListLoader
from modules.codec import MKCodec
from modules.settings import Settings
from ui.mangaDownloading import ThreadedMangaDownload
from ui.mangaLoading import ThreadedMangaLoad
from ui.search import ThreadedSearch
from ui.tree_gen import ThreadedTreeGenerate
from ui.web import ThreadedWebGenerate

from dialogs.main import Ui_MainWindow

from modules.html import HtmlManager

class Ui(QMainWindow, ThreadedSearch, ThreadedMangaLoad, ThreadedMangaDownload, ThreadedTreeGenerate, ThreadedWebGenerate):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('dialogs/main.ui', self)

        # Ui_MainWindow().setupUi(self)

        self.settings = Settings()

        self.stack = self.findChild(QStackedWidget, 'dynamicStack')

        self.navbar = {
            'exit': self.findChild(QAction, 'actionExit'),
            'generate_tree': self.findChild(QAction, 'actionGenerate'),
            'keep_originals': self.findChild(QAction, 'actionKeep_originals'),
            'composite_jpg': self.findChild(QAction, 'actionCompositeJpg'),
            'composite_pdf': self.findChild(QAction, 'actionCompositePdf'),
            'settings_apply': self.findChild(QAction, 'actionSettingsApply'),
            'help': self.findChild(QAction, 'actionHelp'),
        }

        self.navbar['exit'].triggered.connect(self.close)
        self.navbar['generate_tree'].triggered.connect(self.on_generate_clicked)

        self.navbar['composite_jpg'].setChecked(self.settings.settings['composite_jpg'])
        self.navbar['composite_pdf'].setChecked(self.settings.settings['composite_pdf'])
        self.navbar['keep_originals'].setChecked(self.settings.settings['keep_originals'])

        self.navbar['composite_jpg'].triggered.connect(self.update_settings)
        self.navbar['composite_pdf'].triggered.connect(self.update_settings)
        self.navbar['keep_originals'].triggered.connect(self.update_settings)

        self.navigation = {
            'search': self.findChild(QPushButton, 'searchNavButton'),
            'direct': self.findChild(QPushButton, 'directNavButton'),
            'browser': self.findChild(QPushButton, 'viewFunButton')
        }
        
        self.navigation['search'].clicked.connect(lambda : self.stack.setCurrentIndex(0))
        self.navigation['direct'].clicked.connect(lambda : self.stack.setCurrentIndex(1))
        self.navigation['browser'].clicked.connect(self.on_browser_clicked)

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

        self.direct['next_button'].clicked.connect(self.on_direct_download)

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
        self.download['download_button'].clicked.connect(self.on_download_clicked)

        self.progress = {
            'title_label': self.findChild(QLabel, 'progressTitleLabel'),

            'total_label': self.findChild(QLabel, 'totalDownloadProgressLabel'),
            'total_progress': self.findChild(QProgressBar, 'totalDownloadProgressBar'),

            'chapter_label': self.findChild(QLabel, 'chapterDownloadProgressLabel'),
            'chapter_progress': self.findChild(QProgressBar, 'chapterDownloadProgressBar'),

            'page_label': self.findChild(QLabel, 'pageDownloadProgressLabel'),
            'page_progress': self.findChild(QProgressBar, 'pageDownloadProgressBar'),

            'composite_label': self.findChild(QLabel, 'compositingLabel')
        }

        self.show()

    def on_direct_download(self):
        self.direct['input'].setEnabled(False)
        self.load_manga(self.direct['input'].text())

    def update_settings(self):
        self.settings.save_settings(
            self.navbar['composite_jpg'].isChecked(),
            self.navbar['composite_pdf'].isChecked(),
            self.navbar['keep_originals'].isChecked()
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()
