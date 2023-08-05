# (C) British Crown Copyright 2013 - 2019, Met Office
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
"""Unit tests for the :data:`iris.analysis.PROPORTION` aggregator."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

import numpy.ma as ma

from iris.analysis import PROPORTION
import iris.cube
from iris.coords import DimCoord


class Test_units_func(tests.IrisTest):
    def test(self):
        self.assertIsNotNone(PROPORTION.units_func)
        new_units = PROPORTION.units_func(None)
        self.assertEqual(new_units, 1)


class Test_masked(tests.IrisTest):
    def setUp(self):
        self.cube = iris.cube.Cube(ma.masked_equal([1, 2, 3, 4, 5], 3))
        self.cube.add_dim_coord(DimCoord([6, 7, 8, 9, 10], long_name='foo'),
                                0)
        self.func = lambda x: x >= 3

    def test_ma(self):
        cube = self.cube.collapsed("foo", PROPORTION, function=self.func)
        self.assertArrayEqual(cube.data, [0.5])

    def test_false_mask(self):
        # Test corner case where mask is returned as boolean value rather
        # than boolean array when the mask is unspecified on construction.
        masked_cube = iris.cube.Cube(ma.array([1, 2, 3, 4, 5]))
        masked_cube.add_dim_coord(DimCoord([6, 7, 8, 9, 10], long_name='foo'),
                                  0)
        cube = masked_cube.collapsed("foo", PROPORTION, function=self.func)
        self.assertArrayEqual(cube.data, ma.array([0.6]))


class Test_name(tests.IrisTest):
    def test(self):
        self.assertEqual(PROPORTION.name(), 'proportion')


class Test_aggregate_shape(tests.IrisTest):
    def test(self):
        shape = ()
        kwargs = dict()
        self.assertTupleEqual(PROPORTION.aggregate_shape(**kwargs), shape)
        kwargs = dict(captain='caveman', penelope='pitstop')
        self.assertTupleEqual(PROPORTION.aggregate_shape(**kwargs), shape)


if __name__ == "__main__":
    tests.main()
