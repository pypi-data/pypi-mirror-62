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
__date__ = "10/09/2019"


import unittest

import numpy

from darfix.core import imageOperations


class TestImageOperations(unittest.TestCase):

    """Tests for `imageOperations.py`."""

    @classmethod
    def setUpClass(cls):

        cls.data = numpy.array([[[1, 2, 3, 4, 5],
                                 [2, 2, 3, 4, 5],
                                 [3, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 5]],
                                [[1, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 3],
                                 [1, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 5]],
                                [[1, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 5],
                                 [8, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 5]]])

        cls.dark = [[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5],
                     [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],
                    [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5],
                     [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],
                    [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5],
                     [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]]

    def test_background_subtraction(self):

        expected = numpy.array([[[0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [2, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                                [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                                [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                                 [7, 0, 0, 0, 0], [0, 0, 0, 0, 0]]])

        data = imageOperations.background_subtraction(self.data, self.dark)
        numpy.testing.assert_array_equal(expected, data)

    def test_n_sphere_mask(self):
        """ Tests the creation of a mask from a 3d array. """

        expected = numpy.array([[[False, False, False, False, False],
                                 [False, True, True, True, False],
                                 [False, True, True, True, False],
                                 [False, True, True, True, False],
                                 [False, False, False, False, False]],
                                [[False, False, True, False, False],
                                 [False, True, True, True, False],
                                 [True, True, True, True, True],
                                 [False, True, True, True, False],
                                 [False, False, True, False, False]],
                                [[False, False, False, False, False],
                                 [False, True, True, True, False],
                                 [False, True, True, True, False],
                                 [False, True, True, True, False],
                                 [False, False, False, False, False]]])

        mask = imageOperations._create_n_sphere_mask(expected.shape, radius=2)

        numpy.testing.assert_array_equal(expected, mask)

    def test_circular_mask(self):

        expected = numpy.array([[False, False, True, False, False],
                                [False, True, True, True, False],
                                [True, True, True, True, True],
                                [False, True, True, True, False],
                                [False, False, True, False, False]])

        mask = imageOperations._create_circular_mask(expected.shape, radius=2)

        numpy.testing.assert_array_equal(expected, mask)

    def test_hot_pixel_removal(self):

        expected = numpy.array([[[1, 2, 3, 4, 5],
                                 [2, 2, 3, 4, 5],
                                 [2, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 5]],
                                [[1, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 4],
                                 [1, 2, 3, 4, 3],
                                 [1, 2, 3, 4, 4],
                                 [1, 2, 3, 4, 5]],
                                [[1, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 5],
                                 [2, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 5]]], dtype=numpy.float32)

        data = imageOperations.hot_pixel_removal(self.data)
        numpy.testing.assert_array_equal(expected, data)

    def test_threshold_removal(self):
        """ Tests the correct removal from a threshold. """

        expected = numpy.array([[[1, 2, 3, 4, 3], [2, 2, 3, 4, 3], [3, 2, 3, 4, 3],
                                 [1, 2, 3, 4, 3], [1, 2, 3, 4, 3]],
                                [[1, 2, 3, 4, 3], [1, 2, 3, 4, 3], [1, 2, 3, 4, 3],
                                 [1, 2, 3, 4, 3], [1, 2, 3, 4, 3]],
                                [[1, 2, 3, 4, 3], [1, 2, 3, 4, 3], [1, 2, 3, 4, 3],
                                 [3, 2, 3, 4, 3], [1, 2, 3, 4, 3]]])

        data = imageOperations.threshold_removal(self.data, 1, 4)

        numpy.testing.assert_array_equal(expected, data)
