from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
import ui.edit_ui as edit_ui
from windows.base_edit import BaseEdit



class Edit(BaseEdit):
    def __init__(self):
        super().__init__()
        self.EditWindow = QMainWindow()
        self.window = edit_ui.Ui_edit_window()
        self.window.setupUi(self.EditWindow)
        self.vars = vars(self.window)
        self.title = '' # holds the original title of a selected movie because the title might be edited in this window

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



    def show(self, selection: dict):
        # populates the edit screen's fields with what is selected in main table
        self.title = ''
        self.clear()
        self.populate()

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
        self.EditWindow.show()



    def hide(self):
        # clears all the fields then hides the window
        self.title = ''
        self.clear()
        self.EditWindow.hide()



    def get_dict(self) -> dict:
        # returns a dict representing the fields in the window
        data = {
            'title': self.window.title.displayText(),
            'alt_title': self.window.alt_title.displayText(),
            'series': self.window.series_list.currentItem().text() if self.window.series_list.currentItem() else None,
            'order': float(self.window.order.displayText()) if self.window.order.displayText() else None,
            'media_type': self.window.media_type_list.currentItem().text() if self.window.media_type_list.currentItem() else None,
            'animated': self.window.animated_yes.isChecked(),
            'country': self.window.country_list.currentItem().text() if self.window.country_list.currentItem() else None,
            'language': ', '.join([lang.text() for lang in self.window.language_list.selectedItems()]),
            'subtitles': self.window.subtitles_yes.isChecked(),
            'year': int(self.window.year.displayText()) if self.window.year.displayText() else None,
            'genres': ', '.join([self.window.genres_yes_list.item(index).text() for index in range(self.window.genres_yes_list.count())]),
            'director': self.window.director_list.currentItem().text() if self.window.director_list.currentItem() else None,
            'studio': self.window.studio_list.currentItem().text() if self.window.studio_list.currentItem() else None,
            'actors': ', '.join([self.window.actors_yes_list.item(index).text() for index in range(self.window.actors_yes_list.count())]),
            'plot': self.window.plot.toPlainText(),
            'rating': None,
            'tags': ', '.join([self.window.tags_yes_list.item(index).text() for index in range(self.window.tags_yes_list.count())]),
            'notes': self.window.notes.toPlainText()
        }

        for index in range(1, 6):
            if self.vars['rating_' + str(index)].isChecked():
                data['rating'] = index
                break

        return data



