import os

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QRect, QAbstractItemModel, QSortFilterProxyModel
from PySide6.QtGui import Qt, QColor, QPalette, QMouseEvent
from PySide6.QtWidgets import QHeaderView, QAbstractItemView, QApplication, QTableView, \
    QStyleOptionButton, QStyledItemDelegate, QCheckBox, QStyle
from loguru import logger

from app.model.measurement import Measurement
from app.model.measurements_table import MeasurementsTable
from app.view.modules.styles import MAIN_STYLE


class MyHeader(QHeaderView):

    state = Qt.CheckState.Checked

    def __init__(self, orientation, model: MeasurementsTable, parent=None):
        QHeaderView.__init__(self, orientation, parent)
        self.setStretchLastSection(True)
        self.setHighlightSections(False)
        self.setSectionsClickable(True)
        self.model = model
        self.setObjectName("tableHeader")
        self.setSortIndicatorShown(False)

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        QHeaderView.paintSection(self, painter, rect, logicalIndex)
        painter.restore()
        if logicalIndex == 0:
            option = QStyleOptionButton()
            option.rect = QRect(10, 10, 10, 10)
            if self.state == Qt.CheckState.Checked:
                option.state = QtWidgets.QStyle.StateFlag.State_On | QtWidgets.QStyle.StateFlag.State_Enabled
            elif self.state == Qt.CheckState.PartiallyChecked:
                option.state = QtWidgets.QStyle.StateFlag.State_NoChange | QtWidgets.QStyle.StateFlag.State_Enabled
            else:
                option.state = QtWidgets.QStyle.StateFlag.State_Off | QtWidgets.QStyle.StateFlag.State_Enabled
            fakeCheckBox = QCheckBox(self.parent())
            self.style().drawControl(QtWidgets.QStyle.ControlElement.CE_CheckBox, option, painter, fakeCheckBox)

    def mousePressEvent(self, event: QMouseEvent):
        if self.logicalIndexAt(event.pos()) == 0:
            self.setSortIndicatorShown(False)
            if self.state == Qt.CheckState.Unchecked or self.state == Qt.CheckState.PartiallyChecked:
                newState = Qt.CheckState.Checked
            else:
                newState = Qt.CheckState.Unchecked
            self.state = newState
            self.model.defaultState = self.state
            for i in range(0, self.model.rowCount()):
                index = self.model.index(i, 0)
                self.model.setData(index, newState, Qt.ItemDataRole.CheckStateRole)
            self.updateSection(0)
            QHeaderView.mousePressEvent(self, event)
        elif self.logicalIndexAt(event.pos()) == 1:
            self.setSortIndicatorShown(False)
            QHeaderView.mousePressEvent(self, event)
        else:
            QHeaderView.mousePressEvent(self, event)
            self.setSortIndicatorShown(True)

    def updateState(self, newState: Qt.CheckState):
        self.state = newState
        self.updateSection(0)


class MyHeaderModel(QAbstractItemModel):
    def columnCount(self, parent=...) -> int:
        return 5

    def rowCount(self, parent=...) -> int:
        return 0

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if role == Qt.ItemDataRole.TextAlignmentRole and index.column() == 0:
            return Qt.AlignmentFlag.AlignCenter
        else:
            return super().data(index, role)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return ['', 'Color', 'Name', 'Date', 'Path to file'][section]
        return None


