# (C) British Crown Copyright 2013 - 2017, Met Office
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
"""Integration tests for NAME to GRIB2 interoperability."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

from distutils.version import StrictVersion

import cf_units
import numpy as np
import warnings

import iris

if tests.GRIB_AVAILABLE:
    import gribapi


def name_cb(cube, field, filename):
    # NAME files give the time point at the end of the range but Iris'
    # GRIB loader creates it in the middle (the GRIB file itself doesn't
    # encode a time point). Here we make them consistent so we can
    # easily compare them.
    t_coord = cube.coord('time')
    t_coord.points = t_coord.bounds[0][1]
    fp_coord = cube.coord('forecast_period')
    fp_coord.points = fp_coord.bounds[0][1]
    # NAME contains extra vertical meta-data.
    z_coord = cube.coords('height')
    if z_coord:
        z_coord[0].standard_name = 'height'
        z_coord[0].long_name = 'height above ground level'


@tests.skip_grib
class TestNameToGRIB(tests.IrisTest):

    def check_common(self, name_cube, grib_cube):
        self.assertTrue(np.allclose(name_cube.data, name_cube.data))
        self.assertTrue(
            np.allclose(name_cube.coord('latitude').points,
                        grib_cube.coord('latitude').points))
        self.assertTrue(
            np.allclose(name_cube.coord('longitude').points,
                        grib_cube.coord('longitude').points - 360))

        for c in ['height', 'time']:
            if name_cube.coords(c):
                self.assertEqual(name_cube.coord(c),
                                 grib_cube.coord(c))

    @tests.skip_data
    def test_name2_field(self):
        filepath = tests.get_data_path(('NAME', 'NAMEII_field.txt'))
        name_cubes = iris.load(filepath)

        # There is a known load/save problem with numerous
        # gribapi/eccodes versions and
        # zero only data, where min == max.
        # This may be a problem with data scaling.
        for i, name_cube in enumerate(name_cubes):
            data = name_cube.data
            if np.min(data) == np.max(data):
                msg = ('NAMEII cube #{}, "{}" has empty data : '
                       'SKIPPING test for this cube, as save/load will '
                       'not currently work.')
                warnings.warn(msg.format(i, name_cube.name()))
                continue

            with self.temp_filename('.grib2') as temp_filename:
                iris.save(name_cube, temp_filename)
                grib_cube = iris.load_cube(temp_filename, callback=name_cb)
                self.check_common(name_cube, grib_cube)
                self.assertCML(
                    grib_cube, tests.get_result_path(
                        ('integration', 'name_grib', 'NAMEII',
                         '{}_{}.cml'.format(i, name_cube.name()))))

    @tests.skip_data
    def test_name3_field(self):
        filepath = tests.get_data_path(('NAME', 'NAMEIII_field.txt'))
        name_cubes = iris.load(filepath)
        for i, name_cube in enumerate(name_cubes):
            with self.temp_filename('.grib2') as temp_filename:
                iris.save(name_cube, temp_filename)
                grib_cube = iris.load_cube(temp_filename, callback=name_cb)

                self.check_common(name_cube, grib_cube)
                self.assertCML(
                    grib_cube, tests.get_result_path(
                        ('integration', 'name_grib', 'NAMEIII',
                         '{}_{}.cml'.format(i, name_cube.name()))))


if __name__ == "__main__":
    tests.main()
