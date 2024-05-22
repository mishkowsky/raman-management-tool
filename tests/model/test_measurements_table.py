
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush

from app.model.measurement import Measurement
from app.model.measurements_table import MeasurementsTable


class TestMeasurementsTable:

    def testAddNewMeasurement(self):
        m = Measurement()
        m.name = 'TEST'
        table = MeasurementsTable()
        color = QBrush(Qt.GlobalColor.black)
        table.addNewMeasurement(m, color)
        assert table.rowCount() == 1

        measurementTitleIndex = table.index(0, 2)
        assert table.data(measurementTitleIndex, Qt.ItemDataRole.DisplayRole) == 'TEST'

        table.defaultState = Qt.CheckState.PartiallyChecked
        table.addNewMeasurement(Measurement(), color)
        measurementStateIndex = table.index(1, 0)
        assert table.data(measurementStateIndex, Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Unchecked

    def testRemoveSelectedMeasurements(self):
        m1 = Measurement()
        m1.name = '1'
        m2 = Measurement()
        m2.name = '2'

        table = MeasurementsTable()
        table.addNewMeasurement(m1, QBrush(Qt.GlobalColor.black))
        table.addNewMeasurement(m2, QBrush(Qt.GlobalColor.white))
        assert table.rowCount() == 2

        m2CheckBoxIndex = table.index(1, 0)
        table.setData(m2CheckBoxIndex, Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        assert len(table.getSelectedMeasurements()) == 1

        table.removeSelectedMeasurements()
        assert table.rowCount() == 1
        assert len(table.getSelectedMeasurements()) == 0

    def testChangeSelectedLinesColor(self):
        m1 = Measurement()
        m1.name = '1'
        m2 = Measurement()
        m2.name = '2'

        table = MeasurementsTable()
        table.addNewMeasurement(m1, QBrush(Qt.GlobalColor.black))
        table.addNewMeasurement(m2, QBrush(Qt.GlobalColor.white))

        newColor = QBrush(Qt.GlobalColor.black)
        table.changeSelectedLinesColor(newColor)

        for i in range(0, table.rowCount()):
            colorIndex = table.index(i, 1)
            color = table.data(colorIndex, Qt.ItemDataRole.BackgroundRole)
            assert color == newColor

    def testRowCount(self):
        table = MeasurementsTable()
        assert table.rowCount() == 0

        table.addNewMeasurement(Measurement(), QBrush(Qt.GlobalColor.black))
        assert table.rowCount() == 1

    def testColumnCount(self):
        table = MeasurementsTable()
        assert table.columnCount() == 5

    def testData(self):
        m = Measurement()
        name = 'TEST'
        m.name = name
        path = 'C:/file.txt'
        m.loadedFromFilePath = path

        table = MeasurementsTable()
        color = QBrush(Qt.GlobalColor.black)
        table.addNewMeasurement(m, color)
        checkStateIndex = table.index(0, 0)
        checkState = table.data(checkStateIndex, Qt.ItemDataRole.CheckStateRole)
        assert checkState == Qt.CheckState.Checked

        checkStateAlignment = table.data(checkStateIndex, Qt.ItemDataRole.TextAlignmentRole)
        assert checkStateAlignment == Qt.AlignmentFlag.AlignCenter

        checkStateDisplay = table.data(checkStateIndex, Qt.ItemDataRole.DisplayRole)
        assert checkStateDisplay == Qt.CheckState.Checked

        colorIndex = table.index(0, 1)
        colorData = table.data(colorIndex, Qt.ItemDataRole.BackgroundRole)
        assert color == colorData

        colorDisplay = table.data(colorIndex, Qt.ItemDataRole.DisplayRole)
        assert colorDisplay is None

        nameIndex = table.index(0, 2)
        nameData = table.data(nameIndex, Qt.ItemDataRole.DisplayRole)
        assert name == nameData

        dateIndex = table.index(0, 3)
        dateData = table.data(dateIndex, Qt.ItemDataRole.DisplayRole)
        assert m.createDate == dateData

        pathIndex = table.index(0, 4)
        pathData = table.data(pathIndex, Qt.ItemDataRole.DisplayRole)
        assert m.loadedFromFilePath == pathData

        userRole = table.data(pathIndex, Qt.ItemDataRole.UserRole)
        assert userRole is None

    def testFlags(self):

        table = MeasurementsTable()
        table.addNewMeasurement(Measurement(), QBrush(Qt.GlobalColor.black))

        firstColumnIndex = table.index(0, 0)
        firstColumnFlags = table.flags(firstColumnIndex)
        assert firstColumnFlags & Qt.ItemFlag.ItemIsUserCheckable

        secondColumnIndex = table.index(0, 1)
        secondColumnFlags = table.flags(secondColumnIndex)
        assert secondColumnFlags & Qt.ItemFlag.ItemIsEnabled

    def testSetData(self):
        table = MeasurementsTable()
        table.addNewMeasurement(Measurement(), QBrush(Qt.GlobalColor.black))

        state = table.checkStates[0]
        assert state == Qt.CheckState.Checked

        firstColumnIndex = table.index(0, 0)
        table.setData(firstColumnIndex, Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)

        state = table.checkStates[0]
        assert state == Qt.CheckState.Unchecked

        assert not table.setData(firstColumnIndex, Qt.ItemDataRole.UserRole)

    def testGetSelectedMeasurements(self):
        m1 = Measurement()
        m1.name = '1'
        m1.loadedFromFilePath = '1'
        m2 = Measurement()
        m2.name = '2'
        m2.loadedFromFilePath = '2'

        table = MeasurementsTable()
        table.addNewMeasurement(m1, QBrush(Qt.GlobalColor.black))
        table.addNewMeasurement(m2, QBrush(Qt.GlobalColor.white))

        selectedMeasurements = table.getSelectedMeasurements()
        assert {m1, m2} == set(selectedMeasurements)

        index = table.index(0, 0)
        table.setData(index, Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        selectedMeasurements = table.getSelectedMeasurements()
        assert [m2] == selectedMeasurements

        index = table.index(1, 0)
        table.setData(index, Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        selectedMeasurements = table.getSelectedMeasurements()
        assert [] == selectedMeasurements

    def testGetSelectedMeasurementsPaths(self):
        m = Measurement()
        m.name = '1'
        m.loadedFromFilePath = '1'

        table = MeasurementsTable()
        table.addNewMeasurement(m, QBrush(Qt.GlobalColor.black))

        selectedMeasurementsPaths = table.getSelectedMeasurementsPaths()
        assert ['1'] == selectedMeasurementsPaths

    def testGetTotalState(self):
        m1 = Measurement()
        m1.name = '1'
        m1.loadedFromFilePath = '1'
        m2 = Measurement()
        m2.name = '2'
        m2.loadedFromFilePath = '2'

        table = MeasurementsTable()
        assert table.getTotalState() == Qt.CheckState.Checked

        table.addNewMeasurement(m1, QBrush(Qt.GlobalColor.black))
        table.addNewMeasurement(m2, QBrush(Qt.GlobalColor.white))

        assert Qt.CheckState.Checked == table.getTotalState()

        index = table.index(0, 0)
        table.setData(index, Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        assert Qt.CheckState.PartiallyChecked == table.getTotalState()

        index = table.index(1, 0)
        table.setData(index, Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        assert Qt.CheckState.Unchecked == table.getTotalState()
