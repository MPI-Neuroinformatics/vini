# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyqtgraph/canvas/CanvasTemplate.ui'
#
# Created: Wed Nov  9 18:02:00 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(490, 414)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.view = GraphicsView(self.splitter)
        self.view.setObjectName("view")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.autoRangeBtn = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.autoRangeBtn.sizePolicy().hasHeightForWidth())
        self.autoRangeBtn.setSizePolicy(sizePolicy)
        self.autoRangeBtn.setObjectName("autoRangeBtn")
        self.gridLayout_2.addWidget(self.autoRangeBtn, 2, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.redirectCheck = QtGui.QCheckBox(self.layoutWidget)
        self.redirectCheck.setObjectName("redirectCheck")
        self.horizontalLayout.addWidget(self.redirectCheck)
        self.redirectCombo = CanvasCombo(self.layoutWidget)
        self.redirectCombo.setObjectName("redirectCombo")
        self.horizontalLayout.addWidget(self.redirectCombo)
        self.gridLayout_2.addLayout(self.horizontalLayout, 5, 0, 1, 2)
        self.itemList = TreeWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy.Expanding, QtGui.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.itemList.sizePolicy().hasHeightForWidth())
        self.itemList.setSizePolicy(sizePolicy)
        self.itemList.setHeaderHidden(True)
        self.itemList.setObjectName("itemList")
        self.itemList.headerItem().setText(0, "1")
        self.gridLayout_2.addWidget(self.itemList, 6, 0, 1, 2)
        self.ctrlLayout = QtGui.QGridLayout()
        self.ctrlLayout.setSpacing(0)
        self.ctrlLayout.setObjectName("ctrlLayout")
        self.gridLayout_2.addLayout(self.ctrlLayout, 10, 0, 1, 2)
        self.resetTransformsBtn = QtGui.QPushButton(self.layoutWidget)
        self.resetTransformsBtn.setObjectName("resetTransformsBtn")
        self.gridLayout_2.addWidget(self.resetTransformsBtn, 7, 0, 1, 1)
        self.mirrorSelectionBtn = QtGui.QPushButton(self.layoutWidget)
        self.mirrorSelectionBtn.setObjectName("mirrorSelectionBtn")
        self.gridLayout_2.addWidget(self.mirrorSelectionBtn, 3, 0, 1, 1)
        self.reflectSelectionBtn = QtGui.QPushButton(self.layoutWidget)
        self.reflectSelectionBtn.setObjectName("reflectSelectionBtn")
        self.gridLayout_2.addWidget(self.reflectSelectionBtn, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, QtWidgets.QApplication.UnicodeUTF8))
        self.autoRangeBtn.setText(QtWidgets.QApplication.translate("Form", "Auto Range", None, QtWidgets.QApplication.UnicodeUTF8))
        self.redirectCheck.setToolTip(QtWidgets.QApplication.translate("Form", "Check to display all local items in a remote canvas.", None, QtWidgets.QApplication.UnicodeUTF8))
        self.redirectCheck.setText(QtWidgets.QApplication.translate("Form", "Redirect", None, QtWidgets.QApplication.UnicodeUTF8))
        self.resetTransformsBtn.setText(QtWidgets.QApplication.translate("Form", "Reset Transforms", None, QtWidgets.QApplication.UnicodeUTF8))
        self.mirrorSelectionBtn.setText(QtWidgets.QApplication.translate("Form", "Mirror Selection", None, QtWidgets.QApplication.UnicodeUTF8))
        self.reflectSelectionBtn.setText(QtWidgets.QApplication.translate("Form", "MirrorXY", None, QtWidgets.QApplication.UnicodeUTF8))

from .CanvasManager import CanvasCombo
from ..widgets.TreeWidget import TreeWidget
from ..widgets.GraphicsView import GraphicsView
