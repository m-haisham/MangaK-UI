import json
import os
import re
import webbrowser

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from yattag import Doc

from modules.compostion import numericalSort
from modules.settings import Settings
from modules.tree import get_dirs


class HtmlManager(QObject):

    finished = pyqtSignal()

    def __init__(self):
        '''
        Initialize the object
        '''
        super().__init__()

        if not os.path.exists(Settings.style_save_file):
            from modules.styles import style

            with open(Settings.style_save_file , 'w') as f:
                for line in style:
                    f.write(line)

        self.main_menu = os.path.join(Settings.web_files_location, 'index.html')

    def generate_new_chapter(self, manga_title: str, chapter_title: str, page_list: str, destination, prefix='', previous = '#', next = '#'):
        '''
        manga_title (str): title of the manga the chapter belongs to
        chapter_title (str): title of chapter the page belongs to
        page_list (list): list of pages in numerical order
        destination (str): save path for the chapter html file

        prefix (str): relative path to pages
        previous (str): relative path to previous chapter html
        next (str): relative path to next chapter html

        Creates a new html file containing all pages and named (chapter_title).html
        '''
        doc, tag, text = Doc().tagtext()

        # html
        doc.asis('<!DOCTYPE html>')
        doc.asis('<html lang="en" dir="ltr">')
        with tag('head'):
            doc.asis('<meta charset="utf-8">')
            doc.asis('<link rel="stylesheet" href="../../style.css">')
            with tag('title'):
                text(manga_title + ' - ' + chapter_title)
        with tag('body'):
            with tag('div', klass='container'):
                # manga title
                with tag('div', klass='title-container'):
                    doc.asis('<a class="title manga-title" href="' + os.path.join('..', manga_title + '.html') + '" >' + manga_title + '</a>')
                with tag('div', klass='chapter-bar'):
                    doc.asis('<a class="btn btn-left btn-1 btn-1d" href="' + previous + '">Previous</a>')
                    with tag('h3', klass='title chapter-title'):
                        text(chapter_title)
                    doc.asis('<a class="btn btn-right btn-1 btn-1d" href="' + next + '">Next</a>')

                # loop through the page list
                for page in page_list:
                    # add img tag
                    doc.stag('img', src=self.verify_source(os.path.join(prefix, page)), klass='page', style="margin:10px auto;")

                with tag('div', klass='chapter-bar'):
                    doc.asis('<a class="btn btn-left btn-1 btn-1d" href="' + previous + '">Previous</a>')
                    with tag('h3', klass='title chapter-title'):
                        text(chapter_title)
                    doc.asis('<a class="btn btn-right btn-1 btn-1d" href="' + next + '">Next</a>')
        doc.asis('</html>')

        # save html doc in (destination)
        with open(destination, 'w') as f:
            f.write(doc.getvalue())

    def generate_list(self, title: str, mlist: list, destination: str, is_manga_list = True):
        '''
        title (string): manga name
        mlist (list): list of manga or chapters
        destination (str): save path for the chapter html file
        
        is_manga_list (bool): Determines the link of the list items

        Creates a html list from given (mlist) and saves to (destination)
        '''

        doc, tag, text = Doc().tagtext()

        # html
        doc.asis('<!DOCTYPE html>')
        doc.asis('<html lang="en" dir="ltr">')
        with tag('head'):
            doc.asis('<meta charset="utf-8">')
            doc.asis('<link rel="stylesheet" href="../style.css">')
            with tag('title'):
                text(title if is_manga_list else title + '- Chapter list')
        with tag('body'):
            with tag('div', klass='container'):

                # if is a chapter list generate a button to access main menu
                if not is_manga_list:
                    doc.asis('<a class="btn btn-left btn-1 btn-1d" href="index.html">Menu</a>')

                # manga title
                with tag('div', klass='title-container'):
                    with tag('h1', klass='title manga-title'):
                        text(title)
                
                with tag('ul'):
                    # loop through the list
                    for item in mlist:
                        if is_manga_list:
                            link = item + '.html'
                        else:
                            # chapter htmls are stored in folder inside save location named (title)
                            link = os.path.join(title, item + '.html')
                        with tag('li', klass='manga'):
                            doc.asis('<a class="btn btn-1 btn-1d" href="'+link+'">'+item+'</a>')

        doc.asis('</html>') 

        # save html doc in (destination)
        with open(destination, 'w') as f:
            f.write(doc.getvalue())

    def generate_web(self):
        '''
        Uses the tree (which can be generated using MangaManager class) to generate all the necessary html files and links them
        Root is index.html
        '''
        # generate manga list
        all_manga_keys = get_dirs(Settings.manga_save_path)[0]
        if not os.path.exists(Settings.web_files_location):
            os.mkdir(Settings.web_files_location)

        self.generate_list('Manga list', all_manga_keys, self.main_menu)

        # loop through all mangas
        for i in range(len(all_manga_keys)):
            manga_key = all_manga_keys[i]

            manga_data = {}
            try:
                with open(os.path.join(Settings.manga_save_path, manga_key, Settings.manga_tree_name)+'.json') as f:
                    manga_data = json.load(f)
            except FileNotFoundError:
                continue

            all_chapters_keys = list(manga_data.keys())

            # generate chapter list for manga (manga_key)
            self.generate_list(manga_key, all_chapters_keys, os.path.join(Settings.web_files_location, manga_key+'.html'), is_manga_list=False)

            # make chapter html's save path
            save_location = os.path.join(Settings.web_files_location, manga_key)
            if not os.path.exists(save_location):
                os.mkdir(save_location)
            
            # loop through all chapters
            for i in range(len(all_chapters_keys)):
                chapter_key = all_chapters_keys[i]

                next_link = os.path.join(all_chapters_keys[(i + 1) % len(all_chapters_keys)] + '.html')
                previous_link = os.path.join(all_chapters_keys[(i - 1) % len(all_chapters_keys)] + '.html')

                # generate chapter html
                self.generate_new_chapter(manga_key, chapter_key, manga_data[chapter_key],
                                        os.path.join(save_location, chapter_key + '.html'),
                                        os.path.join('..', '..', Settings.manga_save_path, manga_key, chapter_key),
                                        next=next_link, previous=previous_link)

        self.finished.emit()

    def open(self):
        '''
        Opens index.html in default browser

        returns True if successful
        '''
        if os.path.exists(self.main_menu):
            webbrowser.open('file://'+os.path.realpath(self.main_menu))
            return True
        else:
            return False

    def verify_source(self, source):
        '''
        source (str): source to be encoded

        Encodes the string

        [
            replace ' ' with '%20'
        ]
        '''
        new = re.sub(r'[ ]', '%20', source)
        return new
