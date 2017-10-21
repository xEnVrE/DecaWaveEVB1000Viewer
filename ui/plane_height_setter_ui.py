# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plane_height_setter_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_planeHeightSetter(object):
    def setupUi(self, planeHeightSetter):
        planeHeightSetter.setObjectName("planeHeightSetter")
        planeHeightSetter.resize(390, 76)
        planeHeightSetter.setMinimumSize(QtCore.QSize(204, 50))
        planeHeightSetter.setMaximumSize(QtCore.QSize(13131223, 76))
        self.gridLayout = QtWidgets.QGridLayout(planeHeightSetter)
        self.gridLayout.setContentsMargins(-1, 9, -1, 9)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.planeHeightSetButton = QtWidgets.QPushButton(planeHeightSetter)
        self.planeHeightSetButton.setObjectName("planeHeightSetButton")
        self.gridLayout.addWidget(self.planeHeightSetButton, 1, 2, 1, 1)
        self.planeHeightLineEdit = QtWidgets.QLineEdit(planeHeightSetter)
        self.planeHeightLineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.planeHeightLineEdit.setObjectName("planeHeightLineEdit")
        self.gridLayout.addWidget(self.planeHeightLineEdit, 0, 2, 1, 1)
        self.planeHeightLabel = QtWidgets.QLabel(planeHeightSetter)
        self.planeHeightLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        self.planeHeightLabel.setObjectName("planeHeightLabel")
        self.gridLayout.addWidget(self.planeHeightLabel, 0, 0, 1, 1)

        self.retranslateUi(planeHeightSetter)
        QtCore.QMetaObject.connectSlotsByName(planeHeightSetter)

    def retranslateUi(self, planeHeightSetter):
        _translate = QtCore.QCoreApplication.translate
        planeHeightSetter.setWindowTitle(_translate("planeHeightSetter", "Form"))
        self.planeHeightSetButton.setText(_translate("planeHeightSetter", "Set"))
        self.planeHeightLabel.setText(_translate("planeHeightSetter", "Plane height (m):"))

