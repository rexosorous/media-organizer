from PyQt5 import QtWidgets
import windows.main as main
import windows.edit as edit
import windows.batch_edit as batch_edit
import windows.create_delete as create_delete
import db_handler as db
import config as cfg
from functools import partial
from sys import exit
import utilities as util
import os


''' TODO
    MOST IMPORTANT TODO: NAME IT MOEHUNTER
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
        self.app = QtWidgets.QApplication([])

        self.main = main.Main()
        self.edit = edit.Edit()
        self.batch_edit = batch_edit.BatchEdit()
        self.create_delete = create_delete.CreateDelete()

        self.rows = []

        self.connect_events()

        self.main.MainWindow.show()
        exit(self.app.exec_())



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
            old_path = self.to_path(db.get_dict(self.edit.title)['media_type'], self.edit.title)
            new_path = self.to_path(data['media_type'], data['title'])
            if old_path != new_path:
                os.rename(old_path, new_path)
            db.update(self.edit.title, data)
            self.main.update(self.rows, db.get_dict(data['title']))
            self.edit.hide()
        except ValueError:
            # HIGHLIGHT INCORRECT FIELDS
            print('order and year need to be numbers')



    def set_batch_edit(self):
        data = self.batch_edit.get_dict()
        for row in self.rows:
            if 'media_type' in data.keys():
                if data['media_type'] and data['media_type'] != '':
                    title = self.main.get_media_title(row)
                    old_path = self.to_path(db.get_dict(title)['media_type'], title)
                    new_path = self.to_path(data['media_type'], title)
                    os.rename(old_path, new_path)
            db.update_set(self.main.get_media_title(row), data)
            self.main.update([row], db.get_dict(self.main.get_media_title(row)))
        self.batch_edit.hide()



    def remove_batch_edit(self):
        data = self.batch_edit.get_dict()
        fixed_data = {}
        for key in data:
            if key not in ['media_type', 'animated', 'country', 'subtitles']: # required fields
                fixed_data[key] = data[key]
        for row in self.rows:
            db.update_remove(self.main.get_media_title(row), fixed_data)
            self.main.update([row], db.get_dict(self.main.get_media_title(row)))
        self.batch_edit.hide()



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



    def set_directory(self):
        options = QtWidgets.QFileDialog.Options()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self.main.MainWindow, "QtWidgets.QFileDialog.getOpenFileName()", options=options)
        if directory:
            cfg.directory = directory



    def find_media(self):
        data = self.main.get_table_selection()
        path = self.to_path(data['media_type'], data['title'])
        os.startfile(path)



    def to_path(self, media_type: str, filename: str):
        return os.path.realpath(cfg.directory + 'Media' + '\\' + util.to_windows(media_type) + '\\' + util.to_windows(filename))



    def connect_events(self):
        # connects all the events to functions
        # note: partial() allows us to send the source of the event

        # buttons
        self.main.window.edit_button.clicked.connect(self.edit_show)
        self.main.window.set_directory_button.triggered.connect(self.set_directory)
        self.main.window.create_delete_button.triggered.connect(self.create_delete.show)
        self.edit.window.submit.clicked.connect(self.submit_edit)
        self.batch_edit.window.set.clicked.connect(self.set_batch_edit)
        self.batch_edit.window.remove.clicked.connect(self.remove_batch_edit)
        self.create_delete.window.submit_create.clicked.connect(self.create_entry)
        self.create_delete.window.submit_delete.clicked.connect(self.delete_entry)


        self.main.window.table.cellDoubleClicked.connect(self.find_media)




if __name__ == "__main__":
    GUI()