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
    implement imdb and mal scrapers for new entries
    take a look at submit_edit to see if we can input a db entry based on scrapers and edit it from there,
        or if we have to make a new entry when submit is pressed. aka, can we get all required fields from scraping?
        edit: no we can't make an entry based on scrapers because if we can't find it with scrapers,
            then we need to enter everything from scratch and "editing" won't work that way.
    take a good look at db_handler module to see what can be made simpler or better
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



    def connect_events(self):
        # connects all the events to functions
        # note: we only connect events here that require access to classes outside of the source.

        # from main window
        self.main.window.edit_button.clicked.connect(self.edit_show) # shows edit or batch edit window
        self.main.window.create_delete_button.triggered.connect(self.create_delete.show) # shows create and delete window
        self.main.window.scan_button.triggered.connect(self.scan) # scans directory for missing and new files

        # from edit window
        self.edit.window.submit.clicked.connect(self.submit_edit) # submit button in edit window

        # from batch edit window
        self.batch_edit.window.set.clicked.connect(self.set_batch_edit) # set button in batch edit window
        self.batch_edit.window.remove.clicked.connect(self.remove_batch_edit) # remove button in batch edit window

        # from create and dlete window
        self.create_delete.window.submit_delete.clicked.connect(self.delete_entry) # submit button in create and delete window






    # all main based functions
    def edit_show(self):
        # based on how many rows are selected, decides whether to show the edit or batch edit window
        self.rows = self.main.selected_rows()
        if len(self.rows) > 1:
            self.batch_edit.show()
        else:
            self.edit.show(self.main.get_table_selection())



    def scan(self):
        # scans directory for media folders and compares it to the database
        # if there's anything there that isn't in the database, ask to create a new entry
        # if there's anything missing, ask if they want the entries deleted in the database (or backup?)
        local = util.scan(db.get_all('MediaTypes'))
        database = db.get_by_media_type()
        new = {}
        missing = {}

        for media_type in local:
            new_files = [new for new in local[media_type] if new not in database[media_type]]
            missing_files = [missing for missing in database[media_type] if missing not in local[media_type]]

            # check to make sure the lists aren't empty
            if new_files:
                new[media_type] = new_files
            if missing_files:
                missing[media_type] = missing_files

        # make sure to scan the new folder as well
        new_files = util.scan(['New'])
        if new_files:
            new.update(util.scan(['New'])) # util.scan returns a dict, so this is how we merge the keys and values of two dicts

        self.handle_missing(missing)
        self.handle_new(new)



    def handle_missing(self, missing: dict):
        # after scanning the directory, if there's any folders that should be there but aren't,
        # ask the user if they want the entries deleted in the database
        pop_up = QtWidgets.QMessageBox() # we want a dialog box regardless of what happens
        pop_up.setWindowTitle('Missing Files')

        if not missing: # if nothing is missing
            pop_up.setText('No folders are missing.')
            pop_up.setStandardButtons(QtWidgets.QMessageBox.Ok)
            pop_up.exec_()
            return

        # if things are missing
        # create the display text
        missing_list = []
        text =  ''
        for media_type in missing:
            for media in missing[media_type]:
                text += 'In ' + media_type + ': "' + media + '"\n'
                missing_list.append(media)

        pop_up.setText('Files were found missing! Check "Show Details" below to find out which ones.\nWould you like to delete all the database entries?')
        pop_up.setInformativeText('Click yes if you deleted the files or no if you think this program made a mistake.')
        pop_up.setDetailedText(text)
        pop_up.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        pop_up.exec_()

        if pop_up.clickedButton().text() == '&Yes':
            db.delete_media(missing_list)



    def handle_new(self, new: dict):
        # after scanning the directory, if there's any folders that don't appear in our database,
        # ask the user if they want to delete those folders or create a new database entry
        pop_up = QtWidgets.QMessageBox() # we want a dialog box regardless of what happens
        pop_up.setWindowTitle('New Files')

        if not new: # if there are no new files
            pop_up.setText('Did not find any new files.')
            pop_up.setStandardButtons(QtWidgets.QMessageBox.Ok)
            pop_up.exec_()
            return

        # if there are new files
        # create the display text
        text =  ''
        for media_type in new:
            for media in new[media_type]:
                text += 'In ' + media_type + ': "' + media + '"\n'

        pop_up.setText('New files were found! Check "Show Details" below to findout which ones.\nWould you like to create new database entries for them?')
        pop_up.setDetailedText(text)
        pop_up.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        pop_up.exec_()

        if pop_up.clickedButton().text() == '&Yes':
            for media_type in new:
                for media in new[media_type]:
                    if media_type == 'New': # new is not a real media type, so we can't pass it to edit.show()
                        self.edit.show({})
                    else:
                        self.edit.show({'media_type': media_type})






    # all edit based functions
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






    # all batch edit based functions
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






    # all create and delete based functions
    def delete_entry(self):
        # deletes database field entries based on create_delete window data
        data = self.create_delete.get_delete_data()
        for key in data:
            for entry in data[key]:
                db.delete_field(key, entry)
        self.main.refresh()
        self.create_delete.hide()








if __name__ == "__main__":
    GUI()