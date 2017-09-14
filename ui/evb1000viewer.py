# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'evb1000viewer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EVB1000ViewerMainWindow(object):
    def setupUi(self, EVB1000ViewerMainWindow):
        EVB1000ViewerMainWindow.setObjectName("EVB1000ViewerMainWindow")
        EVB1000ViewerMainWindow.resize(892, 611)
        self.centralwidget = QtWidgets.QWidget(EVB1000ViewerMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.logGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.logGroupBox.setMaximumSize(QtCore.QSize(16777215, 150))
        self.logGroupBox.setObjectName("logGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.logGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.logScrollArea = QtWidgets.QScrollArea(self.logGroupBox)
        self.logScrollArea.setStyleSheet("background: white")
        self.logScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.logScrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.logScrollArea.setWidgetResizable(True)
        self.logScrollArea.setObjectName("logScrollArea")
        self.logScrollAreaWidgetContents = QtWidgets.QWidget()
        self.logScrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 848, 106))
        self.logScrollAreaWidgetContents.setObjectName("logScrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.logScrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.logLabel = QtWidgets.QLabel(self.logScrollAreaWidgetContents)
        self.logLabel.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.logLabel.setText("")
        self.logLabel.setObjectName("logLabel")
        self.verticalLayout_2.addWidget(self.logLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.logScrollArea.setWidget(self.logScrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.logScrollArea)
        self.gridLayout.addWidget(self.logGroupBox, 4, 0, 1, 2)
        self.matPlotGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.matPlotGroupBox.setObjectName("matPlotGroupBox")
        self.matPlotGroupBoxLayout = QtWidgets.QVBoxLayout(self.matPlotGroupBox)
        self.matPlotGroupBoxLayout.setObjectName("matPlotGroupBoxLayout")
        self.gridLayout.addWidget(self.matPlotGroupBox, 1, 0, 3, 1)
        self.planeHeightGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.planeHeightGroupBox.sizePolicy().hasHeightForWidth())
        self.planeHeightGroupBox.setSizePolicy(sizePolicy)
        self.planeHeightGroupBox.setMaximumSize(QtCore.QSize(230, 200))
        self.planeHeightGroupBox.setTitle("")
        self.planeHeightGroupBox.setObjectName("planeHeightGroupBox")
        self.planeHeightGroupBoxLayout = QtWidgets.QVBoxLayout(self.planeHeightGroupBox)
        self.planeHeightGroupBoxLayout.setContentsMargins(-1, -1, -1, 20)
        self.planeHeightGroupBoxLayout.setObjectName("planeHeightGroupBoxLayout")
        self.gridLayout.addWidget(self.planeHeightGroupBox, 3, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMaximumSize(QtCore.QSize(230, 16777215))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.anchorsTab = QtWidgets.QWidget()
        self.anchorsTab.setAutoFillBackground(True)
        self.anchorsTab.setObjectName("anchorsTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.anchorsTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.anchorsScrollArea = QtWidgets.QScrollArea(self.anchorsTab)
        self.anchorsScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.anchorsScrollArea.setWidgetResizable(True)
        self.anchorsScrollArea.setObjectName("anchorsScrollArea")
        self.anchorsScrollAreaWidget = QtWidgets.QWidget()
        self.anchorsScrollAreaWidget.setEnabled(True)
        self.anchorsScrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.anchorsScrollAreaWidget.setObjectName("anchorsScrollAreaWidget")
        self.anchorsScrollAreaWidgetLayout = QtWidgets.QVBoxLayout(self.anchorsScrollAreaWidget)
        self.anchorsScrollAreaWidgetLayout.setContentsMargins(0, 0, 15, 0)
        self.anchorsScrollAreaWidgetLayout.setObjectName("anchorsScrollAreaWidgetLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.anchorsScrollAreaWidgetLayout.addItem(spacerItem1)
        self.anchorsScrollArea.setWidget(self.anchorsScrollAreaWidget)
        self.verticalLayout_4.addWidget(self.anchorsScrollArea)
        self.tabWidget.addTab(self.anchorsTab, "")
        self.connectedTagsTab = QtWidgets.QWidget()
        self.connectedTagsTab.setAutoFillBackground(True)
        self.connectedTagsTab.setObjectName("connectedTagsTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.connectedTagsTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.connectedTagsScrollArea = QtWidgets.QScrollArea(self.connectedTagsTab)
        self.connectedTagsScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.connectedTagsScrollArea.setWidgetResizable(True)
        self.connectedTagsScrollArea.setObjectName("connectedTagsScrollArea")
        self.connectedTagsScrollAreaWidget = QtWidgets.QWidget()
        self.connectedTagsScrollAreaWidget.setEnabled(True)
        self.connectedTagsScrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 208, 274))
        self.connectedTagsScrollAreaWidget.setObjectName("connectedTagsScrollAreaWidget")
        self.connectedTagsScrollAreaWidgetLayout = QtWidgets.QVBoxLayout(self.connectedTagsScrollAreaWidget)
        self.connectedTagsScrollAreaWidgetLayout.setContentsMargins(0, 0, 15, 0)
        self.connectedTagsScrollAreaWidgetLayout.setObjectName("connectedTagsScrollAreaWidgetLayout")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.connectedTagsScrollAreaWidgetLayout.addItem(spacerItem2)
        self.connectedTagsScrollArea.setWidget(self.connectedTagsScrollAreaWidget)
        self.verticalLayout_3.addWidget(self.connectedTagsScrollArea)
        self.connectedTagsRecordButtonsHorizontalLayout = QtWidgets.QHBoxLayout()
        self.connectedTagsRecordButtonsHorizontalLayout.setObjectName("connectedTagsRecordButtonsHorizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.connectedTagsRecordButtonsHorizontalLayout.addItem(spacerItem3)
        self.connectedTagsRecordButton = QtWidgets.QPushButton(self.connectedTagsTab)
        self.connectedTagsRecordButton.setObjectName("connectedTagsRecordButton")
        self.connectedTagsRecordButtonsHorizontalLayout.addWidget(self.connectedTagsRecordButton)
        self.connectedTagsStopButton = QtWidgets.QPushButton(self.connectedTagsTab)
        self.connectedTagsStopButton.setObjectName("connectedTagsStopButton")
        self.connectedTagsRecordButtonsHorizontalLayout.addWidget(self.connectedTagsStopButton)
        self.verticalLayout_3.addLayout(self.connectedTagsRecordButtonsHorizontalLayout)
        self.tabWidget.addTab(self.connectedTagsTab, "")
        self.gridLayout.addWidget(self.tabWidget, 2, 1, 1, 1)
        EVB1000ViewerMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(EVB1000ViewerMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 892, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        EVB1000ViewerMainWindow.setMenuBar(self.menubar)
        self.actionQuit = QtWidgets.QAction(EVB1000ViewerMainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(EVB1000ViewerMainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(EVB1000ViewerMainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(EVB1000ViewerMainWindow)

    def retranslateUi(self, EVB1000ViewerMainWindow):
        _translate = QtCore.QCoreApplication.translate
        EVB1000ViewerMainWindow.setWindowTitle(_translate("EVB1000ViewerMainWindow", "EVB1000 Tag Viewer"))
        self.logGroupBox.setTitle(_translate("EVB1000ViewerMainWindow", "Log"))
        self.matPlotGroupBox.setTitle(_translate("EVB1000ViewerMainWindow", "Plot"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.anchorsTab), _translate("EVB1000ViewerMainWindow", "Anchors"))
        self.connectedTagsRecordButton.setText(_translate("EVB1000ViewerMainWindow", "Record"))
        self.connectedTagsStopButton.setText(_translate("EVB1000ViewerMainWindow", "Stop"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.connectedTagsTab), _translate("EVB1000ViewerMainWindow", "Connected Tags"))
        self.menuFile.setTitle(_translate("EVB1000ViewerMainWindow", "&File"))
        self.menuHelp.setTitle(_translate("EVB1000ViewerMainWindow", "&Help"))
        self.actionQuit.setText(_translate("EVB1000ViewerMainWindow", "&Quit"))
        self.actionQuit.setShortcut(_translate("EVB1000ViewerMainWindow", "Ctrl+Q"))
        self.actionAbout.setText(_translate("EVB1000ViewerMainWindow", "&About"))

