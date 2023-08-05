# (C) British Crown Copyright 2010 - 2019, Met Office
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
Definitions of coordinates.

"""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa
import six

from abc import ABCMeta, abstractproperty
from collections import namedtuple
try:  # Python 3
    from collections.abc import Iterator
except ImportError:  # Python 2.7
    from collections import Iterator
import copy
from itertools import chain
from six.moves import zip_longest
import operator
import warnings
import zlib

import cftime
import numpy as np
import numpy.ma as ma

from iris._data_manager import DataManager
from iris._deprecation import warn_deprecated
import iris._lazy_data as _lazy
import iris.aux_factory
import iris.exceptions
import iris.time
import iris.util

from iris._cube_coord_common import CFVariableMixin
from iris.util import points_step


class CoordDefn(namedtuple('CoordDefn',
                           ['standard_name', 'long_name',
                            'var_name', 'units',
                            'attributes', 'coord_system',
                            'climatological'])):
    """
    Criterion for identifying a specific type of :class:`DimCoord` or
    :class:`AuxCoord` based on its metadata.

    """

    __slots__ = ()

    def name(self, default='unknown'):
        """
        Returns a human-readable name.

        First it tries self.standard_name, then it tries the 'long_name'
        attribute, then the 'var_name' attribute, before falling back to
        the value of `default` (which itself defaults to 'unknown').

        """
        return self.standard_name or self.long_name or self.var_name or default

    def __lt__(self, other):
        if not isinstance(other, CoordDefn):
            return NotImplemented

        def _sort_key(defn):
            # Emulate Python 2 behaviour with None
            return (defn.standard_name is not None, defn.standard_name,
                    defn.long_name is not None, defn.long_name,
                    defn.var_name is not None, defn.var_name,
                    defn.units is not None, defn.units,
                    defn.coord_system is not None, defn.coord_system)

        return _sort_key(self) < _sort_key(other)


class CoordExtent(namedtuple('_CoordExtent', ['name_or_coord',
                                              'minimum',
                                              'maximum',
                                              'min_inclusive',
                                              'max_inclusive'])):
    """Defines a range of values for a coordinate."""

    def __new__(cls, name_or_coord, minimum, maximum,
                min_inclusive=True, max_inclusive=True):
        """
        Create a CoordExtent for the specified coordinate and range of
        values.

        Args:

        * name_or_coord
            Either a coordinate name or a coordinate, as defined in
            :meth:`iris.cube.Cube.coords()`.

        * minimum
            The minimum value of the range to select.

        * maximum
            The maximum value of the range to select.

        Kwargs:

        * min_inclusive
            If True, coordinate values equal to `minimum` will be included
            in the selection. Default is True.

        * max_inclusive
            If True, coordinate values equal to `maximum` will be included
            in the selection. Default is True.

        """
        return super(CoordExtent, cls).__new__(cls, name_or_coord, minimum,
                                               maximum, min_inclusive,
                                               max_inclusive)

    __slots__ = ()


# Coordinate cell styles. Used in plot and cartography.
POINT_MODE = 0
BOUND_MODE = 1

BOUND_POSITION_START = 0
BOUND_POSITION_MIDDLE = 0.5
BOUND_POSITION_END = 1


# Private named tuple class for coordinate groups.
_GroupbyItem = namedtuple('GroupbyItem',
                          'groupby_point, groupby_slice')


def _get_2d_coord_bound_grid(bounds):
    """
    Creates a grid using the bounds of a 2D coordinate with 4 sided cells.

    Assumes that the four vertices of the cells are in an anti-clockwise order
    (bottom-left, bottom-right, top-right, top-left).

    Selects the zeroth vertex of each cell. A final column is added, which
    contains the first vertex of the cells in the final column. A final row
    is added, which contains the third vertex of all the cells in the final
    row, except for in the final column where it uses the second vertex.
    e.g.
    # 0-0-0-0-1
    # 0-0-0-0-1
    # 3-3-3-3-2

    Args:
    * bounds: (array)
        Coordinate bounds array of shape (Y, X, 4)

    Returns:
    * grid: (array)
        Grid of shape (Y+1, X+1)

    """
    # Check bds has the shape (ny, nx, 4)
    if not (bounds.ndim == 3 and bounds.shape[-1] == 4):
        raise ValueError('Bounds for 2D coordinates must be 3-dimensional and '
                         'have 4 bounds per point.')

    bounds_shape = bounds.shape
    result = np.zeros((bounds_shape[0] + 1, bounds_shape[1] + 1))

    result[:-1, :-1] = bounds[:, :, 0]
    result[:-1, -1] = bounds[:, -1, 1]
    result[-1, :-1] = bounds[-1, :, 3]
    result[-1, -1] = bounds[-1, -1, 2]

    return result


class Cell(namedtuple('Cell', ['point', 'bound'])):
    """
    An immutable representation of a single cell of a coordinate, including the
    sample point and/or boundary position.

    Notes on cell comparison:

    Cells are compared in two ways, depending on whether they are
    compared to another Cell, or to a number/string.

    Cell-Cell comparison is defined to produce a strict ordering. If
    two cells are not exactly equal (i.e. including whether they both
    define bounds or not) then they will have a consistent relative
    order.

    Cell-number and Cell-string comparison is defined to support
    Constraint matching. The number/string will equal the Cell if, and
    only if, it is within the Cell (including on the boundary). The
    relative comparisons (lt, le, ..) are defined to be consistent with
    this interpretation. So for a given value `n` and Cell `cell`, only
    one of the following can be true:

    |    n < cell
    |    n == cell
    |    n > cell

    Similarly, `n <= cell` implies either `n < cell` or `n == cell`.
    And `n >= cell` implies either `n > cell` or `n == cell`.

    """

    # This subclass adds no attributes.
    __slots__ = ()

    # Make this class's comparison operators override those of numpy
    __array_priority__ = 100

    def __new__(cls, point=None, bound=None):
        """
        Construct a Cell from point or point-and-bound information.

        """
        if point is None:
            raise ValueError('Point must be defined.')

        if bound is not None:
            bound = tuple(bound)

        if isinstance(point, np.ndarray):
            point = tuple(point.flatten())

        if isinstance(point, (tuple, list)):
            if len(point) != 1:
                raise ValueError('Point may only be a list or tuple if it has '
                                 'length 1.')
            point = point[0]

        return super(Cell, cls).__new__(cls, point, bound)

    def __mod__(self, mod):
        point = self.point
        bound = self.bound
        if point is not None:
            point = point % mod
        if bound is not None:
            bound = tuple([val % mod for val in bound])
        return Cell(point, bound)

    def __add__(self, mod):
        point = self.point
        bound = self.bound
        if point is not None:
            point = point + mod
        if bound is not None:
            bound = tuple([val + mod for val in bound])
        return Cell(point, bound)

    def __hash__(self):
        return super(Cell, self).__hash__()

    def __eq__(self, other):
        """
        Compares Cell equality depending on the type of the object to be
        compared.

        """
        if isinstance(other, (int, float, np.number)) or \
                hasattr(other, 'timetuple'):
            if self.bound is not None:
                return self.contains_point(other)
            else:
                return self.point == other
        elif isinstance(other, Cell):
            return (self.point == other.point) and (self.bound == other.bound)
        elif (isinstance(other, six.string_types) and self.bound is None and
              isinstance(self.point, six.string_types)):
            return self.point == other
        else:
            return NotImplemented

    # Must supply __ne__, Python does not defer to __eq__ for negative equality
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is not NotImplemented:
            result = not result
        return result

    def __common_cmp__(self, other, operator_method):
        """
        Common method called by the rich comparison operators. The method of
        checking equality depends on the type of the object to be compared.

        Cell vs Cell comparison is used to define a strict order.
        Non-Cell vs Cell comparison is used to define Constraint matching.

        """
        if not (isinstance(other, (int, float, np.number, Cell)) or
                hasattr(other, 'timetuple')):
            raise TypeError("Unexpected type of other "
                            "{}.".format(type(other)))
        if operator_method not in (operator.gt, operator.lt,
                                   operator.ge, operator.le):
            raise ValueError("Unexpected operator_method")

        # Prevent silent errors resulting from missing cftime
        # behaviour.
        if (isinstance(other, cftime.datetime) or
                (isinstance(self.point, cftime.datetime) and
                 not isinstance(other, iris.time.PartialDateTime))):
            raise TypeError('Cannot determine the order of '
                            'cftime.datetime objects')

        if isinstance(other, Cell):
            # Cell vs Cell comparison for providing a strict sort order
            if self.bound is None:
                if other.bound is None:
                    # Point vs point
                    # - Simple ordering
                    result = operator_method(self.point, other.point)
                else:
                    # Point vs point-and-bound
                    # - Simple ordering of point values, but if the two
                    #   points are equal, we make the arbitrary choice
                    #   that the point-only Cell is defined as less than
                    #   the point-and-bound Cell.
                    if self.point == other.point:
                        result = operator_method in (operator.lt, operator.le)
                    else:
                        result = operator_method(self.point, other.point)
            else:
                if other.bound is None:
                    # Point-and-bound vs point
                    # - Simple ordering of point values, but if the two
                    #   points are equal, we make the arbitrary choice
                    #   that the point-only Cell is defined as less than
                    #   the point-and-bound Cell.
                    if self.point == other.point:
                        result = operator_method in (operator.gt, operator.ge)
                    else:
                        result = operator_method(self.point, other.point)
                else:
                    # Point-and-bound vs point-and-bound
                    # - Primarily ordered on minimum-bound. If the
                    #   minimum-bounds are equal, then ordered on
                    #   maximum-bound. If the maximum-bounds are also
                    #   equal, then ordered on point values.
                    if self.bound[0] == other.bound[0]:
                        if self.bound[1] == other.bound[1]:
                            result = operator_method(self.point, other.point)
                        else:
                            result = operator_method(self.bound[1],
                                                     other.bound[1])
                    else:
                        result = operator_method(self.bound[0], other.bound[0])
        else:
            # Cell vs number (or string, or datetime-like) for providing
            # Constraint behaviour.
            if self.bound is None:
                # Point vs number
                # - Simple matching
                me = self.point
            else:
                if hasattr(other, 'timetuple'):
                    raise TypeError('Cannot determine whether a point lies '
                                    'within a bounded region for '
                                    'datetime-like objects.')
                # Point-and-bound vs number
                # - Match if "within" the Cell
                if operator_method in [operator.gt, operator.le]:
                    me = min(self.bound)
                else:
                    me = max(self.bound)

            # Work around to handle cftime.datetime comparison, which
            # doesn't return NotImplemented on failure in some versions of the
            # library
            try:
                result = operator_method(me, other)
            except TypeError:
                rop = {operator.lt: operator.gt,
                       operator.gt: operator.lt,
                       operator.le: operator.ge,
                       operator.ge: operator.le}[operator_method]
                result = rop(other, me)

        return result

    def __ge__(self, other):
        return self.__common_cmp__(other, operator.ge)

    def __le__(self, other):
        return self.__common_cmp__(other, operator.le)

    def __gt__(self, other):
        return self.__common_cmp__(other, operator.gt)

    def __lt__(self, other):
        return self.__common_cmp__(other, operator.lt)

    def __str__(self):
        if self.bound is not None:
            return repr(self)
        else:
            return str(self.point)

    def contains_point(self, point):
        """
        For a bounded cell, returns whether the given point lies within the
        bounds.

        .. note:: The test carried out is equivalent to min(bound)
                  <= point <= max(bound).

        """
        if self.bound is None:
            raise ValueError('Point cannot exist inside an unbounded cell.')
        if hasattr(point, 'timetuple') or np.any([hasattr(val, 'timetuple') for
                                                  val in self.bound]):
            raise TypeError('Cannot determine whether a point lies within '
                            'a bounded region for datetime-like objects.')

        return np.min(self.bound) <= point <= np.max(self.bound)


class Coord(six.with_metaclass(ABCMeta, CFVariableMixin)):
    """
    Abstract superclass for coordinates.

    """

    _MODE_ADD = 1
    _MODE_SUB = 2
    _MODE_MUL = 3
    _MODE_DIV = 4
    _MODE_RDIV = 5
    _MODE_SYMBOL = {_MODE_ADD: '+', _MODE_SUB: '-',
                    _MODE_MUL: '*', _MODE_DIV: '/',
                    _MODE_RDIV: '/'}

    def __init__(self, points, standard_name=None, long_name=None,
                 var_name=None, units='1', bounds=None,
                 attributes=None, coord_system=None,
                 climatological=False):

        """
        Constructs a single coordinate.

        Args:

        * points:
            The values (or value in the case of a scalar coordinate) of the
            coordinate for each cell.

        Kwargs:

        * standard_name:
            CF standard name of the coordinate.
        * long_name:
            Descriptive name of the coordinate.
        * var_name:
            The netCDF variable name for the coordinate.
        * units
            The :class:`~cf_units.Unit` of the coordinate's values.
            Can be a string, which will be converted to a Unit object.
        * bounds
            An array of values describing the bounds of each cell. Given n
            bounds for each cell, the shape of the bounds array should be
            points.shape + (n,). For example, a 1d coordinate with 100 points
            and two bounds per cell would have a bounds array of shape
            (100, 2)
            Note if the data is a climatology, `climatological`
            should be set.
        * attributes
            A dictionary containing other cf and user-defined attributes.
        * coord_system
            A :class:`~iris.coord_systems.CoordSystem` representing the
            coordinate system of the coordinate,
            e.g. a :class:`~iris.coord_systems.GeogCS` for a longitude Coord.
        * climatological (bool):
            When True: the coordinate is a NetCDF climatological time axis.
            When True: saving in NetCDF will give the coordinate variable a
            'climatology' attribute and will create a boundary variable called
            '<coordinate-name>_climatology' in place of a standard bounds
            attribute and bounds variable.
            Will set to True when a climatological time axis is loaded
            from NetCDF.
            Always False if no bounds exist.
        """
        #: CF standard name of the quantity that the coordinate represents.
        self.standard_name = standard_name

        #: Descriptive name of the coordinate.
        self.long_name = long_name

        #: The netCDF variable name for the coordinate.
        self.var_name = var_name

        #: Unit of the quantity that the coordinate represents.
        self.units = units

        #: Other attributes, including user specified attributes that
        #: have no meaning to Iris.
        self.attributes = attributes

        #: Relevant coordinate system (if any).
        self.coord_system = coord_system

        # Set up DataManager attributes and points and bounds values.
        self._points_dm = None
        self._bounds_dm = None
        self.points = points
        self.bounds = bounds
        self.climatological = climatological

    def __getitem__(self, keys):
        """
        Returns a new Coord whose values are obtained by conventional array
        indexing.

        .. note::

            Indexing of a circular coordinate results in a non-circular
            coordinate if the overall shape of the coordinate changes after
            indexing.

        """
        # Fetch the points and bounds.
        points = self._points_dm.core_data()
        if self.has_bounds():
            bounds = self._bounds_dm.core_data()
        else:
            bounds = None

        # Index both points and bounds with the keys.
        _, points = iris.util._slice_data_with_keys(
            points, keys)
        if bounds is not None:
            _, bounds = iris.util._slice_data_with_keys(
                bounds, keys)

        # Copy data after indexing, to avoid making coords that are
        # views on other coords.  This will not realise lazy data.
        points = points.copy()
        if bounds is not None:
            bounds = bounds.copy()

        # The new coordinate is a copy of the old one with replaced content.
        new_coord = self.copy(points=points, bounds=bounds)
        return new_coord

    def copy(self, points=None, bounds=None):
        """
        Returns a copy of this coordinate.

        Kwargs:

        * points: A points array for the new coordinate.
                  This may be a different shape to the points of the coordinate
                  being copied.

        * bounds: A bounds array for the new coordinate.
                  Given n bounds for each cell, the shape of the bounds array
                  should be points.shape + (n,). For example, a 1d coordinate
                  with 100 points and two bounds per cell would have a bounds
                  array of shape (100, 2).

        .. note:: If the points argument is specified and bounds are not, the
                  resulting coordinate will have no bounds.

        """
        if points is None and bounds is not None:
            raise ValueError('If bounds are specified, points must also be '
                             'specified')

        new_coord = copy.deepcopy(self)
        if points is not None:
            new_coord._points_dm = None
            new_coord.points = points
            # Regardless of whether bounds are provided as an argument, new
            # points will result in new bounds, discarding those copied from
            # self.
            new_coord.bounds = bounds

        return new_coord

    @classmethod
    def from_coord(cls, coord):
        """Create a new Coord of this type, from the given coordinate."""
        kwargs = {'points': coord.core_points(),
                  'bounds': coord.core_bounds(),
                  'standard_name': coord.standard_name,
                  'long_name': coord.long_name,
                  'var_name': coord.var_name,
                  'units': coord.units,
                  'attributes': coord.attributes,
                  'coord_system': copy.deepcopy(coord.coord_system)}
        if issubclass(cls, DimCoord):
            # DimCoord introduces an extra constructor keyword.
            kwargs['circular'] = getattr(coord, 'circular', False)
        return cls(**kwargs)

    @staticmethod
    def _sanitise_array(src, ndmin):
        if _lazy.is_lazy_data(src):
            # Lazy data : just ensure ndmin requirement.
            ndims_missing = ndmin - src.ndim
            if ndims_missing <= 0:
                result = src
            else:
                extended_shape = tuple([1] * ndims_missing + list(src.shape))
                result = src.reshape(extended_shape)
        else:
            # Real data : a few more things to do in this case.
            # Ensure the array is writeable.
            # NB. Returns the *same object* if src is already writeable.
            result = np.require(src, requirements='W')
            # Ensure the array has enough dimensions.
            # NB. Returns the *same object* if result.ndim >= ndmin
            func = ma.array if ma.isMaskedArray(result) else np.array
            result = func(result, ndmin=ndmin, copy=False)
            # We don't need to copy the data, but we do need to have our
            # own view so we can control the shape, etc.
            result = result.view()
        return result

    @property
    def points(self):
        """The coordinate points values as a NumPy array."""
        return self._points_dm.data.view()

    @points.setter
    def points(self, points):
        # Set the points to a new array - as long as it's the same shape.

        # Ensure points has an ndmin of 1 and is either a numpy or lazy array.
        # This will avoid Scalar coords with points of shape () rather
        # than the desired (1,).
        points = self._sanitise_array(points, 1)

        # Set or update DataManager.
        if self._points_dm is None:
            self._points_dm = DataManager(points)
        else:
            self._points_dm.data = points

    @property
    def bounds(self):
        """
        The coordinate bounds values, as a NumPy array,
        or None if no bound values are defined.

        .. note:: The shape of the bound array should be: ``points.shape +
            (n_bounds, )``.

        """
        bounds = None
        if self.has_bounds():
            bounds = self._bounds_dm.data.view()
        return bounds

    @bounds.setter
    def bounds(self, bounds):
        # Ensure the bounds are a compatible shape.
        if bounds is None:
            self._bounds_dm = None
            self._climatological = False
        else:
            bounds = self._sanitise_array(bounds, 2)
            if self.shape != bounds.shape[:-1]:
                raise ValueError("Bounds shape must be compatible with points "
                                 "shape.")
            if not self.has_bounds() \
                    or self.core_bounds().shape != bounds.shape:
                # Construct a new bounds DataManager.
                self._bounds_dm = DataManager(bounds)
            else:
                self._bounds_dm.data = bounds

    @property
    def climatological(self):
        """
        A boolean that controls whether the coordinate is a climatological
        time axis, in which case the bounds represent a climatological period
        rather than a normal period.

        Always reads as False if there are no bounds.
        On set, the input value is cast to a boolean, exceptions raised
        if units are not time units or if there are no bounds.
        """
        return self._climatological if self.has_bounds() else False

    @climatological.setter
    def climatological(self, value):
        # Ensure the bounds are a compatible shape.
        value = bool(value)
        if value:
            if not self.units.is_time_reference():
                emsg = ("Cannot set climatological coordinate, does not have"
                        " valid time reference units, got {!r}.")
                raise TypeError(emsg.format(self.units))

            if not self.has_bounds():
                emsg = "Cannot set climatological coordinate, no bounds exist."
                raise ValueError(emsg)

        self._climatological = value

    def lazy_points(self):
        """
        Return a lazy array representing the coord points.

        Accessing this method will never cause the points values to be loaded.
        Similarly, calling methods on, or indexing, the returned Array
        will not cause the coord to have loaded points.

        If the data have already been loaded for the coord, the returned
        Array will be a new lazy array wrapper.

        Returns:
            A lazy array, representing the coord points array.

        """
        return self._points_dm.lazy_data()

    def lazy_bounds(self):
        """
        Return a lazy array representing the coord bounds.

        Accessing this method will never cause the bounds values to be loaded.
        Similarly, calling methods on, or indexing, the returned Array
        will not cause the coord to have loaded bounds.

        If the data have already been loaded for the coord, the returned
        Array will be a new lazy array wrapper.

        Returns:
            A lazy array representing the coord bounds array or `None` if the
            coord does not have bounds.

        """
        lazy_bounds = None
        if self.has_bounds():
            lazy_bounds = self._bounds_dm.lazy_data()
        return lazy_bounds

    def core_points(self):
        """
        The points array at the core of this coord, which may be a NumPy array
        or a dask array.

        """
        result = self._points_dm.core_data()
        if not _lazy.is_lazy_data(result):
            result = result.view()
        return result

    def core_bounds(self):
        """
        The points array at the core of this coord, which may be a NumPy array
        or a dask array.

        """
        result = None
        if self.has_bounds():
            result = self._bounds_dm.core_data()
            if not _lazy.is_lazy_data(result):
                result = result.view()
        return result

    def has_lazy_points(self):
        """
        Return a boolean indicating whether the coord's points array is a
        lazy dask array or not.

        """
        return self._points_dm.has_lazy_data()

    def has_lazy_bounds(self):
        """
        Return a boolean indicating whether the coord's bounds array is a
        lazy dask array or not.

        """
        result = False
        if self.has_bounds():
            result = self._bounds_dm.has_lazy_data()
        return result

    def _repr_other_metadata(self):
        fmt = ''
        if self.long_name:
            fmt = ', long_name={self.long_name!r}'
        if self.var_name:
            fmt += ', var_name={self.var_name!r}'
        if len(self.attributes) > 0:
            fmt += ', attributes={self.attributes}'
        if self.coord_system:
            fmt += ', coord_system={self.coord_system}'
        if self.climatological:
            fmt += ', climatological={' \
                   'self.climatological}'
        result = fmt.format(self=self)
        return result

    def _str_dates(self, dates_as_numbers):
        date_obj_array = self.units.num2date(dates_as_numbers)
        kwargs = {'separator': ', ', 'prefix': '      '}
        return np.core.arrayprint.array2string(date_obj_array,
                                               formatter={'all': str},
                                               **kwargs)

    def __str__(self):
        if self.units.is_time_reference():
            fmt = '{cls}({points}{bounds}' \
                  ', standard_name={self.standard_name!r}' \
                  ', calendar={self.units.calendar!r}{other_metadata})'
            if self.units.is_long_time_interval():
                # A time unit with a long time interval ("months" or "years")
                # cannot be converted to a date using `num2date` so gracefully
                # fall back to printing points as numbers, not datetimes.
                points = self.points
            else:
                points = self._str_dates(self.points)
            bounds = ''
            if self.has_bounds():
                if self.units.is_long_time_interval():
                    bounds_vals = self.bounds
                else:
                    bounds_vals = self._str_dates(self.bounds)
                bounds = ', bounds={vals}'.format(vals=bounds_vals)
            result = fmt.format(self=self, cls=type(self).__name__,
                                points=points, bounds=bounds,
                                other_metadata=self._repr_other_metadata())
        else:
            result = repr(self)
        return result

    def __repr__(self):
        fmt = '{cls}({self.points!r}{bounds}' \
              ', standard_name={self.standard_name!r}, units={self.units!r}' \
              '{other_metadata})'
        bounds = ''
        if self.has_bounds():
            bounds = ', bounds=' + repr(self.bounds)
        result = fmt.format(self=self, cls=type(self).__name__,
                            bounds=bounds,
                            other_metadata=self._repr_other_metadata())
        return result

    def __eq__(self, other):
        eq = NotImplemented
        # If the other object has a means of getting its definition, and
        # whether or not it has_points and has_bounds, then do the
        # comparison, otherwise return a NotImplemented to let Python try to
        # resolve the operator elsewhere.
        if hasattr(other, '_as_defn'):
            # metadata comparison
            eq = self._as_defn() == other._as_defn()
            # points comparison
            if eq:
                eq = iris.util.array_equal(self.points, other.points,
                                           withnans=True)
            # bounds comparison
            if eq:
                if self.has_bounds() and other.has_bounds():
                    eq = iris.util.array_equal(self.bounds, other.bounds,
                                               withnans=True)
                else:
                    eq = self.bounds is None and other.bounds is None

        return eq

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is not NotImplemented:
            result = not result
        return result

    def _as_defn(self):
        defn = CoordDefn(self.standard_name, self.long_name, self.var_name,
                         self.units, self.attributes, self.coord_system,
                         self.climatological)
        return defn

    # Must supply __hash__ as Python 3 does not enable it if __eq__ is defined.
    # NOTE: Violates "objects which compare equal must have the same hash".
    # We ought to remove this, as equality of two coords can *change*, so they
    # really should not be hashable.
    # However, current code needs it, e.g. so we can put them in sets.
    # Fixing it will require changing those uses.  See #962 and #1772.
    def __hash__(self):
        return hash(id(self))

    def __binary_operator__(self, other, mode_constant):
        """
        Common code which is called by add, sub, mul and div

        Mode constant is one of ADD, SUB, MUL, DIV, RDIV

        .. note::

            The unit is *not* changed when doing scalar operations on a
            coordinate. This means that a coordinate which represents
            "10 meters" when multiplied by a scalar i.e. "1000" would result
            in a coordinate of "10000 meters". An alternative approach could
            be taken to multiply the *unit* by 1000 and the resultant
            coordinate would represent "10 kilometers".

        """
        if isinstance(other, Coord):
            emsg = 'coord {} coord'.format(Coord._MODE_SYMBOL[mode_constant])
            raise iris.exceptions.NotYetImplementedError(emsg)

        elif isinstance(other, (int, float, np.number)):
            points = self._points_dm.core_data()

            if mode_constant == Coord._MODE_ADD:
                new_points = points + other
            elif mode_constant == Coord._MODE_SUB:
                new_points = points - other
            elif mode_constant == Coord._MODE_MUL:
                new_points = points * other
            elif mode_constant == Coord._MODE_DIV:
                new_points = points / other
            elif mode_constant == Coord._MODE_RDIV:
                new_points = other / points

            if self.has_bounds():
                bounds = self._bounds_dm.core_data()

                if mode_constant == Coord._MODE_ADD:
                    new_bounds = bounds + other
                elif mode_constant == Coord._MODE_SUB:
                    new_bounds = bounds - other
                elif mode_constant == Coord._MODE_MUL:
                    new_bounds = bounds * other
                elif mode_constant == Coord._MODE_DIV:
                    new_bounds = bounds / other
                elif mode_constant == Coord._MODE_RDIV:
                    new_bounds = other / bounds

            else:
                new_bounds = None
            new_coord = self.copy(new_points, new_bounds)
            return new_coord

        else:
            return NotImplemented

    def __add__(self, other):
        return self.__binary_operator__(other, Coord._MODE_ADD)

    def __sub__(self, other):
        return self.__binary_operator__(other, Coord._MODE_SUB)

    def __mul__(self, other):
        return self.__binary_operator__(other, Coord._MODE_MUL)

    def __div__(self, other):
        return self.__binary_operator__(other, Coord._MODE_DIV)

    def __truediv__(self, other):
        return self.__binary_operator__(other, Coord._MODE_DIV)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return (-self) + other

    def __rdiv__(self, other):
        return self.__binary_operator__(other, Coord._MODE_RDIV)

    def __rtruediv__(self, other):
        return self.__binary_operator__(other, Coord._MODE_RDIV)

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return self.copy(-self.core_points(),
                         -self.core_bounds() if self.has_bounds() else None)

    def convert_units(self, unit):
        """
        Change the coordinate's units, converting the values in its points
        and bounds arrays.

        For example, if a coordinate's :attr:`~iris.coords.Coord.units`
        attribute is set to radians then::

            coord.convert_units('degrees')

        will change the coordinate's
        :attr:`~iris.coords.Coord.units` attribute to degrees and
        multiply each value in :attr:`~iris.coords.Coord.points` and
        :attr:`~iris.coords.Coord.bounds` by 180.0/:math:`\pi`.

        """
        # If the coord has units convert the values in points (and bounds if
        # present).
        if self.units.is_unknown():
            raise iris.exceptions.UnitConversionError(
                'Cannot convert from unknown units. '
                'The "coord.units" attribute may be set directly.')
        if self.has_lazy_points() or self.has_lazy_bounds():
            # Make fixed copies of old + new units for a delayed conversion.
            old_unit = self.units
            new_unit = unit

            # Define a delayed conversion operation (i.e. a callback).
            def pointwise_convert(values):
                return old_unit.convert(values, new_unit)

        if self.has_lazy_points():
            new_points = _lazy.lazy_elementwise(self.lazy_points(),
                                                pointwise_convert)
        else:
            new_points = self.units.convert(self.points, unit)
        self.points = new_points
        if self.has_bounds():
            if self.has_lazy_bounds():
                new_bounds = _lazy.lazy_elementwise(self.lazy_bounds(),
                                                    pointwise_convert)
            else:
                new_bounds = self.units.convert(self.bounds, unit)
            self.bounds = new_bounds
        self.units = unit

    def cells(self):
        """
        Returns an iterable of Cell instances for this Coord.

        For example::

           for cell in self.cells():
              ...

        """
        return _CellIterator(self)

    def _sanity_check_bounds(self):
        if self.ndim == 1:
            if self.nbounds != 2:
                raise ValueError('Invalid operation for {!r}, with {} '
                                 'bound(s). Contiguous bounds are only '
                                 'defined for 1D coordinates with 2 '
                                 'bounds.'.format(self.name(), self.nbounds))
        elif self.ndim == 2:
            if self.nbounds != 4:
                raise ValueError('Invalid operation for {!r}, with {} '
                                 'bound(s). Contiguous bounds are only '
                                 'defined for 2D coordinates with 4 '
                                 'bounds.'.format(self.name(), self.nbounds))
        else:
            raise ValueError('Invalid operation for {!r}. Contiguous bounds '
                             'are not defined for coordinates with more than '
                             '2 dimensions.'.format(self.name()))

    def _discontiguity_in_bounds(self, rtol=1e-5, atol=1e-8):
        """
        Checks that the bounds of the coordinate are contiguous.

        Kwargs:
        * rtol: (float)
            Relative tolerance that is used when checking contiguity. Defaults
            to 1e-5.
        * atol: (float)
            Absolute tolerance that is used when checking contiguity. Defaults
            to 1e-8.

        Returns:
        * contiguous: (boolean)
            True if there are no discontiguities.
        * diffs: (array or tuple of arrays)
            The diffs along the bounds of the coordinate. If self is a 2D
            coord of shape (Y, X), a tuple of arrays is returned, where the
            first is an array of differences along the x-axis, of the shape
            (Y, X-1) and the second is an array of differences along the
            y-axis, of the shape (Y-1, X).

        """
        self._sanity_check_bounds()

        if self.ndim == 1:
            contiguous = np.allclose(self.bounds[1:, 0],
                                     self.bounds[:-1, 1],
                                     rtol=rtol, atol=atol)
            diffs = np.abs(self.bounds[:-1, 1] - self.bounds[1:, 0])

        elif self.ndim == 2:
            def mod360_adjust(compare_axis):
                bounds = self.bounds.copy()

                if compare_axis == 'x':
                    upper_bounds = bounds[:, :-1, 1]
                    lower_bounds = bounds[:, 1:, 0]
                elif compare_axis == 'y':
                    upper_bounds = bounds[:-1, :, 3]
                    lower_bounds = bounds[1:, :, 0]

                if self.name() in ['longitude', 'grid_longitude']:
                    # If longitude, adjust for longitude wrapping
                    diffs = upper_bounds - lower_bounds
                    index = diffs > 180
                    if index.any():
                        sign = np.sign(diffs)
                        modification = (index.astype(int) * 360) * sign
                        upper_bounds -= modification

                diffs_between_cells = np.abs(upper_bounds - lower_bounds)
                cell_size = lower_bounds - upper_bounds
                diffs_along_axis = diffs_between_cells > (atol +
                                                          rtol * cell_size)

                points_close_enough = diffs_along_axis <= (atol +
                                                           rtol * cell_size)
                contiguous_along_axis = np.all(points_close_enough)
                return diffs_along_axis, contiguous_along_axis

            diffs_along_x, match_cell_x1 = mod360_adjust(compare_axis='x')
            diffs_along_y, match_cell_y1 = mod360_adjust(compare_axis='y')

            contiguous = match_cell_x1 and match_cell_y1
            diffs = (diffs_along_x, diffs_along_y)

        return contiguous, diffs

    def is_contiguous(self, rtol=1e-05, atol=1e-08):
        """
        Return True if, and only if, this Coord is bounded with contiguous
        bounds to within the specified relative and absolute tolerances.

        1D coords are contiguous if the upper bound of a cell aligns,
        within a tolerance, to the lower bound of the next cell along.

        2D coords, with 4 bounds, are contiguous if the lower right corner of
        each cell aligns with the lower left corner of the cell to the right of
        it, and the upper left corner of each cell aligns with the lower left
        corner of the cell above it.

        Args:

        * rtol:
            The relative tolerance parameter (default is 1e-05).
        * atol:
            The absolute tolerance parameter (default is 1e-08).

        Returns:
            Boolean.

        """
        if self.has_bounds():
            contiguous, _ = self._discontiguity_in_bounds(rtol=rtol, atol=atol)
        else:
            contiguous = False
        return contiguous

    def contiguous_bounds(self):
        """
        Returns the N+1 bound values for a contiguous bounded 1D coordinate
        of length N, or the (N+1, M+1) bound values for a contiguous bounded 2D
        coordinate of shape (N, M).

        Only 1D or 2D coordinates are supported.

        .. note::

            If the coordinate has bounds, this method assumes they are
            contiguous.

            If the coordinate is 1D and does not have bounds, this method will
            return bounds positioned halfway between the coordinate's points.

            If the coordinate is 2D and does not have bounds, an error will be
            raised.

        """
        if not self.has_bounds():
            if self.ndim == 1:
                warnings.warn('Coordinate {!r} is not bounded, guessing '
                              'contiguous bounds.'.format(self.name()))
                bounds = self._guess_bounds()
            elif self.ndim == 2:
                raise ValueError('2D coordinate {!r} is not bounded. Guessing '
                                 'bounds of 2D coords is not currently '
                                 'supported.'.format(self.name()))
        else:
            self._sanity_check_bounds()
            bounds = self.bounds

        if self.ndim == 1:
            c_bounds = np.resize(bounds[:, 0], bounds.shape[0] + 1)
            c_bounds[-1] = bounds[-1, 1]
        elif self.ndim == 2:
            c_bounds = _get_2d_coord_bound_grid(bounds)
        return c_bounds

    def is_monotonic(self):
        """Return True if, and only if, this Coord is monotonic."""

        if self.ndim != 1:
            raise iris.exceptions.CoordinateMultiDimError(self)

        if self.shape == (1,):
            return True

        if self.points is not None:
            if not iris.util.monotonic(self.points, strict=True):
                return False

        if self.has_bounds():
            for b_index in range(self.nbounds):
                if not iris.util.monotonic(self.bounds[..., b_index],
                                           strict=True):
                    return False

        return True

    def is_compatible(self, other, ignore=None):
        """
        Return whether the coordinate is compatible with another.

        Compatibility is determined by comparing
        :meth:`iris.coords.Coord.name()`, :attr:`iris.coords.Coord.units`,
        :attr:`iris.coords.Coord.coord_system` and
        :attr:`iris.coords.Coord.attributes` that are present in both objects.

        Args:

        * other:
            An instance of :class:`iris.coords.Coord` or
            :class:`iris.coords.CoordDefn`.
        * ignore:
           A single attribute key or iterable of attribute keys to ignore when
           comparing the coordinates. Default is None. To ignore all
           attributes, set this to other.attributes.

        Returns:
           Boolean.

        """
        compatible = (self.name() == other.name() and
                      self.units == other.units and
                      self.coord_system == other.coord_system)

        if compatible:
            common_keys = set(self.attributes).intersection(other.attributes)
            if ignore is not None:
                if isinstance(ignore, six.string_types):
                    ignore = (ignore,)
                common_keys = common_keys.difference(ignore)
            for key in common_keys:
                if np.any(self.attributes[key] != other.attributes[key]):
                    compatible = False
                    break

        return compatible

    @property
    def dtype(self):
        """
        The NumPy dtype of the coord, as specified by its points.

        """
        return self._points_dm.dtype

    @property
    def bounds_dtype(self):
        """
        The NumPy dtype of the coord's bounds. Will be `None` if the coord
        does not have bounds.

        """
        result = None
        if self.has_bounds():
            result = self._bounds_dm.dtype
        return result

    @property
    def ndim(self):
        """
        Return the number of dimensions of the coordinate (not including the
        bounded dimension).

        """
        return self._points_dm.ndim

    @property
    def nbounds(self):
        """
        Return the number of bounds that this coordinate has (0 for no bounds).

        """
        nbounds = 0
        if self.has_bounds():
            nbounds = self._bounds_dm.shape[-1]
        return nbounds

    def has_bounds(self):
        """Return a boolean indicating whether the coord has a bounds array."""
        return self._bounds_dm is not None

    @property
    def shape(self):
        """The fundamental shape of the Coord, expressed as a tuple."""
        return self._points_dm.shape

    def cell(self, index):
        """
        Return the single :class:`Cell` instance which results from slicing the
        points/bounds with the given index.

        .. note::

            If `iris.FUTURE.cell_datetime_objects` is True, then this
            method will return Cell objects whose `points` and `bounds`
            attributes contain either datetime.datetime instances or
            cftime.datetime instances (depending on the calendar).

        .. deprecated:: 2.0.0

            The option `iris.FUTURE.cell_datetime_objects` is deprecated and
            will be removed in a future release; it is now set to True by
            default. Please update your code to support using cells as
            datetime objects.

        """
        index = iris.util._build_full_slice_given_keys(index, self.ndim)

        point = tuple(np.array(self.points[index], ndmin=1).flatten())
        if len(point) != 1:
            raise IndexError('The index %s did not uniquely identify a single '
                             'point to create a cell with.' % (index, ))

        bound = None
        if self.has_bounds():
            bound = tuple(np.array(self.bounds[index], ndmin=1).flatten())

        if iris.FUTURE.cell_datetime_objects:
            if self.units.is_time_reference():
                point = self.units.num2date(point)
                if bound is not None:
                    bound = self.units.num2date(bound)
        else:
            wmsg = ("disabling cells as datetime objects is deprecated "
                    "behaviour. "
                    "Please update your code to support using cells as "
                    "datetime objects."
                    "See the userguide section 2.2.1 for examples of this.")
            warn_deprecated(wmsg)

        return Cell(point, bound)

    def collapsed(self, dims_to_collapse=None):
        """
        Returns a copy of this coordinate, which has been collapsed along
        the specified dimensions.

        Replaces the points & bounds with a simple bounded region.
        """
        import dask.array as da
        # Ensure dims_to_collapse is a tuple to be able to pass
        # through to numpy
        if isinstance(dims_to_collapse, (int, np.integer)):
            dims_to_collapse = (dims_to_collapse, )
        if isinstance(dims_to_collapse, list):
            dims_to_collapse = tuple(dims_to_collapse)

        if np.issubdtype(self.dtype, np.str_):
            # Collapse the coordinate by serializing the points and
            # bounds as strings.
            def serialize(x):
                return '|'.join([str(i) for i in x.flatten()])
            bounds = None
            string_type_fmt = 'S{}' if six.PY2 else 'U{}'
            if self.has_bounds():
                shape = self._bounds_dm.shape[1:]
                bounds = []
                for index in np.ndindex(shape):
                    index_slice = (slice(None),) + tuple(index)
                    bounds.append(serialize(self.bounds[index_slice]))
                dtype = np.dtype(string_type_fmt.format(max(map(len, bounds))))
                bounds = np.array(bounds, dtype=dtype).reshape((1,) + shape)
            points = serialize(self.points)
            dtype = np.dtype(string_type_fmt.format(len(points)))
            # Create the new collapsed coordinate.
            coord = self.copy(points=np.array(points, dtype=dtype),
                              bounds=bounds)
        else:
            # Collapse the coordinate by calculating the bounded extremes.
            if self.ndim > 1:
                msg = 'Collapsing a multi-dimensional coordinate. ' \
                    'Metadata may not be fully descriptive for {!r}.'
                warnings.warn(msg.format(self.name()))
            elif not self.is_contiguous():
                msg = 'Collapsing a non-contiguous coordinate. ' \
                    'Metadata may not be fully descriptive for {!r}.'
                warnings.warn(msg.format(self.name()))

            if self.has_bounds():
                item = self.core_bounds()
                if dims_to_collapse is not None:
                    # Express main dims_to_collapse as non-negative integers
                    # and add the last (bounds specific) dimension.
                    dims_to_collapse = tuple(
                        dim % self.ndim for dim in dims_to_collapse) + (-1,)
            else:
                item = self.core_points()

            # Determine the array library for stacking
            al = da if _lazy.is_lazy_data(item) else np

            # Calculate the bounds and points along the right dims
            bounds = al.stack([item.min(axis=dims_to_collapse),
                               item.max(axis=dims_to_collapse)], axis=-1)
            points = al.array(bounds.sum(axis=-1) * 0.5, dtype=self.dtype)

            # Create the new collapsed coordinate.
            coord = self.copy(points=points, bounds=bounds)
        return coord

    def _guess_bounds(self, bound_position=0.5):
        """
        Return bounds for this coordinate based on its points.

        Kwargs:

        * bound_position:
            The desired position of the bounds relative to the position
            of the points.

        Returns:
            A numpy array of shape (len(self.points), 2).

        .. note::

            This method only works for coordinates with ``coord.ndim == 1``.

        .. note::

            If `iris.FUTURE.clip_latitudes` is True, then this method
            will clip the coordinate bounds to the range [-90, 90] when:

            - it is a `latitude` or `grid_latitude` coordinate,
            - the units are degrees,
            - all the points are in the range [-90, 90].

        .. deprecated:: 2.0.0

            The `iris.FUTURE.clip_latitudes` option is now deprecated
            and is set to True by default. Please remove code which
            relies on coordinate bounds being outside the range
            [-90, 90].

        """
        # XXX Consider moving into DimCoord
        # ensure we have monotonic points
        if not self.is_monotonic():
            raise ValueError("Need monotonic points to generate bounds for %s"
                             % self.name())

        if self.ndim != 1:
            raise iris.exceptions.CoordinateMultiDimError(self)

        if self.shape[0] < 2:
            raise ValueError('Cannot guess bounds for a coordinate of length '
                             '1.')

        if self.has_bounds():
            raise ValueError('Coord already has bounds. Remove the bounds '
                             'before guessing new ones.')

        if getattr(self, 'circular', False):
            points = np.empty(self.shape[0] + 2)
            points[1:-1] = self.points
            direction = 1 if self.points[-1] > self.points[0] else -1
            points[0] = self.points[-1] - (self.units.modulus * direction)
            points[-1] = self.points[0] + (self.units.modulus * direction)
            diffs = np.diff(points)
        else:
            diffs = np.diff(self.points)
            diffs = np.insert(diffs, 0, diffs[0])
            diffs = np.append(diffs, diffs[-1])

        min_bounds = self.points - diffs[:-1] * bound_position
        max_bounds = self.points + diffs[1:] * (1 - bound_position)

        bounds = np.array([min_bounds, max_bounds]).transpose()

        if iris.FUTURE.clip_latitudes:
            if (self.name() in ('latitude', 'grid_latitude') and
                    self.units == 'degree'):
                points = self.points
                if (points >= -90).all() and (points <= 90).all():
                    np.clip(bounds, -90, 90, out=bounds)
        else:
            wmsg = ("guessing latitude bounds outside of [-90, 90] is "
                    "deprecated behaviour. "
                    "All latitude points will be clipped to the range "
                    "[-90, 90].")
            warn_deprecated(wmsg)

        return bounds

    def guess_bounds(self, bound_position=0.5):
        """
        Add contiguous bounds to a coordinate, calculated from its points.

        Puts a cell boundary at the specified fraction between each point and
        the next, plus extrapolated lowermost and uppermost bound points, so
        that each point lies within a cell.

        With regularly spaced points, the resulting bounds will also be
        regular, and all points lie at the same position within their cell.
        With irregular points, the first and last cells are given the same
        widths as the ones next to them.

        Kwargs:

        * bound_position:
            The desired position of the bounds relative to the position
            of the points.

        .. note::

            An error is raised if the coordinate already has bounds, is not
            one-dimensional, or is not monotonic.

        .. note::

            Unevenly spaced values, such from a wrapped longitude range, can
            produce unexpected results :  In such cases you should assign
            suitable values directly to the bounds property, instead.

        .. note::

            If `iris.FUTURE.clip_latitudes` is True, then this method
            will clip the coordinate bounds to the range [-90, 90] when:

            - it is a `latitude` or `grid_latitude` coordinate,
            - the units are degrees,
            - all the points are in the range [-90, 90].

        .. deprecated:: 2.0.0

            The `iris.FUTURE.clip_latitudes` option is now deprecated
            and is set to True by default. Please remove code which
            relies on coordinate bounds being outside the range
            [-90, 90].

        """
        self.bounds = self._guess_bounds(bound_position)

    def intersect(self, other, return_indices=False):
        """
        Returns a new coordinate from the intersection of two coordinates.

        Both coordinates must be compatible as defined by
        :meth:`~iris.coords.Coord.is_compatible`.

        Kwargs:

        * return_indices:
            If True, changes the return behaviour to return the intersection
            indices for the "self" coordinate.

        """
        if not self.is_compatible(other):
            msg = 'The coordinates cannot be intersected. They are not ' \
                  'compatible because of differing metadata.'
            raise ValueError(msg)

        # Cache self.cells for speed. We can also use the index operation on a
        # list conveniently.
        self_cells = [cell for cell in self.cells()]

        # Maintain a list of indices on self for which cells exist in both self
        # and other.
        self_intersect_indices = []
        for cell in other.cells():
            try:
                self_intersect_indices.append(self_cells.index(cell))
            except ValueError:
                pass

        if return_indices is False and self_intersect_indices == []:
            raise ValueError('No intersection between %s coords possible.' %
                             self.name())

        self_intersect_indices = np.array(self_intersect_indices)

        # Return either the indices, or a Coordinate instance of the
        # intersection.
        if return_indices:
            return self_intersect_indices
        else:
            return self[self_intersect_indices]

    def nearest_neighbour_index(self, point):
        """
        Returns the index of the cell nearest to the given point.

        Only works for one-dimensional coordinates.

        For example:

        >>> cube = iris.load_cube(iris.sample_data_path('ostia_monthly.nc'))
        >>> cube.coord('latitude').nearest_neighbour_index(0)
        9
        >>> cube.coord('longitude').nearest_neighbour_index(10)
        12

        .. note:: If the coordinate contains bounds, these will be used to
            determine the nearest neighbour instead of the point values.

        .. note:: For circular coordinates, the 'nearest' point can wrap around
            to the other end of the values.

        """
        points = self.points
        bounds = self.bounds if self.has_bounds() else np.array([])
        if self.ndim != 1:
            raise ValueError('Nearest-neighbour is currently limited'
                             ' to one-dimensional coordinates.')
        do_circular = getattr(self, 'circular', False)
        if do_circular:
            wrap_modulus = self.units.modulus
            # wrap 'point' to a range based on lowest points or bounds value.
            wrap_origin = np.min(np.hstack((points, bounds.flatten())))
            point = wrap_origin + (point - wrap_origin) % wrap_modulus

        # Calculate the nearest neighbour.
        # The algorithm:  given a single value (V),
        #   if coord has bounds,
        #     make bounds cells complete and non-overlapping
        #     return first cell containing V
        #   else (no bounds),
        #     find the point which is closest to V
        #     or if two are equally close, return the lowest index
        if self.has_bounds():
            # make bounds ranges complete+separate, so point is in at least one
            increasing = self.bounds[0, 1] > self.bounds[0, 0]
            bounds = bounds.copy()
            # sort the bounds cells by their centre values
            sort_inds = np.argsort(np.mean(bounds, axis=1))
            bounds = bounds[sort_inds]
            # replace all adjacent bounds with their averages
            if increasing:
                mid_bounds = 0.5 * (bounds[:-1, 1] + bounds[1:, 0])
                bounds[:-1, 1] = mid_bounds
                bounds[1:, 0] = mid_bounds
            else:
                mid_bounds = 0.5 * (bounds[:-1, 0] + bounds[1:, 1])
                bounds[:-1, 0] = mid_bounds
                bounds[1:, 1] = mid_bounds

            # if point lies beyond either end, fix the end cell to include it
            bounds[0, 0] = min(point, bounds[0, 0])
            bounds[-1, 1] = max(point, bounds[-1, 1])
            # get index of first-occurring cell that contains the point
            inside_cells = np.logical_and(point >= np.min(bounds, axis=1),
                                          point <= np.max(bounds, axis=1))
            result_index = np.where(inside_cells)[0][0]
            # return the original index of the cell (before the bounds sort)
            result_index = sort_inds[result_index]

        # Or, if no bounds, we always have points ...
        else:
            if do_circular:
                # add an extra, wrapped max point (simpler than bounds case)
                # NOTE: circular implies a DimCoord, so *must* be monotonic
                if points[-1] >= points[0]:
                    # ascending value order : add wrapped lowest value to end
                    index_offset = 0
                    points = np.hstack((points, points[0] + wrap_modulus))
                else:
                    # descending order : add wrapped lowest value at start
                    index_offset = 1
                    points = np.hstack((points[-1] + wrap_modulus, points))
            # return index of first-occurring nearest point
            distances = np.abs(points - point)
            result_index = np.where(distances == np.min(distances))[0][0]
            if do_circular:
                # convert index back from circular-adjusted points
                result_index = (result_index - index_offset) % self.shape[0]

        return result_index

    def xml_element(self, doc):
        """Return a DOM element describing this Coord."""
        # Create the XML element as the camelCaseEquivalent of the
        # class name.
        element_name = type(self).__name__
        element_name = element_name[0].lower() + element_name[1:]
        element = doc.createElement(element_name)

        element.setAttribute('id', self._xml_id())

        if self.standard_name:
            element.setAttribute('standard_name', str(self.standard_name))
        if self.long_name:
            element.setAttribute('long_name', str(self.long_name))
        if self.var_name:
            element.setAttribute('var_name', str(self.var_name))
        element.setAttribute('units', repr(self.units))
        if self.climatological:
            element.setAttribute('climatological', str(self.climatological))

        if self.attributes:
            attributes_element = doc.createElement('attributes')
            for name in sorted(six.iterkeys(self.attributes)):
                attribute_element = doc.createElement('attribute')
                attribute_element.setAttribute('name', name)
                attribute_element.setAttribute('value',
                                               str(self.attributes[name]))
                attributes_element.appendChild(attribute_element)
            element.appendChild(attributes_element)

        # Add a coord system sub-element?
        if self.coord_system:
            element.appendChild(self.coord_system.xml_element(doc))

        # Add the values
        element.setAttribute('value_type', str(self._value_type_name()))
        element.setAttribute('shape', str(self.shape))
        if hasattr(self.points, 'to_xml_attr'):
            element.setAttribute('points', self.points.to_xml_attr())
        else:
            element.setAttribute('points', iris.util.format_array(self.points))

        if self.has_bounds():
            if hasattr(self.bounds, 'to_xml_attr'):
                element.setAttribute('bounds', self.bounds.to_xml_attr())
            else:
                element.setAttribute('bounds',
                                     iris.util.format_array(self.bounds))

        return element

    def _xml_id(self):
        # Returns a consistent, unique string identifier for this coordinate.
        unique_value = b''
        if self.standard_name:
            unique_value += self.standard_name.encode('utf-8')
        unique_value += b'\0'
        if self.long_name:
            unique_value += self.long_name.encode('utf-8')
        unique_value += b'\0'
        unique_value += str(self.units).encode('utf-8') + b'\0'
        for k, v in sorted(self.attributes.items()):
            unique_value += (str(k) + ':' + str(v)).encode('utf-8') + b'\0'
        unique_value += str(self.coord_system).encode('utf-8') + b'\0'
        # Mask to ensure consistency across Python versions & platforms.
        crc = zlib.crc32(unique_value) & 0xffffffff
        return '%08x' % (crc, )

    def _value_type_name(self):
        """
        A simple, readable name for the data type of the Coord point/bound
        values.

        """
        dtype = self.core_points().dtype
        kind = dtype.kind
        if kind in 'SU':
            # Establish the basic type name for 'string' type data.
            # N.B. this means "unicode" in Python3, and "str" in Python2.
            value_type_name = 'string'

            # Override this if not the 'native' string type.
            if six.PY3:
                if kind == 'S':
                    value_type_name = 'bytes'
            else:
                if kind == 'U':
                    value_type_name = 'unicode'
        else:
            value_type_name = dtype.name

        return value_type_name


class DimCoord(Coord):
    """
    A coordinate that is 1D, numeric, and strictly monotonic.

    """
    @classmethod
    def from_regular(cls, zeroth, step, count, standard_name=None,
                     long_name=None, var_name=None, units='1', attributes=None,
                     coord_system=None, circular=False, with_bounds=False):
        """
        Create a :class:`DimCoord` with regularly spaced points, and
        optionally bounds.

        The majority of the arguments are defined as for
        :meth:`Coord.__init__`, but those which differ are defined below.

        Args:

        * zeroth:
            The value *prior* to the first point value.
        * step:
            The numeric difference between successive point values.
        * count:
            The number of point values.

        Kwargs:

        * with_bounds:
            If True, the resulting DimCoord will possess bound values
            which are equally spaced around the points. Otherwise no
            bounds values will be defined. Defaults to False.

        """
        points = (zeroth + step) + step * np.arange(count, dtype=np.float32)
        _, regular = points_step(points)
        if not regular:
            points = (zeroth + step) + step * np.arange(count,
                                                        dtype=np.float64)
        points.flags.writeable = False

        if with_bounds:
            delta = 0.5 * step
            bounds = np.concatenate([[points - delta], [points + delta]]).T
            bounds.flags.writeable = False
        else:
            bounds = None

        return cls(points, standard_name=standard_name,
                   long_name=long_name, var_name=var_name, units=units,
                   bounds=bounds, attributes=attributes,
                   coord_system=coord_system, circular=circular)

    def __init__(self, points, standard_name=None, long_name=None,
                 var_name=None, units='1', bounds=None,
                 attributes=None, coord_system=None, circular=False,
                 climatological=False):
        """
        Create a 1D, numeric, and strictly monotonic :class:`Coord` with
        read-only points and bounds.

        """
        super(DimCoord, self).__init__(
            points, standard_name=standard_name,
            long_name=long_name, var_name=var_name,
            units=units, bounds=bounds,
            attributes=attributes,
            coord_system=coord_system,
            climatological=climatological)

        #: Whether the coordinate wraps by ``coord.units.modulus``.
        self.circular = bool(circular)

    def __deepcopy__(self, memo):
        """
        coord.__deepcopy__() -> Deep copy of coordinate.

        Used if copy.deepcopy is called on a coordinate.

        """
        new_coord = copy.deepcopy(super(DimCoord, self), memo)
        # Ensure points and bounds arrays are read-only.
        new_coord._points_dm.data.flags.writeable = False
        if new_coord._bounds_dm is not None:
            new_coord._bounds_dm.data.flags.writeable = False
        return new_coord

    def copy(self, points=None, bounds=None):
        new_coord = super(DimCoord, self).copy(points=points, bounds=bounds)
        # Make the arrays read-only.
        new_coord._points_dm.data.flags.writeable = False
        if bounds is not None:
            new_coord._bounds_dm.data.flags.writeable = False
        return new_coord

    def __eq__(self, other):
        # TODO investigate equality of AuxCoord and DimCoord if circular is
        # False.
        result = NotImplemented
        if isinstance(other, DimCoord):
            result = (Coord.__eq__(self, other) and self.circular ==
                      other.circular)
        return result

    # The __ne__ operator from Coord implements the not __eq__ method.

    # For Python 3, we must explicitly re-implement the '__hash__' method, as
    # defining an '__eq__' has blocked its inheritance.  See ...
    # https://docs.python.org/3.1/reference/datamodel.html#object.__hash__
    # "If a class that overrides __eq__() needs to retain the
    # implementation of __hash__() from a parent class, the interpreter
    # must be told this explicitly".
    __hash__ = Coord.__hash__

    def __getitem__(self, key):
        coord = super(DimCoord, self).__getitem__(key)
        coord.circular = self.circular and coord.shape == self.shape
        return coord

    def collapsed(self, dims_to_collapse=None):
        coord = Coord.collapsed(self, dims_to_collapse=dims_to_collapse)
        if self.circular and self.units.modulus is not None:
            bnds = coord.bounds.copy()
            bnds[0, 1] = coord.bounds[0, 0] + self.units.modulus
            coord.bounds = bnds
            coord.points = np.array(np.sum(coord.bounds) * 0.5,
                                    dtype=self.points.dtype)
        # XXX This isn't actually correct, but is ported from the old world.
        coord.circular = False
        return coord

    def _repr_other_metadata(self):
        result = Coord._repr_other_metadata(self)
        if self.circular:
            result += ', circular=%r' % self.circular
        return result

    def _new_points_requirements(self, points):
        """
        Confirm that a new set of coord points adheres to the requirements for
        :class:`~iris.coords.DimCoord` points, being:
            * points are scalar or 1D,
            * points are numeric,
            * points are not masked, and
            * points are monotonic.

        """
        if points.ndim not in (0, 1):
            emsg = 'The {!r} {} points array must be scalar or 1-dimensional.'
            raise ValueError(emsg.format(self.name(), self.__class__.__name__))
        if not np.issubdtype(points.dtype, np.number):
            emsg = 'The {!r} {} points array must be numeric.'
            raise ValueError(emsg.format(self.name(), self.__class__.__name__))
        if ma.is_masked(points):
            emsg = 'A {!r} {} points array must not be masked.'
            raise TypeError(emsg.format(self.name(), self.__class__.__name__))
        if points.size > 1 and not iris.util.monotonic(points, strict=True):
            emsg = 'The {!r} {} points array must be strictly monotonic.'
            raise ValueError(emsg.format(self.name(), self.__class__.__name__))

    @Coord.points.setter
    def points(self, points):
        # DimCoord always realises the points, to allow monotonicity checks.
        # Ensure it is an actual array, and also make our own copy so that we
        # can make it read-only.
        points = _lazy.as_concrete_data(points)
        # Make sure that we have an array (any type of array).
        points = np.asanyarray(points)

        # Check validity requirements for dimension-coordinate points.
        self._new_points_requirements(points)
        # Cast to a numpy array for masked arrays with no mask.
        points = np.array(points)

        # Call the parent points setter.
        super(DimCoord, self.__class__).points.fset(self, points)

        if self._points_dm is not None:
            # Re-fetch the core array, as the super call may replace it.
            points = self._points_dm.core_data()
            # N.B. always a *real* array, as we realised 'points' at the start.

            # Make the array read-only.
            points.flags.writeable = False

    def _new_bounds_requirements(self, bounds):
        """
        Confirm that a new set of coord bounds adheres to the requirements for
        :class:`~iris.coords.DimCoord` bounds, being:
            * bounds are compatible in shape with the points
            * bounds are numeric,
            * bounds are not masked, and
            * bounds are monotonic in the first dimension.

        """
        # Ensure the bounds are a compatible shape.
        if self.shape != bounds.shape[:-1] and \
                not (self.shape == (1,) and bounds.ndim == 1):
            emsg = ('The shape of the {!r} {} bounds array should be '
                    'points.shape + (n_bounds)')
            raise ValueError(emsg.format(self.name(), self.__class__.__name__))
        # Checks for numeric.
        if not np.issubdtype(bounds.dtype, np.number):
            emsg = 'The {!r} {} bounds array must be numeric.'
            raise ValueError(emsg.format(self.name(), self.__class__.__name__))
        # Check not masked.
        if ma.is_masked(bounds):
            emsg = 'A {!r} {} bounds array must not be masked.'
            raise TypeError(emsg.format(self.name(), self.__class__.__name__))

        # Check bounds are monotonic.
        if bounds.ndim > 1:
            n_bounds = bounds.shape[-1]
            n_points = bounds.shape[0]
            if n_points > 1:

                directions = set()
                for b_index in range(n_bounds):
                    monotonic, direction = iris.util.monotonic(
                        bounds[:, b_index], strict=True, return_direction=True)
                    if not monotonic:
                        emsg = ('The {!r} {} bounds array must be strictly '
                                'monotonic.')
                        raise ValueError(emsg.format(self.name(),
                                                     self.__class__.__name__))
                    directions.add(direction)

                if len(directions) != 1:
                    emsg = ('The direction of monotonicity for {!r} {} must '
                            'be consistent across all bounds.')
                    raise ValueError(emsg.format(self.name(),
                                                 self.__class__.__name__))

    @Coord.bounds.setter
    def bounds(self, bounds):
        if bounds is not None:
            # Ensure we have a realised array of new bounds values.
            bounds = _lazy.as_concrete_data(bounds)
            # Make sure we have an array (any type of array).
            bounds = np.asanyarray(bounds)

            # Check validity requirements for dimension-coordinate bounds.
            self._new_bounds_requirements(bounds)
            # Cast to a numpy array for masked arrays with no mask.
            bounds = np.array(bounds)

        # Call the parent bounds setter.
        super(DimCoord, self.__class__).bounds.fset(self, bounds)

        if self._bounds_dm is not None:
            # Re-fetch the core array, as the super call may replace it.
            bounds = self._bounds_dm.core_data()
            # N.B. always a *real* array, as we realised 'bounds' at the start.

            # Ensure the array is read-only.
            bounds.flags.writeable = False

    def is_monotonic(self):
        return True

    def xml_element(self, doc):
        """Return DOM element describing this :class:`iris.coords.DimCoord`."""
        element = super(DimCoord, self).xml_element(doc)
        if self.circular:
            element.setAttribute('circular', str(self.circular))
        return element


class AuxCoord(Coord):
    """
    A CF auxiliary coordinate.

    .. note::

        There are currently no specific properties of :class:`AuxCoord`,
        everything is inherited from :class:`Coord`.

    """
    # Logically, :class:`Coord` is an abstract class and all actual coords must
    # be members of some concrete subclass, i.e. an :class:`AuxCoord` or
    # a :class:`DimCoord`.
    # So we retain :class:`AuxCoord` as a distinct concrete subclass.
    # This provides clarity, backwards compatibility, and so we can add
    # AuxCoord-specific code if needed in future.


class CellMeasure(six.with_metaclass(ABCMeta, CFVariableMixin)):
    """
    A CF Cell Measure, providing area or volume properties of a cell
    where these cannot be inferred from the Coordinates and
    Coordinate Reference System.

    """

    def __init__(self, data, standard_name=None, long_name=None,
                 var_name=None, units='1', attributes=None, measure=None):

        """
        Constructs a single cell measure.

        Args:

        * data:
            The values of the measure for each cell.
            Either a 'real' array (:class:`numpy.ndarray`) or a 'lazy' array
            (:class:`dask.array.Array`).

        Kwargs:

        * standard_name:
            CF standard name of the cell measure.
        * long_name:
            Descriptive name of the cell measure.
        * var_name:
            The netCDF variable name for the cell measure.
        * units
            The :class:`~cf_units.Unit` of the cell measure's values.
            Can be a string, which will be converted to a Unit object.
        * attributes
            A dictionary containing other CF and user-defined attributes.
        * measure
            A string describing the type of measure.  'area' and 'volume'
            are the only valid entries.

        """
        #: CF standard name of the quantity that the cell measure represents.
        self.standard_name = standard_name

        #: Descriptive name of the cell measure.
        self.long_name = long_name

        #: The netCDF variable name for the cell measure.
        self.var_name = var_name

        #: Unit of the quantity that the cell measure represents.
        self.units = units

        #: Other attributes, including user specified attributes that
        #: have no meaning to Iris.
        self.attributes = attributes

        #: String naming the measure type.
        self.measure = measure

        # Initialise data via the data setter code, which applies standard
        # checks and ajustments.
        self.data = data

    @property
    def measure(self):
        return self._measure

    @property
    def data(self):
        """Property containing the data values as a numpy array"""
        return self._data_manager.data

    @data.setter
    def data(self, data):
        # Set the data to a new array - as long as it's the same shape.
        # If data are already defined for this CellMeasure,
        if data is None:
            raise ValueError('The data payload of a CellMeasure may not be '
                             'None; it must be a numpy array or equivalent.')
        if data.shape == ():
            # If we have a scalar value, promote the shape from () to (1,).
            # NOTE: this way also *realises* it.  Don't think that matters.
            data = np.array(data, ndmin=1)
        if hasattr(self, '_data_manager') and self._data_manager is not None:
            # Check that setting these data wouldn't change self.shape
            if data.shape != self.shape:
                raise ValueError("New data shape must match existing data "
                                 "shape.")

        self._data_manager = DataManager(data)

    @property
    def shape(self):
        """Returns the shape of the Cell Measure, expressed as a tuple."""
        return self._data_manager.shape

    @property
    def ndim(self):
        """Returns the number of dimensions of the cell measure."""
        return self._data_manager.ndim

    @measure.setter
    def measure(self, measure):
        if measure not in ['area', 'volume']:
            raise ValueError("measure must be 'area' or 'volume', "
                             "not {}".format(measure))
        self._measure = measure

    def __getitem__(self, keys):
        """
        Returns a new CellMeasure whose values are obtained by
        conventional array indexing.

        """
        # Get the data, all or part of which will become the new data.
        data = self._data_manager.core_data()

        # Index data with the keys.
        # Note: does not copy data unless it has to.
        _, data = iris.util._slice_data_with_keys(data, keys)

        # Always copy data, to avoid making the new measure a view onto the old
        # one.
        data = data.copy()

        # The result is a copy with replacement data.
        return self.copy(data=data)

    def copy(self, data=None):
        """
        Returns a copy of this CellMeasure.

        Kwargs:

        * data: A data array for the new cell_measure.
                This may be a different shape to the data of the
                cell_measure being copied.

        """
        new_cell_measure = copy.deepcopy(self)
        if data is not None:
            # Remove the existing data manager, to prevent the data setter
            # checking against existing content.
            new_cell_measure._data_manager = None
            # Set new data via the data setter code, which applies standard
            # checks and ajustments.
            new_cell_measure.data = data

        return new_cell_measure

    def _repr_other_metadata(self):
        fmt = ''
        if self.long_name:
            fmt = ', long_name={self.long_name!r}'
        if self.var_name:
            fmt += ', var_name={self.var_name!r}'
        if len(self.attributes) > 0:
            fmt += ', attributes={self.attributes}'
        result = fmt.format(self=self)
        return result

    def __str__(self):
        result = repr(self)
        return result

    def __repr__(self):
        fmt = ('{cls}({self.data!r}'
               ', measure={self.measure}, standard_name={self.standard_name!r}'
               ', units={self.units!r}{other_metadata})')
        result = fmt.format(self=self, cls=type(self).__name__,
                            other_metadata=self._repr_other_metadata())
        return result

    def _as_defn(self):
        defn = (self.standard_name, self.long_name, self.var_name,
                self.units, self.attributes, self.measure)
        return defn

    def __eq__(self, other):
        eq = NotImplemented
        if isinstance(other, CellMeasure):
            eq = self._as_defn() == other._as_defn()
            if eq:
                eq = (self.data == other.data).all()
        return eq

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is not NotImplemented:
            result = not result
        return result


class CellMethod(iris.util._OrderedHashable):
    """
    Represents a sub-cell pre-processing operation.

    """

    # Declare the attribute names relevant to the _OrderedHashable behaviour.
    _names = ('method', 'coord_names', 'intervals', 'comments')

    #: The name of the operation that was applied. e.g. "mean", "max", etc.
    method = None

    #: The tuple of coordinate names over which the operation was applied.
    coord_names = None

    #: A description of the original intervals over which the operation
    #: was applied.
    intervals = None

    #: Additional comments.
    comments = None

    def __init__(self, method, coords=None, intervals=None, comments=None):
        """
        Args:

        * method:
            The name of the operation.

        Kwargs:

        * coords:
            A single instance or sequence of :class:`.Coord` instances or
            coordinate names.

        * intervals:
            A single string, or a sequence strings, describing the intervals
            within the cell method.

        * comments:
            A single string, or a sequence strings, containing any additional
            comments.

        """
        if not isinstance(method, six.string_types):
            raise TypeError("'method' must be a string - got a '%s'" %
                            type(method))

        default_name = CFVariableMixin._DEFAULT_NAME
        _coords = []
        if coords is None:
            pass
        elif isinstance(coords, Coord):
            _coords.append(coords.name(token=True))
        elif isinstance(coords, six.string_types):
            _coords.append(CFVariableMixin.token(coords) or default_name)
        else:
            normalise = (lambda coord: coord.name(token=True) if
                         isinstance(coord, Coord) else
                         CFVariableMixin.token(coord) or default_name)
            _coords.extend([normalise(coord) for coord in coords])

        _intervals = []
        if intervals is None:
            pass
        elif isinstance(intervals, six.string_types):
            _intervals = [intervals]
        else:
            _intervals.extend(intervals)

        _comments = []
        if comments is None:
            pass
        elif isinstance(comments, six.string_types):
            _comments = [comments]
        else:
            _comments.extend(comments)

        self._init(method, tuple(_coords), tuple(_intervals), tuple(_comments))

    def __str__(self):
        """Return a custom string representation of CellMethod"""
        # Group related coord names intervals and comments together
        cell_components = zip_longest(self.coord_names, self.intervals,
                                      self.comments, fillvalue="")

        collection_summaries = []
        cm_summary = "%s: " % self.method

        for coord_name, interval, comment in cell_components:
            other_info = ", ".join(filter(None, chain((interval, comment))))
            if other_info:
                coord_summary = "%s (%s)" % (coord_name, other_info)
            else:
                coord_summary = "%s" % coord_name

            collection_summaries.append(coord_summary)

        return cm_summary + ", ".join(collection_summaries)

    def __add__(self, other):
        # Disable the default tuple behaviour of tuple concatenation
        raise NotImplementedError()

    def xml_element(self, doc):
        """
        Return a dom element describing itself

        """
        cellMethod_xml_element = doc.createElement('cellMethod')
        cellMethod_xml_element.setAttribute('method', self.method)

        for coord_name, interval, comment in zip_longest(self.coord_names,
                                                         self.intervals,
                                                         self.comments):
            coord_xml_element = doc.createElement('coord')
            if coord_name is not None:
                coord_xml_element.setAttribute('name', coord_name)
                if interval is not None:
                    coord_xml_element.setAttribute('interval', interval)
                if comment is not None:
                    coord_xml_element.setAttribute('comment', comment)
                cellMethod_xml_element.appendChild(coord_xml_element)

        return cellMethod_xml_element


# See Coord.cells() for the description/context.
class _CellIterator(Iterator):
    def __init__(self, coord):
        self._coord = coord
        if coord.ndim != 1:
            raise iris.exceptions.CoordinateMultiDimError(coord)
        self._indices = iter(range(coord.shape[0]))

    def __next__(self):
        # NB. When self._indices runs out it will raise StopIteration for us.
        i = next(self._indices)
        return self._coord.cell(i)

    next = __next__


# See ExplicitCoord._group() for the description/context.
class _GroupIterator(Iterator):
    def __init__(self, points):
        self._points = points
        self._start = 0

    def __next__(self):
        num_points = len(self._points)
        if self._start >= num_points:
            raise StopIteration

        stop = self._start + 1
        m = self._points[self._start]
        while stop < num_points and self._points[stop] == m:
            stop += 1

        group = _GroupbyItem(m, slice(self._start, stop))
        self._start = stop
        return group

    next = __next__
