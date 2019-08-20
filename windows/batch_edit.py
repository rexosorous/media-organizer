from PyQt5 import QtWidgets, QtCore
import db_handler as db
import ui.batch_edit_ui as batch_edit_ui
from functools import partial



class BatchEdit():
    def __init__(self):
        self.BatchEditWindow = QtWidgets.QMainWindow()
        self.window = batch_edit_ui.Ui_batch_edit_window()
        self.window.setupUi(self.BatchEditWindow)
        self.vars = vars(self.window)

        self.create_menus()



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
        # clears all the fields in the edit screen

        # basic
        self.window.order.clear()
        self.window.year.clear()

        # lists
        self.window.series.clear()
        self.window.series_list.clear()
        self.window.director.clear()
        self.window.director_list.clear()
        self.window.studio.clear()
        self.window.studio_list.clear()
        self.window.language.clear()
        self.window.language_list.clear()
        self.window.media_type.clear()
        self.window.media_type_list.clear()
        self.window.country.clear()
        self.window.country_list.clear()

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



    def show(self):
        self.clear()
        self.populate()
        self.BatchEditWindow.show()



    def hide(self):
        # clears all the fields then hides the window
        self.clear()
        self.BatchEditWindow.hide()



    def create_menus(self):
        # creates drop down menus for search bars
        all_list_fields = ['genres_yes', 'genres_no', 'tags_yes', 'tags_no', 'series', 'actors_yes', 'actors_no', 'media_type', 'studio', 'director', 'country', 'language']
        with_deselect = ['series', 'studio', 'director', 'media_type', 'country', 'language']
        with_remove_all = ['genres_yes', 'tags_yes', 'actors_yes']

        for field in all_list_fields:
            qlist = self.vars[field + '_list']
            button = self.vars[field + '_button']
            button.setMenu(QtWidgets.QMenu(button))
            button.menu().addAction(QtWidgets.QAction('Create', button))
            if field in with_deselect:
                button.menu().addAction(QtWidgets.QAction('Deselect', button))
            if field in with_remove_all:
                button.menu().addAction(QtWidgets.QAction('Remove All', button))
            button.menu().triggered[QtWidgets.QAction].connect(partial(self.filter_menu, qlist))
            button.clicked.connect(partial(self.show_menu, button))



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



    def list_transfer(self, source):
        # when a user double clicks an item in a mtm list view, transfer it to the other list
        selected = source.takeItem(source.currentRow()) # the item to be transferred
        src_name = source.objectName() # name of the list field
        if 'yes' in src_name: # converts the name. ex: genres_yes_list ---> genres_no_list and vice versa
            src_name = src_name.replace('yes', 'no')
        else:
            src_name = src_name.replace('no', 'yes')
        self.vars[src_name].addItem(selected) # add the item to the opposite list



    def list_transfer_all(self, source):
        # transfers all items from the yes side to the no side
        count = list(range(source.count()))
        count.reverse()
        for index in count:
            item = source.takeItem(index)
            destination = source.objectName().replace('yes', 'no')
            self.vars[destination].addItem(item)



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

        for index in range(1, 6):
            if self.vars['rating_' + str(index)].isChecked():
                data['rating'] = index
                break

        if self.window.animated_yes.isChecked() and not self.window.animated_no.isChecked():
            data['animated'] = True
        elif self.window.animated_no.isChecked() and not self.window.animated_yes.isChecked():
            data['animated'] = False

        if self.window.subtitles_yes.isChecked() and not self.window.subtitles_no.isChecked():
            data['subtitles'] = True
        elif self.window.subtitles_no.isChecked() and not self.window.subtitles_yes.isChecked():
            data['subtitles'] = False

        fixed_data = {}
        for key in data:
            if data[key] != None and data[key] != '':
                fixed_data[key] = data[key]

        return fixed_data