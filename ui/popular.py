import traceback

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.codec import PopularPageCodec
from widgets.list.list_extension import PopularListItem


class PopularPage(object):
    def __init__(self):
        super().__init__()
        
        self.popular_codec = PopularPageCodec()
        self.popular_thread = QThread()

        self.popular_codec.maximum.connect(self.on_popular_maximum)
        self.popular_codec.progress.connect(self.on_popular_progress)
        self.popular_codec.page_updated.connect(lambda i: self.popular['page_spinbox'].setValue(i))

        self.popular_codec.moveToThread(self.popular_thread)

        self.popular_codec.finished.connect(self.on_refresh_done)

        self.popular_thread.started.connect(self.popular_codec.load_popular)

    def popular_button_enabled(self, is_enabled):
        self.popular['refresh_button'].setEnabled(is_enabled)
        self.popular['previous_button'].setEnabled(is_enabled)
        self.popular['next_button'].setEnabled(is_enabled)
        self.popular['proceed_button'].setEnabled(is_enabled)
        self.popular['page_spinbox'].setEnabled(is_enabled)
        self.popular['page_button'].setEnabled(is_enabled)
    
    def show_popular_progress(self, show):
        if show:
            self.popular['progress'].show()
            self.popular['pageno_label'].hide()
        else:
            self.popular['progress'].hide()
            self.popular['progress'].setMaximum(-1)
            self.popular['progress'].setValue(-1)
            self.popular['pageno_label'].show()

    def on_refresh(self):
        self.popular_button_enabled(False)
        self.popular['table'].clear()

        self.popular_codec.thumbnails = self.settings.settings['download_thumbnails']
        self.popular_thread.start()

    def on_refresh_done(self):
        self._set_page()
        
        self.popular_button_enabled(True)
        self.show_popular_progress(False)
        self.popular_thread.exit()

    def on_next_page(self):
        last_page = self.popular_codec.page
        self.popular_codec.increment_page()

        if not self.popular_codec.page == last_page:
            self.on_refresh()
    
    def on_previous_page(self):
        last_page = self.popular_codec.page
        self.popular_codec.decrement_page()

        if not self.popular_codec.page == last_page:
            self.on_refresh()

    def on_proceed_popular(self):
        self.popular['proceed_button'].setEnabled(False)
        selected_items = self.popular['table'].selectedItems()
        if len(selected_items) <= 0:
            self.popular['proceed_button'].setEnabled(True)
            return

        widget = self.popular['table'].itemWidget(self.popular['table'].selectedItems()[0])
        self.load_manga(widget.url)
        
    def on_popular_maximum(self, i):
        self.popular['progress'].setMaximum(i)
        self.show_popular_progress(True)

    def on_popular_progress(self, i, data : dict):
        # Create widget item
        item_widget = PopularListItem()
        item_widget.setThumbnail(data['image_bytes'])
        item_widget.url = data['url']
        item_widget.setMangaTitle(data['manga_title'])
        item_widget.setLastChapter(data['last_chapter'])
        item_widget.setViews(data['views'])
        item_widget.setDescription(data['description'])

        # Add widget item
        item = QListWidgetItem(self.popular['table'])
        item.setSizeHint(item_widget.sizeHint())
        self.popular['table'].addItem(item)
        self.popular['table'].setItemWidget(item, item_widget)
        
        # update progress
        self.popular['progress'].setValue(i)

    def _set_page(self):
        self.popular['pageno_label'].setText('of {0} pages'.format(self.popular_codec.max_page))

    def on_custom_page_select(self):
        try:
            last_page = self.popular_codec.page
            page = self.popular['page_spinbox'].value()
            if self.popular_codec.max_page == '':
                self.popular_codec.get_max_page()
                self._set_page()
            if page <= int(self.popular_codec.max_page):
                self.popular_codec.page = page
                self.on_refresh()
        except:
            traceback.print_exc()

    def on_popular_double_click(self, item):
        self.popular['proceed_button'].setEnabled(False)
        widget = self.popular['table'].itemWidget(item)
        self.load_manga(widget.url)
