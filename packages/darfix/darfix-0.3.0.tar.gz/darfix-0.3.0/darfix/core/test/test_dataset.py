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
__date__ = "11/09/2019"

import copy
import unittest
import numpy
import tempfile
import shutil

from darfix.test import utils
from darfix.core.dataset import Dimension, POSITIONER_METADATA


class TestDataset(unittest.TestCase):

    """Tests for `dataset.py`."""

    def setUp(self):
        self._dir = tempfile.mkdtemp()
        self.dataset = utils.createRandomDataset(dims=(100, 100), nb_data_files=3,
                                                 nb_dark_files=1, header=True, _dir=self._dir)

    def test_data_load(self):
        """ Tests the correct load of the data"""
        self.assertEqual(len(self.dataset.data_urls), 3)
        self.assertEqual(self.dataset.data.ndim, 3)

    def test_dark_load(self):
        """ Tests the correct load of the dark data"""
        self.assertEqual(len(self.dataset.dark_frames), 1)
        self.assertEqual(self.dataset.dark_frames.ndim, 3)

    def test_nframes(self):
        """Tests the nframes method"""
        self.assertEqual(self.dataset.nframes, 3)

    def test_deepcopy(self):
        """Tests the correct deepcopy of the object"""
        dataset_copy = copy.deepcopy(self.dataset)
        self.assertEqual(self.dataset.nframes, dataset_copy.nframes)
        self.assertTrue(numpy.array_equal(self.dataset.data, dataset_copy.data))
        self.assertTrue(numpy.array_equal(self.dataset.dark_frames, dataset_copy.dark_frames))

    def test_filter_data(self):
        """ Tests the correct separation of empty frames and data frames"""
        dims = (10, 100, 100)
        data = numpy.zeros(dims)
        background = numpy.random.random(dims)
        idxs = [0, 2, 4]
        data[idxs] += background[idxs]
        dataset = utils.createDataset(data=data, dark_frames=background,
                                      filter_data=True, _dir=self._dir)

        self.assertEqual(dataset.hi_data.shape[0], 3)
        self.assertEqual(dataset.li_data.shape[0], 7)


class TestDimensions(unittest.TestCase):

    def setUp(self):
        """"
        Creating random dataset with specific headers.
        """
        self._dir = tempfile.mkdtemp()
        counter_mne = "a b c d e f g h"
        motor_mne = "x y z k h m n"
        dims = (10, 100, 100)
        # Create headers
        header = []
        # Dimensions for reshaping
        a = numpy.random.rand(2)
        b = numpy.random.rand(5)
        motors = numpy.random.rand(7)
        for i in numpy.arange(10):
            header.append({})
            header[i]["HeaderID"] = i
            header[i]["counter_mne"] = counter_mne
            header[i]["motor_mne"] = motor_mne
            header[i]["counter_pos"] = ""
            header[i]["motor_pos"] = ""
            for c in counter_mne:
                header[i]["counter_pos"] += str(numpy.random.rand(1)[0]) + " "
            for j, m in enumerate(motor_mne.split()):
                if m == "z":
                    header[i]["motor_pos"] += str(a[i % 2]) + " "
                elif m == "m":
                    header[i]["motor_pos"] += str(b[i % 5]) + " "
                else:
                    header[i]["motor_pos"] += str(motors[j]) + " "

        data = numpy.zeros(dims)
        background = numpy.random.random(dims)
        idxs = [0, 2, 4]
        data[idxs] += background[idxs]
        self.dataset = utils.createDataset(data=data, dark_frames=background,
                                           filter_data=True, header=header, _dir=self._dir)

    def test_add_one_dimension(self):
        """ Tests the correct add of a dimension """

        dimension = Dimension(POSITIONER_METADATA, "test", 20)
        self.dataset.add_dim(0, dimension)
        saved_dimension = self.dataset.dims.get(0)
        self.assertEqual(saved_dimension.name, "test")
        self.assertEqual(saved_dimension.kind, POSITIONER_METADATA)
        self.assertEqual(saved_dimension.size, 20)

    def test_add_several_dimensions(self):
        """ Tests the correct add of several dimensions """

        dimension1 = Dimension(POSITIONER_METADATA, "test1", 20)
        dimension2 = Dimension(POSITIONER_METADATA, "test2", 30)
        dimension3 = Dimension(POSITIONER_METADATA, "test3", 40)

        self.dataset.add_dim(0, dimension1)
        self.dataset.add_dim(1, dimension2)
        self.dataset.add_dim(2, dimension3)
        self.assertEqual(self.dataset.dims.ndim, 3)

    def test_remove_dimension(self):
        """ Tests the correct removal of a dimension """

        dimension = Dimension(POSITIONER_METADATA, "test", 20)
        self.dataset.add_dim(0, dimension)
        self.dataset.remove_dim(0)

        self.assertEqual(self.dataset.dims.ndim, 0)

    def test_remove_dimensions(self):
        """ Tests the correct removal of several dimensions """

        dimension1 = Dimension(POSITIONER_METADATA, "test1", 20)
        dimension2 = Dimension(POSITIONER_METADATA, "test2", 30)
        dimension3 = Dimension(POSITIONER_METADATA, "test3", 40)

        self.dataset.add_dim(0, dimension1)
        self.dataset.add_dim(1, dimension2)
        self.dataset.add_dim(2, dimension3)

        self.dataset.remove_dim(0)
        self.dataset.remove_dim(2)

        self.assertEqual(self.dataset.dims.ndim, 1)
        self.assertEqual(self.dataset.dims.get(1).name, "test2")

    def test_find_dimensions(self):
        """ Tests the correct finding of the dimensions"""

        self.dataset.find_dimensions(POSITIONER_METADATA)
        self.assertEqual(self.dataset.dims.ndim, 2)
        self.assertEqual(self.dataset.dims.get(0).name, "z")
        self.assertEqual(self.dataset.dims.get(1).name, "m")

    def test_reshaped_data(self):
        """ Tests the correct reshaping of the data """
        self.dataset.find_dimensions(POSITIONER_METADATA)

        self.dataset.reshape_data()
        self.assertEqual(self.dataset.reshaped_data.shape, (2, 5, 100, 100))

    def test_data_reshaped_data(self):
        """ Tests that data and reshaped data have same values """
        self.dataset.find_dimensions(POSITIONER_METADATA)
        self.dataset.reshape_data()

        numpy.testing.assert_array_equal(self.dataset.data.flatten(), self.dataset.reshaped_data.flatten())

    def test_clear_dimensions(self):
        """ Tests the clear dimensions function """
        self.dataset.find_dimensions(POSITIONER_METADATA)
        self.dataset.clear_dims()

        self.assertEqual(self.dataset.dims.ndim, 0)

    def tearDown(self):
        shutil.rmtree(self._dir)


if __name__ == '__main__':
    unittest.main()
