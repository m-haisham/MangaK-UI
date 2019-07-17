import os
import shutil
import sys

import requests
from bs4 import BeautifulSoup
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from requests.exceptions import InvalidSchema, InvalidURL, MissingSchema
from modules.settings import Settings
from modules.compostion import dir_to_pdf, stack
from modules.tree import generate_chapter_tree

class ChapterListLoader(QObject):

    finished = pyqtSignal()
    valid_url = pyqtSignal(bool)
    title = pyqtSignal(str)
    maximum = pyqtSignal(int)
    progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.manga_link =''
        self.loaded_list = []

    def load(self):
        r = None
        try:
            r = requests.get(self.manga_link)
        except InvalidURL or InvalidSchema or MissingSchema:
            self.valid_url.emit(False)
            return
        else:
            self.valid_url.emit(True)

        soup = BeautifulSoup(r.content, "html.parser")
        chapterbox = soup.find_all(class_="chapter-list")
        rows = chapterbox[0].find_all(class_="row")
        title = soup.find(class_="manga-info-text").find("h1").text
        self.title.emit(title)
        self.maximum.emit(len(rows))

        count = 0
        self.loaded_list = []
        for i in range(len(rows) - 1, -1, -1):
            self.loaded_list.append({
                'name': rows[i].find('a', href=True).text,
                'href': rows[i].find('a', href=True)['href']
            })
            count += 1
            self.progress.emit(count)

        self.finished.emit()

class ChapterListDownloader(QObject):
    
    finished = pyqtSignal()

    total_title_changed = pyqtSignal(str)
    chapter_title_changed = pyqtSignal(str)
    page_title_changed = pyqtSignal(str)

    total_maximum_changed = pyqtSignal(int)
    chapter_maximum_changed = pyqtSignal(int)
    page_maximum_changed = pyqtSignal(int)

    total_progress_changed = pyqtSignal(int)
    chapter_progress_changed = pyqtSignal(int)
    page_progress_changed = pyqtSignal(int)

    composition_label_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.manga_name = ''

        self.chapter_list = []
        self.compile_jpg = None
        self.compile_pdf = None
        self.keep_originals = None

    def download(self):

        self.total_maximum_changed.emit(len(self.chapter_list))
        self.total_progress_changed.emit(0)

        # Setting manga directory
        manga_directory = os.path.join(Settings.manga_save_path, self.manga_name)
        if not os.path.exists(manga_directory):
            os.mkdir(manga_directory)

        # Loop through all chapters in chapter list
        for i in range(len(self.chapter_list)):
            chapter_href = self.chapter_list[i]['href']

            page_list = self.get_page_list(chapter_href)

            chapter_name = chapter_href.split('/')[-1]
            self.chapter_title_changed.emit(chapter_name)

            # Setting chapter directory
            chapter_directory = os.path.join(Settings.manga_save_path, self.manga_name, chapter_name)
            if not os.path.exists(chapter_directory):
                os.mkdir(chapter_directory)

            self.chapter_progress_changed.emit(0)
            self.chapter_maximum_changed.emit(len(page_list))

            for j in range(len(page_list)):
                page = page_list[j]
                self.save_image(page, chapter_directory)
                self.chapter_progress_changed.emit(j + 1)

            # Do compositions here
            if self.compile_jpg:
                self.composition_label_changed.emit('Compositing [{}] to JPG'.format(chapter_name))

                jpg_dir = os.path.join(Settings.manga_save_path, self.manga_name, Settings.jpg_composite_path)
                if not os.path.exists(jpg_dir):
                    os.mkdir(jpg_dir)
                
                # jpg
                stack(chapter_directory, jpg_dir)

            if self.compile_pdf:
                self.composition_label_changed.emit('Compositing [{}] to PDF'.format(chapter_name))

                pdf_dir = os.path.join(Settings.manga_save_path, self.manga_name, Settings.pdf_composite_path)
                if not os.path.exists(pdf_dir):
                    os.mkdir(pdf_dir)
                
                # pdf
                dir_to_pdf(chapter_directory, pdf_dir)

            if not self.keep_originals:
                self.composition_label_changed.emit('Removing [{}]'.format(chapter_name))
                shutil.rmtree(chapter_directory)
            else:
                generate_chapter_tree(manga_directory)

            self.composition_label_changed.emit('')
            
            self.chapter_progress_changed.emit(0)
            self.total_progress_changed.emit(i + 1)

        self.finished.emit()

    def save_image(self, url, directory):
        """
        url (String): online image file path
        directory (String): Image file save path

        returns: None

        This function downloads [url] and prints the progress of the download to the console and save the file to [directory]
        """
        filename = url.split('/')[-1]
        self.page_title_changed.emit(filename)
        with open(os.path.join(directory, filename), 'wb') as f:
            response = requests.get(url, stream=True)

            total_length = response.headers.get('content-length')
            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)

                self.page_maximum_changed.emit(total_length)

                chunksize = int(total_length / 100)
                for data in response.iter_content(chunk_size=chunksize):
                    dl += len(data)
                    f.write(data)

                    self.page_progress_changed.emit(dl)

    def get_page_list(self, chapter_path):
        """
        chapter_path (string): path of the chapter 

        returns (list): pages of the chapter
        """
        r = requests.get(chapter_path)
        soup = BeautifulSoup(r.content, "html.parser")
        pagebox = soup.find(id="vungdoc")
        rows = pagebox.find_all('img')
        pages = []
        for row in rows:
            pages.append(row['src'])
        return pages
