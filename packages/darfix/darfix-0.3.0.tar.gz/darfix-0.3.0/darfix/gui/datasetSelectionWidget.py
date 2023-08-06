# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "02/12/2019"

import logging
import os

from silx.gui import qt
from darfix.core.dataset import Dataset

_logger = logging.getLogger(__file__)


class DatasetSelectionWidget(qt.QTabWidget):
    """
    Widget that creates a dataset from a list of files or from a single filename.
    It lets the user add the first filename of a directory of files, or to
    upload manually each of the files to be read.
    If both options are filled up, only the files in the list of filenames
    are read.
    """
    sigProgressChanged = qt.Signal(int)

    def __init__(self, parent=None):
        qt.QTabWidget.__init__(self, parent)

        # Raw data
        self._rawFilenameData = FilenameSelectionWidget(parent=self)
        self._rawFilesData = FilesSelectionWidget(parent=self)
        self._filterDataCB = qt.QCheckBox("Filter data", self)
        rawData = qt.QWidget(self)
        rawData.setLayout(qt.QVBoxLayout())
        rawData.layout().addWidget(self._rawFilenameData)
        rawData.layout().addWidget(self._rawFilesData)
        rawData.layout().addWidget(self._filterDataCB)
        self.addTab(rawData, 'raw data')

        self._filterData = False

        # Dark data
        self._darkFilenameData = FilenameSelectionWidget(parent=self)
        self.addTab(self._darkFilenameData, 'dark data')

        self._dataset = None

        self.getRawFilenames = self._rawFilesData.getFiles
        self.getRawFilename = self._rawFilenameData.getFilename
        self.getDarkFilename = self._darkFilenameData.getFilename
        self.setRawFilenames = self._rawFilesData.setFiles
        self.setRawFilename = self._rawFilenameData.setFilename
        self.setDarkFilename = self._darkFilenameData.setFilename

        self._filterDataCB.stateChanged.connect(self.__filterData)

    def loadDataset(self):
        """
        Loads the dataset from the filenames.
        """
        if not self._rawFilesData.getFiles():
            self._dataset = Dataset(raw_filename=self._rawFilenameData.getFilename(),
                                    dark_filename=self._darkFilenameData.getFilename(),
                                    load_data=False, filter_data=self._filterData)
        else:
            self._dataset = Dataset(filenames=self._rawFilesData.getFiles(),
                                    dark_filename=self._darkFilenameData.getFilename(),
                                    load_data=False, filter_data=self._filterData)
        self._dataset.sigProgressChanged.connect(self.updateProgress)
        _logger.info("Loading data urls")
        self._dataset.load_data(0.3)
        _logger.info("Loading data")
        print("Loading data")
        self._dataset.get_data(0.7, 30)

    @property
    def dataset(self):
        return self._dataset

    def updateProgress(self, progress):
        self.sigProgressChanged.emit(progress)

    def __filterData(self, filterData):
        self._filterData = filterData


class FilesSelectionWidget(qt.QWidget):
    """
    Widget used to get one or more files from the computer and add them to a list.
    """
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        self._files = []

        self.setLayout(qt.QVBoxLayout())
        self._table = self._init_table()
        self._addButton = qt.QPushButton("Add")
        self._rmButton = qt.QPushButton("Remove")
        self.layout().addWidget(self._table)
        self.layout().addWidget(self._addButton)
        self.layout().addWidget(self._rmButton)
        self._addButton.clicked.connect(self._addFiles)
        self._rmButton.clicked.connect(self._removeFiles)

    def _init_table(self):

        table = qt.QTableWidget(0, 1, parent=self)
        table.horizontalHeader().hide()
        # Resize horizontal header to fill all the column size
        if hasattr(table.horizontalHeader(), 'setSectionResizeMode'):  # Qt5
            table.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        else:  # Qt4
            table.horizontalHeader().setResizeMode(0, qt.QHeaderView.Stretch)

        return table

    def _addFiles(self):
        """
        Opens the file dialog and let's the user choose one or more files.
        """
        dialog = qt.QFileDialog(self)
        dialog.setFileMode(qt.QFileDialog.ExistingFiles)

        if not dialog.exec_():
            dialog.close()
            return

        for file in dialog.selectedFiles():
            self.addFile(file)

    def _removeFiles(self):
        """
        Removes the selected items from the table.
        """
        selectedItems = self._table.selectedItems()
        if selectedItems is not None:
            for item in selectedItems:
                self._files.remove(item.text())
                self._table.removeRow(item.row())

    def addFile(self, file):
        """
        Adds a file to the table.

        :param str file: filepath to add to the table.
        """
        assert (os.path.isfile(file))
        item = qt.QTableWidgetItem()
        item.setText(file)
        row = self._table.rowCount()
        self._table.setRowCount(row + 1)
        self._table.setItem(row, 0, item)
        self._files.append(file)

    def getFiles(self):
        return self._files

    def setFiles(self, files):
        """
        Adds a list of files to the table.

        :param array_like files: List to add
        """
        for file in files:
            self.addFile(file)


class FilenameSelectionWidget(qt.QWidget):
    """
    Widget used to obtain a filename (manually or from a file)
    """

    filenameChanged = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        self._filename = qt.QLineEdit('', parent=self)
        self._filename.editingFinished.connect(self.filenameChanged)
        self._addButton = qt.QPushButton("Upload file", parent=self)
        # self._okButton =  qt.QPushButton("Ok", parent=self)
        self._addButton.pressed.connect(self._uploadFilename)
        # self._okButton.pressed.connect(self.close)
        self.setLayout(qt.QHBoxLayout())

        self.layout().addWidget(self._filename)
        self.layout().addWidget(self._addButton)
        # self.layout().addWidget(self._okButton)

    def _uploadFilename(self):
        """
        Loads the file from a FileDialog.
        """
        fileDialog = qt.QFileDialog()

        fileDialog.setFileMode(qt.QFileDialog.ExistingFile)
        if fileDialog.exec_():
            self._filename.setText(fileDialog.selectedFiles()[0])
            self.filenameChanged.emit()
        else:
            _logger.warning("Could not open file")

    def getFilename(self):
        return str(self._filename.text())

    def setFilename(self, filename):
        self._filename.setText(str(filename))
