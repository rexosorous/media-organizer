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
        self.green = (0, 255, 0, 255)   # AND
        self.red = (255, 0, 0, 255)     # NOT
        self.blue = (0, 255, 255, 255)  # OR

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

        # for filtering
        self.and_chars = ['+', '=', '&']
        self.not_chars = ['-', '!']
        self.or_chars = ['/', '|', '\\']

        self.create_menus()
        self.connect_events()



    def show(self, selection: dict):
        # populates the filter screen's fields with what is selected in main table
        self.clear()
        self.populate()
        self.window.and_filter.setChecked(True)

        # display
        self.FilterWindow.exec_()



    def hide(self):
        # clears all the fields then hides the window
        self.title = ''
        self.clear()
        self.window.and_filter.setChecked(True)
        self.FilterWindow.done(0)



    def list_filter(self, source, text):
        # filters through a list based on what is typed in the textbox
        field = self.to_list(source)
        contents = [field.item(index).text() for index in range(field.count())]
        if text:
            if text[0] in self.and_chars + self.not_chars + self.or_chars:
                text = text[1:]
        for item in contents:
            if text.lower() in item.lower():
                field.findItems(item, Qt.MatchExactly)[0].setHidden(False)
            else:
                field.findItems(item, Qt.MatchExactly)[0].setHidden(True)



    def list_transfer(self, source):
        # when a user double clicks an item in a mtm list view, transfer it to the other list
        # background of each item should change colors to reflect AND, NOT, OR filtering
        selected = source.takeItem(source.currentRow()) # the item to be transferred
        src_name = source.objectName() # name of the list field
        if 'yes' in src_name: # converts the name. ex: genres_yes_list ---> genres_no_list and vice versa
            src_name = src_name.replace('yes', 'no')
            selected.setBackground(QColor(*self.normal))
        else:
            search = self.vars[src_name[:src_name.find('_list')]].displayText()
            src_name = src_name.replace('no', 'yes')

            if src_name[:src_name.find('_yes')] in ['media_type', 'country', 'series', 'studio', 'director']: # forced OR fields
                selected.setBackground(QColor(*self.blue))
            elif search[0] in self.and_chars + self.not_chars + self.or_chars: # if there is a special char up front, ignore the radio button
                if search[0] in self.and_chars:
                    selected.setBackground(QColor(*self.green))
                elif search[0] in self.not_chars:
                    selected.setBackground(QColor(*self.red))
                elif search[0] in self.or_chars:
                    selected.setBackground(QColor(*self.blue))
            # check the search bar for symbols
            elif self.window.and_filter.isChecked():
                selected.setBackground(QColor(*self.green))
            elif self.window.not_filter.isChecked():
                selected.setBackground(QColor(*self.red))
            elif self.window.or_filter.isChecked():
                selected.setBackground(QColor(*self.blue))
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
        basic_data = {}
        and_data = {}
        not_data = {}
        or_data = {'rating': []}

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

            fixed_field = field[:field.find('_yes')]
            if field_data['AND']:
                and_data[fixed_field] = field_data['AND']
            if field_data['NOT']:
                not_data[fixed_field] = field_data['NOT']
            if field_data['OR']:
                or_data[fixed_field] = field_data['OR']


        # rating checkboxes
        for index in range(1, 6):
            if self.vars['rating_' + str(index)].isChecked():
                or_data['rating'].append(index)
        if self.window.rating_none.isChecked():
            or_data['rating'].append(None)
        if not or_data['rating']:
            del or_data['rating']


        if self.window.subtitles_yes.isChecked():
            basic_data['subtitles'] = True
        elif self.window.subtitles_no.isChecked():
            basic_data['subtitles'] = False

        if self.window.animated_yes.isChecked():
            basic_data['animated'] = True
        elif self.window.animated_no.isChecked():
            basic_data['animated'] = False


        year_text = self.window.year.displayText()
        if self.window.year_less.isChecked():
            year_text = '<' + year_text
        if self.window.year_greater.isChecked():
            year_text = '>' + year_text
        if self.window.year_equals.isChecked():
            year_text = '=' + year_text
        if year_text:
            basic_data['year'] = year_text

        return [basic_data, and_data, not_data, or_data]








# selected.setBackground(QColor('green'))
# selected.background().color().getRgb()