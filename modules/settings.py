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

    def __init__(self):
        if self.settings_exists():
            self.load_settings()
        else:
            self.settings = {
                'composite_jpg': False,
                'composite_pdf': False,
                'keep_originals': True
            }
            with open(self.save_path, 'w') as f:
                json.dump(self.settings, f)
        
        if not os.path.exists(self.manga_save_path):
            os.mkdir(self.manga_save_path)

    def save_settings(self, composite_jpg: bool, composite_pdf: bool, keep_originals: bool) -> None:
            '''
            saves the current settings
            '''
            self.settings = {
                'composite_jpg': composite_jpg,
                'composite_pdf': composite_pdf,
                'keep_originals': keep_originals
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