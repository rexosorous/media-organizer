# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1280, 720)
        main_window.setMinimumSize(QtCore.QSize(1280, 720))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 159, 159))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 159, 159))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        main_window.setPalette(palette)
        main_window.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.gridLayout = QtWidgets.QGridLayout(self.main_frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.table = QtWidgets.QTableWidget(self.main_frame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(143, 143, 143))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(143, 143, 143))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(143, 143, 143))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        self.table.setPalette(palette)
        self.table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.table.setShowGrid(False)
        self.table.setObjectName("table")
        self.table.setColumnCount(18)
        self.table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(17, item)
        self.table.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.table, 2, 0, 1, 1)
        self.frame_11 = QtWidgets.QFrame(self.main_frame)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_19 = QtWidgets.QLabel(self.frame_11)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_6.addWidget(self.label_19)
        self.search_bar = QtWidgets.QLineEdit(self.frame_11)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(159, 159, 159))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 159, 159))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.search_bar.setPalette(palette)
        self.search_bar.setAutoFillBackground(True)
        self.search_bar.setFrame(False)
        self.search_bar.setObjectName("search_bar")
        self.horizontalLayout_6.addWidget(self.search_bar)
        self.gridLayout.addWidget(self.frame_11, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.main_frame)
        self.edit_button = QtWidgets.QPushButton(self.centralwidget)
        self.edit_button.setObjectName("edit_button")
        self.verticalLayout_3.addWidget(self.edit_button)
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Main Window"))
        self.table.setSortingEnabled(True)
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("main_window", "Title"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("main_window", "Alternate Title"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("main_window", "Series"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("main_window", "Order"))
        item = self.table.horizontalHeaderItem(4)
        item.setText(_translate("main_window", "Media Type"))
        item = self.table.horizontalHeaderItem(5)
        item.setText(_translate("main_window", "Animated?"))
        item = self.table.horizontalHeaderItem(6)
        item.setText(_translate("main_window", "Country of Origin"))
        item = self.table.horizontalHeaderItem(7)
        item.setText(_translate("main_window", "Languages"))
        item = self.table.horizontalHeaderItem(8)
        item.setText(_translate("main_window", "Subtitles?"))
        item = self.table.horizontalHeaderItem(9)
        item.setText(_translate("main_window", "Release Year"))
        item = self.table.horizontalHeaderItem(10)
        item.setText(_translate("main_window", "Genres"))
        item = self.table.horizontalHeaderItem(11)
        item.setText(_translate("main_window", "Director"))
        item = self.table.horizontalHeaderItem(12)
        item.setText(_translate("main_window", "Studio"))
        item = self.table.horizontalHeaderItem(13)
        item.setText(_translate("main_window", "Actors"))
        item = self.table.horizontalHeaderItem(14)
        item.setText(_translate("main_window", "Plot"))
        item = self.table.horizontalHeaderItem(15)
        item.setText(_translate("main_window", "Rating"))
        item = self.table.horizontalHeaderItem(16)
        item.setText(_translate("main_window", "Tags"))
        item = self.table.horizontalHeaderItem(17)
        item.setText(_translate("main_window", "Notes"))
        self.label_19.setText(_translate("main_window", "Search"))
        self.edit_button.setText(_translate("main_window", "EDIT"))