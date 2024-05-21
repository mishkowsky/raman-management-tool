import ctypes
import json
import sys
import os
import platform
import threading
from json import JSONDecodeError
from pathlib import Path
import elevate
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow, QFileDialog, QColorDialog, QMessageBox, QApplication
from waitress import serve
import app.view.modules.resources_rc
from PySide6 import QtCore, QtGui, QtWidgets
from loguru import logger
from app.config import THREAD_LOGGER_FORMAT, SERVER_ADDRESS
from app.model.measurements_table import MeasurementsTable
from app.network import server
from app.network.firewall import Firewall, HotspotInterfaceIndexNotFoundException
from app.network.lan_setup import stopHotspot, setupLANInfrastructure, FirewallThreadException
from app.view.modules import UiMainWindow, Settings, UIFunctions
from app.view.modules.styles import MAIN_STYLE, MATPLOT_WIDGET_STYLESHEET
from app.network.server import serverApp
from app.model.measurement import Measurement
from app.model.file_tree_selector import FileTreeSelectorModel
from app.view.widgets.dialogs.firewall_exception import FirewallExceptionDialog
from app.view.widgets.dialogs.hotspot_exception_dialog import HotspotExceptionDialog
from app.view.widgets.dialogs.warn_to_check_dd_wrt_connection import CheckDDWrtConnectionDialog
from app.view.widgets.matplot.view import MatplotLayout


os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%

CONFIG_FILENAME = 'config'


