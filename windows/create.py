from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from functools import partial
import ui.create_ui as create_ui
from windows.base_edit import BaseEdit



class Create(BaseEdit):
    def __init__(self):
        super().__init__()
        self.CreateWindow = QDialog()
        self.window = create_ui.Ui_create_window()
        self.window.setupUi(self.CreateWindow)
        self.vars = vars(self.window)

        self.imdb_data = []
        self.mal_data =[]

        # for events
        self.double_clicks = ['genres_yes_list', 'genres_no_list', 'actors_yes_list', 'actors_no_list', 'tags_yes_list', 'tags_no_list']
        self.search_bars = ['genres_yes', 'genres_no', 'tags_yes', 'tags_no', 'series', 'actors_yes', 'actors_no', 'media_type', 'studio', 'director', 'country', 'language']

        # for creating drop down menus
        self.all_list_fields = ['genres_yes', 'genres_no', 'tags_yes', 'tags_no', 'series', 'actors_yes', 'actors_no', 'media_type', 'studio', 'director', 'country', 'language']
        self.with_deselect = ['series', 'studio', 'director']
        self.with_remove_all = ['genres_yes', 'tags_yes', 'actors_yes']

        # for clearing fields
        self.all_clear_fields = ['title', 'alt_title', 'order', 'year', 'plot', 'notes', 'series', 'series_list', 'director', 'director_list', 'studio', 'studio_list', 'language', 'language_list', 'media_type', 'media_type_list', 'country', 'country_list', 'genres_yes', 'genres_yes_list', 'genres_no', 'genres_no_list', 'tags_yes', 'tags_yes_list', 'tags_no', 'tags_no_list', 'actors_yes', 'actors_yes_list', 'actors_no', 'actors_no_list']
        self.all_radio_buttons = ['rating_none', 'rating_1', 'rating_2', 'rating_3', 'rating_4', 'rating_5', 'animated_yes', 'animated_no', 'subtitles_yes', 'subtitles_no']

        self.create_menus()
        self.connect_events()



    def show(self, imdb_data: [dict], mal_data: [dict]):
        self.imdb_data = imdb_data
        self.mal_data = mal_data
        self.rename_buttons()
        self.connect_scrape_buttons()
        self.CreateWindow.exec_()



    def rename_buttons(self):
        # sets the text of each button to reflect some very basic info about that scraped data
        for site in ['imdb', 'mal']:
            for index in range(5):
                data = self.vars[site+'_data'][index]
                display = ['Title: ' + data['title'],
                            'Alt Title: ' + data['alt_title'],
                            'Year: ' + data['year'],
                            'Director: ' + data['director']]
                text = '\n'.join(display)
                self.vars[site+'_'+index].setText(text)



    def connect_scrape_buttons(self):
        # when a button is pressed, it'll repopulate the window with information scraped from that site
        for site in ['imdb', 'mal']:
            for index in range(5):
                self.vars[site+'_'+index].clicked.connect(partial(self.repopulate, self.vars[site+'_data'][index]))



    def repopulate(self, scraped_info: dict):
        # populates the create screen's fields with information scraped from imdb or myanimelist
        self.clear()
        self.populate()

        if 'title' in scraped_info:
            self.title = scraped_info['title']

        for key in scraped_info:
            if key in ['title', 'alt_title', 'order', 'year', 'plot', 'notes']: # text fields
                self.vars[key].setText(scraped_info[key])
            elif key in ['series', 'director', 'studio', 'media_type', 'country']: # lists
                field = key + '_list'
                highlight = self.vars[field].findItems(scraped_info[key], Qt.MatchExactly)
                if len(highlight) == 1:
                    self.vars[field].setCurrentItem(highlight[0])
            elif key == 'language': # multi select lists
                if scraped_info['language']:
                    langs = scraped_info['language'].split(', ')    # languages is a many to many field
                    for lang in langs:
                        highlight = self.window.language_list.findItems(lang, Qt.MatchExactly)
                        highlight[0].setSelected(True)
            elif key == 'rating':
                try:
                    field = 'rating_' + scraped_info['rating']
                    self.vars[field].setChecked(True)
                except KeyError:
                    self.window.rating_none.setChecked(True)
            elif key in ['animated', 'subtitles']:
                field = key + '_no'
                if scraped_info[key] == 'True':
                    field = key + '_yes'
                self.vars[field].setChecked(True)
            elif key in ['genres', 'actors', 'tags']:
                transfer = scraped_info[key].split(', ')
                field_no = key + '_no_list'
                field_yes = key + '_yes_list'
                for val in transfer:
                    if val:
                        take = self.vars[field_no].findItems(val, Qt.MatchExactly)
                        place = self.vars[field_no].takeItem(self.vars[field_no].row(take[0]))
                        self.vars[field_yes].addItem(place)

        self.window.title.setFocus()



    def hide(self):
        # clears all the fields then hides the window
        self.imdb_data = []
        self.mal_data = []
        self.clear()
        self.CreateWindow.done(0)