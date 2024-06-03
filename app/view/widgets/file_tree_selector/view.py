import os
import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QFileDialog, QTreeView
from loguru import logger

from app.model.file_tree_selector import FileTreeSelectorModel
from app.view.modules.styles import MAIN_STYLE


class FileSystemTreeView(QTreeView):

    def __init__(self, parent, model: FileTreeSelectorModel):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setAnimated(False)
        self.setSortingEnabled(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setItemDelegate(StyledItemDelegate(self))
        self.setModel(model)
        self.setRootIndex(model.parent_index)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)

    def setupPalette(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(221, 221, 221))
        self.setPalette(palette)


class StyledItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parentView):
        super().__init__()
        self.view = parentView

    def editorEvent(self, event, model, option, index):
        lastState = index.data(QtCore.Qt.ItemDataRole.CheckStateRole)

        val = super(StyledItemDelegate, self).editorEvent(event, model, option, index)

        newState = index.data(QtCore.Qt.ItemDataRole.CheckStateRole)
        if lastState != newState:
            selectedIndexes = self.view.selectedIndexes()
            if index in selectedIndexes:
                for selectedIndex in selectedIndexes:
                    model.setData(selectedIndex, newState, QtCore.Qt.ItemDataRole.CheckStateRole)
            logger.debug(self.view.selectedIndexes())
            return val
        return val


class FileTreeSelectorDialog(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        windowlayout = QtWidgets.QVBoxLayout(self)
        self.setLayout(windowlayout)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.setStyleSheet(MAIN_STYLE)

        self.setStyleSheet("""
            border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 
                rgba(255, 121, 198, 255), 
                stop:0.5 rgba(85, 170, 255, 0));
            background-color: rgb(40, 44, 52);
        """)

        self.root_path = os.getcwd()

        # Widget
        self.title = "My Window"
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 640

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Button
        self.button = QtWidgets.QPushButton('Change root folder', parent=self)
        self.button.clicked.connect(self.changeRootFolderButtonHandler)

        # Model
        self.model = FileTreeSelectorModel(rootpath=self.root_path)
        self.model.removeColumn(2)
        self.model.removeColumn(1)
        self.model.dataChanged.emit(self.model, self.model)

        # View
        self.view = FileSystemTreeView(parent=self, model=self.model)
        self.view.setStyleSheet(MAIN_STYLE)
        self.view.setupPalette()

        # GUI
        windowlayout.addWidget(self.button)
        windowlayout.addWidget(self.view)

        self.show()

    def changeRootFolderButtonHandler(self):
        path = QFileDialog.getExistingDirectory(self, 'Select new working directory')
        if path:
            newRoot = self.model.setRootPath(path)
            self.view.setRootIndex(newRoot)
            logger.debug(f'NEW PATH IS {path}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = FileTreeSelectorDialog()
    sys.exit(app.exec())
