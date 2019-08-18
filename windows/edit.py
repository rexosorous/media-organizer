from PyQt5 import QtWidgets, QtCore
import ui.edit_ui as edit_ui



class Edit():
    def __init__(self, app):
        self.EditWindow = QtWidgets.QMainWindow()
        self.window = edit_ui.Ui_edit_window()
        self.window.setupUi(self.EditWindow)
        self.vars = globals()


    def populate(self):
        # adds all the contents for lists and combo boxes

        # list adds
        self.window.series_list.addItems(db.get_all('Series'))
        self.window.director_list.addItems(db.get_all('Directors'))
        self.window.studio_list.addItems(db.get_all('Studios'))
        self.window.language_list.addItems(db.get_all('Languages'))

        # many to many list adds
        self.window.genres_no_list.addItems(db.get_all('Genres'))
        self.window.tags_no_list.addItems(db.get_all('Tags'))
        self.window.actors_no_list.addItems(db.get_all('Actors'))

        # combo box adds
        # TO DO: sort before adding
        self.window.media_type.addItems(db.get_all('MediaTypes'))
        self.window.country.addItems(db.get_all('Countries'))


        # sorting
        self.window.series_list.setSortingEnabled(True)
        self.window.director_list.setSortingEnabled(True)
        self.window.studio_list.setSortingEnabled(True)
        self.window.language_list.setSortingEnabled(True)
        self.window.genres_yes_list.setSortingEnabled(True)
        self.window.genres_no_list.setSortingEnabled(True)
        self.window.tags_yes_list.setSortingEnabled(True)
        self.window.tags_no_list.setSortingEnabled(True)
        self.window.actors_yes_list.setSortingEnabled(True)
        self.window.actors_no_list.setSortingEnabled(True)



    def clear(self):
        # clears all the fields in the edit screen
        # basic
        self.window.title.clear()
        self.window.alt_title.clear()
        self.window.order.clear()
        self.window.year.clear()
        self.window.plot.clear()
        self.window.notes.clear()
        self.window.media_type.clear()
        self.window.country.clear()

        # lists
        self.window.series.clear()
        self.window.series_list.clear()
        self.window.director.clear()
        self.window.director_list.clear()
        self.window.studio.clear()
        self.window.studio_list.clear()
        self.window.language.clear()
        self.window.language_list.clear()

        # mtm lists
        self.window.genres_yes.clear()
        self.window.genres_yes_list.clear()
        self.window.genres_no.clear()
        self.window.genres_no_list.clear()
        self.window.tags_yes.clear()
        self.window.tags_yes_list.clear()
        self.window.tags_no.clear()
        self.window.tags_no_list.clear()
        self.window.actors_yes.clear()
        self.window.actors_yes_list.clear()
        self.window.actors_no.clear()
        self.window.actors_no_list.clear()

        # radio buttons
        self.window.rating_1.setChecked(False)
        self.window.rating_2.setChecked(False)
        self.window.rating_3.setChecked(False)
        self.window.rating_4.setChecked(False)
        self.window.rating_5.setChecked(False)
        self.window.rating_none.setChecked(False)
        self.window.animated_yes.setChecked(False)
        self.window.animated_no.setChecked(False)
        self.window.subtitles_yes.setChecked(False)
        self.window.subtitles_no.setChecked(False)



    def show(self, selection: dict):
        # populates the edit screen's fields with what is selected in main table
        self.clear()
        self.populate_edit()

        for key in selection:
            if key in ['title', 'alt_title', 'order', 'year', 'plot', 'notes']: # text fields
                self.vars[key].setText(selection[key])
            elif key in ['series', 'director', 'studio']: # lists
                field = key + '_list'
                highlight = self.vars[field].findItems(selection[key], QtCore.Qt.MatchExactly)
                if len(highlight) == 1:
                    self.vars[field].setCurrentItem(highlight[0])
            elif key == 'language': # multi select lists
                langs = self.selection['language'].split(', ')    # languages is a many to many field
                for lang in langs:
                    highlight = self.window.language_list.findItems(lang, QtCore.Qt.MatchExactly)
                    highlight[0].setSelected(True)
            elif key == 'rating':
                try:
                    field = 'rating_' + selection['rating']
                    self.vars[field].setChecked(True)
                except AttributeError:
                    self.window.rating_none.setChecked(True)
            elif key in ['animated, subtitles']:
                field = key + '_no'
                if selection[key] == 'True':
                    field = key + '_yes'
                vars[field].setChecked(True)
            elif key in ['media_type', 'country']:
                vars[key].setCurrentIndex(vars[key].findText(selection[key], QtCore.Qt.MatchExactly))
            elif key in ['genres', 'actors', 'tags']:
                transfer = self.main.main_table.item(row, 10).text().split(', ')
                for val in transfer:
                    if val:
                        take = self.window.genres_no_list.findItems(val, QtCore.Qt.MatchExactly)
                        place = self.window.genres_no_list.takeItem(self.window.genres_no_list.row(take[0]))
                        self.window.genres_yes_list.addItem(place)


        # basic
        # self.window.title.setText(self.main.main_table.item(row, 0).text())
        # self.window.alt_title.setText(self.main.main_table.item(row, 1).text())
        # self.window.order.setText(self.main.main_table.item(row, 3).text())
        # self.window.year.setText(self.main.main_table.item(row, 9).text())
        # self.window.plot.setText(self.main.main_table.item(row, 14).text())
        # self.window.notes.setText(self.main.main_table.item(row, 17).text())


        # lists
        # highlight = self.window.series_list.findItems(self.main.main_table.item(row, 2).text(), QtCore.Qt.MatchExactly)
        # if len(highlight) == 1:
        #     self.window.series_list.setCurrentItem(highlight[0])

        # highlight = self.window.director_list.findItems(self.main.main_table.item(row, 11).text(), QtCore.Qt.MatchExactly)
        # if len(highlight) == 1:
        #     self.window.director_list.setCurrentItem(highlight[0])

        # highlight = self.window.studio_list.findItems(self.main.main_table.item(row, 12).text(), QtCore.Qt.MatchExactly)
        # if len(highlight) == 1:
        #     self.window.studio_list.setCurrentItem(highlight[0])

        # langs = self.main.main_table.item(row, 7).text().split(', ')    # languages is a many to many field
        # for lang in langs:
        #     highlight = self.window.language_list.findItems(lang, QtCore.Qt.MatchExactly)
        #     highlight[0].setSelected(True)


        # radio buttons
        # try:
        #     rating = int(self.main.main_table.item(row, 15).text())
        #     if rating == 1:
        #         self.window.rating_1.setChecked(True)
        #     elif rating == 2:
        #         self.window.rating_2.setChecked(True)
        #     elif rating == 3:
        #         self.window.rating_3.setChecked(True)
        #     elif rating == 4:
        #         self.window.rating_4.setChecked(True)
        #     elif rating == 5:
        #         self.window.rating_5.setChecked(True)
        # except:
        #     self.window.rating_none.setChecked(True)

        # if self.main.main_table.item(row, 5).text() == 'True':
        #     self.window.animated_yes.setChecked(True)
        # else:
        #     self.window.animated_no.setChecked(True)

        # if self.main.main_table.item(row, 8).text() == 'True':
        #     self.window.subtitles_yes.setChecked(True)
        # else:
        #     self.window.subtitles_no.setChecked(True)


        # combo box
        # self.window.media_type.setCurrentIndex(self.window.media_type.findText(self.main.main_table.item(row, 4).text(), QtCore.Qt.MatchExactly))
        # self.window.country.setCurrentIndex(self.window.country.findText(self.main.main_table.item(row, 6).text(), QtCore.Qt.MatchExactly))


        # many to many fields
        # transfer = self.main.main_table.item(row, 10).text().split(', ')
        # for val in transfer:
        #     if val:
        #         take = self.window.genres_no_list.findItems(val, QtCore.Qt.MatchExactly)
        #         place = self.window.genres_no_list.takeItem(self.window.genres_no_list.row(take[0]))
        #         self.window.genres_yes_list.addItem(place)

        # transfer = self.main.main_table.item(row, 13).text().split(', ')
        # for val in transfer:
        #     if val:
        #         take = self.window.actors_no_list.findItems(val, QtCore.Qt.MatchExactly)
        #         place = self.window.actors_no_list.takeItem(self.window.actors_no_list.row(take[0]))
        #         self.window.actors_yes_list.addItem(place)

        # transfer = self.main.main_table.item(row, 16).text().split(', ')
        # for val in transfer:
        #     if val:
        #         take = self.window.tags_no_list.findItems(val, QtCore.Qt.MatchExactly)
        #         place = self.window.tags_no_list.takeItem(self.window.tags_no_list.row(take[0]))
        #         self.window.tags_yes_list.addItem(place)


        # display
        self.window.title.setFocus()
        self.EditWindow.show()





    def list_transfer(self, source):
        # when a user double clicks an item in a mtm list view, transfer it to the other list
        selected = source.takeItem(source.currentRow()) # the item to be transferred
        src_name = source.objectName() # name of the list field
        if 'yes' in src_name: # converts the name. ex: genres_yes_list ---> genres_no_list and vice versa
            src_name = src_name.replace('yes', 'no')
        else:
            src_name = src_name.replace('no', 'yes')
        vars(self.edit)[src_name].addItem(selected) # add the item to the opposite list



    def list_filter(self, source, text):
        # filters through a list based on what is typed in the textbox
        src_name = source.objectName() + '_list'
        field = vars(self.edit)[src_name]
        contents = [field.item(index).text() for index in range(field.count())]
        for item in contents:
            if text.lower() in item.lower():
                field.findItems(item, QtCore.Qt.MatchExactly)[0].setHidden(False)
            else:
                field.findItems(item, QtCore.Qt.MatchExactly)[0].setHidden(True)