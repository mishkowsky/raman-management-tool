
from PySide6 import QtCore
from PySide6.QtCore import QAbstractTableModel
from PySide6.QtGui import Qt, QBrush
from loguru import logger

from app.model.measurement import Measurement


class MeasurementsTable(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.defaultState: Qt.CheckState = Qt.CheckState.Checked
        self.checkStates: list[Qt.CheckState] = []
        self.measurements: list[Measurement] = []
        self.colors: list[QBrush] = []

    def addNewMeasurement(self, measurement: Measurement, color: QBrush):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.measurements), len(self.measurements))
        self.measurements.append(measurement)
        self.colors.append(color)
        if self.defaultState == Qt.CheckState.PartiallyChecked:
            newMeasurementState = Qt.CheckState.Unchecked
        else:
            newMeasurementState = self.defaultState
        self.checkStates.append(newMeasurementState)
        newRowIndex = self.rowCount() - 1
        self.dataChanged.emit(self.index(newRowIndex, 0), self.index(newRowIndex, 4))
        self.endInsertRows()

    def removeSelectedMeasurements(self):
        # self.beginRemoveRows(QtCore.QModelIndex(), 0, len(self.measurements) - 1)
        rowsToRemove = []
        i = -1
        for checkState in self.checkStates:
            i += 1
            if checkState == Qt.CheckState.Checked:
                rowsToRemove.append(i)
        rowsToRemove.sort(reverse=True)
        logger.debug(f'ROWS TO REMOVE: {rowsToRemove}')
        for row in rowsToRemove:
            self.beginRemoveRows(QtCore.QModelIndex(), row, row)
            del self.measurements[row]
            del self.checkStates[row]
            del self.colors[row]
            self.dataChanged.emit(self.index(row, 0), self.index(row, 4))
            self.endRemoveRows()
        # self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount(), 4))

    def changeSelectedLinesColor(self, color: QBrush):
        for rowIndex in range(0, self.rowCount()):
            if self.checkStates[rowIndex] == QtCore.Qt.CheckState.Checked:
                self.colors[rowIndex] = color

    def rowCount(self, parent=None):
        return len(self.measurements)

    def columnCount(self, parent=None):
        return 5

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if index.column() == 0:
                return Qt.AlignmentFlag.AlignCenter
        if role == Qt.ItemDataRole.BackgroundRole and index.column() == 1:
            return self.colors[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            column = index.column()
            measurement = self.measurements[row]
            if column == 0:
                return self.checkStates[row]
            elif column == 1:
                return None  # COLOR
            elif column == 2:
                return measurement.name
            elif column == 3:
                return measurement.createDate
                # return measurement.createDate.strftime(Measurement.UI_DATETIME_FORMAT)
            elif column == 4:
                return measurement.loadedFromFilePath
        if role == QtCore.Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            return self.checkStates[index.row()]
        return None

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemFlag.ItemIsUserCheckable | super().flags(index)
        else:
            return super().flags(index)

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if role == QtCore.Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            checkState = QtCore.Qt.CheckState(value)
            self.checkStates[index.row()] = checkState
            self.dataChanged.emit(index, index)
            return True
        return False

    def getSelectedMeasurements(self) -> list[Measurement]:
        selectedMeasurements = []
        for (checkState, measurement) in zip(self.checkStates, self.measurements):
            if checkState == Qt.CheckState.Checked:
                selectedMeasurements.append(measurement)
        return selectedMeasurements

    def getSelectedMeasurementsPaths(self) -> list[str]:
        selectedMeasurementsPaths = []
        for (checkState, measurement) in zip(self.checkStates, self.measurements):
            if checkState == Qt.CheckState.Checked:
                selectedMeasurementsPaths.append(measurement.loadedFromFilePath)
        return selectedMeasurementsPaths

    def getTotalState(self):
        checked = False
        unchecked = False
        for state in self.checkStates:
            if state == Qt.CheckState.Checked:
                checked = True
            if state == Qt.CheckState.Unchecked:
                unchecked = True
        if checked and unchecked:
            return Qt.CheckState.PartiallyChecked
        elif checked and not unchecked:
            return Qt.CheckState.Checked
        elif not checked and unchecked:
            return Qt.CheckState.Unchecked
        else:  # default
            return Qt.CheckState.Checked
