from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import ui.filter_ui as filter_ui
from windows.base import Base



class Filter(Base):
    def __init__(self):
        super().__init__()
        self.FilterWindow = QDialog()
        self.window = filter_ui.Ui_filter_window()
        self.window.setupUi(self.FilterWindow)
        self.vars = vars(self.window)

        # colors
        self.normal = (120, 120, 120, 255)
        self.green = (0, 255, 0, 255)
        self.red = (255, 0, 0, 255)
        self.blue = (0, 255, 255, 255)

        # for events
        self.double_clicks = ['genres_yes_list', 'genres_no_list', 'actors_yes_list', 'actors_no_list', 'tags_yes_list', 'tags_no_list', 'series_yes_list', 'series_no_list', 'studio_yes_list', 'studio_no_list', 'director_yes_list', 'director_no_list', 'media_type_yes_list', 'media_type_no_list', 'country_yes_list', 'country_no_list', 'language_yes_list', 'language_no_list']
        self.search_bars = ['genres_yes', 'genres_no', 'tags_yes', 'tags_no', 'actors_yes', 'actors_no', 'series_no', 'studio_yes', 'studio_no', 'director_yes', 'director_no', 'media_type_yes', 'media_type_no', 'country_yes', 'country_no', 'language_yes', 'language_no']

        # for creating drop down menus
        self.all_list_fields = ['genres_yes', 'genres_no', 'tags_yes', 'tags_no', 'actors_yes', 'actors_no', 'series_yes', 'series_no', 'studio_yes', 'studio_no', 'director_yes', 'director_no', 'media_type_yes', 'media_type_no', 'country_yes', 'country_no', 'language_yes', 'language_no', 'year', 'subtitles', 'animated']
        self.with_create = []
        self.with_deselect = ['year', 'subtitles', 'animated']
        self.with_remove_all = ['genres_yes', 'tags_yes', 'actors_yes', 'series_yes', 'studio_yes', 'director_yes', 'media_type_yes', 'country_yes', 'language_yes']

        # for clearing fields
        self.all_clear_fields = self.double_clicks + self.search_bars + ['year']
        self.all_radio_buttons = ['rating_none', 'rating_1', 'rating_2', 'rating_3', 'rating_4', 'rating_5', 'year_less', 'year_greater', 'year_equals', 'animated_yes', 'animated_no', 'subtitles_yes', 'subtitles_no']

        self.create_menus()
        self.connect_events()



    def show(self, selection: dict):
        # populates the filter screen's fields with what is selected in main table
        self.clear()
        self.populate()

        # display
        self.FilterWindow.exec_()



    def hide(self):
        # clears all the fields then hides the window
        self.title = ''
        self.clear()
        self.FilterWindow.done(0)



    def list_transfer(self, source):
        # when a user double clicks an item in a mtm list view, transfer it to the other list
        # background of each item should change colors to reflect AND, NOT, OR filtering
        selected = source.takeItem(source.currentRow()) # the item to be transferred
        src_name = source.objectName() # name of the list field
        if 'yes' in src_name: # converts the name. ex: genres_yes_list ---> genres_no_list and vice versa
            src_name = src_name.replace('yes', 'no')
            selected.setBackground(QColor(*self.normal))
        else:
            src_name = src_name.replace('no', 'yes')
            if src_name[:src_name.find('_yes')] in ['media_type', 'country', 'series', 'studio', 'director'] or self.window.or_filter.isChecked():
                selected.setBackground(QColor(*self.blue))
            elif self.window.and_filter.isChecked():
                selected.setBackground(QColor(*self.green))
            elif self.window.not_filter.isChecked():
                selected.setBackground(QColor(*self.red))
        self.vars[src_name].addItem(selected) # add the item to the opposite list



    def list_transfer_all(self, src):
        # transfers all items from the yes side to the no side
        source = self.vars[src + '_list']
        count = list(range(source.count()))
        count.reverse()
        for index in count:
            item = source.takeItem(index)
            destination = source.objectName().replace('yes', 'no')
            self.vars[destination].addItem(item)
            item.setBackground(QColor(*self.normal))



    def get_dict(self) -> dict:
        # returns a dict representing the fields in the window
        fields = [f for f in self.all_list_fields if f.endswith('yes')]
        data = {
            'rating': {'AND': [], 'NOT': [], 'OR': []},
            }

        for field in fields:
            field_data = {
                'AND': [],
                'NOT': [],
                'OR': []
            }

            f_list = self.vars[field+'_list']
            for index in range(f_list.count()):
                item = f_list.item(index)
                if item.background().color().getRgb() == self.green:
                    field_data['AND'].append(item.text())
                elif item.background().color().getRgb() == self.red:
                    field_data['NOT'].append(item.text())
                elif item.background().color().getRgb() == self.blue:
                    field_data['OR'].append(item.text())
            if field_data['AND'] or field_data['NOT'] or field_data['OR']: # if there's any data in the dict
                data[field[:field.find('_yes')]] = field_data



        for index in range(1, 6): # rating radio buttons
            if self.vars['rating_' + str(index)].isChecked():
                data['rating']['OR'].append(index)
        if self.window.rating_none.isChecked():
            data['rating']['OR'].append('None')
        if not data['rating']['OR']:
            del data['rating']


        if self.window.subtitles_yes.isChecked():
            data['subtitles'] = True
        elif self.window.subtitles_no.isChecked():
            data['subtitles'] = False

        if self.window.animated_yes.isChecked():
            data['animated'] = True
        elif self.window.animated_no.isChecked():
            data['animated'] = False


        year_text = self.window.year.displayText()
        if self.window.year_less.isChecked():
            year_text = '<' + year_text
        if self.window.year_greater.isChecked():
            year_text = '>' + year_text
        if self.window.year_equals.isChecked():
            year_text = '=' + year_text
        if year_text:
            data['year'] = year_text

        return data








# selected.setBackground(QColor('green'))
# selected.background().color().getRgb()