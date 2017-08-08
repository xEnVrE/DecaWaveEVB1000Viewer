# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tag_item_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_tagItem(object):
    def setupUi(self, tagItem):
        tagItem.setObjectName("tagItem")
        tagItem.resize(258, 127)
        tagItem.setMaximumSize(QtCore.QSize(16777215, 127))
        self.verticalLayout = QtWidgets.QVBoxLayout(tagItem)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tagItemFrame = QtWidgets.QFrame(tagItem)
        self.tagItemFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.tagItemFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tagItemFrame.setLineWidth(1)
        self.tagItemFrame.setObjectName("tagItemFrame")
        self.tagItemFrameLayout = QtWidgets.QGridLayout(self.tagItemFrame)
        self.tagItemFrameLayout.setContentsMargins(-1, -1, -1, 0)
        self.tagItemFrameLayout.setObjectName("tagItemFrameLayout")
        self.frequencyLabel = QtWidgets.QLabel(self.tagItemFrame)
        self.frequencyLabel.setObjectName("frequencyLabel")
        self.tagItemFrameLayout.addWidget(self.frequencyLabel, 2, 0, 1, 1)
        self.tagIdLabel = QtWidgets.QLabel(self.tagItemFrame)
        self.tagIdLabel.setObjectName("tagIdLabel")
        self.tagItemFrameLayout.addWidget(self.tagIdLabel, 0, 0, 1, 1)
        self.portLabel = QtWidgets.QLabel(self.tagItemFrame)
        self.portLabel.setObjectName("portLabel")
        self.tagItemFrameLayout.addWidget(self.portLabel, 1, 0, 1, 1)
        self.frequencyLabelValue = QtWidgets.QLabel(self.tagItemFrame)
        self.frequencyLabelValue.setObjectName("frequencyLabelValue")
        self.tagItemFrameLayout.addWidget(self.frequencyLabelValue, 2, 2, 1, 1)
        self.portLabelValue = QtWidgets.QLabel(self.tagItemFrame)
        self.portLabelValue.setObjectName("portLabelValue")
        self.tagItemFrameLayout.addWidget(self.portLabelValue, 1, 2, 1, 1)
        self.tagIdLabelValue = QtWidgets.QLabel(self.tagItemFrame)
        self.tagIdLabelValue.setObjectName("tagIdLabelValue")
        self.tagItemFrameLayout.addWidget(self.tagIdLabelValue, 0, 2, 1, 1)
        self.recordCheckbox = QtWidgets.QCheckBox(self.tagItemFrame)
        self.recordCheckbox.setObjectName("recordCheckbox")
        self.tagItemFrameLayout.addWidget(self.recordCheckbox, 3, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.tagItemFrameLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.tagItemFrameLayout.addItem(spacerItem1, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.tagItemFrameLayout.addItem(spacerItem2, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.tagItemFrame)

        self.retranslateUi(tagItem)
        QtCore.QMetaObject.connectSlotsByName(tagItem)

    def retranslateUi(self, tagItem):
        _translate = QtCore.QCoreApplication.translate
        tagItem.setWindowTitle(_translate("tagItem", "Form"))
        self.frequencyLabel.setText(_translate("tagItem", "Frequency:"))
        self.tagIdLabel.setText(_translate("tagItem", "Tag ID:"))
        self.portLabel.setText(_translate("tagItem", "Port:"))
        self.frequencyLabelValue.setText(_translate("tagItem", "TextLabel"))
        self.portLabelValue.setText(_translate("tagItem", "TextLabel"))
        self.tagIdLabelValue.setText(_translate("tagItem", "TextLabel"))
        self.recordCheckbox.setText(_translate("tagItem", "Record"))

