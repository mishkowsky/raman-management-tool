import pytest
from PySide6 import QtCore
from app.model.file_tree_selector import FileTreeSelectorModel


class TestFileTreeSelectorModel:

    TEST_FILES_COUNT = 3

    @pytest.fixture(scope="class", autouse=True)
    def create_files(self, tmp_path_factory):
        for i in range(0, self.TEST_FILES_COUNT):
            tmp_file_path = tmp_path_factory.getbasetemp().joinpath(f"test_file_{i}.txt")
            tmp_file_path.write_text(str(i))
        self.tempDirectory = str(tmp_path_factory.getbasetemp())
        self.model = FileTreeSelectorModel(rootpath=self.tempDirectory)
        self.__class__.tempDirectory = str(tmp_path_factory.getbasetemp())
        self.__class__.model = FileTreeSelectorModel(rootpath=self.tempDirectory)

    def testInit(self):
        assert self.model.root_path == self.tempDirectory

    def testData(self, create_files):
        filename = 'test_file_0.txt'
        filepath = f'{self.tempDirectory}/{filename}'
        index = self.model.index(filepath, column=0)
        data = self.model.data(index, QtCore.Qt.ItemDataRole.DisplayRole)
        assert data == filename

    def testFlags(self):
        filename = 'test_file_0.txt'
        filepath = f'{self.tempDirectory}/{filename}'
        index = self.model.index(filepath, column=0)
        flag = self.model.flags(index)
        assert flag & QtCore.Qt.ItemFlag.ItemIsUserCheckable

    def testCheckState(self):
        filename = 'test_file_0.txt'
        filepath = f'{self.tempDirectory}/{filename}'
        index = self.model.index(filepath, column=0)
        checkState = self.model.checkState(index)
        assert checkState == QtCore.Qt.CheckState.Unchecked

    # def testSetDataForIndex(self):
    #     filename = 'test_file_0.txt'
    #     filepath = f'{self.tempDirectory}/{filename}'
    #     index = self.model.index(filepath, column=0)
    #     self.model.setDataForIndex()
    #     pass

    def testSetData(self):
        filename = 'test_file_0.txt'
        filepath = f'{self.tempDirectory}/{filename}'
        index = self.model.index(filepath, column=0)
        self.model.setData(index, QtCore.Qt.CheckState.Checked, QtCore.Qt.ItemDataRole.CheckStateRole)
        state = self.model.data(index, QtCore.Qt.ItemDataRole.CheckStateRole)
        assert state == QtCore.Qt.CheckState.Checked

    def testUpdateChildrenCheckStates(self):
        index = self.model.index(self.tempDirectory, column=0)
        self.model.setData(index, QtCore.Qt.CheckState.Checked, QtCore.Qt.ItemDataRole.CheckStateRole)
        for i in range(0, self.TEST_FILES_COUNT):
            filepath = f'{self.tempDirectory}/test_file_{i}.txt'
            index = self.model.index(filepath, column=0)
            state = self.model.data(index, QtCore.Qt.ItemDataRole.CheckStateRole)
            assert state == QtCore.Qt.CheckState.Checked

    def testUpdateParentCheckStates(self):
        filename = 'test_file_0.txt'
        filepath = f'{self.tempDirectory}/{filename}'
        index = self.model.index(filepath, column=0)
        self.model.setData(index, QtCore.Qt.CheckState.Checked, QtCore.Qt.ItemDataRole.CheckStateRole)

        filename = 'test_file_1.txt'
        filepath = f'{self.tempDirectory}/{filename}'
        index = self.model.index(filepath, column=0)
        self.model.setData(index, QtCore.Qt.CheckState.Unchecked, QtCore.Qt.ItemDataRole.CheckStateRole)

        parentIndex = self.model.index(self.tempDirectory, column=0)
        parentState = self.model.data(parentIndex, QtCore.Qt.ItemDataRole.CheckStateRole)
        assert parentState == QtCore.Qt.CheckState.PartiallyChecked

    def testCheckSiblingsCheckStates(self):

        for i in range(0, self.TEST_FILES_COUNT):
            filepath = f'{self.tempDirectory}/test_file_{i}.txt'
            index = self.model.index(filepath, column=0)
            self.model.setData(index, QtCore.Qt.CheckState.Checked, QtCore.Qt.ItemDataRole.CheckStateRole)
        index = self.model.index(f'{self.tempDirectory}/test_file_0.txt', column=0)
        assert self.model.checkSiblingsCheckStates(index) == QtCore.Qt.CheckState.Checked

    def testGetCheckedFilesPaths(self):
        tempDirectory = self.tempDirectory.replace('\\', '/')
        index = self.model.index(tempDirectory, column=0)
        self.model.setData(index, QtCore.Qt.CheckState.Unchecked, QtCore.Qt.ItemDataRole.CheckStateRole)
        assert self.model.getCheckedFilesPaths() == []

        checkedFilePaths = []
        for i in range(0, self.TEST_FILES_COUNT):
            filepath = f'{tempDirectory}/test_file_{i}.txt'
            index = self.model.index(filepath, column=0)
            self.model.setData(index, QtCore.Qt.CheckState.Checked, QtCore.Qt.ItemDataRole.CheckStateRole)
            checkedFilePaths.append(filepath)

        assert set(self.model.getCheckedFilesPaths()) == set(checkedFilePaths)
