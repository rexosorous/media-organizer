# superclass of edit, batch_edit, and create_delete
# allows all of the above to have shared functions between them

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from functools import partial
import db_handler as db



class BaseEdit:
    def __init__(self):
        pass


    def populate(self):
        # adds all the contents for lists

        # list adds
        self.window.series_list.addItems(db.get_all('Series'))
        self.window.director_list.addItems(db.get_all('Directors'))
        self.window.studio_list.addItems(db.get_all('Studios'))
        self.window.language_list.addItems(db.get_all('Languages'))
        self.window.media_type_list.addItems(db.get_all('MediaTypes'))
        self.window.country_list.addItems(db.get_all('Countries'))

        # many to many list adds
        self.window.genres_no_list.addItems(db.get_all('Genres'))
        self.window.tags_no_list.addItems(db.get_all('Tags'))
        self.window.actors_no_list.addItems(db.get_all('Actors'))

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
        self.window.media_type_list.setSortingEnabled(True)
        self.window.country_list.setSortingEnabled(True)



    def clear(self):
        # clears all fields
        for field in self.all_clear_fields:
            self.vars[field].clear()
        for radio in self.all_radio_buttons:
            self.vars[radio].setChecked(False)



    def create_menus(self):
        # creates drop down menus for search bars
        for field in self.all_list_fields:
            qlist = self.vars[field + '_list']
            button = self.vars[field + '_button']
            button.setMenu(QtWidgets.QMenu(button))
            button.menu().addAction(QtWidgets.QAction('Create', button))
            if field in self.with_deselect:
                button.menu().addAction(QtWidgets.QAction('Deselect', button))
            if field in self.with_remove_all:
                button.menu().addAction(QtWidgets.QAction('Remove All', button))
            button.menu().triggered[QtWidgets.QAction].connect(partial(self.filter_menu, qlist))
            button.clicked.connect(partial(self.show_menu, button))



    def connect_events(self):
        for field in self.double_clicks:
            self.vars[field].doubleClicked.connect(partial(self.list_transfer, self.vars[field]))

        for field in self.search_bars:
            self.vars[field].textChanged.connect(partial(self.list_filter, self.vars[field]))
            self.vars[field].returnPressed.connect(partial(self.select_top, self.vars[field]))



    def show_menu(self, source):
        # shows the menus associated with the tool buttons
        source.showMenu()



    def filter_menu(self, field, source):
        # filters which button is pressed in the drop down menu
        if source.text() == 'Create':
            self.create_field(field)
        elif source.text() == 'Deselect':
            self.deselect(field)
        elif source.text() == 'Remove All':
            self.list_transfer_all(field)



    def create_field(self, source):
        # creates a new field entry in db
        obj_name = source.objectName()
        data = self.vars[obj_name.replace('_list', '')].displayText()
        db.create(obj_name[:obj_name.find('_')], data)
        source.addItem(data)



    def deselect(self, source):
        # deselects an item in listwidget
        source.setCurrentRow(-1)



    def list_transfer_all(self, source):
        # transfers all items from the yes side to the no side
        count = list(range(source.count()))
        count.reverse()
        for index in count:
            item = source.takeItem(index)
            destination = source.objectName().replace('yes', 'no')
            self.vars[destination].addItem(item)



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
        field = self.to_list(source)
        contents = [field.item(index).text() for index in range(field.count())]
        for item in contents:
            if text.lower() in item.lower():
                field.findItems(item, QtCore.Qt.MatchExactly)[0].setHidden(False)
            else:
                field.findItems(item, QtCore.Qt.MatchExactly)[0].setHidden(True)



    def select_top(self, source):
        # after pressing enter, selects the topmost item
        src = self.to_list(source)
        for index in range(src.count()):
            if not src.item(index).isHidden():
                src.setCurrentItem(src.item(index))
                if 'yes' in src.objectName() or 'no' in src.objectName():
                    self.list_transfer(src)
                break



    def to_list(self, source):
        # converts a source to its list counterpart
        src_name = source.objectName() + '_list'
        return self.vars[src_name]



    def get_dict(self) -> dict:
        # returns a dict representing the fields in the window
        data = {
            'title': self.window.title.displayText(),
            'alt_title': self.window.alt_title.displayText() if self.window.alt_title.displayText() else None,
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
            'plot': self.window.plot.toPlainText() if self.window.plot.toPlainText() else None,
            'rating': None,
            'tags': ', '.join([self.window.tags_yes_list.item(index).text() for index in range(self.window.tags_yes_list.count())]),
            'notes': self.window.notes.toPlainText() if self.window.notes.toPlainText() else None
        }

        for index in range(1, 6): # rating radio buttons
            if self.vars['rating_' + str(index)].isChecked():
                data['rating'] = index
                break

        return data