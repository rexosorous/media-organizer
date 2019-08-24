from PyQt5 import QtWidgets
import ui.main_ui as main_ui
import db_handler as db
import utilities as util
import config as cfg


TABLE_FIELDS = ['title', 'alt_title', 'series', 'order', 'media_type', 'animated', 'country', 'language', 'subtitles', 'year', 'genres', 'director', 'studio', 'actors', 'plot', 'rating', 'tags', 'notes']
FIELD_NUM = {
    'title': 0,
    'alt_title': 1,
    'series': 2,
    'order': 3,
    'media_type': 4,
    'animated': 5,
    'country': 6,
    'language': 7,
    'subtitles': 8,
    'year': 9,
    'genres': 10,
    'director': 11,
    'studio': 12,
    'actors': 13,
    'plot': 14,
    'rating': 15,
    'tags': 16,
    'notes': 17
}



class Main:
    def __init__(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.window = main_ui.Ui_main_window()
        self.window.setupUi(self.MainWindow)

        self.populate_table()
        self.resize_columns()
        self.create_menus()
        self.connect_events()



    def create_menus(self):
        self.window.table.addAction(self.window.edit_action)
        self.window.table.addAction(self.window.delete_action)
        self.window.table.addAction(self.window.clear_filter_action)



    def connect_events(self):
        self.window.search_bar.textChanged.connect(self.search_table)

        # table related
        self.window.table.cellDoubleClicked.connect(self.find_media) # opens a file's location when you double click an entry
        self.window.delete_action.triggered.connect(self.delete) # deletes selected media
        self.window.clear_filter_action.triggered.connect(self.refresh_table) # clears any filters that may apply

        # top-bar menus
        self.window.set_directory_button.triggered.connect(self.set_directory) # opens file explorer if you wanted to change the file directory
        self.window.backup_button.triggered.connect(self.backup_database)
        self.window.load_button.triggered.connect(self.load_database)
        self.window.refresh_button.triggered.connect(self.refresh_table) # refreshes the table



    def resize_columns(self):
        self.window.table.setColumnWidth(0, 200)     # title
        self.window.table.setColumnWidth(1, 200)     # alt title
        self.window.table.setColumnWidth(2, 200)     # series
        self.window.table.setColumnWidth(3, 25)      # order
        self.window.table.setColumnWidth(4, 75)      # media type
        self.window.table.setColumnWidth(5, 100)     # animated
        self.window.table.setColumnWidth(6, 100)     # country
        self.window.table.setColumnWidth(7, 100)     # language
        self.window.table.setColumnWidth(8, 100)     # subtitles
        self.window.table.setColumnWidth(9, 25)      # year
        self.window.table.setColumnWidth(10, 100)    # genres
        self.window.table.setColumnWidth(11, 100)    # director
        self.window.table.setColumnWidth(12, 100)    # studio
        self.window.table.setColumnWidth(13, 100)    # actors
        self.window.table.setColumnWidth(14, 200)    # plot
        self.window.table.setColumnWidth(15, 25)     # rating
        self.window.table.setColumnWidth(16, 100)    # tags
        self.window.table.setColumnWidth(17, 200)    # notes



    def populate_table(self):
        self.window.table.setSortingEnabled(False)
        row = 0
        for entry in db.get_table():
            self.window.table.insertRow(row)
            for key in entry:
                self.window.table.setItem(row, FIELD_NUM[key], QtWidgets.QTableWidgetItem(util.stringify(entry[key])))
            row += 1
        self.window.table.setSortingEnabled(True)



    def clear_table(self):
        self.window.search_bar.clear()
        count = list(range(self.window.table.rowCount()))
        count.reverse() # if we don't reverse and start deleting at 0, then everything gets shifted down a position during runtime
        for index in count:
            self.window.table.removeRow(index)



    def filter_table(self, data):
        # populates the filter with data instead of with db
        self.window.table.setSortingEnabled(False)
        row = 0
        for entry in data:
            self.window.table.insertRow(row)
            for key in entry:
                self.window.table.setItem(row, FIELD_NUM[key], QtWidgets.QTableWidgetItem(util.stringify(entry[key])))
            row += 1
        self.window.table.setSortingEnabled(True)



    def search_table(self):
        # narrows down table with what is in search bar
        contents = [[self.window.table.item(row, 0).text(), self.window.table.item(row, 1).text()] for row in range(self.window.table.rowCount())]
        for index in range(len(contents)):
            search = self.window.search_bar.displayText().lower()
            if search in contents[index][0].lower() or search in contents[index][1].lower():
                self.window.table.setRowHidden(index, False)
            else:
                self.window.table.setRowHidden(index, True)



    def refresh_table(self):
        self.clear_table()
        self.populate_table()



    def update(self, rows: [int], data: dict):
        # updates table entries
        # make sure data is from database!!
        for row in rows:
            for key in data:
                self.window.table.item(row, FIELD_NUM[key]).setText(util.stringify(data[key]))



    def get_table_selection(self) -> dict:
        # returns a dictionary with all the data of the selected entry
        row = self.window.table.currentRow()
        data = {}
        for index in range(len(TABLE_FIELDS)):
            data[TABLE_FIELDS[index]] = self.window.table.item(row, index).text()
        return data



    def selected_rows(self) -> [int]:
        # returns a list of all rows highlighted/selected
        rows = []
        ranges = [list(range(x.topRow(), x.bottomRow()+1)) for x in self.window.table.selectedRanges()]
        for group in ranges:
            rows += group
        return rows



    def get_media_title(self, index: int) -> str:
        # returns the title of the entry at row int
        return self.window.table.item(index, 0).text()



    def set_directory(self):
        # opens file explorer if you wanted to change the file directory
        options = QtWidgets.QFileDialog.Options()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self.MainWindow, "Set Directory", options=options)
        if directory:
            cfg.directory = directory
            self.scan()



    def find_media(self):
        # opens a file's location when you double click an entry
        data = self.get_table_selection()
        path = util.to_path(data['media_type'], data['title'])
        util.open_file(path)



    def delete(self):
        # deletes an entry or entries from the table, database, and hdd
        selected = self.selected_rows()
        titles = [self.window.table.item(row, 0).text() for row in selected]

        pop_up = QtWidgets.QMessageBox() # we want to confirm that the user wants to delete those entries
        pop_up.setWindowTitle('Confirm')
        pop_up.setText('Are you sure you want to delete the selected media\nfrom both the database and your local storage?')
        pop_up.setInformativeText('Click "Show Details" below to see what\n you\'re trying to delete')
        pop_up.setDetailedText('\n'.join(titles))
        pop_up.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        pop_up.exec_()

        if pop_up.clickedButton().text() == '&Yes':
            db.delete_media(titles)
            media_types = [self.window.table.item(row, 4).text() for row in selected]
            for index in range(len(titles)):
                util.recycle(media_types[index], titles[index])
            selected.reverse()
            for row in selected:
                self.window.table.removeRow(row)



    def backup_database(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self.MainWindow, "Backup Database", "database", "Database Files (*.db)", options=options)
        util.copy_database(filename)



    def load_database(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow, "Load Database", "database", "Database Files (*.db)", options=options)
        print('loading database not implemented yet')
        # db.load_database(filename)