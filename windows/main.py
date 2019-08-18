from PyQt5 import QtWidgets
import ui.main_ui as main_ui
import db_handler as db


TABLE_FIELDS = ['title', 'alt_title', 'series', 'order', 'media_type', 'animated', 'country', 'language', 'subtitles', 'year', 'genres', 'director', 'studio', 'actors', 'plot', 'rating', 'tags', 'notes']
TABLE_COL = 18


class Main():
    def __init__(self, app):
        self.MainWindow = QtWidgets.QMainWindow()
        self.window = main_ui.Ui_main_window()
        self.window.setupUi(self.MainWindow)

        self.populate_table()
        self.resize_columns()



    def resize_columns(self):
        self.window.table.setColumnWidth(0, 300)     # title
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
            if not entry['order']: # if these checks are skipped, 'None' appears in the table
                entry['order'] = ''
            if not entry['year']:
                entry['year'] = ''
            if not entry['rating']:
                entry['rating'] = ''

            self.window.table.insertRow(row)
            self.window.table.setItem(row, 0, QtWidgets.QTableWidgetItem(entry['title']))                  # required
            self.window.table.setItem(row, 1, QtWidgets.QTableWidgetItem(entry['alt_title']))
            self.window.table.setItem(row, 2, QtWidgets.QTableWidgetItem(entry['series']))
            self.window.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(entry['order'])))
            self.window.table.setItem(row, 4, QtWidgets.QTableWidgetItem(entry['media_type']))             # required
            self.window.table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(entry['animated'])))          # requried
            self.window.table.setItem(row, 6, QtWidgets.QTableWidgetItem(entry['country']))                # required
            self.window.table.setItem(row, 7, QtWidgets.QTableWidgetItem(', '.join(entry['language'])))
            self.window.table.setItem(row, 8, QtWidgets.QTableWidgetItem(str(entry['subtitles'])))         # required
            self.window.table.setItem(row, 9, QtWidgets.QTableWidgetItem(str(entry['year'])))
            self.window.table.setItem(row, 10, QtWidgets.QTableWidgetItem(', '.join(entry['genres'])))
            self.window.table.setItem(row, 11, QtWidgets.QTableWidgetItem(entry['director']))
            self.window.table.setItem(row, 12, QtWidgets.QTableWidgetItem(entry['studio']))
            self.window.table.setItem(row, 13, QtWidgets.QTableWidgetItem(', '.join(entry['actors'])))
            self.window.table.setItem(row, 14, QtWidgets.QTableWidgetItem(entry['plot']))
            self.window.table.setItem(row, 15, QtWidgets.QTableWidgetItem(str(entry['rating'])))
            self.window.table.setItem(row, 16, QtWidgets.QTableWidgetItem(', '.join(entry['tags'])))
            self.window.table.setItem(row, 17, QtWidgets.QTableWidgetItem(entry['notes']))

            row += 1



    def get_table_selection(self) -> dict:
        row = self.window.table.currentRow()
        data = {}
        for index in range(TABLE_COL):
            data[TABLE_FIELDS[index]] = self.window.table.item(row, index).text()
        return data