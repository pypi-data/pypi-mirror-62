# (C) British Crown Copyright 2014 - 2017, Met Office
#
# This file is part of Iris.
#
# Iris is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Iris is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris.  If not, see <http://www.gnu.org/licenses/>.
"""Unit tests for the :mod:`iris.tests.IrisTest` class."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa
import six

# import iris tests first so that some things can be initialised before
# importing anything else
import iris.tests as tests

from abc import ABCMeta, abstractproperty

import numpy as np


class _MaskedArrayEquality(six.with_metaclass(ABCMeta, object)):
    def setUp(self):
        self.arr1 = np.ma.array([1, 2, 3, 4], mask=[False, True, True, False])
        self.arr2 = np.ma.array([1, 3, 2, 4], mask=[False, True, True, False])

    @abstractproperty
    def _func(self):
        pass

    def test_strict_comparison(self):
        # Comparing both mask and data array completely.
        with self.assertRaises(AssertionError):
            self._func(self.arr1, self.arr2, strict=True)

    def test_non_strict_comparison(self):
        # Checking masked array equality and all unmasked array data values.
        self._func(self.arr1, self.arr2, strict=False)

    def test_default_strict_arg_comparison(self):
        self._func(self.arr1, self.arr2)

    def test_nomask(self):
        # Test that an assertion is raised when comparing a masked array
        # containing masked and unmasked values with a masked array with
        # 'nomask'.
        arr1 = np.ma.array([1, 2, 3, 4])
        with self.assertRaises(AssertionError):
            self._func(arr1, self.arr2, strict=False)

    def test_nomask_unmasked(self):
        # Ensure that a masked array with 'nomask' can compare with an entirely
        # unmasked array.
        arr1 = np.ma.array([1, 2, 3, 4])
        arr2 = np.ma.array([1, 2, 3, 4], mask=False)
        self._func(arr1, arr2, strict=False)

    def test_different_mask_strict(self):
        # Differing masks, equal data
        arr2 = self.arr1.copy()
        arr2[0] = np.ma.masked
        with self.assertRaises(AssertionError):
            self._func(self.arr1, arr2, strict=True)

    def test_different_mask_nonstrict(self):
        # Differing masks, equal data
        arr2 = self.arr1.copy()
        arr2[0] = np.ma.masked
        with self.assertRaises(AssertionError):
            self._func(self.arr1, arr2, strict=False)


@tests.iristest_timing_decorator
class Test_assertMaskedArrayEqual(_MaskedArrayEquality,
                                  tests.IrisTest_nometa):
    @property
    def _func(self):
        return self.assertMaskedArrayEqual


class Test_assertMaskedArrayEqual__Nonmaasked(tests.IrisTest):
    def test_nonmasked_same(self):
        # Masked test can be used on non-masked arrays.
        arr1 = np.array([1, 2])
        self.assertMaskedArrayEqual(arr1, arr1)

    def test_masked_nonmasked_same(self):
        # Masked test can be used between masked + non-masked arrays, and will
        # consider them equal, when mask=None.
        arr1 = np.ma.masked_array([1, 2])
        arr2 = np.array([1, 2])
        self.assertMaskedArrayEqual(arr1, arr2)

    def test_masked_nonmasked_different(self):
        arr1 = np.ma.masked_array([1, 2])
        arr2 = np.array([1, 3])
        with self.assertRaisesRegexp(AssertionError, 'Arrays are not equal'):
            self.assertMaskedArrayEqual(arr1, arr2)

    def test_nonmasked_masked_same(self):
        # Masked test can be used between masked + non-masked arrays, and will
        # consider them equal, when mask=None.
        arr1 = np.array([1, 2])
        arr2 = np.ma.masked_array([1, 2])
        self.assertMaskedArrayEqual(arr1, arr2)

    def test_masked_nonmasked_same_falsemask(self):
        # Masked test can be used between masked + non-masked arrays, and will
        # consider them equal, when mask=False.
        arr1 = np.ma.masked_array([1, 2], mask=False)
        arr2 = np.array([1, 2])
        self.assertMaskedArrayEqual(arr1, arr2)

    def test_masked_nonmasked_same_emptymask(self):
        # Masked test can be used between masked + non-masked arrays, and will
        # consider them equal, when mask=zeros.
        arr1 = np.ma.masked_array([1, 2], mask=[False, False])
        arr2 = np.array([1, 2])
        self.assertMaskedArrayEqual(arr1, arr2)


@tests.iristest_timing_decorator
class Test_assertMaskedArrayAlmostEqual(_MaskedArrayEquality,
                                        tests.IrisTest_nometa):
    @property
    def _func(self):
        return self.assertMaskedArrayAlmostEqual

    def test_decimal(self):
        arr1, arr2 = np.ma.array([100.0]), np.ma.array([100.003])
        self.assertMaskedArrayAlmostEqual(arr1, arr2, decimal=2)
        with self.assertRaises(AssertionError):
            self.assertMaskedArrayAlmostEqual(arr1, arr2, decimal=3)


if __name__ == '__main__':
    tests.main()
