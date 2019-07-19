from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.codec import MKCodec


class ThreadedSearch(object):
    def __init__(self):
        super().__init__()

        self.codec = MKCodec()
        self.search_thread = QThread()
        self._init_search_thread()
        
    def _init_search_thread(self):
        self.codec.progress.connect(self._on_search_progress)
        self.codec.maximum.connect(self._set_search_maximum)

        self.codec.moveToThread(self.search_thread)

        self.codec.finished.connect(self._on_search_finished)

        self.search_thread.started.connect(self.codec.search)

    def _search(self):

        # disable controls
        self._set_controls(False)

        self.codec.keyword = self.codec.search_prefix + self.search['input'].text()

        self.search_thread.start()

    def on_search_double_clicked(self, i):
        if not self.search['next_button'].isEnabled():
            return
        
        self.search['next_button'].setEnabled(False)
        self.load_manga(self.codec.search_result[i.row()]['href'])

    def _on_search_progress(self, i):
        self.search['progress_bar'].setValue(i)

    def _set_search_maximum(self, i):
        self.search['progress_bar'].setMaximum(i)
        self.search['progress_bar'].show()

    def _on_search_finished(self):

        self.search_thread.quit()

        # fill table
        self.search['table'].setRowCount(len(self.codec.search_result))
        for i in range(len(self.codec.search_result)):
            manga = self.codec.search_result[i]

            name = QTableWidgetItem(manga['name'])
            name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            
            last_chapter = QTableWidgetItem(manga['last_chapter'])
            last_chapter.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            self.search['table'].setItem(i, 0, name)
            self.search['table'].setItem(i, 1, last_chapter)

        # enable controls
        self._set_controls(True)
        self.search['progress_bar'].hide()

    def _search_to_manga_download(self):
        self.search['next_button'].setEnabled(False)
        selected_index = self.search['table'].selectedIndexes()[0].row()
        self.load_manga(self.codec.search_result[selected_index]['href'])

    def _set_controls(self, is_active):
        self.search['input'].setEnabled(is_active)
        self.search['search_button'].setEnabled(is_active)
        self.search['next_button'].setEnabled(is_active)
    