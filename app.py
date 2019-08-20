from PyQt5 import QtWidgets
import windows.main as main
import windows.edit as edit
import db_handler as db
from functools import partial
import sys


''' TODO
    allow adding of non-media entries (in its own window)
    batch editing
    when changing media type, move file using shutil (can use relative directories)
    double clicking opens file or location (set as config)
    handle new entries
    scan for deleted media
    settings to allow which columns are shown
    configs
'''


class GUI:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        self.main = main.Main()
        self.edit = edit.Edit()

        self.rows = []

        self.connect_events()

        self.main.MainWindow.show()
        sys.exit(self.app.exec_())



    def edit_show(self):
        # populates the edit window and then shows it
        self.rows = self.main.selected_rows()
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


    def connect_events(self):
        # connects all the events to functions
        # note: partial() allows us to send the source of the event

        # buttons
        self.main.window.edit_button.clicked.connect(self.edit_show)
        self.edit.window.submit.clicked.connect(self.submit_edit)

        # list double clicks
        self.edit.window.genres_yes_list.doubleClicked.connect(partial(self.edit.list_transfer, self.edit.window.genres_yes_list))
        self.edit.window.genres_no_list.doubleClicked.connect(partial(self.edit.list_transfer, self.edit.window.genres_no_list))
        self.edit.window.actors_yes_list.doubleClicked.connect(partial(self.edit.list_transfer, self.edit.window.actors_yes_list))
        self.edit.window.actors_no_list.doubleClicked.connect(partial(self.edit.list_transfer, self.edit.window.actors_no_list))
        self.edit.window.tags_yes_list.doubleClicked.connect(partial(self.edit.list_transfer, self.edit.window.tags_yes_list))
        self.edit.window.tags_no_list.doubleClicked.connect(partial(self.edit.list_transfer, self.edit.window.tags_no_list))

        search_bars = ['genres_yes', 'genres_no', 'tags_yes', 'tags_no', 'series', 'actors_yes', 'actors_no', 'media_type', 'studio', 'director', 'country', 'language']
        for field in search_bars:
            self.edit.vars[field].textChanged.connect(partial(self.edit.list_filter, self.edit.vars[field]))
            self.edit.vars[field].returnPressed.connect(partial(self.edit.select_top, self.edit.vars[field]))



if __name__ == "__main__":
    GUI()