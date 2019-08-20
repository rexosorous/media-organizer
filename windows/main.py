from PyQt5 import QtWidgets
import ui.main_ui as main_ui
import db_handler as db


TABLE_FIELDS = ['title', 'alt_title', 'series', 'order', 'media_type', 'animated', 'country', 'language', 'subtitles', 'year', 'genres', 'director', 'studio', 'actors', 'plot', 'rating', 'tags', 'notes']
TABLE_COL = 18
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



class Main():
    def __init__(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.window = main_ui.Ui_main_window()
        self.window.setupUi(self.MainWindow)

        self.populate_table()
        self.resize_columns()



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
        row = 0
        for entry in db.get_table():
            self.window.table.insertRow(row)
            for key in entry:
                self.window.table.setItem(row, FIELD_NUM[key], QtWidgets.QTableWidgetItem(self.stringify(entry[key])))
            row += 1



    def clear_table(self):
        count = list(range(self.window.table.rowCount()))
        count.reverse()
        for index in count:
            self.window.table.removeRow(index)



    def update(self, rows: [int], data: dict):
        # updates entries of table at row with data
        for row in rows:
            for key in data:
                self.window.table.item(row, FIELD_NUM[key]).setText(self.stringify(data[key]))



    def get_table_selection(self) -> dict:
        row = self.window.table.currentRow()
        data = {}
        for index in range(TABLE_COL):
            data[TABLE_FIELDS[index]] = self.window.table.item(row, index).text()
        return data



    def stringify(self, data):
        # table only accepts strings, so we convert non-strings datatypes to output to table
        if type(data) is list:
            data = ', '.join(data)
        elif type(data) in [int, float, bool]:
            data = str(data)
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