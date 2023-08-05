# (C) British Crown Copyright 2010 - 2015, Met Office
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
Test the intersection of Coords

"""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# import iris tests first so that some things can be initialised before importing anything else
import iris.tests as tests

import numpy as np

import iris
import iris.cube
import iris.coord_systems
import iris.coords
import iris.tests.stock


class TestCubeIntersectTheoretical(tests.IrisTest):
    def test_simple_intersect(self):
        cube = iris.cube.Cube(np.array([[1, 2, 3, 4, 5],
                                        [2, 3, 4, 5, 6],
                                        [3, 4, 5, 6, 7],
                                        [4, 5, 6, 7, 8],
                                        [5, 6, 7, 8, 9]], dtype=np.int32))

        lonlat_cs = iris.coord_systems.RotatedGeogCS(10, 20)
        cube.add_dim_coord(iris.coords.DimCoord(np.arange(5, dtype=np.float32) * 90 - 180, 'longitude', units='degrees', coord_system=lonlat_cs), 1)
        cube.add_dim_coord(iris.coords.DimCoord(np.arange(5, dtype=np.float32) * 45 - 90, 'latitude', units='degrees', coord_system=lonlat_cs), 0)
        cube.add_aux_coord(iris.coords.DimCoord(points=np.int32(11), long_name='pressure', units='Pa'))
        cube.rename("temperature")
        cube.units = "K"

        cube2 = iris.cube.Cube(np.array([[1, 2, 3, 4, 5],
                                         [2, 3, 4, 5, 6],
                                         [3, 4, 5, 6, 7],
                                         [4, 5, 6, 7, 8],
                                         [5, 6, 7, 8, 50]], dtype=np.int32))

        lonlat_cs = iris.coord_systems.RotatedGeogCS(10, 20)
        cube2.add_dim_coord(iris.coords.DimCoord(np.arange(5, dtype=np.float32) * 90, 'longitude', units='degrees', coord_system=lonlat_cs), 1)
        cube2.add_dim_coord(iris.coords.DimCoord(np.arange(5, dtype=np.float32) * 45 - 90, 'latitude', units='degrees', coord_system=lonlat_cs), 0)
        cube2.add_aux_coord(iris.coords.DimCoord(points=np.int32(11), long_name='pressure', units='Pa'))
        cube2.rename("")

        r = iris.analysis.maths.intersection_of_cubes(cube, cube2)
        self.assertCML(r, ('cdm', 'test_simple_cube_intersection.cml'))


class TestCoordIntersect(tests.IrisTest):
    def test_commutative(self):
        step = 4.0
        c1 = iris.coords.DimCoord(np.arange(100) * step)
        offset_points = c1.points.copy()
        offset_points -= step * 30
        c2 = c1.copy(points=offset_points)

        i1 = c1.intersect(c2)
        i2 = c2.intersect(c1)
        self.assertEqual(i1, i2)


if __name__ == "__main__":
    tests.main()
