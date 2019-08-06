from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.codec import Top10Codec
from modules.internet import have_internet
from widgets.list.list_extension import SimpleListItem

class Top10List(object):
    def __init__(self):
        super().__init__()

        self.top_codec = Top10Codec()
        self.top_thread = QThread()

        self.top_codec.moveToThread(self.top_thread)

        self.top_codec.finished.connect(self.on_top10_load_finished)
        self.top_thread.started.connect(self.top_codec.load_top10)

    def set_buttons_enabled(self, enabled: bool):
        self.top['refresh'].setEnabled(enabled)
        self.top['next_button'].setEnabled(enabled)

    def on_top10_refresh(self):
        if not have_internet():
            return

        self.set_buttons_enabled(False)
        self.top['list'].clear()
        self.top_thread.start()

    def on_top10_load_finished(self):
        for block in self.top_codec.top10:
            item_widget = SimpleListItem()
            item_widget.url = block['href']
            item_widget.setTitle(block['manga'])
            item_widget.setChapter(block['last_chapter'])

            item = QListWidgetItem(self.top['list'])
            item.setSizeHint(item_widget.sizeHint())
            self.top['list'].addItem(item)
            self.top['list'].setItemWidget(item, item_widget)

        self.set_buttons_enabled(True)
        self.top_thread.exit()
    
    def on_top10_next(self):
        self.top['next_button'].setEnabled(False)
        selected_items = self.top['list'].selectedItems()
        if len(selected_items) <= 0:
            self.top['next_button'].setEnabled(True)
            return

        widget = self.top['list'].itemWidget(selected_items[0])
        self.load_manga(widget.url)

    def on_top10_double_clicked(self, item):
        if not self.top['next_button'].isEnabled():
            return

        self.top['next_button'].setEnabled(False)
        widget = self.top['list'].itemWidget(item)
        self.load_manga(widget.url)