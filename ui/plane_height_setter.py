# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plane_height_setter.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(204, 89)
        Form.setMaximumSize(QtCore.QSize(204, 89))
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.planeHeightLabel = QtWidgets.QLabel(Form)
        self.planeHeightLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        self.planeHeightLabel.setObjectName("planeHeightLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.planeHeightLabel)
        self.planeHeightTextEdit = QtWidgets.QTextEdit(Form)
        self.planeHeightTextEdit.setMinimumSize(QtCore.QSize(75, 30))
        self.planeHeightTextEdit.setMaximumSize(QtCore.QSize(75, 30))
        self.planeHeightTextEdit.setObjectName("planeHeightTextEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.planeHeightTextEdit)
        self.planeHeightHorizontalLayout = QtWidgets.QHBoxLayout()
        self.planeHeightHorizontalLayout.setObjectName("planeHeightHorizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.planeHeightHorizontalLayout.addItem(spacerItem)
        self.planeHeightSetButton = QtWidgets.QPushButton(Form)
        self.planeHeightSetButton.setObjectName("planeHeightSetButton")
        self.planeHeightHorizontalLayout.addWidget(self.planeHeightSetButton)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.SpanningRole, self.planeHeightHorizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.planeHeightLabel.setText(_translate("Form", "Plane height (m):"))
        self.planeHeightTextEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0</p></body></html>"))
        self.planeHeightSetButton.setText(_translate("Form", "Set"))