class MainWindow(QMainWindow):
    def __init__(self, firewall: Firewall):
        self.currentDialog = None
        self.firewall = firewall
        QMainWindow.__init__(self, parent=None)
        self.measureTableModel = MeasurementsTable()
        root_path = os.getcwd()
        self.fileSystemModel = FileTreeSelectorModel(rootpath=root_path, parent=None)

        self.dragPos = None
        self.ui = UiMainWindow()

        QtCore.QCoreApplication.setOrganizationName('spbstu')
        QtCore.QCoreApplication.setApplicationName('raman_management_tool')

        self.ui.setupUi(self, style=MAIN_STYLE)

        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        title = "Raman management tool"
        description = "Raman management tool"
        self.setWindowTitle(title)
        self.ui.titleRightInfo.setText(description)

        # SPLITTER #1: TREEVIEW/SPLITTER #2
        width = self.ui.splitter_2.width()
        self.ui.splitter_2.setSizes([width * 1 / 4, width * 3 / 4])
        self.ui.splitter_2.setCollapsible(0, False)
        self.ui.splitter_2.setCollapsible(1, False)

        # SPLITTER #2: MATPLOT/TABLE
        height = self.ui.splitter.height()
        self.ui.splitter.setSizes([height / 2, height / 2])
        self.ui.splitter.setCollapsible(0, False)
        self.ui.splitter.setCollapsible(1, False)

        # CONNECT BUTTON HANDLERS
        self.ui.countAverageButton.clicked.connect(self.countAverageButtonHandler)
        self.ui.viewMeasureButton.clicked.connect(self.viewMeasureButtonHandler)
        self.ui.changeWorkDirButton.clicked.connect(self.changeRootFolderButtonHandler)
        self.ui.changeBackupFolderButton.clicked.connect(self.changeBackupFolderButtonHandler)
        self.ui.changeUploadFolderButton.clicked.connect(self.changeUploadFolderButtonHandler)
        self.ui.normalizeButton.clicked.connect(self.normalizeButtonHandler)
        self.ui.settingsTopBtn.setCheckable(True)
        self.ui.settingsTopBtn.released.connect(self.settingsTopButtonHandler)

        # TREEVIEW
        self.ui.treeView.setupPalette()

        # MATPLOT
        self.matplotLayout = MatplotLayout(self.ui.matplotWidget, self.measureTableModel)
        self.ui.matplotWidget.setLayout(self.matplotLayout.getLayout())
        self.ui.matplotWidget.setStyleSheet(MATPLOT_WIDGET_STYLESHEET)
        if self.matplotLayout.canvas.tightLayout:
            self.matplotLayout.canvas.fig.tight_layout()
            self.matplotLayout.canvas.fig.canvas.draw()
        for action in self.matplotLayout.toolbar.actions():
            if action.text() == 'Delete':
                action.triggered.connect(self.removeLinesFromPlot)
            elif action.text() == 'Brush':
                action.triggered.connect(self.changeSelectedLineColor)
            elif action.text() == 'Resize':
                action.triggered.connect(self.matplotLayout.canvas.resizeVerticalAxes)

        UIFunctions.uiDefinitions(self)

        self.readConfig()
        self.show()

        self.runServer()
        self.ui.stackedWidget.setCurrentWidget(self.ui.mainPage)

    def settingsTopButtonHandler(self):
        state = self.ui.settingsTopBtn.isChecked()
        logger.debug(state)
        self.ui.settingsTopBtn.setDown(state)
        if state:
            self.ui.stackedWidget.setCurrentWidget(self.ui.settingsPage)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.mainPage)

    def changeRootFolderButtonHandler(self):
        self.currentDialog = QFileDialog()
        path = self.currentDialog.getExistingDirectory(self, 'Select new working directory')
        if path:
            newRoot = self.fileSystemModel.setRootPath(path)
            self.ui.treeView.setRootIndex(newRoot)
            self.currentDialog = None
            return path
        self.currentDialog = None

    def changeUploadFolderButtonHandler(self):
        self.currentDialog = QFileDialog()
        path = self.currentDialog.getExistingDirectory(self, 'Select where new measurements will be uploaded')
        if path:
            logger.debug(path)
            self.ui.uploadFolderPathLabel.setText(path)
            self.editConfigVariable('uploadFolder', path)
            server.uploadFolder = path
            self.currentDialog = None
            return path
        self.currentDialog = None

    def changeBackupFolderButtonHandler(self):
        self.currentDialog = QFileDialog()
        path = self.currentDialog.getExistingDirectory(self, 'Select new backup folder')
        if path:
            logger.debug(path)
            self.ui.backupFolderPathLabel.setText(path)
            self.editConfigVariable('backupFolder', path)
            self.currentDialog = None
        self.currentDialog = None

    @staticmethod
    def editConfigVariable(variableName, value):
        dataPath = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppConfigLocation)
        logger.debug(dataPath)
        dataPathDir = QtCore.QDir(dataPath)
        if not dataPathDir.exists():
            dataPathDir.mkpath('.')
        try:
            with open(f'{dataPath}/{CONFIG_FILENAME}', 'r') as file:
                jsonString = file.read()
                configDict = json.loads(jsonString)
        except (FileNotFoundError, JSONDecodeError):
            configDict = {}
        configDict[variableName] = value
        with open(f'{dataPath}/{CONFIG_FILENAME}', 'w') as file:
            textToWrite = json.dumps(configDict, indent=4, sort_keys=True)
            file.write(textToWrite)

    def readConfig(self):
        dataPath = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppConfigLocation)
        logger.debug(dataPath)
        dataPathDir = QtCore.QDir(dataPath)
        if not dataPathDir.exists():
            dataPathDir.mkpath('.')
        try:
            with open(f'{dataPath}/{CONFIG_FILENAME}', 'r') as file:
                jsonString = file.read()
                configDict = json.loads(jsonString)
        except (FileNotFoundError, JSONDecodeError):
            configDict = {}
        uploadPath = configDict.get('uploadFolder', 'Folder is not defined!')
        self.ui.uploadFolderPathLabel.setText(uploadPath)
        backupPath = configDict.get('backupFolder', 'Folder is not defined!')
        self.ui.backupFolderPathLabel.setText(backupPath)

    def viewMeasureButtonHandler(self):
        logger.debug('viewMeasureButton WAS PRESSED')
        chosenFilesPaths = self.fileSystemModel.getCheckedFilesPaths()
        logger.debug(chosenFilesPaths)
        for filePath in chosenFilesPaths:
            try:
                m = Measurement()
                m.loadFromFile(filePath)
                self.viewMeasurement(m)
            except JSONDecodeError:
                logger.debug('FILE WRONG FORMAT')

    def viewMeasurement(self, measurement: Measurement):
        if measurement in self.measureTableModel.measurements:
            return
        line = self.matplotLayout.canvas.addMeasurementGraphic(measurement)
        rgbColor = list(int(line.get_color().lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        qColor = QtGui.QBrush(QColor(rgbColor[0], rgbColor[1], rgbColor[2]))
        self.measureTableModel.addNewMeasurement(measurement, qColor)
        self.ui.measureTableView.updateHeaderState()
        self.ui.measureTableView.header.updateGeometries()

    def changeSelectedLineColor(self):
        selectedColor = QColorDialog.getColor()
        if selectedColor:
            self.matplotLayout.canvas.changeSelectedLinesColor(selectedColor.name())
            self.measureTableModel.changeSelectedLinesColor(selectedColor)
            logger.debug(selectedColor.name())

    def countAverageButtonHandler(self):
        logger.debug('countAverageButton WAS PRESSED')
        filesToCount = self.fileSystemModel.getCheckedFilesPaths()
        if len(filesToCount) <= 1:
            self.showChooseFilesMessage()
            return
        longestParentPath = ''
        for file in filesToCount:
            parentPath = Path(file).parent
            if len(str(parentPath)) > len(str(longestParentPath)):
                longestParentPath = parentPath
        self.currentDialog = QFileDialog()

        fileName, _ = self.currentDialog.getSaveFileName(self, "Select file to save average", f"{longestParentPath}",
                                                  "Text Files (*.txt)")  # , options=options)
        if fileName:
            if not fileName.endswith('.txt'):
                fileName = f'{fileName}.txt'
            logger.debug(f'SELECTED FILE {fileName}')
            measurementsList = []
            for file in filesToCount:
                m = Measurement()
                m.loadFromFile(file)
                measurementsList.append(m)
            Measurement.countAverageAndSave(measurementsList, fileName)
        self.currentDialog = None

    def normalizeButtonHandler(self):
        filesToNormalize = self.fileSystemModel.getCheckedFilesPaths()
        lastFolder = ''
        lastChosenFolder = None
        for file in filesToNormalize:
            p = Path(file)
            fileName = p.stem
            folder = p.parent
            if folder == lastFolder and lastChosenFolder is not None:
                folder = lastChosenFolder
            self.currentDialog = QFileDialog()
            filePath, _ = self.currentDialog.getSaveFileName(self, f"Please select file to save normalized {fileName} measurement",
                                                      f"{folder}/{fileName} (Normalized)",
                                                      "Text Files (*.txt)")  # , options=options)
            lastFolder = p.parent
            if filePath:
                lastChosenFolder = Path(filePath).parent
                if not filePath.endswith('.txt'):
                    filePath = f'{filePath}.txt'
                logger.debug(f'SELECTED FILE {filePath}')
                m = Measurement()
                m.loadFromFile(file)
                m.normalizeAndSave(filePath)
            self.currentDialog = None

    def showChooseFilesMessage(self):
        msgBox = QMessageBox(icon=QMessageBox.Icon.Information,
                             text="Please choose more than 1 measurement in filesystem tree to count average",
                             title="Not enough measurements to count")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.currentDialog = msgBox
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.StandardButton.Ok:
            logger.debug('OK clicked')
        self.currentDialog = None

    def removeLinesFromPlot(self):
        logger.debug('REMOVE BUTTON PRESSED')
        measurementsToRemove = self.measureTableModel.getSelectedMeasurements()
        self.measureTableModel.removeSelectedMeasurements()
        logger.debug(measurementsToRemove)
        self.matplotLayout.canvas.removeMeasurementLines(measurementsToRemove)
        self.ui.measureTableView.updateHeaderState()

    def resizeEvent(self, event):
        UIFunctions.resize_grips(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    @QtCore.Slot(QtCore.QModelIndex)
    def on_treeView_doubleClicked(self, index):
        logger.debug('AAAAAAAAA')
        if os.path.isfile(self.fileSystemModel.filePath(index)):
            lastState = self.fileSystemModel.data(index, QtCore.Qt.ItemDataRole.CheckStateRole)
            newState = QtCore.Qt.CheckState.Checked \
                if lastState == QtCore.Qt.CheckState.Unchecked else QtCore.Qt.CheckState.Unchecked
            self.fileSystemModel.setData(index, newState, QtCore.Qt.ItemDataRole.CheckStateRole)

    def close(self):
        super().close()

    def runServer(self):

        dataPath = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppConfigLocation)
        logger.debug(dataPath)
        dataPathDir = QtCore.QDir(dataPath)
        if not dataPathDir.exists():
            dataPathDir.mkpath('.')
        if not os.path.isfile(f'{dataPath}/{CONFIG_FILENAME}'):
            # self.changeBackupFolderButtonHandler()
            self.changeUploadFolderButtonHandler()
        with open(f'{dataPath}/{CONFIG_FILENAME}', 'r') as file:
            jsonString = file.read()
        try:
            configDict = json.loads(jsonString)
            path = configDict['uploadFolder']
        except (JSONDecodeError, KeyError):
            path = self.changeUploadFolderButtonHandler()

        logger.debug(f'WE GOT PATH: {path}')

        server.uploadFolder = path

        thread = threading.Thread(target=serve, kwargs={'serverApp': serverApp, 'port': 80, 'host': SERVER_ADDRESS})
        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    elevate.elevate(show_console=False)
    app = QApplication()
    logger.remove()
    logger.add(sys.stdout, format=THREAD_LOGGER_FORMAT)
    firewall_ = Firewall()
    try:
        setupLANInfrastructure(firewall_)
    except FirewallThreadException:
        w = FirewallExceptionDialog()
        dialogCode = w.exec()
        if not dialogCode:
            sys.exit()

        stopHotspot()
        SERVER_ADDRESS = '192.168.1.111'
        window = MainWindow(firewall_)
        sys.exit(app.exec())
    except HotspotInterfaceIndexNotFoundException:
        w = HotspotExceptionDialog()
        w.show()
        sys.exit(app.exec())
    window = MainWindow(firewall_)
    sys.exit(app.exec())
