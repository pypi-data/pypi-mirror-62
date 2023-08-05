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
"""
Unit tests for
:func:`iris.fileformats.pp_load_rules._convert_scalar_realization_coords`.

"""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

from iris.coords import DimCoord
from iris.tests.unit.fileformats import TestField

from iris.fileformats.pp_load_rules import _convert_scalar_realization_coords


class Test(TestField):
    def test_valid(self):
        coords_and_dims = _convert_scalar_realization_coords(lbrsvd4=21)
        self.assertEqual(coords_and_dims,
                         [(DimCoord([21], standard_name='realization'), None)])

    def test_missing_indicator(self):
        coords_and_dims = _convert_scalar_realization_coords(lbrsvd4=0)
        self.assertEqual(coords_and_dims, [])


if __name__ == "__main__":
    tests.main()
