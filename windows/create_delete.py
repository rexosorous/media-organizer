from PyQt5 import QtWidgets, QtCore
import db_handler as db
import ui.create_delete_ui as create_delete_ui
from functools import partial



class CreateDelete:
    def __init__(self):
        self.CreateDeleteWindow = QtWidgets.QMainWindow()
        self.window = create_delete_ui.Ui_create_delete_window()
        self.window.setupUi(self.CreateDeleteWindow)
        self.vars = vars(self.window)

        self.fields = ['genres', 'tags', 'actors', 'series', 'director', 'studio', 'media_type', 'country', 'language']


    def populate(self):
        # adds all the contents for lists

        # list adds
        self.window.series_yes_list.addItems(db.get_all('Series'))
        self.window.director_yes_list.addItems(db.get_all('Directors'))
        self.window.studio_yes_list.addItems(db.get_all('Studios'))
        self.window.language_yes_list.addItems(db.get_all('Languages'))
        self.window.media_type_yes_list.addItems(db.get_all('MediaTypes'))
        self.window.country_yes_list.addItems(db.get_all('Countries'))
        self.window.genres_yes_list.addItems(db.get_all('Genres'))
        self.window.tags_yes_list.addItems(db.get_all('Tags'))
        self.window.actors_yes_list.addItems(db.get_all('Actors'))

        # sorting
        self.window.media_type_yes_list.setSortingEnabled(True)
        self.window.media_type_no_list.setSortingEnabled(True)
        self.window.country_yes_list.setSortingEnabled(True)
        self.window.country_no_list.setSortingEnabled(True)
        self.window.series_yes_list.setSortingEnabled(True)
        self.window.series_no_list.setSortingEnabled(True)
        self.window.director_yes_list.setSortingEnabled(True)
        self.window.director_no_list.setSortingEnabled(True)
        self.window.studio_yes_list.setSortingEnabled(True)
        self.window.studio_no_list.setSortingEnabled(True)
        self.window.language_yes_list.setSortingEnabled(True)
        self.window.language_no_list.setSortingEnabled(True)
        self.window.genres_yes_list.setSortingEnabled(True)
        self.window.genres_no_list.setSortingEnabled(True)
        self.window.tags_yes_list.setSortingEnabled(True)
        self.window.tags_no_list.setSortingEnabled(True)
        self.window.actors_yes_list.setSortingEnabled(True)
        self.window.actors_no_list.setSortingEnabled(True)



    def clear(self):
        # clears all the fields in the edit screen
        self.title = None

        for field in self.fields:
            self.vars[field + '_create'].clear()
            for yes_no in ['_yes', '_no']:
                ynfield = field + yes_no
                self.vars[ynfield].clear()
                self.vars[ynfield+'_list'].clear()



    def show(self):
        # populates the edit screen's fields with what is selected in main table
        self.clear()
        self.populate()

        # display
        self.CreateDeleteWindow.show()



    def hide(self):
        # clears all the fields then hides the window
        self.clear()
        self.CreateDeleteWindow.hide()









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



    def get_create_data(self) -> dict:
        # returns all data in create tab
        data = {}
        for field in self.fields:
            fixed_field = field + '_create'
            data[field] = self.vars[fixed_field].toPlainText()
        return data



    def get_delete_data(self) -> dict:
        # returns all data in delete tab
        data = {}
        for field in self.fields:
            data[field] = []
            fixed_field = field + '_no_list'
            count = list(range(self.vars[fixed_field].count()))
            for index in count:
                data[field].append(self.vars[fixed_field].item(index).text())
        return data






    def to_list(self, source):
        # converts a source to its list counterpart
        src_name = source.objectName() + '_list'
        return self.vars[src_name]