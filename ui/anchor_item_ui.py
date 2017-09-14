# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'anchor_item_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_anchItem(object):
    def setupUi(self, anchItem):
        anchItem.setObjectName("anchItem")
        anchItem.resize(232, 114)
        anchItem.setMaximumSize(QtCore.QSize(16777215, 114))
        self.gridLayout = QtWidgets.QGridLayout(anchItem)
        self.gridLayout.setObjectName("gridLayout")
        self.xLabelValue = QtWidgets.QLabel(anchItem)
        self.xLabelValue.setObjectName("xLabelValue")
        self.gridLayout.addWidget(self.xLabelValue, 0, 3, 1, 1)
        self.yLabelValue = QtWidgets.QLabel(anchItem)
        self.yLabelValue.setObjectName("yLabelValue")
        self.gridLayout.addWidget(self.yLabelValue, 1, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.yLabel = QtWidgets.QLabel(anchItem)
        self.yLabel.setObjectName("yLabel")
        self.gridLayout.addWidget(self.yLabel, 1, 1, 1, 1)
        self.xLabel = QtWidgets.QLabel(anchItem)
        self.xLabel.setObjectName("xLabel")
        self.gridLayout.addWidget(self.xLabel, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.zLabel = QtWidgets.QLabel(anchItem)
        self.zLabel.setObjectName("zLabel")
        self.gridLayout.addWidget(self.zLabel, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 2, 1, 1)
        self.zLabelValue = QtWidgets.QLabel(anchItem)
        self.zLabelValue.setObjectName("zLabelValue")
        self.gridLayout.addWidget(self.zLabelValue, 2, 3, 1, 1)

        self.retranslateUi(anchItem)
        QtCore.QMetaObject.connectSlotsByName(anchItem)

    def retranslateUi(self, anchItem):
        _translate = QtCore.QCoreApplication.translate
        anchItem.setWindowTitle(_translate("anchItem", "GroupBox"))
        anchItem.setTitle(_translate("anchItem", "GroupBox"))
        self.xLabelValue.setText(_translate("anchItem", "TextLabel"))
        self.yLabelValue.setText(_translate("anchItem", "TextLabel"))
        self.yLabel.setText(_translate("anchItem", "y (m):"))
        self.xLabel.setText(_translate("anchItem", "x (m):"))
        self.zLabel.setText(_translate("anchItem", "z (m):"))
        self.zLabelValue.setText(_translate("anchItem", "TextLabel"))

