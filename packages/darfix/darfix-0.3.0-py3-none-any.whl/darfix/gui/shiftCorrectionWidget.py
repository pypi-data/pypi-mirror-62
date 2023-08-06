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
__date__ = "23/07/2019"

# import os
import numpy

from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot.StackView import StackViewMainWindow

import darfix
from darfix.core.imageRegistration import shift_correction, shift_detection

from .operationThread import OperationThread
from .utils import ChooseDimensionDock


class ShiftCorrectionWidget(qt.QMainWindow):
    """
    A widget to apply shift correction to a stack of images
    """
    sigComputed = qt.Signal()
    sigProgressChanged = qt.Signal(int)

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)

        self.setWindowFlags(qt.Qt.Widget)

        self.thread_detection = OperationThread(shift_detection)
        self.thread_correction = OperationThread(shift_correction)
        self._shift = [0, 0]
        self._shift2dataset = True

        self._inputDock = _InputDock()
        self._inputDock.widget.correctionB.setEnabled(False)

        self._sv = StackViewMainWindow()
        self._sv.setColormap(Colormap(name=darfix.config.DEFAULT_COLORMAP_NAME,
                                      normalization='linear',
                                      vmin=None,
                                      vmax=None))
        self.setCentralWidget(self._sv)
        self._chooseDimensionDock = ChooseDimensionDock(self)
        spacer1 = qt.QWidget(parent=self)
        spacer1.setLayout(qt.QVBoxLayout())
        spacer1.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        spacer2 = qt.QWidget(parent=self)
        spacer2.setLayout(qt.QVBoxLayout())
        spacer2.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self._chooseDimensionDock.widget.layout().addWidget(spacer1)
        self._inputDock.widget.layout().addWidget(spacer2)
        self._chooseDimensionDock.hide()
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._chooseDimensionDock)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._inputDock)

        self._inputDock.widget.correctionB.clicked.connect(self.correct)
        self._inputDock.widget._findShiftB.clicked.connect(self._findShift)
        self._inputDock.widget.checkbox.stateChanged.connect(self._changeDataShiftFlag)
        self._chooseDimensionDock.widget.filterChanged.connect(self._filterStack)
        self._chooseDimensionDock.widget.stateDisabled.connect(self._wholeStack)

    def setDataset(self, dataset):
        """
        Dataset setter. Saves the dataset and updates the stack with the dataset
        data

        :param Dataset dataset: dataset
        """
        self.dataset = dataset
        self.setStack(dataset.hi_data)
        self._inputDock.widget.correctionB.setEnabled(True)
        if self.dataset.reshaped_data is not None:
            self._chooseDimensionDock.show()
            self._chooseDimensionDock.widget.setDimensions(self.dataset.dims)

    def correct(self):
        """
        Function that starts the thread to compute the shift given
        at the input widget
        """
        dx = self._inputDock.widget.getDx()
        dy = self._inputDock.widget.getDy()
        self.shift = [dx, dy]
        if self._shift2dataset:
            data = self.dataset.hi_data
        else:
            data = self.dataset.get_reshaped_data(self.dimension, self.value)
        frames = numpy.arange(data.shape[0])
        self.thread_correction.setArgs(data, numpy.outer(self.shift, frames))
        self.thread_correction.finished.connect(self._updateData)
        self._inputDock.widget.correctionB.setEnabled(False)
        self.thread_correction.start()

    def updateProgress(self, progress):
        self.sigProgressChanged.emit(progress)

    def _changeDataShiftFlag(self, state):
        self._shift2dataset = state

    def _findShift(self):
        self._inputDock.widget._findShiftB.setEnabled(False)
        self.thread_detection.setArgs(self._sv.getStack()[0])
        self.thread_detection.finished.connect(self._updateShift)
        self.thread_detection.start()

    def _updateShift(self):
        self._inputDock.widget._findShiftB.setEnabled(True)
        self.thread_detection.finished.disconnect(self._updateShift)
        self.shift = self.thread_detection.data[:, 1]

    def _updateData(self):
        """
        Updates the stack with the data computed in the thread
        """
        self.thread_correction.finished.disconnect(self._updateData)
        self._inputDock.widget.correctionB.setEnabled(True)
        data = self.thread_correction.data
        assert data is not None
        self.setStack(data)
        self.sigComputed.emit()

        if self._shift2dataset:
            self.dataset.hi_dataset = data
        else:
            self.dataset.set_reshaped_data(data, self.dimension, self.value)

    def setStack(self, *arg, **kwargs):
        """
        Sets the data passed as aguments in the stack.
        Mantains the current frame showed in the view.
        """
        nframe = self._sv.getFrameNumber()
        self._sv.setStack(*arg, **kwargs)
        self._sv.setFrameNumber(nframe)

    def clearStack(self):
        self._sv.setStack(None)
        self._inputDock.widget.correctionB.setEnabled(False)

    def _filterStack(self, dim=0, val=0):
        self._inputDock.widget.checkbox.show()
        self.dimension = dim
        self.value = val
        data = self.dataset.get_reshaped_data(dim, val)
        if data.shape[0]:
            self.setStack(data)
        else:
            self.setStack(None)

    def _wholeStack(self):
        self._inputDock.widget.checkbox.hide()
        self.setStack(self.dataset.hi_data)

    def getStack(self):
        """
        Stack getter

        :returns: StackViewMainWindow:
        """
        return self._sv

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, shift):
        self._shift = shift
        self._inputDock.widget.setDx(shift[0])
        self._inputDock.widget.setDy(shift[1])


class _InputDock(qt.QDockWidget):

    def __init__(self, parent=None):
        qt.QDockWidget.__init__(self, parent)
        self.widget = _InputWidget()
        self.setWidget(self.widget)


class _InputWidget(qt.QWidget):
    """
    Widget used to obtain the double parameters for the shift correction.
    """
    def __init__(self, parent=None):
        super(_InputWidget, self).__init__(parent)

        self._findShiftB = qt.QPushButton("Find shift")
        labelx = qt.QLabel("Horizontal shift:")
        labely = qt.QLabel("Vertical shift:")
        self.dxLE = qt.QLineEdit("0.0")
        self.dyLE = qt.QLineEdit("0.0")
        self.correctionB = qt.QPushButton("Correct")
        self.checkbox = qt.QCheckBox("Apply to whole dataset")
        self.checkbox.setChecked(True)
        self.checkbox.hide()

        self.dxLE.setValidator(qt.QDoubleValidator())
        self.dyLE.setValidator(qt.QDoubleValidator())

        layout = qt.QGridLayout()

        layout.addWidget(self._findShiftB, 0, 0, 1, 2)
        layout.addWidget(labelx, 1, 0)
        layout.addWidget(labely, 2, 0)
        layout.addWidget(self.dxLE, 1, 1)
        layout.addWidget(self.dyLE, 2, 1)
        layout.addWidget(self.correctionB, 4, 0, 1, 2)
        layout.addWidget(self.checkbox, 3, 1)

        self.setLayout(layout)

    def setDx(self, dx):
        """
        Set the shift in the x axis
        """
        self.dxLE.setText(str(dx))

    def getDx(self):
        """
        Get the shift in the x axis

        :return float:
        """
        return float(self.dxLE.text())

    def setDy(self, dy):
        """
        Set the shift in the x axis
        """
        self.dyLE.setText(str(dy))

    def getDy(self):
        """
        Get the shift in the y axis

        :return float:
        """
        return float(self.dyLE.text())
