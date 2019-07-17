
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.tree import GenerateTree

class ThreadedTreeGenerate(object):
    def __init__(self):
        super().__init__()

        self.tree = GenerateTree()
        self.tree_thread = QThread()

        self.tree.moveToThread(self.tree_thread)

        self.tree.finished.connect(self.tree_thread.exit)
        self.tree.finished.connect(self.on_generate_finished)

        self.tree_thread.started.connect(self.tree.generate)


    def on_generate_clicked(self):
        self.setEnabled(False)
        
        self.tree_thread.start()

    def on_generate_finished(self):
        self.setEnabled(True)