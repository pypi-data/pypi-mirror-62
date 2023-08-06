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
__date__ = "29/11/2019"

import numpy
import silx.math

from enum import Enum


class Method(Enum):
    """
    Methods available to compute the background.
    """
    mean = "mean"
    median = "median"

    @staticmethod
    def values():
        return list(map(lambda c: c.value, Method))


def background_subtraction(data, bg_frames, method='median'):

    """Function that computes the median between a series of dark images from a dataset
    and substracts it to each frame of the raw data to remove the noise.

    :param ndarray data: The raw data
    :param array_like dark_frames: List of dark frames
    :param method: Method used to determine the background image.
    :type method: Union['mean', 'median', None]
    :returns: ndarray
    :raises: ValueError
    """
    assert bg_frames is not None, "Background frames must be given"
    background = numpy.zeros(data[0].shape, data.dtype)
    if len(bg_frames):
        if method == 'mean':
            numpy.mean(bg_frames, out=background, axis=0)
        elif method == 'median':
            numpy.median(bg_frames, out=background, axis=0)
        else:
            raise ValueError("Invalid method specified. Please use `mean`, "
                             "or `median`.")
    new_data = numpy.subtract(data, background, dtype=numpy.int64)
    new_data[new_data < 0] = 0

    return new_data.astype(data.dtype)


def _create_circular_mask(shape, center=None, radius=None):
    """
    Function that given a height and a width returns a circular mask image.

    :param int h: Height
    :param int w: Width
    :param center: Center of the circle
    :type center: Union[[int, int], None]
    :param radius: Radius of the circle
    :type radius: Union[int, None]
    :returns: ndarray
    """
    h, w = shape
    if center is None:  # use the middle of the image
        center = [int(h / 2), int(w / 2)]
    if radius is None:  # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], h - center[0], w - center[1])

    X, Y = numpy.ogrid[:h, :w]
    dist_from_center = numpy.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

    mask = dist_from_center <= radius
    return mask


def _create_n_sphere_mask(shape, center=None, radius=None):
    """
    Function that given a list of dimensions returns a n-dimensional sphere mask.

    :param shape: Dimensions of the mask
    :type shape: array_like
    :param center: Center of the sphere
    :type center: Union[array_like, None]
    :param radius: Radius of the sphere
    :type radius: Union[int, None]
    :returns: ndarray
    """

    assert shape or radius, "If dimensions are not entered radius must be given"

    dimensions = numpy.array(shape)

    if center is None:  # use the middle of the image
        center = (dimensions / 2).astype(int)
    if radius is None:  # use the smallest distance between the center and image walls
        radius = min(numpy.concatenate([center, dimensions - center]))

    C = numpy.ogrid[[slice(0, dim) for dim in dimensions]]
    dist_from_center = numpy.sqrt(numpy.sum((C - center) ** 2))

    mask = dist_from_center <= radius
    return mask


def hot_pixel_removal(data, ksize=3):
    """
    Function to remove hot pixels of the data using median filter.

    :param array_like data: Input data.
    :param str mask: Radius of the cylinder.
    :param int ksize: Size of the mask to apply.
    :returns: ndarray
    """
    corrected_data = numpy.empty(data.shape, dtype=data.dtype)
    for i, frame in enumerate(data):
        if frame.dtype == numpy.int or frame.dtype == numpy.uint:
            # Cast to int and not uint to later subtract
            frame = frame.astype(numpy.int16)
        elif frame.dtype == numpy.float:
            frame = frame.astype(numpy.float32)
        corrected_frame = numpy.array(frame)
        median = silx.math.medfilt(frame, ksize)
        hot_pixels = numpy.subtract(frame, median, dtype=numpy.int64)
        threshold = numpy.std(hot_pixels)
        corrected_frame[hot_pixels > threshold] = median[hot_pixels > threshold]
        corrected_data[i] = corrected_frame
    return corrected_data


def threshold_removal(data, bottom=None, top=None):
    """
    Set bottom and top threshold to the images in the dataset.

    :param Dataset dataset: Dataset with the data
    :param int bottom: Bottom threshold
    :param int top: Top threshold
    :returns: ndarray
    """

    frames = []

    for frame in data:
        median = numpy.median(frame)
        if bottom is not None:
            frame[frame < bottom] = median
        if top is not None:
            frame[frame > top] = median

        frames.append(frame)

    return numpy.asarray(frames)
