from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.html import HtmlManager

class ThreadedWebGenerate(object):
    def __init__(self):
        super().__init__()

        self.should_open_browser = True

        self.html = HtmlManager()
        self.html_thread = QThread()

        self.html.moveToThread(self.html_thread)

        self.html.finished.connect(self.html_thread.exit)
        self.html.finished.connect(self.on_web_finished)

        self.html_thread.started.connect(self.html.generate_web)

    def on_browser_clicked(self):
        self.setEnabled(False)
        self.html_thread.start()

    def on_web_finished(self):
        self.setEnabled(True)
        if self.should_open_browser:
            self.html.open()
        self.should_open_browser = True

    def on_bdata_clicked(self):
        self.should_open_browser = False
        self.setEnabled(False)
        self.html_thread.start()