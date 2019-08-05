import os
import json

class Settings:
    save_path = 'config.json'
    manga_save_path = 'Manga'
    style_save_file = 'style.css'
    jpg_composite_path = 'jpg'
    pdf_composite_path = 'pdf'
    manga_tree_name = 'tree'
    web_files_location = 'web'
    download_log = 'dlog.json'
    mangakakalot_home = 'https://mangakakalot.com/page'
    web_keybinding = 'keybinding.js'

    kfave_path = 'Kfave.jar'

    manga_data_file = os.path.join(web_files_location, 'data.json')
    favourite_data_file = os.path.join(manga_save_path, 'fave.json')

    html_index = 'index.html'

    css_folder = os.path.join(web_files_location, 'css')
    css_custom = 'custom-style.css'
    css_bootstrap = 'bootstrap.min.css'

    js_folder = os.path.join(web_files_location, 'js')
    js_jquery = 'jquery-1.12.4.min.js'
    js_bootstrap = 'bootstrap.min.js'
    js_custom = 'script.js'

    def __init__(self):
        if self.settings_exists():
            self.load_settings()
        else:
            self.settings = {
                'startup_fave': False,
                'startup_popular': False,
                'startup_top10': True,
                'composite_jpg': False,
                'composite_pdf': False,
                'keep_originals': True,
                'download_thumbnails': True,
                'dark_mode': False
            }
            with open(self.save_path, 'w') as f:
                json.dump(self.settings, f)
        
        if not os.path.exists(self.manga_save_path):
            os.mkdir(self.manga_save_path)

    def save_settings(self, startup_fave: bool, startup_popular: bool, startup_top10: bool, composite_jpg: bool, composite_pdf: bool, keep_originals: bool, download_thumbnails: bool) -> None:
        """
        saves the current settings
        """
        self.settings = {
            'startup_fave': startup_fave,
            'startup_popular': startup_popular,
            'startup_top10': startup_top10,
            'composite_jpg': composite_jpg,
            'composite_pdf': composite_pdf,
            'keep_originals': keep_originals,
            'download_thumbnails': download_thumbnails,
            'dark_mode': self.settings['dark_mode']
        }
        with open(self.save_path, 'w') as f:
            json.dump(self.settings, f)

    def dark_mode_enabled(self, dark_mode : bool) -> None:
        self.settings = {
            'startup_fave': self.settings['startup_fave'],
            'startup_popular': self.settings['startup_popular'],
            'startup_top10': self.settings['startup_top10'],
            'composite_jpg': self.settings['composite_jpg'],
            'composite_pdf': self.settings['composite_pdf'],
            'keep_originals': self.settings['keep_originals'],
            'download_thumbnails': self.settings['download_thumbnails'],
            'dark_mode': dark_mode
        }
        with open(self.save_path, 'w') as f:
            json.dump(self.settings, f)

    def load_settings(self):
        '''
        load the settings from file
        '''
        with open(self.save_path, 'r') as f:
            self.settings = json.load(f)

    def settings_exists(self) -> bool:
        '''
        checks if save file exists
        '''
        return os.path.exists(self.save_path)