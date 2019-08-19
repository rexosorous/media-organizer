from PyQt5 import QtWidgets, QtCore
import db_handler as db
import ui.edit_ui as edit_ui



class Edit():
    def __init__(self):
        self.EditWindow = QtWidgets.QMainWindow()
        self.window = edit_ui.Ui_edit_window()
        self.window.setupUi(self.EditWindow)
        self.vars = vars(self.window)

        self.title = '' # holds the original title of the movie because user might change it


    def populate(self):
        # adds all the contents for lists and combo boxes

        # list adds
        self.window.series_list.addItems(db.get_all('Series'))
        self.window.director_list.addItems(db.get_all('Directors'))
        self.window.studio_list.addItems(db.get_all('Studios'))
        self.window.language_list.addItems(db.get_all('Languages'))

        # many to many list adds
        self.window.genres_no_list.addItems(db.get_all('Genres'))
        self.window.tags_no_list.addItems(db.get_all('Tags'))
        self.window.actors_no_list.addItems(db.get_all('Actors'))

        # combo box adds
        # TO DO: sort before adding
        self.window.media_type.addItems(db.get_all('MediaTypes'))
        self.window.country.addItems(db.get_all('Countries'))


        # sorting
        self.window.series_list.setSortingEnabled(True)
        self.window.director_list.setSortingEnabled(True)
        self.window.studio_list.setSortingEnabled(True)
        self.window.language_list.setSortingEnabled(True)
        self.window.genres_yes_list.setSortingEnabled(True)
        self.window.genres_no_list.setSortingEnabled(True)
        self.window.tags_yes_list.setSortingEnabled(True)
        self.window.tags_no_list.setSortingEnabled(True)
        self.window.actors_yes_list.setSortingEnabled(True)
        self.window.actors_no_list.setSortingEnabled(True)



    def clear(self):
        # clears all the fields in the edit screen
        self.title = None

        # basic
        self.window.title.clear()
        self.window.alt_title.clear()
        self.window.order.clear()
        self.window.year.clear()
        self.window.plot.clear()
        self.window.notes.clear()
        self.window.media_type.clear()
        self.window.country.clear()

        # lists
        self.window.series.clear()
        self.window.series_list.clear()
        self.window.director.clear()
        self.window.director_list.clear()
        self.window.studio.clear()
        self.window.studio_list.clear()
        self.window.language.clear()
        self.window.language_list.clear()

        # mtm lists
        self.window.genres_yes.clear()
        self.window.genres_yes_list.clear()
        self.window.genres_no.clear()
        self.window.genres_no_list.clear()
        self.window.tags_yes.clear()
        self.window.tags_yes_list.clear()
        self.window.tags_no.clear()
        self.window.tags_no_list.clear()
        self.window.actors_yes.clear()
        self.window.actors_yes_list.clear()
        self.window.actors_no.clear()
        self.window.actors_no_list.clear()

        # radio buttons
        self.window.rating_1.setChecked(False)
        self.window.rating_2.setChecked(False)
        self.window.rating_3.setChecked(False)
        self.window.rating_4.setChecked(False)
        self.window.rating_5.setChecked(False)
        self.window.rating_none.setChecked(False)
        self.window.animated_yes.setChecked(False)
        self.window.animated_no.setChecked(False)
        self.window.subtitles_yes.setChecked(False)
        self.window.subtitles_no.setChecked(False)



    def show(self, selection: dict):
        # populates the edit screen's fields with what is selected in main table
        self.clear()
        self.populate()

        self.title = selection['title']

        for key in selection:
            if key in ['title', 'alt_title', 'order', 'year', 'plot', 'notes']: # text fields
                self.vars[key].setText(selection[key])
            elif key in ['series', 'director', 'studio']: # lists
                field = key + '_list'
                highlight = self.vars[field].findItems(selection[key], QtCore.Qt.MatchExactly)
                if len(highlight) == 1:
                    self.vars[field].setCurrentItem(highlight[0])
            elif key == 'language': # multi select lists
                if selection['language']:
                    langs = selection['language'].split(', ')    # languages is a many to many field
                    for lang in langs:
                        highlight = self.window.language_list.findItems(lang, QtCore.Qt.MatchExactly)
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
            elif key in ['media_type', 'country']:
                self.vars[key].setCurrentIndex(self.vars[key].findText(selection[key], QtCore.Qt.MatchExactly))
            elif key in ['genres', 'actors', 'tags']:
                transfer = selection[key].split(', ')
                field_no = key + '_no_list'
                field_yes = key + '_yes_list'
                for val in transfer:
                    if val:
                        take = self.vars[field_no].findItems(val, QtCore.Qt.MatchExactly)
                        place = self.vars[field_no].takeItem(self.vars[field_no].row(take[0]))
                        self.vars[field_yes].addItem(place)

        # display
        self.window.title.setFocus()
        self.EditWindow.show()



    def hide(self):
        # clears all the fields then hides the window
        self.clear()
        self.EditWindow.hide()



    def list_transfer(self, source):
        # when a user double clicks an item in a mtm list view, transfer it to the other list
        selected = source.takeItem(source.currentRow()) # the item to be transferred
        src_name = source.objectName() # name of the list field
        if 'yes' in src_name: # converts the name. ex: genres_yes_list ---> genres_no_list and vice versa
            src_name = src_name.replace('yes', 'no')
        else:
            src_name = src_name.replace('no', 'yes')
        self.vars[src_name].addItem(selected) # add the item to the opposite list



    def list_filter(self, source, text):
        # filters through a list based on what is typed in the textbox
        src_name = source.objectName() + '_list'
        field = self.vars[src_name]
        contents = [field.item(index).text() for index in range(field.count())]
        for item in contents:
            if text.lower() in item.lower():
                field.findItems(item, QtCore.Qt.MatchExactly)[0].setHidden(False)
            else:
                field.findItems(item, QtCore.Qt.MatchExactly)[0].setHidden(True)



    def get_dict(self) -> dict:
        # returns a dict representing the fields in the window
        data = {
            'title': self.window.title.displayText(),
            'alt_title': self.window.alt_title.displayText(),
            'series': self.window.series_list.currentItem().text() if self.window.series_list.currentItem() else None,
            'order': float(self.window.order.displayText()) if self.window.order.displayText() else None,
            'media_type': self.window.media_type.currentText(),
            'animated': self.window.animated_yes.isChecked(),
            'country': self.window.country.currentText(),
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