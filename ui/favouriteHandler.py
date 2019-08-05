from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.favourite import Favourite

class FavouriteHandler(object):
    def __init__(self):
        super(FavouriteHandler, self).__init__()

        self.favourite_handle = Favourite()
        self.favourite_thread = QThread()

        self.favourite_handle.moveToThread(self.favourite_thread)

        self.favourite_handle.finished.connect(self.on_favourite_loaded)
        self.favourite_thread.started.connect(self.favourite_handle.load)

    def on_favourite_refresh(self):
        self.set_favourite_controls(False)
        self.favourite['progress'].show()
        self.favourite_thread.start()

    def on_favourite_loaded(self):
        self.favourite_thread.quit()
        self.favourite['progress'].hide()

        self.favourite['table'].clear()
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