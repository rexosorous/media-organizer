from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from functools import partial
import ui.create_ui as create_ui
from windows.base import Base

# website scrapers
import scrapers.mal_scraper as mal
import scrapers.imdb_scraper as imdb



class Create(Base):
    def __init__(self):
        super().__init__()
        self.CreateWindow = QDialog()
        self.window = create_ui.Ui_create_window()
        self.window.setupUi(self.CreateWindow)
        self.vars = vars(self.window)
        self.title=''

        self.imdb_data = []
        self.mal_data =[]

        # for events
        self.double_clicks = ['genres_yes_list', 'genres_no_list', 'actors_yes_list', 'actors_no_list', 'tags_yes_list', 'tags_no_list']
        self.search_bars = ['genres_yes', 'genres_no', 'tags_yes', 'tags_no', 'series', 'actors_yes', 'actors_no', 'media_type', 'studio', 'director', 'country', 'language']

        # for creating drop down menus
        self.all_list_fields = ['genres_yes', 'genres_no', 'tags_yes', 'tags_no', 'series', 'actors_yes', 'actors_no', 'media_type', 'studio', 'director', 'country', 'language']
        self.with_create = ['genres_yes', 'genres_no', 'tags_yes', 'tags_no', 'series', 'actors_yes', 'actors_no', 'media_type', 'studio', 'director', 'country', 'language']
        self.with_deselect = ['series', 'studio', 'director']
        self.with_remove_all = ['genres_yes', 'tags_yes', 'actors_yes']

        # for clearing fields
        self.all_clear_fields = ['title', 'alt_title', 'order', 'year', 'plot', 'notes', 'series', 'series_list', 'director', 'director_list', 'studio', 'studio_list', 'language', 'language_list', 'media_type', 'media_type_list', 'country', 'country_list', 'genres_yes', 'genres_yes_list', 'genres_no', 'genres_no_list', 'tags_yes', 'tags_yes_list', 'tags_no', 'tags_no_list', 'actors_yes', 'actors_yes_list', 'actors_no', 'actors_no_list']
        self.all_radio_buttons = ['rating_none', 'rating_1', 'rating_2', 'rating_3', 'rating_4', 'rating_5', 'animated_yes', 'animated_no', 'subtitles_yes', 'subtitles_no']

        self.create_menus()
        self.connect_events()



    def show(self, filename):
        self.title = filename
        self.window.title.setText(filename)
        self.populate()
        self.connect_other_events()
        self.CreateWindow.exec_()



    def connect_other_events(self):
        self.window.clear.clicked.connect(self.clear)
        self.window.imdb_scan.clicked.connect(self.scan_imdb)
        self.window.mal_scan.clicked.connect(self.scan_mal)



    def scan_imdb(self):
        # when a scan button is pressed, search for the 3 most likely results from whatever is in the title field
        self.imdb_data = imdb.search(self.window.title.displayText())
        for index in self.imdb_data:
            for key in index:
                if not index[key]:
                    index[key] = ''
        self.rename_imdb_buttons() # rename the buttons with appropriate data
        for index in range(3):
            try:
                self.vars['imdb_'+str(index+1)].clicked.connect(partial(self.repopulate, self.imdb_data[index]))
            except:
                pass



    def scan_mal(self):
        # when a scan button is pressed, search for the 3 most likely results from whatever is in the title field
        self.mal_data = mal.search(self.window.title.displayText())

        for index in self.mal_data:
            for key in index:
                if not index[key]:
                    index[key] = ''

        self.rename_mal_buttons() # rename the buttons with appropriate data
        for index in range(3):
            self.vars['mal_'+str(index+1)].clicked.connect(partial(self.repopulate, self.mal_data[index]))



    def rename_imdb_buttons(self):
        # sets the text of each button to reflect some very basic info about that scraped data
        for index in range(3):
            try:
                data = self.imdb_data[index]
                display = [ 'Title: ' + data['title'],
                            'Alt Title: ' + data['alt_title'],
                            'Year: ' + data['year'],
                            'Media Type: ' + data['media_type'],
                            'Director: ' + data['director']]
                text = '\n'.join(display)
                self.vars['imdb_'+str(index+1)].setText(text)
            except:
                self.vars['imdb_'+str(index+1)].setText('could not find')



    def rename_mal_buttons(self):
        # sets the text of each button to reflect some very basic info about that scraped data
        for index in range(3):
            data = self.mal_data[index]
            display = [ 'Title: ' + data['title'],
                        'Alt Title: ' + data['alt_title'],
                        'Year: ' + data['year'],
                        'Media Type: ' + data['media_type'],
                        'Director: ' + data['director']]
            text = '\n'.join(display)
            self.vars['mal_'+str(index+1)].setText(text)



    def repopulate(self, scraped_info: dict):
        # populates the create screen's fields with information scraped from imdb or myanimelist
        self.clear()
        self.populate()

        # for key in scraped_info:
        #     print(f'{key}: {scraped_info[key]}')

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
                    highlight = self.window.language_list.findItems(scraped_info['language'], Qt.MatchExactly)
                    highlight[0].setSelected(True)
            elif key == 'rating':
                try:
                    field = 'rating_' + scraped_info['rating']
                    self.vars[field].setChecked(True)
                except KeyError:
                    self.window.rating_none.setChecked(True)
            elif key in ['animated', 'subtitles']:
                field = key + '_no'
                if scraped_info[key]:
                    field = key + '_yes'
                self.vars[field].setChecked(True)
            elif key in ['genres', 'actors', 'tags']:
                field_no = key + '_no_list'
                field_yes = key + '_yes_list'
                for val in scraped_info[key]:
                    if val:
                        take = self.vars[field_no].findItems(val, Qt.MatchExactly)
                        place = self.vars[field_no].takeItem(self.vars[field_no].row(take[0]))
                        self.vars[field_yes].addItem(place)

        self.window.title.setFocus()



    def hide(self):
        # clears all the fields then hides the window
        self.title = ''
        self.imdb_data = []
        self.mal_data = []
        self.clear()
        self.CreateWindow.done(0)