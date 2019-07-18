import requests
from bs4 import BeautifulSoup
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.settings import Settings
from widgets.list.list_extension import PopularListItem

class MKCodec(QObject):
    finished = pyqtSignal()
    maximum = pyqtSignal(int)
    progress = pyqtSignal(int)

    def __init__(self):
        ''' 
        initialize the object
        '''
        super().__init__()

        self.search_prefix = 'https://mangakakalot.com/search/'
        self.search_postfix = '?page='
        self.keyword = ''

        self.search_result = []
        self.page_prefix = ''
        self.current_page = 0
        self.max_page = -1

    def search(self):
        '''
        Searches for the (keyword) on mangakakalot database and updates the variables
        Search result can be accessed as MKCodec.search_result (list)
        '''
        if len(self.keyword) < len(self.search_prefix) + 3:
            return

        r = requests.get(self.keyword)
        soup = BeautifulSoup(r.content, 'html.parser')

        self.search_result = []

        page_list = None
        try:
            page_list = soup.find('div', {'class': 'group_page'}).find_all('a')
        except AttributeError:
            self.page_prefix = ''
            self.max_page = -1
            self.maximum.emit(1)
        else:
            self.page_prefix = page_list[0]['href'][:-1]
            self.max_page = int(page_list[-1].text[5:-1])
            self.maximum.emit(self.max_page)

        count = 0
        while True:
            key = self.keyword+self.search_postfix+str(count+1)
            if count != 0:
                r = requests.get(key)
                soup = BeautifulSoup(r.content, 'html.parser')

            self._populate(soup)
            if self.max_page == -1 or count >= self.max_page - 1:
                self.progress.emit(self.max_page)
                self.finished.emit()
                break
            
            count += 1
            self.progress.emit(count)

    def _populate(self, dish):
        '''
        dish (BeautifulSoup): Beautiful soup object

        Parses the data (dish) and extracts information and updates object
        '''
        result_list = dish.find('div', {'class': 'panel_story_list'}).find_all('div', {'class': 'story_item'})
        for result in result_list:
            self.search_result.append({
                'name': result.find('h3', {'class': 'story_name'}).text.strip('\n'),
                'last_chapter': result.find_all('em', {'class': 'story_chapter'})[0].text.strip('\n'),
                'href': result.find('a')['href']
                })

class PopularPageCodec(QObject):

    finished = pyqtSignal()
    maximum = pyqtSignal(int)
    progress = pyqtSignal(int, dict)
    page_updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.page = 1
        self.url = 'https://mangakakalot.com/manga_list?type=topview&category=all&state=all&page='
        self.max_page = ''
        self.popular = {}

    def load_popular(self) -> None:
        self.page_updated.emit(self.page)
        full_url = self.url + str(self.page)

        r = requests.get(full_url)
        soup = BeautifulSoup(r.content, 'html.parser')

        self.max_page = soup.find('div', {'class': 'group_page'}).find_all('a')[-1].text[5:-1]

        cards = soup.find_all('div', {'class': 'list-truyen-item-wrap'})

        self.maximum.emit(len(cards))

        count = 0
        for card in cards:
            
            data = {
                'image_bytes': requests.get(card.find_all('a')[0].find('img')['src']).content,
                'url': card.find_all('a')[0]['href'],
                'manga_title': card.find('h3').text.strip('\n'),
                'last_chapter': card.find('a', {'class': 'list-story-item-wrap-chapter'}).text.strip('\n'),
                'views': card.find('span', {'class': 'aye_icon'}).text.strip('\n'),
                'description': card.find('p').text.strip('\n')
            }

            count+=1
            self.progress.emit(count, data)

        self.finished.emit()

    def increment_page(self):
        if self.max_page == '':
            self.get_max_page()
        self.page = min(int(self.max_page), self.page+1)

    def decrement_page(self):
        self.page = max(1, self.page-1)

    def get_max_page(self):
        full_url = self.url + str(self.page)

        r = requests.get(full_url)
        soup = BeautifulSoup(r.content, 'html.parser')

        self.max_page = soup.find('div', {'class': 'group_page'}).find_all('a')[-1].text[5:-1]

class Top10Codec(QObject):

    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.top10 = []

    def load_top10(self):
        r = requests.get(Settings.mangakakalot_home)
        soup = BeautifulSoup(r.content, 'html.parser')

        self.top10.clear()
        blocks = soup.find_all('div', {'class': 'xem-nhieu-item'})
        for block in blocks:
            details = block.find('a')
            self.top10.append({
                'href': details['href'],
                'manga': details['title'].strip('\n'),
                'last_chapter': details.text.strip('\n').split('-')[-1][1:]
            })

        self.finished.emit()