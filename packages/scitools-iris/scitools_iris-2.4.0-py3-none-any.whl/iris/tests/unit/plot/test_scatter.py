# (C) British Crown Copyright 2014 - 2016, Met Office
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
"""Unit tests for the `iris.plot.scatter` function."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests
from iris.tests.unit.plot import TestGraphicStringCoord

if tests.MPL_AVAILABLE:
    import iris.plot as iplt


@tests.skip_plot
class TestStringCoordPlot(TestGraphicStringCoord):
    def setUp(self):
        super(TestStringCoordPlot, self).setUp()
        self.cube = self.cube[0, :]
        self.lat_lon_cube = self.lat_lon_cube[0, :]

    def test_xaxis_labels(self):
        iplt.scatter(self.cube.coord('str_coord'), self.cube)
        self.assertBoundsTickLabels('xaxis')

    def test_yaxis_labels(self):
        iplt.scatter(self.cube, self.cube.coord('str_coord'))
        self.assertBoundsTickLabels('yaxis')

    def test_xaxis_labels_with_axes(self):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlim(0, 3)
        iplt.scatter(self.cube.coord('str_coord'), self.cube, axes=ax)
        plt.close(fig)
        self.assertPointsTickLabels('xaxis', ax)

    def test_yaxis_labels_with_axes(self):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_ylim(0, 3)
        iplt.scatter(self.cube, self.cube.coord('str_coord'), axes=ax)
        plt.close(fig)
        self.assertPointsTickLabels('yaxis', ax)

    def test_scatter_longitude(self):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        iplt.scatter(self.lat_lon_cube,
                     self.lat_lon_cube.coord('longitude'), axes=ax)
        plt.close(fig)


if __name__ == "__main__":
    tests.main()
