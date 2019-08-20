from PyQt5 import QtWidgets
import windows.main as main
import windows.edit as edit
import windows.batch_edit as batch_edit
import windows.create_delete as create_delete
import db_handler as db
from functools import partial
import sys


''' TODO
    MOST IMPORTANT TODO: NAME IT MOEHUNTER
    find a better way to handle repeated code in edit, batch_edit, and create_delete
    when changing media type, move file using shutil (can use relative directories)
    double clicking opens file or location (set as config)
    handle new entries
    pressing tab and shift-tab moves cursor to next area (select each radio button)
    scan for deleted media
    settings to allow which columns are shown
    configs
    reformat code so that windows.py files don't import db_handler
    confirmation messages?
'''


class GUI:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        self.main = main.Main()
        self.edit = edit.Edit()
        self.batch_edit = batch_edit.BatchEdit()
        self.create_delete = create_delete.CreateDelete()

        self.rows = []

        self.connect_events()

        self.main.MainWindow.show()
        sys.exit(self.app.exec_())



    def edit_show(self):
        # populates the edit window and then shows it
        self.rows = self.main.selected_rows()
        if len(self.rows) > 1:
            self.batch_edit.show()
        else:
            self.edit.show(self.main.get_table_selection())



    def submit_edit(self):
        # edits database entry based on edit window data
        try:
            data = self.edit.get_dict()
            db.update(self.edit.title, data)
            self.main.update(self.rows, db.get_dict(data['title']))
            self.edit.hide()
        except ValueError:
            # HIGHLIGHT INCORRECT FIELDS
            print('order and year need to be numbers')



    def create_entry(self):
        # adds database entries based on create_delete window data
        data = self.create_delete.get_create_data()
        for key in data:
            data[key] = data[key].split('\n')
            for entry in data[key]:
                if entry != '':
                    db.create(key, entry)
        self.create_delete.hide()



    def delete_entry(self):
        # deletes database entries based on create_delete window data
        data = self.create_delete.get_delete_data()
        for key in data:
            for entry in data[key]:
                db.delete_field(key, entry)
        self.main.clear_table()
        self.main.populate_table()
        self.create_delete.hide()



    def set_batch_edit(self):
        data = self.batch_edit.get_dict()
        for row in self.rows:
            db.update_set(self.main.get_media_title(row), data)
            self.main.update([row], db.get_dict(self.main.get_media_title(row)))
        self.batch_edit.hide()



    def remove_batch_edit(self):
        data = self.batch_edit.get_dict()
        fixed_data = {}
        for key in data:
            if key not in ['media_type', 'animated', 'country', 'subtitles']:
                fixed_data[key] = data[key]
        for row in self.rows:
            db.update_remove(self.main.get_media_title(row), fixed_data)
            self.main.update([row], db.get_dict(self.main.get_media_title(row)))
        self.batch_edit.hide()



    def connect_events(self):
        # connects all the events to functions
        # note: partial() allows us to send the source of the event

        # buttons
        self.main.window.edit_button.clicked.connect(self.edit_show)
        self.main.window.create_delete_button.triggered.connect(self.create_delete.show)
        self.edit.window.submit.clicked.connect(self.submit_edit)
        self.batch_edit.window.set.clicked.connect(self.set_batch_edit)
        self.batch_edit.window.remove.clicked.connect(self.remove_batch_edit)
        self.create_delete.window.submit_create.clicked.connect(self.create_entry)
        self.create_delete.window.submit_delete.clicked.connect(self.delete_entry)

        # list double clicks
        edit_double_clicks = ['genres_yes_list', 'genres_no_list', 'actors_yes_list', 'actors_no_list', 'tags_yes_list', 'tags_no_list']
        for field in edit_double_clicks:
            self.edit.vars[field].doubleClicked.connect(partial(self.edit.list_transfer, self.edit.vars[field]))
            self.batch_edit.vars[field].doubleClicked.connect(partial(self.batch_edit.list_transfer, self.batch_edit.vars[field]))

        # search bars
        edit_search_bars = ['genres_yes', 'genres_no', 'tags_yes', 'tags_no', 'series', 'actors_yes', 'actors_no', 'media_type', 'studio', 'director', 'country', 'language']
        for field in edit_search_bars:
            self.edit.vars[field].textChanged.connect(partial(self.edit.list_filter, self.edit.vars[field]))
            self.edit.vars[field].returnPressed.connect(partial(self.edit.select_top, self.edit.vars[field]))
            self.batch_edit.vars[field].textChanged.connect(partial(self.batch_edit.list_filter, self.batch_edit.vars[field]))
            self.batch_edit.vars[field].returnPressed.connect(partial(self.batch_edit.select_top, self.batch_edit.vars[field]))

        # delete fields
        delete_fields = ['series', 'director', 'studio', 'language', 'media_type', 'country', 'genres', 'tags', 'actors']
        for field in delete_fields:
            for yes_no in ['_yes', '_no']:
                fixed_field = field + yes_no
                self.create_delete.vars[fixed_field].textChanged.connect(partial(self.create_delete.list_filter, self.create_delete.vars[fixed_field]))
                self.create_delete.vars[fixed_field].returnPressed.connect(partial(self.create_delete.select_top, self.create_delete.vars[fixed_field]))
                fixed_field = fixed_field + '_list'
                self.create_delete.vars[fixed_field].doubleClicked.connect(partial(self.create_delete.list_transfer, self.create_delete.vars[fixed_field]))



if __name__ == "__main__":
    GUI()