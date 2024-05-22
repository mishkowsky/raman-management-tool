import os
from PySide6 import QtWidgets, QtCore, QtGui
from loguru import logger


class FileTreeSelectorModel(QtWidgets.QFileSystemModel):
    def __init__(self, parent=None, rootpath='/'):
        QtWidgets.QFileSystemModel.__init__(self, parent)
        self.root_path = rootpath
        self.checkBoxStatuses: dict[str, QtCore.Qt.CheckState] = {}
        self.parent_index = self.setRootPath(self.root_path)
        self.removeColumn(1)
        self.removeColumn(2)
        self.removeColumn(3)
        self.dataChanged.emit(self, self)
        # self.setFilter(QtCore.QDir.Filter.AllEntries | QtCore.QDir.Filter.Hidden |
        #                QtCore.QDir.Filter.NoDot | QtCore.QDir.Filter.NoDotDot)

    def data(self, index, role=QtCore.Qt.ItemDataRole):
        if role == QtCore.Qt.ItemDataRole.DecorationRole:
            if os.path.isfile(self.filePath(index)):
                return QtGui.QIcon(':/icons/images/icons/cil-file.png')
            else:
                icon = QtGui.QIcon(':/icons/images/icons/cil-folder.png')
                icon.addFile(':/icons/images/icons/cil-folder-open.png', state=QtGui.QIcon.State.On)
                return icon
        if role == QtCore.Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            return self.checkState(index)
        else:
            return QtWidgets.QFileSystemModel.data(self, index, role)

    def flags(self, index):
        return QtWidgets.QFileSystemModel.flags(self, index) | QtCore.Qt.ItemFlag.ItemIsUserCheckable

    def checkState(self, index):
        return self.checkBoxStatuses.get(self.filePath(index), QtCore.Qt.CheckState.Unchecked)

    def setDataForIndex(self, index: QtCore.QModelIndex, value: QtCore.Qt.CheckState):
        checkState = QtCore.Qt.CheckState(value)
        self.checkBoxStatuses[self.filePath(index)] = checkState
        self.dataChanged.emit(index, index)
        logger.debug(f'SETTING {value} FOR {self.filePath(index)}')

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        logger.info(f'SETTING {QtCore.Qt.CheckState(value)} FOR {self.filePath(index)}')
        if role == QtCore.Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            checkState = QtCore.Qt.CheckState(value)
            self.setDataForIndex(index, checkState)
            if self.hasChildren(index):
                self.updateChildrenCheckStates(index, checkState)
            if index.parent().isValid():
                self.updateParentsCheckStates(index)
            return True
        return QtWidgets.QFileSystemModel.setData(self, index, value, role)

    def updateChildrenCheckStates(self, index, value):
        path = self.filePath(index)
        logger.debug(f'setting children checkStates of {path}')
        it = QtCore.QDirIterator(path, self.filter())
        while it.hasNext():
            childIndex = self.index(it.next())
            logger.debug(f'SETTING FOR CHILD DIRECTORY {self.filePath(childIndex)} {value} STATE')
            self.setDataForIndex(childIndex, value)
            if self.hasChildren(childIndex):
                self.updateChildrenCheckStates(childIndex, value)

    def updateParentsCheckStates(self, index):
        logger.debug('setting parents checkStates')
        parentIndex = index.parent()
        siblingsStatus = self.checkSiblingsCheckStates(index)
        logger.debug(f'SETTING FOR PARENT DIRECTORY {self.filePath(parentIndex)} {siblingsStatus} STATE')
        self.setDataForIndex(parentIndex, siblingsStatus)
        if parentIndex.parent().isValid():
            self.updateParentsCheckStates(parentIndex)

    def checkSiblingsCheckStates(self, index):
        checked = False
        unchecked = False
        for row_index in range(self.rowCount(index.parent())):
            sibling = index.siblingAtRow(row_index)
            if self.checkState(sibling) == QtCore.Qt.CheckState.Checked:
                logger.debug(f'SIBLING AT {self.filePath(sibling)} IS Checked')
                checked = True
            elif self.checkState(sibling) == QtCore.Qt.CheckState.Unchecked:
                logger.debug(f'SIBLING AT {self.filePath(sibling)} IS Unchecked')
                unchecked = True
            elif self.checkState(sibling) == QtCore.Qt.CheckState.PartiallyChecked:
                logger.debug(f'SIBLING AT {self.filePath(sibling)} IS PartiallyChecked')
                return QtCore.Qt.CheckState.PartiallyChecked
        if checked and not unchecked:
            return QtCore.Qt.CheckState.Checked
        elif unchecked and not checked:
            return QtCore.Qt.CheckState.Unchecked
        else:
            return QtCore.Qt.CheckState.PartiallyChecked

    def getCheckedFilesPaths(self):
        return [k for k, v in self.checkBoxStatuses.items() if v == QtCore.Qt.CheckState.Checked and os.path.isfile(k)]
