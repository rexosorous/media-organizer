from PyQt5.QtWidgets import QDialog
import ui.batch_edit_ui as batch_edit_ui
from windows.base_edit import BaseEdit



class BatchEdit(BaseEdit):
    def __init__(self):
        super().__init__()
        self.BatchEditWindow = QDialog()
        self.window = batch_edit_ui.Ui_batch_edit_window()
        self.window.setupUi(self.BatchEditWindow)
        self.vars = vars(self.window)

        # for events
        self.double_clicks = ['genres_yes_list', 'genres_no_list', 'actors_yes_list', 'actors_no_list', 'tags_yes_list', 'tags_no_list']
        self.search_bars = ['genres_yes', 'genres_no', 'tags_yes', 'tags_no', 'series', 'actors_yes', 'actors_no', 'media_type', 'studio', 'director', 'country', 'language']

        # for creating drop down menus
        self.all_list_fields = ['genres_yes', 'genres_no', 'tags_yes', 'tags_no', 'series', 'actors_yes', 'actors_no', 'media_type', 'studio', 'director', 'country', 'language']
        self.with_deselect = ['series', 'studio', 'director', 'media_type', 'country', 'language']
        self.with_remove_all = ['genres_yes', 'tags_yes', 'actors_yes']

        # for clearing fields
        self.all_clear_fields = ['order', 'year', 'series', 'series', 'series_list', 'director', 'director_list', 'studio', 'studio_list', 'language', 'language_list', 'media_type', 'media_type_list', 'country', 'country_list', 'genres_yes', 'genres_yes_list', 'genres_no', 'genres_no_list', 'tags_yes', 'tags_yes_list', 'tags_no', 'tags_no_list', 'actors_yes', 'actors_yes_list', 'actors_no', 'actors_no_list']
        self.all_radio_buttons = ['rating_none', 'rating_1', 'rating_2', 'rating_3', 'rating_4', 'rating_5', 'animated_yes', 'animated_no', 'subtitles_yes', 'subtitles_no']

        self.create_menus()
        self.connect_events()



    def show(self):
        self.clear()
        self.populate()
        self.BatchEditWindow.exec_()



    def hide(self):
        # clears all the fields then hides the window
        self.clear()
        self.BatchEditWindow.done(0)



    def get_dict(self) -> dict:
        # returns a dict representing the fields in the window
        fields = ['series', 'order', 'media_type', 'country',]
        data = {
            'series': self.window.series_list.currentItem().text() if self.window.series_list.currentItem() else None,
            'order': float(self.window.order.displayText()) if self.window.order.displayText() else None,
            'media_type': self.window.media_type_list.currentItem().text() if self.window.media_type_list.currentItem() else None,
            'animated': None,
            'country': self.window.country_list.currentItem().text() if self.window.country_list.currentItem() else None,
            'language': ', '.join([lang.text() for lang in self.window.language_list.selectedItems()]),
            'subtitles': None,
            'year': int(self.window.year.displayText()) if self.window.year.displayText() else None,
            'genres': ', '.join([self.window.genres_yes_list.item(index).text() for index in range(self.window.genres_yes_list.count())]),
            'director': self.window.director_list.currentItem().text() if self.window.director_list.currentItem() else None,
            'studio': self.window.studio_list.currentItem().text() if self.window.studio_list.currentItem() else None,
            'actors': ', '.join([self.window.actors_yes_list.item(index).text() for index in range(self.window.actors_yes_list.count())]),
            'rating': None,
            'tags': ', '.join([self.window.tags_yes_list.item(index).text() for index in range(self.window.tags_yes_list.count())]),
        }

        for index in range(1, 6): # rating radio buttons
            if self.vars['rating_' + str(index)].isChecked():
                data['rating'] = index
                break

        # true/false radio buttons
        # make sure the checks are done this way because None != False
        # if a field is None, it means we don't want to include it in our editing

        # animated radio buttons
        if self.window.animated_yes.isChecked() and not self.window.animated_no.isChecked():
            data['animated'] = True
        elif self.window.animated_no.isChecked() and not self.window.animated_yes.isChecked():
            data['animated'] = False

        # subtitles radio buttons
        if self.window.subtitles_yes.isChecked() and not self.window.subtitles_no.isChecked():
            data['subtitles'] = True
        elif self.window.subtitles_no.isChecked() and not self.window.subtitles_yes.isChecked():
            data['subtitles'] = False

        fixed_data = {}
        for key in data:
            if data[key] != None and data[key] != '': # make sure we leave out any fields that are none or empty
                fixed_data[key] = data[key]

        return fixed_data