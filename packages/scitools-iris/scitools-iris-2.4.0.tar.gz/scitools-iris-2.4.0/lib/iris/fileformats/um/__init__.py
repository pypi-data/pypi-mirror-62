# (C) British Crown Copyright 2014 - 2018, Met Office
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
Provides iris loading support for UM Fieldsfile-like file types, and PP.

At present, the only UM file types supported are true FieldsFiles and LBCs.
Other types of UM file may fail to load correctly (or at all).

"""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Publish the FF-replacement features here, and include documentation.
from ._ff_replacement import um_to_pp, load_cubes, load_cubes_32bit_ieee
from ._fast_load import structured_um_loading, FieldCollation
__all__ = ['um_to_pp', 'load_cubes', 'load_cubes_32bit_ieee',
           'structured_um_loading', 'FieldCollation']
