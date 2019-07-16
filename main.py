from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from modules.codec import MKCodec

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('dialogs/main.ui', self)
        
        self.codec = MKCodec()
        self.search_thread = QThread()
        self._init_search_thread()

        self.search = {
            'input': self.findChild(QLineEdit, 'searchInputBox'),
            'search_button': self.findChild(QPushButton, 'mangaSearchButton'),
            'table': self.findChild(QTableWidget, 'searchResultTable'),
            'progress_bar': self.findChild(QProgressBar, 'searchProgressBar'),
            'next_button': self.findChild(QPushButton, 'searchNextButton')
        }

        self.search['progress_bar'].hide()
        self.search['search_button'].clicked.connect(self._search)

        self.direct = {
            'input': self.findChild(QLineEdit, 'directDownloadInput'),
            'next_button': self.findChild(QPushButton, 'directNextButton'),
            'error_label': self.findChild(QLabel, 'directDownloadErrorLabel')
        }

        self.download = {
            'select_all': self.findChild(QPushButton, 'selectAllMangaButton'),
            'inverse': self.findChild(QPushButton, 'inverseSelectedMangaButton'),
            'list': self.findChild(QListWidget, 'chapterListWidget'),
            'download_button': self.findChild(QPushButton, 'selectedMangaDownloadButton')
        }

        self.progress = {
            'total_label': self.findChild(QLabel, 'totalDownloadProgressLabel'),
            'total_progress': self.findChild(QProgressBar, 'totalDownloadProgressBar'),

            'chapter_label': self.findChild(QLabel, 'chapterDownloadProgressLabel'),
            'chapter_progress': self.findChild(QProgressBar, 'chapterDownloadProgressBar'),

            'page_label': self.findChild(QLabel, 'pageDownloadProgressLabel'),
            'page_progress': self.findChild(QProgressBar, 'pageDownloadProgressBar'),
        }

        for i in range(100):
            new = QListWidgetItem()
            new.setText('item {}'.format(i))
            new.setCheckState(Qt.Checked)
            self.download['list'].addItem(new)

        self.show()
    
    def _init_search_thread(self):
        self.codec.progress.connect(self._on_search_progress)
        self.codec.maximum.connect(self._set_search_maximum)

        self.codec.moveToThread(self.search_thread)

        self.codec.finished.connect(self.search_thread.quit)
        self.codec.finished.connect(self._on_search_finished)

        self.search_thread.started.connect(self.codec.search)

    def _search(self):

        # disable controls
        self.search['input'].setEnabled(False)
        self.search['search_button'].setEnabled(False)

        self.codec.keyword = self.codec.search_prefix + self.search['input'].text()

        self.search_thread.start()

    def _on_search_progress(self, i):
        self.search['progress_bar'].setValue(i)

    def _set_search_maximum(self, i):
        self.search['progress_bar'].setMaximum(i)
        self.search['progress_bar'].show()

    def _on_search_finished(self):

        # fill table
        self.search['table'].setRowCount(len(self.codec.search_result))
        for i in range(len(self.codec.search_result)):
            manga = self.codec.search_result[i]

            self.search['table'].setItem(i, 0, QTableWidgetItem(manga['name']))
            self.search['table'].setItem(i, 1, QTableWidgetItem(manga['last_chapter']))

        # enable controls
        self.search['input'].setEnabled(True)
        self.search['search_button'].setEnabled(True)
        self.search['progress_bar'].hide()
        print('search done')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()