from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.chapterList import ChapterListLoader

class ThreadedMangaLoad(object):
    def __init__(self):
        super().__init__()

        self.loader = ChapterListLoader()
        self.loader_thread = QThread()
        self.init_loader_thread()
    
    def init_loader_thread(self):
        self.loader.title.connect(self.set_title)
        self.loader.maximum.connect(self.set_manga_maximum)
        self.loader.progress.connect(self.on_manga_progress)

        self.loader.valid_url.connect(self.on_valid_url)

        self.loader.moveToThread(self.loader_thread)

        self.loader.finished.connect(self.loader_thread.exit)
        self.loader.finished.connect(self.on_manga_loaded)

        self.loader_thread.started.connect(self.loader.load)

    def on_valid_url(self, valid):
        if valid:
            self.direct['error_label'].setText('')
            self.stack.setCurrentIndex(2)
        else:
            self.direct['error_label'].setText('Invalid url!')
            self.loader_thread.exit()

    def set_title(self, title):
        self.download['title'].setText(title)

    def on_manga_progress(self, i):
        self.download['progress_bar'].setValue(i)

    def set_manga_maximum(self, i):
        self.download['progress_bar'].setMaximum(i)
        self.download['progress_bar'].show()

    def load_manga(self, manga_link):
        self.set_controls(False)
        
        self.loader.manga_link = manga_link
        self.loader_thread.start()

    def on_manga_loaded(self):
        self.direct['next_button'].setEnabled(True)
        self.search['next_button'].setEnabled(True)

        self.download['list'].clear()
        for i in range(len(self.loader.loaded_list)):
            item = QListWidgetItem()
            item.setText(self.loader.loaded_list[i]['name'])
            item.setToolTip(self.loader.loaded_list[i]['href'])
            item.setCheckState(Qt.Checked)

            self.download['list'].addItem(item)

        self.set_controls(True)
        self.download['progress_bar'].hide()

    def set_controls(self, is_active):
        self.download['select_all'].setEnabled(is_active)
        self.download['inverse'].setEnabled(is_active)
        self.download['download_button'].setEnabled(is_active)

    def select_all(self):
        items = self.download['list'].count()

        for i in range(items):
            item = self.download['list'].item(i)
            item.setCheckState(Qt.Checked)

    def inverse_all(self):
        items = self.download['list'].count()

        for i in range(items):
            item = self.download['list'].item(i)
            if item.checkState() == Qt.Checked:
                item.setCheckState(Qt.Unchecked)
            elif item.checkState() == Qt.Unchecked:
                item.setCheckState(Qt.Checked)

    def on_download_clicked(self):
        self.download['download_button'].setEnabled(False)
        item_count = self.download['list'].count()

        checked_chapters = []
        for i in range(item_count):
            item = self.download['list'].item(i)
            if item.checkState() == Qt.Checked:
                checked_chapters.append(self.loader.loaded_list[i])
        
        if len(checked_chapters) <= 0:
            self.download['download_button'].setEnabled(True)
            return

        self.start_download_task(checked_chapters)
