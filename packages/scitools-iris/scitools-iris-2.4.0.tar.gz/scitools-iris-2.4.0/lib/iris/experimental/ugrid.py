# (C) British Crown Copyright 2014 - 2015, Met Office
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
Ugrid functions.

"""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

import iris


def ugrid(location, name):
    """
    Create a cube from an unstructured grid.

    Args:

    * location:
        A string whose value represents the path to a file or
        URL to an OpenDAP resource conforming to the
        Unstructured Grid Metadata Conventions for Scientific Datasets
        https://github.com/ugrid-conventions/ugrid-conventions

    * name:
        A string whose value represents a cube loading constraint of
        first the standard name if found, then the long name if found,
        then the variable name if found, before falling back to
        the value of the default which itself defaults to "unknown"

    Returns:
        An instance of :class:`iris.cube.Cube` decorated with
        an instance of :class:`pyugrid.ugrid.Ugrid`
        bound to an attribute of the cube called "mesh"

    """
    # Lazy import so we can build the docs with no pyugrid.
    import pyugrid

    cube = iris.load_cube(location, name)
    ug = pyugrid.ugrid.UGrid.from_ncfile(location)
    cube.mesh = ug
    cube.mesh_dimension = 1  # {0:time, 1:node}
    return cube
