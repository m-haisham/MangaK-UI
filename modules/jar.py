import os
import subprocess
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject

from modules.settings import Settings


def j_call(*, file: str, args: list = []):
    """ call java (file) (.jar) as a subprocess with arguments (args) """
    if type(file) != str:
        raise TypeError("'file' must be of type str")
    if not (os.path.exists(file) and os.path.isfile(file)):
        raise FileNotFoundError(f"{file} of type 'file' not found")
    if type(args) != list:
        raise TypeError("'args' must be of type list")
    if args != [] and type(args[0]) != str:
        raise TypeError("'args' must be a list of strings")
    child = subprocess.run([
                               'javaw',
                               '-jar',
                               file,
                           ] + args)
    return child.returncode


def fave(args: list):
    return j_call(file=Settings.kfave_path, args=[Settings.favourite_data_file, 'mangakakalot'] + args)


class FinishedQObject(QObject):
    finished = pyqtSignal()


class FaveThreaded(QRunnable):
    def __init__(self, args):
        super(FaveThreaded, self).__init__()
        self.signal = FinishedQObject()
        self.args = args

    def run(self):
        fave(args=self.args)
        self.signal.finished.emit()
