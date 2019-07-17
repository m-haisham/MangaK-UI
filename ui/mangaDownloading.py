from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.chapterList import ChapterListDownloader

class ThreadedMangaDownload(object):
    def __init__(self):
        super().__init__()

        self.downloader = ChapterListDownloader()
        self.downloader_thread = QThread()
        self.init_downloader_thread()
    
    def start_download_task(self, chapter_list : list):

        self.progress['composite_label'].setText('')
        self.stack.setCurrentIndex(3)
        self.download['download_button'].setEnabled(True)

        self.downloader.manga_name = self.download['title'].text()
        self.progress['title_label'].setText(self.download['title'].text())

        self.downloader.chapter_list = chapter_list
        self.downloader.compile_jpg = self.settings.settings['composite_jpg']
        self.downloader.compile_pdf = self.settings.settings['composite_pdf']
        self.downloader.keep_originals = self.settings.settings['keep_originals']

        self.downloader_thread.start()

    def init_downloader_thread(self):
        self.downloader.total_title_changed.connect(lambda text: self.progress['total_label'].setText(text))
        self.downloader.total_maximum_changed.connect(lambda i: self.progress['total_progress'].setMaximum(i))
        self.downloader.total_progress_changed.connect(lambda i: self.progress['total_progress'].setValue(i))

        self.downloader.chapter_title_changed.connect(lambda text: self.progress['chapter_label'].setText(text))
        self.downloader.chapter_maximum_changed.connect(lambda i: self.progress['chapter_progress'].setMaximum(i))
        self.downloader.chapter_progress_changed.connect(lambda i: self.progress['chapter_progress'].setValue(i))
        
        self.downloader.page_title_changed.connect(lambda text: self.progress['page_label'].setText(text))
        self.downloader.page_maximum_changed.connect(lambda i: self.progress['page_progress'].setMaximum(i / 1024))
        self.downloader.page_progress_changed.connect(lambda i: self.progress['page_progress'].setValue(i / 1024))

        self.downloader.composition_label_changed.connect(lambda text: self.progress['composite_label'].setText(text))

        self.downloader.moveToThread(self.downloader_thread)

        self.downloader.finished.connect(self.downloader_thread.exit)
        self.downloader.finished.connect(self.on_download_finished)

        self.downloader_thread.started.connect(self.downloader.download)

    def on_download_finished(self):
        self.progress['total_progress'].setValue(self.progress['total_progress'].maximum())
        self.progress['chapter_progress'].setValue(self.progress['chapter_progress'].maximum())
        self.progress['page_progress'].setValue(self.progress['page_progress'].maximum())

        self.progress['composite_label'].setText('Download Task Finished!')
