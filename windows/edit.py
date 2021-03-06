from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
import ui.edit_ui as edit_ui
from windows.base import Base



class Edit(Base):
    def __init__(self):
        super().__init__()
        self.EditWindow = QDialog()
        self.window = edit_ui.Ui_edit_window()
        self.window.setupUi(self.EditWindow)
        self.vars = vars(self.window)
        self.title = '' # holds the original title of a selected movie because the title might be edited in this window

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



    def show(self, selection: dict):
        # populates the edit screen's fields with what is selected in main table
        self.title = ''
        self.clear()
        self.populate()

        if 'title' in selection:
            self.title = selection['title']

        for key in selection:
            if key in ['title', 'alt_title', 'order', 'year', 'plot', 'notes']: # text fields
                self.vars[key].setText(selection[key])
            elif key in ['series', 'director', 'studio', 'media_type', 'country']: # lists
                field = key + '_list'
                highlight = self.vars[field].findItems(selection[key], Qt.MatchExactly)
                if len(highlight) == 1:
                    self.vars[field].setCurrentItem(highlight[0])
            elif key == 'language': # multi select lists
                if selection['language']:
                    langs = selection['language'].split(', ')    # languages is a many to many field
                    for lang in langs:
                        highlight = self.window.language_list.findItems(lang, Qt.MatchExactly)
                        highlight[0].setSelected(True)
            elif key == 'rating':
                try:
                    field = 'rating_' + selection['rating']
                    self.vars[field].setChecked(True)
                except KeyError:
                    self.window.rating_none.setChecked(True)
            elif key in ['animated', 'subtitles']:
                field = key + '_no'
                if selection[key] == 'True':
                    field = key + '_yes'
                self.vars[field].setChecked(True)
            elif key in ['genres', 'actors', 'tags']:
                transfer = selection[key].split(', ')
                field_no = key + '_no_list'
                field_yes = key + '_yes_list'
                for val in transfer:
                    if val:
                        take = self.vars[field_no].findItems(val, Qt.MatchExactly)
                        place = self.vars[field_no].takeItem(self.vars[field_no].row(take[0]))
                        self.vars[field_yes].addItem(place)

        # display
        self.window.title.setFocus()
        self.EditWindow.exec_()



    def hide(self):
        # clears all the fields then hides the window
        self.title = ''
        self.clear()
        self.EditWindow.done(0)