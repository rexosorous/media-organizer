from PyQt5.QtWidgets import QDialog
from functools import partial
import db_handler as db
import ui.create_delete_ui as create_delete_ui
from windows.base import Base



class CreateDelete(Base):
    def __init__(self):
        super().__init__()
        self.CreateDeleteWindow = QDialog()
        self.window = create_delete_ui.Ui_create_delete_window()
        self.window.setupUi(self.CreateDeleteWindow)
        self.vars = vars(self.window)

        # all fields in their "general" form
        self.fields = ['genres', 'tags', 'actors', 'series', 'director', 'studio', 'media_type', 'country', 'language']

        self.connect_events()



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



    def connect_events(self):
        self.window.submit_create.clicked.connect(self.create_entry)
        for field in self.fields:
            for yes_no in ['_yes', '_no']:
                fixed_field = field + yes_no
                self.vars[fixed_field].textChanged.connect(partial(self.list_filter, self.vars[fixed_field]))
                self.vars[fixed_field].returnPressed.connect(partial(self.select_top, self.vars[fixed_field]))
                fixed_field = fixed_field + '_list'
                self.vars[fixed_field].doubleClicked.connect(partial(self.list_transfer, self.vars[fixed_field]))



    def show(self):
        # populates the edit screen's fields with what is selected in main table
        self.clear()
        self.populate()
        self.CreateDeleteWindow.exec_()



    def hide(self):
        # clears all the fields then hides the window
        self.clear()
        self.CreateDeleteWindow.done(0)



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



    def create_entry(self):
        # adds database field entries based on create_delete window data
        data = self.get_create_data()
        for key in data:
            data[key] = data[key].split('\n')
            for entry in data[key]:
                if entry != '':
                    db.create(key, entry)
        self.hide()