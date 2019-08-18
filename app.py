from PyQt5 import QtWidgets
import windows.main as main
import windows.edit as edit
from functools import partial
import sys




class GUI:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        self.main = main.Main(self.app)
        self.edit = edit.Edit(self.app)

        self.connect_events()

        self.main.MainWindow.show()
        sys.exit(self.app.exec_())



    def edit_show(self):
        # populates the edit window and then shows it
        x = self.main.get_table_selection()
        for key in x:
            print(f'{key} - {x[key]}')
        # self.edit.show(self.main.get_table_selection())


    def connect_events(self):
        # connects all the events to functions

        # buttons
        self.main.window.edit_button.clicked.connect(self.edit_show)

        # list double clicks
        # note: partial() allows us to send the source of the event
        # self.edit.window.genres_yes_list.doubleClicked.connect(partial(self.list_transfer, self.edit.window.genres_yes_list))
        # self.edit.window.genres_no_list.doubleClicked.connect(partial(self.list_transfer, self.edit.window.genres_no_list))
        # self.edit.window.actors_yes_list.doubleClicked.connect(partial(self.list_transfer, self.edit.window.actors_yes_list))
        # self.edit.window.actors_no_list.doubleClicked.connect(partial(self.list_transfer, self.edit.window.actors_no_list))
        # self.edit.window.tags_yes_list.doubleClicked.connect(partial(self.list_transfer, self.edit.window.tags_yes_list))
        # self.edit.window.tags_no_list.doubleClicked.connect(partial(self.list_transfer, self.edit.window.tags_no_list))

        # # search bars
        # self.edit.window.genres_yes.textChanged.connect(partial(self.list_filter, self.edit.window.genres_yes))
        # self.edit.window.genres_no.textChanged.connect(partial(self.list_filter, self.edit.window.genres_no))
        # self.edit.window.tags_yes.textChanged.connect(partial(self.list_filter, self.edit.window.tags_yes))
        # self.edit.window.tags_no.textChanged.connect(partial(self.list_filter, self.edit.window.tags_no))
        # self.edit.window.actors_yes.textChanged.connect(partial(self.list_filter, self.edit.window.actors_yes))
        # self.edit.window.actors_no.textChanged.connect(partial(self.list_filter, self.edit.window.actors_no))
        # self.edit.window.studio.textChanged.connect(partial(self.list_filter, self.edit.window.studio))
        # self.edit.window.director.textChanged.connect(partial(self.list_filter, self.edit.window.director))
        # self.edit.window.series.textChanged.connect(partial(self.list_filter, self.edit.window.series))
        # self.edit.window.language.textChanged.connect(partial(self.list_filter, self.edit.window.language))



if __name__ == "__main__":
    GUI()