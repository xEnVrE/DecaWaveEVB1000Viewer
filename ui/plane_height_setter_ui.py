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
        planeHeightSetter.resize(204, 72)
        planeHeightSetter.setMinimumSize(QtCore.QSize(204, 50))
        planeHeightSetter.setMaximumSize(QtCore.QSize(204, 72))
        self.formLayout = QtWidgets.QFormLayout(planeHeightSetter)
        self.formLayout.setContentsMargins(-1, 9, -1, 9)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.planeHeightLabel = QtWidgets.QLabel(planeHeightSetter)
        self.planeHeightLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        self.planeHeightLabel.setObjectName("planeHeightLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.planeHeightLabel)
        self.planeHeightLineEdit = QtWidgets.QLineEdit(planeHeightSetter)
        self.planeHeightLineEdit.setObjectName("planeHeightLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.planeHeightLineEdit)
        self.planeHeightHorizontalLayout = QtWidgets.QHBoxLayout()
        self.planeHeightHorizontalLayout.setObjectName("planeHeightHorizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.planeHeightHorizontalLayout.addItem(spacerItem)
        self.planeHeightSetButton = QtWidgets.QPushButton(planeHeightSetter)
        self.planeHeightSetButton.setObjectName("planeHeightSetButton")
        self.planeHeightHorizontalLayout.addWidget(self.planeHeightSetButton)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.SpanningRole, self.planeHeightHorizontalLayout)

        self.retranslateUi(planeHeightSetter)
        QtCore.QMetaObject.connectSlotsByName(planeHeightSetter)

    def retranslateUi(self, planeHeightSetter):
        _translate = QtCore.QCoreApplication.translate
        planeHeightSetter.setWindowTitle(_translate("planeHeightSetter", "Form"))
        self.planeHeightLabel.setText(_translate("planeHeightSetter", "Plane height (m):"))
        self.planeHeightSetButton.setText(_translate("planeHeightSetter", "Set"))

