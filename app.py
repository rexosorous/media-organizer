# modules not created by me
from PyQt5 import QtWidgets
from sys import exit

# windows
import windows.main as main
import windows.edit as edit
import windows.batch_edit as batch_edit
import windows.create_delete as create_delete

# toher modules crreated by me
import db_handler as db
import utilities as util



''' TODO
    MOST IMPORTANT TODO: NAME IT MOEHUNTER
    handle new entries
    pressing tab and shift-tab moves cursor to next area (select each radio button)
    scan for deleted media
    settings to allow which columns are shown
    configs
    reformat code so that windows.py files don't import db_handler?
    confirmation messages?
'''


class GUI:
    def __init__(self):
        self.app = QtWidgets.QApplication([])

        # create all the windows
        self.main = main.Main()
        self.edit = edit.Edit()
        self.batch_edit = batch_edit.BatchEdit()
        self.create_delete = create_delete.CreateDelete()

        self.rows = []

        self.connect_events()

        self.main.MainWindow.show()
        exit(self.app.exec_())



    def edit_show(self):
        # based on how many rows are selected, decides whether to show the edit or batch edit window
        self.rows = self.main.selected_rows()
        if len(self.rows) > 1:
            self.batch_edit.show()
        else:
            self.edit.show(self.main.get_table_selection())



    def submit_edit(self):
        # edits database entry based on edit window data
        try:
            data = self.edit.get_dict()
            old_path = util.to_path(db.get_dict(self.edit.title)['media_type'], self.edit.title)
            new_path = util.to_path(data['media_type'], data['title'])
            if old_path != new_path:
                util.move(old_path, new_path) # move and/or rename folder if needed
            db.update(self.edit.title, data)
            self.main.update(self.rows, db.get_dict(data['title']))
            self.edit.hide()
        except ValueError:
            # HIGHLIGHT INCORRECT FIELDS
            print('order and year need to be numbers')



    def set_batch_edit(self):
        # sets database fields to that value if it's a foreignkeyfield
        # adds values to database fields if it's a manytomanyfield
        data = self.batch_edit.get_dict()
        for row in self.rows:
            if 'media_type' in data.keys(): # determine if we need to move the files
                if data['media_type'] and data['media_type'] != '': # make sure data['media_type'] isn't blank
                    title = self.main.get_media_title(row)
                    old_path = util.to_path(db.get_dict(title)['media_type'], title)
                    new_path = util.to_path(data['media_type'], title)
                    util.move(old_path, new_path) # move folder if needed
            db.update_set(self.main.get_media_title(row), data)
            self.main.update([row], db.get_dict(self.main.get_media_title(row)))
        self.batch_edit.hide()



    def remove_batch_edit(self):
        # removes values from database fields
        data = self.batch_edit.get_dict()
        fixed_data = {}
        for key in data:
            if key not in ['media_type', 'animated', 'country', 'subtitles']: # can't remove required fields
                fixed_data[key] = data[key] # done this way because deleting dictionary entries during a loop causes a runtime error
        for row in self.rows:
            db.update_remove(self.main.get_media_title(row), fixed_data)
            self.main.update([row], db.get_dict(self.main.get_media_title(row)))
        self.batch_edit.hide()



    def delete_entry(self):
        # deletes database field entries based on create_delete window data
        data = self.create_delete.get_delete_data()
        for key in data:
            for entry in data[key]:
                db.delete_field(key, entry)
        self.main.clear_table() # we don't know which media entries were effected, so we recreate the table entirely
        self.main.populate_table() # we could know which entries were effected, but this way is faster
        self.create_delete.hide()



    def connect_events(self):
        # connects all the events to functions
        # note: we only connect events here that require access to classes outside of the source.

        # from main window
        self.main.window.edit_button.clicked.connect(self.edit_show) # shows edit or batch edit window
        self.main.window.create_delete_button.triggered.connect(self.create_delete.show) # shows create and delete window

        # from edit window
        self.edit.window.submit.clicked.connect(self.submit_edit) # submit button in edit window

        # from batch edit window
        self.batch_edit.window.set.clicked.connect(self.set_batch_edit) # set button in batch edit window
        self.batch_edit.window.remove.clicked.connect(self.remove_batch_edit) # remove button in batch edit window

        # from create and dlete window
        self.create_delete.window.submit_delete.clicked.connect(self.delete_entry) # submit button in create and delete window







if __name__ == "__main__":
    GUI()