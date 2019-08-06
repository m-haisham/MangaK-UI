from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.favourite import Favourite
from modules.jar import j_call
from modules.settings import Settings


class FavouriteHandler(object):
    def __init__(self):
        super(FavouriteHandler, self).__init__()

        self.favourite_handle = Favourite()
        self.favourite_thread = QThread()

        self.favourite_handle.on_progress.connect(self.on_favourite_progress)
        self.favourite_handle.on_maximum.connect(self.on_favourite_maximum)

        self.favourite_handle.moveToThread(self.favourite_thread)

        self.favourite_handle.finished.connect(self.on_favourite_loaded)
        self.favourite_thread.started.connect(self.favourite_handle.load)

    def on_favourite_progress(self, i):
        self.favourite['progress'].setValue(i)

    def on_favourite_maximum(self, i):
        self.favourite['progress'].setMaximum(i)
        self.favourite['progress'].setValue(0)
        self.favourite['progress'].show()

    def on_favourite_refresh(self):
        self.set_favourite_controls(False)
        self.favourite_thread.start()

    def on_favourite_delete(self):
        indexes = self.favourite['table'].selectedIndexes()
        rows = set()
        links = set()
        for index in indexes:
            rows.add(index.row())
            links.add(self.favourite_handle.loaded[index.row()]['url'])

        j_call(file=Settings.kfave_path, args=[Settings.favourite_data_file, 'remove']+list(links))

        rows = list(rows)
        while len(rows) > 0:
            self.favourite['table'].removeRow(rows.pop(-1))

    def on_favourite_go(self):
        indexes = self.favourite['table'].selectedIndexes()
        if len(indexes) != 1:
            return

        self.search['next_button'].setEnabled(False)
        self.load_manga(self.favourite_handle.loaded[indexes[0].row()]['url'])

    def on_favourite_double_click(self, i):
        if not self.favourite['go'].isEnabled():
            return

        self.search['next_button'].setEnabled(False)
        self.load_manga(self.favourite_handle.loaded[i.row()]['url'])

    def on_favourite_loaded(self):
        self.favourite_thread.quit()
        self.favourite['progress'].hide()

        self.favourite['table'].setRowCount(len(self.favourite_handle.loaded))
        for i in range(len(self.favourite_handle.loaded)):
            data_piece = self.favourite_handle.loaded[i]

            name = QTableWidgetItem(data_piece['title'])
            name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            status = QTableWidgetItem(data_piece['status'])
            status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            last = QTableWidgetItem(data_piece['chapter'])
            last.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            self.favourite['table'].setItem(i, 0, name)
            self.favourite['table'].setItem(i, 1, status)
            self.favourite['table'].setItem(i, 2, last)

        self.set_favourite_controls(True)

    def set_favourite_controls(self, value: bool):
        self.favourite['remove'].setEnabled(value)
        self.favourite['go'].setEnabled(value)
        self.favourite['refresh'].setEnabled(value)