class TableView(QTableView):
    hoverIndexChangedSignal = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self, parent, model: MeasurementsTable):
        super().__init__(parent=parent)
        # self.setModel(model)
        proxy = RenderTypeProxyModel(model, self)
        self.setModel(proxy)
        self.tableModel = model
        self.setSortingEnabled(True)
        self.verticalHeader().setVisible(False)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.header: MyHeader = MyHeader(QtCore.Qt.Orientation.Horizontal, model, self)
        self.setHorizontalHeader(self.header)
        self.header.setModel(MyHeaderModel())
        self.setWordWrap(False)
        self.setTextElideMode(Qt.TextElideMode.ElideLeft)
        for i in range(0, 6):
            self.header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        self.header.setSizeAdjustPolicy(QHeaderView.SizeAdjustPolicy.AdjustToContents)
        self.setSizeAdjustPolicy(QHeaderView.SizeAdjustPolicy.AdjustToContents)
        delegate = Delegate(self)
        self.setItemDelegate(delegate)
        # delegate = DateDelegate(tableView)
        # tableView.setItemDelegateForColumn(3, delegate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(221, 221, 221))
        self.setPalette(palette)
        self.setObjectName(u"measureList")
        self.setEnabled(True)
        self.setMouseTracking(True)
        self.hoverIndexChangedSignal.connect(delegate.onHoverIndexChanged)
        self.clickedIndex = None
        self.horizontalHeader().setSortIndicatorShown(False)

    def dataChanged(self, topLeft, bottomRight, roles=...) -> None:
        logger.debug('DATA CHANGED CALLED')
        self.updateHeaderState()
        self.header.updateGeometries()
        selectedIndexes = self.selectionModel().selectedRows()
        if topLeft.column() == 0 and topLeft in selectedIndexes and topLeft == self.clickedIndex:
            clickedIndexState = self.model().data(topLeft, Qt.ItemDataRole.CheckStateRole)
            for index in selectedIndexes:
                if index != self.clickedIndex:
                    self.model().setData(index, clickedIndexState, Qt.ItemDataRole.CheckStateRole)
        super().dataChanged(topLeft, bottomRight, roles)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        index = self.indexAt(event.pos())
        self.hoverIndexChangedSignal.emit(index)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.clickedIndex = self.indexAt(event.pos())
        super().mouseReleaseEvent(event)

    def updateHeaderState(self):
        newState = self.tableModel.getTotalState()
        logger.debug(f'UPDATING HEADER NEW STATE IS {newState}')
        self.header.updateState(newState)
        self.tableModel.defaultState = self.header.state


class Delegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent=parent)
        self.hoveredRow = -1

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.column() == 3:
            option.text = index.data().strftime(Measurement.UI_DATETIME_FORMAT)

    def onHoverIndexChanged(self, index: QtCore.QModelIndex):
        self.hoveredRow = index.row()

    def paint(self, painter, option, index):
        painter.save()
        adjusted_option = option
        if index.column() == 1:
            b = index.data(Qt.ItemDataRole.BackgroundRole)
            if b is None:
                painter.restore()
                QStyledItemDelegate.paint(self, painter, adjusted_option, index)
                return
            rect = QtCore.QRect(option.rect.left(), option.rect.top(), option.rect.width(), option.rect.height())
            brush = QtGui.QBrush(b)
            painter.fillRect(rect, brush)
            adjusted_option.backgroundBrush = QtGui.QBrush(QtCore.Qt.BrushStyle.NoBrush)
            painter.restore()
            return
        if index.row() == self.hoveredRow:
            painter.fillRect(option.rect, QColor(76, 82, 96))
            option.state = option.state & ~QStyle.StateFlag.State_Selected
        elif option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, QColor(62, 67, 79))
            option.state = option.state & ~QStyle.StateFlag.State_Selected
        else:
            painter.fillRect(option.rect, QColor(40, 44, 52))

        QStyledItemDelegate.paint(self, painter, adjusted_option, index)


class RenderTypeProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, model, parent=None):
        super(RenderTypeProxyModel, self).__init__(parent)
        self.setSourceModel(model)

    def lessThan(self, source_left, source_right) -> bool:
        if source_left.column() == 3:
            leftDate = self.sourceModel().data(source_left, Qt.ItemDataRole.DisplayRole)
            rightDate = self.sourceModel().data(source_right, Qt.ItemDataRole.DisplayRole)
            return leftDate < rightDate
        else:
            return super().lessThan(source_left, source_right)
