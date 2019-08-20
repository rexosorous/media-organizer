from PyQt5 import QtWidgets
import sys
import ui.create_delete_ui as cd

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
window = cd.Ui_create_delete_window()
window.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())