# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'main.ui'
#
# Created by: Qt User Interface Compiler version 6.6.1
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt, QRect)
from PySide6.QtGui import (QCursor, QFont, QIcon)
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel,
                               QPushButton, QSizePolicy, QSplitter, QStackedWidget, QVBoxLayout, QWidget, QLayout)

from app.view.widgets.measurements_table.view import TableView
from app.view.widgets.file_tree_selector.view import FileSystemTreeView


class UiMainWindow(object):
    def setupUi(self, MainWindow, style):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(940, 883)
        MainWindow.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)

        # style = open('../themes/my_dark.qss', 'r').read()
        self.styleSheet.setStyleSheet(style)

        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.Shape.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Shadow.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.Shape.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.Shape.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy)
        self.leftBox.setFrameShape(QFrame.Shape.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy1)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)

        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.Shape.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settingsTopBtn = QPushButton(self.rightButtons)
        self.settingsTopBtn.setObjectName(u"settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsTopBtn.setIcon(icon)
        self.settingsTopBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.settingsTopBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeAppBtn.setIcon(icon1)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font1)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.maximizeRestoreAppBtn.setIcon(icon2)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.closeAppBtn.setIcon(icon3)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)

        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)

        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.mainPage = QWidget()
        self.mainPage.setObjectName(u"mainPage")
        self.horizontalLayout_6 = QHBoxLayout(self.mainPage)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_64")
        self.splitter_2 = QSplitter(self.mainPage)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.verticalLayoutWidget = QWidget(self.splitter_2)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.fileSystemWidget = QVBoxLayout(self.verticalLayoutWidget)
        self.fileSystemWidget.setObjectName(u"fileSystemWidget")
        self.fileSystemWidget.setContentsMargins(0, 0, 0, 0)

        self.normalizeButton = QPushButton(self.verticalLayoutWidget)
        self.normalizeButton.setMinimumSize(QSize(150, 30))
        self.normalizeButton.setFont(font)
        self.normalizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.normalizeButton.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon88 = QIcon()
        icon88.addFile(u":/icons/images/icons/cil-chart-normalize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.normalizeButton.setIcon(icon88)

        self.fileSystemWidget.addWidget(self.normalizeButton)

        self.countAverageButton = QPushButton(self.verticalLayoutWidget)
        self.countAverageButton.setObjectName(u"countAverageButton")
        self.countAverageButton.setMinimumSize(QSize(150, 30))
        self.countAverageButton.setFont(font)
        self.countAverageButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.countAverageButton.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/cil-chart.png", QSize(), QIcon.Normal, QIcon.Off)
        self.countAverageButton.setIcon(icon4)

        self.fileSystemWidget.addWidget(self.countAverageButton)

        self.viewMeasureButton = QPushButton(self.verticalLayoutWidget)
        self.viewMeasureButton.setObjectName(u"viewMeasureButton")
        self.viewMeasureButton.setMinimumSize(QSize(150, 30))
        self.viewMeasureButton.setFont(font)
        self.viewMeasureButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.viewMeasureButton.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon5 = QIcon()
        icon5.addFile(u":/icons/images/icons/cil-eye.png", QSize(), QIcon.Normal, QIcon.Off)
        self.viewMeasureButton.setIcon(icon5)

        self.fileSystemWidget.addWidget(self.viewMeasureButton)

        self.changeWorkDirButton = QPushButton(self.verticalLayoutWidget)
        self.changeWorkDirButton.setObjectName(u"changeWorkDirButton")
        self.changeWorkDirButton.setMinimumSize(QSize(150, 30))
        self.changeWorkDirButton.setFont(font)
        self.changeWorkDirButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.changeWorkDirButton.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon6 = QIcon()
        icon6.addFile(u":/icons/images/icons/cil-folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.changeWorkDirButton.setIcon(icon6)

        self.fileSystemWidget.addWidget(self.changeWorkDirButton)

        self.treeView = FileSystemTreeView(self.verticalLayoutWidget, MainWindow.fileSystemModel)
        self.treeView.setObjectName(u"treeView")

        self.fileSystemWidget.addWidget(self.treeView)

        self.splitter_2.addWidget(self.verticalLayoutWidget)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.matplotWidget = QWidget(self.splitter)
        self.matplotWidget.setObjectName(u"matplotWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.matplotWidget.sizePolicy().hasHeightForWidth())
        self.matplotWidget.setSizePolicy(sizePolicy2)
        self.matplotWidget.setMinimumSize(QSize(0, 400))
        self.splitter.addWidget(self.matplotWidget)

        # TABLE
        self.measureTableView = TableView(self.splitter, MainWindow.measureTableModel)
        self.measureTableView.setObjectName(u"measureTableView")
        self.splitter.addWidget(self.measureTableView)

        self.splitter_2.addWidget(self.splitter)

        self.horizontalLayout_6.addWidget(self.splitter_2)

        self.stackedWidget.addWidget(self.mainPage)

        # =================
        # Settings page
        # =================
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName(u"settingsPage")
        self.verticalLayoutWidget_221 = QWidget(self.settingsPage)
        self.verticalLayoutWidget_221.setObjectName(u"verticalLayoutWidget_221")
        self.verticalLayoutWidget_221.setGeometry(QRect(0, 10, 831, 50))
        self.verticalLayout_222 = QVBoxLayout(self.verticalLayoutWidget_221)
        self.verticalLayout_222.setObjectName(u"verticalLayout_222")
        self.verticalLayout_222.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout_222.setContentsMargins(0, 0, 0, 0)

        self.uploadFolderLabel = QLabel(self.verticalLayoutWidget_221)
        self.uploadFolderLabel.setObjectName(u"uploadFolderLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uploadFolderLabel.sizePolicy().hasHeightForWidth())
        self.uploadFolderLabel.setSizePolicy(sizePolicy)

        self.verticalLayout_222.addWidget(self.uploadFolderLabel)

        self.horizontalLayout_64 = QHBoxLayout()
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.horizontalLayout_64.setSizeConstraint(QLayout.SetMinimumSize)
        self.uploadFolderPathLabel = QLabel(self.verticalLayoutWidget_221)
        self.uploadFolderPathLabel.setObjectName(u"uploadFolderPathLabel")
        sizePolicy.setHeightForWidth(self.uploadFolderPathLabel.sizePolicy().hasHeightForWidth())
        self.uploadFolderPathLabel.setSizePolicy(sizePolicy)

        self.horizontalLayout_64.addWidget(self.uploadFolderPathLabel)

        self.changeUploadFolderButton = QPushButton(self.verticalLayoutWidget_221)
        self.changeUploadFolderButton.setObjectName(u"changeUploadFolderButton")
        sizePolicy15 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.changeUploadFolderButton.sizePolicy().hasHeightForWidth())
        self.changeUploadFolderButton.setSizePolicy(sizePolicy15)
        self.changeUploadFolderButton.setMinimumSize(QSize(150, 30))
        self.changeUploadFolderButton.setFont(font)
        self.changeUploadFolderButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.changeUploadFolderButton.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon6 = QIcon()
        icon6.addFile(u":/icons/images/icons/cil-folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.changeUploadFolderButton.setIcon(icon6)

        self.horizontalLayout_64.addWidget(self.changeUploadFolderButton)

        self.verticalLayout_222.addLayout(self.horizontalLayout_64)

        self.widget = QWidget()  # self.settingsPage)  TODO uncomment to enable backup menu
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(1, 67, 831, 50))
        self.verticalLayout_201 = QVBoxLayout(self.widget)
        self.verticalLayout_201.setObjectName(u"verticalLayout_201")
        self.verticalLayout_201.setContentsMargins(0, 0, 0, 0)
        self.backupFolderLabel = QLabel(self.widget)
        self.backupFolderLabel.setObjectName(u"backupFolderLabel")
        sizePolicy.setHeightForWidth(self.backupFolderLabel.sizePolicy().hasHeightForWidth())
        self.backupFolderLabel.setSizePolicy(sizePolicy)

        self.verticalLayout_201.addWidget(self.backupFolderLabel)

        self.horizontalLayout_78 = QHBoxLayout()
        self.horizontalLayout_78.setObjectName(u"horizontalLayout_78")
        self.backupFolderPathLabel = QLabel(self.widget)
        self.backupFolderPathLabel.setObjectName(u"backupFolderPathLabel")
        sizePolicy22 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy22.setHorizontalStretch(0)
        sizePolicy22.setVerticalStretch(0)
        sizePolicy22.setHeightForWidth(self.backupFolderPathLabel.sizePolicy().hasHeightForWidth())
        self.backupFolderPathLabel.setSizePolicy(sizePolicy22)

        self.horizontalLayout_78.addWidget(self.backupFolderPathLabel)

        self.changeBackupFolderButton = QPushButton(self.widget)
        self.changeBackupFolderButton.setObjectName(u"changeBackupFolderButton")
        sizePolicy15.setHeightForWidth(self.changeBackupFolderButton.sizePolicy().hasHeightForWidth())
        self.changeBackupFolderButton.setSizePolicy(sizePolicy15)
        self.changeBackupFolderButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.changeBackupFolderButton.setInputMethodHints(Qt.ImhFormattedNumbersOnly | Qt.ImhUppercaseOnly)

        self.horizontalLayout_78.addWidget(self.changeBackupFolderButton)

        self.verticalLayout_201.addLayout(self.horizontalLayout_78)

        self.stackedWidget.addWidget(self.settingsPage)
        # ================

        self.verticalLayout_15.addWidget(self.stackedWidget)

        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.Shape.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFrameShape(QFrame.Shape.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u"contentSettings")
        self.contentSettings.setFrameShape(QFrame.Shape.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.topMenus = QFrame(self.contentSettings)
        self.topMenus.setObjectName(u"topMenus")
        self.topMenus.setFrameShape(QFrame.Shape.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.topMenus)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.btn_message = QPushButton(self.topMenus)
        self.btn_message.setObjectName(u"btn_message")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_message.sizePolicy().hasHeightForWidth())
        self.btn_message.setSizePolicy(sizePolicy3)
        self.btn_message.setMinimumSize(QSize(0, 45))
        self.btn_message.setFont(font)
        self.btn_message.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_message.setLayoutDirection(Qt.LeftToRight)
        self.btn_message.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-envelope-open.png);")

        self.verticalLayout_14.addWidget(self.btn_message)

        self.btn_print = QPushButton(self.topMenus)
        self.btn_print.setObjectName(u"btn_print")
        sizePolicy3.setHeightForWidth(self.btn_print.sizePolicy().hasHeightForWidth())
        self.btn_print.setSizePolicy(sizePolicy3)
        self.btn_print.setMinimumSize(QSize(0, 45))
        self.btn_print.setFont(font)
        self.btn_print.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_print.setLayoutDirection(Qt.LeftToRight)
        self.btn_print.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-print.png);")

        self.verticalLayout_14.addWidget(self.btn_print)

        self.btn_logout = QPushButton(self.topMenus)
        self.btn_logout.setObjectName(u"btn_logout")
        sizePolicy3.setHeightForWidth(self.btn_logout.sizePolicy().hasHeightForWidth())
        self.btn_logout.setSizePolicy(sizePolicy3)
        self.btn_logout.setMinimumSize(QSize(0, 45))
        self.btn_logout.setFont(font)
        self.btn_logout.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_logout.setLayoutDirection(Qt.LeftToRight)
        self.btn_logout.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-account-logout.png);")

        self.verticalLayout_14.addWidget(self.btn_logout)

        self.verticalLayout_13.addWidget(self.topMenus, 0, Qt.AlignTop)

        self.verticalLayout_7.addWidget(self.contentSettings)

        self.horizontalLayout_4.addWidget(self.extraRightBox)

        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.Shape.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)

        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setBold(False)
        font3.setItalic(False)
        self.creditsLabel.setFont(font3)
        self.creditsLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)

        self.verticalLayout_6.addWidget(self.bottomBar)

        self.verticalLayout_2.addWidget(self.contentBottom)

        self.appLayout.addWidget(self.contentBox)

        self.appMargins.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"Raman management tool", None))
        # if QT_CONFIG(tooltip)
        self.settingsTopBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
        # endif // QT_CONFIG(tooltip)
        self.settingsTopBtn.setText("")
        # if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
        # endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
        # if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
        # endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
        # if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
        # endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.countAverageButton.setText(QCoreApplication.translate("MainWindow", u"Count average", None))
        self.viewMeasureButton.setText(QCoreApplication.translate("MainWindow", u"View", None))
        self.changeWorkDirButton.setText(QCoreApplication.translate("MainWindow", u"Change working directory", None))
        self.normalizeButton.setText(QCoreApplication.translate("MainWindow", u"Normalize", None))


        self.btn_message.setText(QCoreApplication.translate("MainWindow", u"Message", None))
        self.btn_print.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.btn_logout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.creditsLabel.setText("")
        self.version.setText(QCoreApplication.translate("MainWindow", u"v0.1.0", None))


        # ==============
        # Settings Page
        # ==============
        self.uploadFolderLabel.setText(QCoreApplication.translate("MainWindow", u"Upload folder", None))
        self.uploadFolderPathLabel.setText(QCoreApplication.translate("MainWindow", u"AnothrerPathToDirectory", None))
        self.changeUploadFolderButton.setText(QCoreApplication.translate("MainWindow", u"Change folder", None))
        self.backupFolderLabel.setText(QCoreApplication.translate("MainWindow", u"Backup folder", None))
        self.backupFolderPathLabel.setText(QCoreApplication.translate("MainWindow", u"SomePathToDirectory", None))
        self.changeBackupFolderButton.setText(QCoreApplication.translate("MainWindow", u"Change folder", None))

    # retranslateUi

