
import os
import json
from modules.compostion import numericalSort
from modules.settings import Settings

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

def generate_chapter_tree(manga_directory : str) -> None:
    # get all chapters
    chapter_dirs = sorted(get_dirs(manga_directory)[0], key=numericalSort)

    chapter_dict = {}
    for chapter_dir in chapter_dirs:
        if chapter_dir == Settings.jpg_composite_path or chapter_dir == Settings.pdf_composite_path:
            continue

        pages = get_dirs(os.path.join(manga_directory, chapter_dir))[1]

        chapter_dict[chapter_dir] = sorted(pages, key=numericalSort)

    with open(os.path.join(manga_directory, Settings.manga_tree_name)+'.json', 'w') as f:
        json.dump(chapter_dict, f)

def get_dirs(path : str) -> tuple:
        '''
        Seperates the files and folders of directory

        return dirs, files
        '''
        full_list = os.listdir(path)

        dir_list = []
        files_list = []
        for i in full_list:
            if os.path.isdir(os.path.join(path, i)):
                dir_list.append(i)
            else:
                files_list.append(i)

        return dir_list, files_list

class GenerateTree(QObject):

    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def generate(self):
        mangas = get_dirs(Settings.manga_save_path)[0]

        for manga in mangas:
            generate_chapter_tree(os.path.join(Settings.manga_save_path, manga))

        self.finished.emit()