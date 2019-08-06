import os
import logging
import os
import platform
import sys
import traceback

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dialogs.main_window import Ui_MainWindow
from modules.internet import have_internet
from modules.settings import Settings
from modules.internet import have_internet
from ui.favouriteHandler import FavouriteHandler
from ui.mangaDownloading import ThreadedMangaDownload
from ui.mangaLoading import ThreadedMangaLoad
from ui.popular import PopularPage
from ui.search import ThreadedSearch
from ui.top10 import Top10List
from ui.tree_gen import ThreadedTreeGenerate
from ui.web import ThreadedWebGenerate


class Ui(QMainWindow, ThreadedSearch, ThreadedMangaLoad, ThreadedMangaDownload, ThreadedTreeGenerate,
         ThreadedWebGenerate, PopularPage, Top10List, FavouriteHandler):
    def __init__(self, _app: QApplication):
        super(Ui, self).__init__()
        # uic.loadUi('dialogs/main.ui', self)

        Ui_MainWindow().setupUi(self)
        self.show()
        self.setEnabled(False)

        self.app = _app

        self.settings = Settings()
        self.dark_palette = QPalette()
        self.init_dark_palette()

        self.stack = self.findChild(QStackedWidget, 'dynamicStack')

        self.navbar = {
            'chapter': self.findChild(QAction, 'actionChapterView'),
            'favourite': self.findChild(QAction, 'actionFavourites'),
            'download': self.findChild(QAction, 'actionDownloadsView'),
            'exit': self.findChild(QAction, 'actionExit'),
            'generate_tree': self.findChild(QAction, 'actionGenerate'),
            'generate_bdata': self.findChild(QAction, 'actionBData'),
            'generate_startup': self.findChild(QAction, 'actionFavouriteStartup'),
            'keep_originals': self.findChild(QAction, 'actionKeep_originals'),
            'composite_jpg': self.findChild(QAction, 'actionCompositeJpg'),
            'startup_fave': self.findChild(QAction, 'actionLoadFavourites'),
            'startup_popular': self.findChild(QAction, 'actionLoadPopular'),
            'startup_top10': self.findChild(QAction, 'actionLoadTop10'),
            'composite_pdf': self.findChild(QAction, 'actionCompositePdf'),
            'download_thumbnails': self.findChild(QAction, 'actionThumbnails'),
            'dark_mode': self.findChild(QAction, 'actionDarkMode'),
            'documentation': self.findChild(QAction, 'actionDocumentation'),
            'about': self.findChild(QAction, 'actionAbout'),
        }
        self.navbar['chapter'].triggered.connect(lambda: self.stack.setCurrentIndex(2))
        self.navbar['favourite'].triggered.connect(lambda: self.stack.setCurrentIndex(6))
        self.navbar['download'].triggered.connect(lambda: self.stack.setCurrentIndex(3))
        self.navbar['exit'].triggered.connect(self.close)
        self.navbar['generate_tree'].triggered.connect(self.on_generate_clicked)
        self.navbar['generate_startup'].triggered.connect(lambda: self.set_fave_startup(override=True))
        self.navbar['generate_bdata'].triggered.connect(self.on_bdata_clicked)
        self.navbar['about'].triggered.connect(lambda: QMessageBox.information(self, 'About',
                                                                               'Author: mHaisham\nDescription: '
                                                                               'Supports download from '
                                                                               'mangakakalot.com, composition options '
                                                                               'and viewing the downloaded manga'))

        self.navbar['startup_fave'].setChecked(self.settings.settings['startup_fave'])
        self.navbar['startup_popular'].setChecked(self.settings.settings['startup_popular'])
        self.navbar['startup_top10'].setChecked(self.settings.settings['startup_top10'])
        self.navbar['composite_jpg'].setChecked(self.settings.settings['composite_jpg'])
        self.navbar['composite_pdf'].setChecked(self.settings.settings['composite_pdf'])
        self.navbar['keep_originals'].setChecked(self.settings.settings['keep_originals'])
        self.navbar['download_thumbnails'].setChecked(self.settings.settings['download_thumbnails'])
        self.navbar['dark_mode'].setChecked(self.settings.settings['dark_mode'])

        self.navbar['startup_fave'].triggered.connect(self.update_settings)
        self.navbar['startup_popular'].triggered.connect(self.update_settings)
        self.navbar['startup_top10'].triggered.connect(self.update_settings)
        self.navbar['composite_jpg'].triggered.connect(self.update_settings)
        self.navbar['composite_pdf'].triggered.connect(self.update_settings)
        self.navbar['keep_originals'].triggered.connect(self.update_settings)
        self.navbar['download_thumbnails'].triggered.connect(self.update_settings)
        self.navbar['dark_mode'].triggered.connect(lambda: self.set_theme(True))

        self.navigation = {
            'hot': self.findChild(QPushButton, 'hotNavButton'),
            'top10': self.findChild(QPushButton, 'top10NavButton'),
            'search': self.findChild(QPushButton, 'searchNavButton'),
            'direct': self.findChild(QPushButton, 'directNavButton'),
            'browser': self.findChild(QPushButton, 'viewFunButton')
        }

        self.navigation['hot'].clicked.connect(lambda: self.stack.setCurrentIndex(4))
        self.navigation['top10'].clicked.connect(lambda: self.stack.setCurrentIndex(5))
        self.navigation['search'].clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.navigation['direct'].clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.navigation['browser'].clicked.connect(self.on_browser_clicked)

        self.popular = {
            'previous_button': self.findChild(QPushButton, 'previousPopularButton'),
            'next_button': self.findChild(QPushButton, 'nextPopularButton'),
            'refresh_button': self.findChild(QPushButton, 'refreshPopularButton'),
            'pageno_label': self.findChild(QLabel, 'pagePopularLabel'),
            'page_spinbox': self.findChild(QSpinBox, 'selectPopularPageSpinBox'),
            'page_button': self.findChild(QPushButton, 'selectPopularPageButton'),
            'table': self.findChild(QListWidget, 'popularTableWidget'),
            'proceed_button': self.findChild(QPushButton, 'proceedPopularButton'),
            'progress': self.findChild(QProgressBar, 'popularProgressBar')
        }

        self.popular['progress'].hide()

        self.popular['table'].itemDoubleClicked.connect(self.on_popular_double_click)

        self.popular['refresh_button'].clicked.connect(self.on_refresh)
        self.popular['previous_button'].clicked.connect(self.on_previous_page)
        self.popular['page_button'].clicked.connect(self.on_custom_page_select)
        self.popular['next_button'].clicked.connect(self.on_next_page)
        self.popular['proceed_button'].clicked.connect(self.on_proceed_popular)

        self.top = {
            'list': self.findChild(QListWidget, 'top10ListWidget'),
            'refresh': self.findChild(QPushButton, 'refreshTopButton'),
            'next_button': self.findChild(QPushButton, 'nextTopButton')
        }
        self.top['list'].itemDoubleClicked.connect(self.on_top10_double_clicked)
        self.top['refresh'].clicked.connect(self.on_top10_refresh)
        self.top['next_button'].clicked.connect(self.on_top10_next)

        self.search = {
            'input': self.findChild(QLineEdit, 'searchInputBox'),
            'search_button': self.findChild(QPushButton, 'mangaSearchButton'),
            'table': self.findChild(QTableWidget, 'searchResultTable'),
            'progress_bar': self.findChild(QProgressBar, 'searchProgressBar'),
            'next_button': self.findChild(QPushButton, 'searchNextButton')
        }

        self.search['table'].doubleClicked.connect(self.on_search_double_clicked)
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
            'show_updates': self.findChild(QToolButton, 'ShowUpdatesToolButton'),
            'browser': self.findChild(QToolButton, 'ChapterBrowserToolButton'),
            'select_all': self.findChild(QPushButton, 'selectAllMangaButton'),
            'inverse': self.findChild(QPushButton, 'inverseSelectedMangaButton'),
            'select_updates': self.findChild(QPushButton, 'SelectUpdatedChaptersPushButton'),
            'list': self.findChild(QListWidget, 'chapterListWidget'),
            'progress_bar': self.findChild(QProgressBar, 'mangaDataLoadProgressBar'),
            'fave': self.findChild(QPushButton, 'FavouriteThisMangaPushButton'),
            'download_button': self.findChild(QPushButton, 'selectedMangaDownloadButton')
        }

        self.download['list'].doubleClicked.connect(self.on_download_double_clicked)
        self.download['show_updates'].clicked.connect(self.on_show_updates_clicked)
        self.download['browser'].clicked.connect(self.on_chapter_view_browser_clicked)
        self.download['progress_bar'].hide()
        self.download['select_all'].clicked.connect(self.select_all)
        self.download['inverse'].clicked.connect(self.inverse_all)
        self.download['select_updates'].clicked.connect(self.on_select_updates_clicked)
        self.download['fave'].clicked.connect(self.on_fave_this_clicked)
        self.download['download_button'].clicked.connect(self.on_download_clicked)

        self.progress = {
            'title_label': self.findChild(QLabel, 'progressTitleLabel'),

            'total_label': self.findChild(QLabel, 'totalDownloadProgressLabel'),
            'total_progress': self.findChild(QProgressBar, 'totalDownloadProgressBar'),

            'chapter_label': self.findChild(QLabel, 'chapterDownloadProgressLabel'),
            'chapter_progress': self.findChild(QProgressBar, 'chapterDownloadProgressBar'),

            'page_label': self.findChild(QLabel, 'pageDownloadProgressLabel'),
            'page_progress': self.findChild(QProgressBar, 'pageDownloadProgressBar'),

            'composite_label': self.findChild(QLabel, 'compositingLabel'),
            'open_button': self.findChild(QPushButton, 'progressOpenDirectoryButton')
        }

        self.progress['open_button'].hide()
        self.progress['open_button'].clicked.connect(self.on_progress_open_clicked)

        self.favourite = {
            'table': self.findChild(QTableWidget, 'FavouriteResultTable'),
            'progress': self.findChild(QProgressBar, 'FavouriteProgressBar'),
            'remove': self.findChild(QPushButton, 'FavouriteRemoveButton'),
            'go': self.findChild(QPushButton, 'FavouriteGoButton'),
            'refresh': self.findChild(QPushButton, 'FavouriteRefreshButton')
        }
        self.favourite['table'].doubleClicked.connect(self.on_favourite_double_click)
        self.favourite['progress'].hide()

        self.favourite['refresh'].clicked.connect(self.on_favourite_refresh)
        self.favourite['remove'].clicked.connect(self.on_favourite_delete)
        self.favourite['go'].clicked.connect(self.on_favourite_go)

        if self.settings.settings['startup_fave']:
            self.on_favourite_refresh()
        if self.settings.settings['startup_popular']:
            self.on_refresh()
        if self.settings.settings['startup_top10']:
            self.on_top10_refresh()

        self.set_theme(False)
        self.download_resume_init()

        self.set_fave_startup()

        self.setEnabled(True)

    def set_fave_startup(self, override=False):
        home = os.path.expanduser("~")
        working_directory = os.getcwd()
        if platform.system() == 'Windows':
            vbscript = 'mangak.vbs'

            extension = os.path.join('AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            commands = f"""Set oShell = WScript.CreateObject("WScript.shell")
            oShell.Run "cmd /c cd {working_directory} & javaw -jar {os.path.join(working_directory, Settings.kfave_path)}", 0, false"""

            if not override and os.path.exists(os.path.join(home, extension, vbscript)):
                return

            print(os.path.join(home, extension, vbscript))
            print(commands)

            with open(os.path.join(home, extension, vbscript), 'w') as f:
                f.write(commands)


    def on_direct_download(self):
        if not have_internet():
            return

        self.direct['input'].setEnabled(False)
        self.load_manga(self.direct['input'].text())

    def update_settings(self):
        self.settings.save_settings(
            self.navbar['startup_fave'].isChecked(),
            self.navbar['startup_popular'].isChecked(),
            self.navbar['startup_top10'].isChecked(),
            self.navbar['composite_jpg'].isChecked(),
            self.navbar['composite_pdf'].isChecked(),
            self.navbar['keep_originals'].isChecked(),
            self.navbar['download_thumbnails'].isChecked()
        )

    def init_dark_palette(self):
        self.dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        self.dark_palette.setColor(QPalette.WindowText, Qt.white)
        self.dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        self.dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        self.dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        self.dark_palette.setColor(QPalette.Text, Qt.white)
        self.dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        self.dark_palette.setColor(QPalette.ButtonText, Qt.white)
        self.dark_palette.setColor(QPalette.BrightText, Qt.red)
        self.dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        self.dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    def set_theme(self, save) -> None:
        is_dark = self.navbar['dark_mode'].isChecked()
        self.app.setPalette(self.dark_palette if is_dark else self.app.style().standardPalette())
        if save:
            self.settings.dark_mode_enabled(is_dark)


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        window = Ui(app)
        app.exec_()
    except Exception as e:
        traceback.print_exc()
        logging.exception(e)
