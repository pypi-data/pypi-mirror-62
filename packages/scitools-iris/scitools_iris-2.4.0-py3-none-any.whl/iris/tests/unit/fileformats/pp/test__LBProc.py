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
"""Unit tests for :class:`iris.fileformats.pp._LBProc`."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

from iris.fileformats.pp import _LBProc
from iris.tests import mock


class Test___init__(tests.IrisTest):
    def test_int(self):
        _LBProc(42)

    def test_str(self):
        _LBProc('245')

    def test_negative(self):
        msg = 'Negative numbers not supported with splittable integers object'
        with self.assertRaisesRegexp(ValueError, msg):
            _LBProc(-1)
        with self.assertRaisesRegexp(ValueError, msg):
            _LBProc('-1')

    def test_invalid_str(self):
        with self.assertRaisesRegexp(ValueError, 'invalid literal for int'):
            _LBProc('asdf')


class Test_flag1(tests.IrisTest):
    def test_true(self):
        lbproc = _LBProc(1)
        with mock.patch('warnings.warn') as warn:
            flag = lbproc.flag1
        self.assertEqual(warn.call_count, 1)
        self.assertTrue(flag)

    def test_false(self):
        lbproc = _LBProc(2)
        with mock.patch('warnings.warn') as warn:
            flag = lbproc.flag1
        self.assertEqual(warn.call_count, 1)
        self.assertFalse(flag)

    def test_many(self):
        for i in range(100):
            lbproc = _LBProc(i)
            with mock.patch('warnings.warn') as warn:
                flag = lbproc.flag1
            self.assertEqual(warn.call_count, 1)
            self.assertEqual(flag, i & 1)


class Test_flag2(tests.IrisTest):
    def test_true(self):
        lbproc = _LBProc(3)
        with mock.patch('warnings.warn') as warn:
            flag = lbproc.flag2
        self.assertEqual(warn.call_count, 1)
        self.assertTrue(flag)

    def test_false(self):
        lbproc = _LBProc(1)
        with mock.patch('warnings.warn') as warn:
            flag = lbproc.flag2
        self.assertEqual(warn.call_count, 1)
        self.assertFalse(flag)

    def test_many(self):
        for i in range(100):
            lbproc = _LBProc(i)
            with mock.patch('warnings.warn') as warn:
                flag = lbproc.flag2
            self.assertEqual(warn.call_count, 1)
            self.assertEqual(flag, bool(i & 2))


class Test_flag4(tests.IrisTest):
    def test_true(self):
        lbproc = _LBProc(6)
        with mock.patch('warnings.warn') as warn:
            flag = lbproc.flag4
        self.assertEqual(warn.call_count, 1)
        self.assertTrue(flag)

    def test_false(self):
        lbproc = _LBProc(8)
        with mock.patch('warnings.warn') as warn:
            flag = lbproc.flag4
        self.assertEqual(warn.call_count, 1)
        self.assertFalse(flag)

    def test_many(self):
        for i in range(100):
            lbproc = _LBProc(i)
            with mock.patch('warnings.warn') as warn:
                flag = lbproc.flag4
            self.assertEqual(warn.call_count, 1)
            self.assertEqual(flag, bool(i & 4))


class Test_flag131072(tests.IrisTest):
    def test_true(self):
        lbproc = _LBProc(135448)
        with mock.patch('warnings.warn') as warn:
            flag = lbproc.flag131072
        self.assertEqual(warn.call_count, 1)
        self.assertTrue(flag)

    def test_false(self):
        lbproc = _LBProc(4376)
        with mock.patch('warnings.warn') as warn:
            flag = lbproc.flag131072
        self.assertEqual(warn.call_count, 1)
        self.assertFalse(flag)

    def test_many(self):
        for i in range(0, 260000, 1000):
            lbproc = _LBProc(i)
            with mock.patch('warnings.warn') as warn:
                flag = lbproc.flag131072
            self.assertEqual(warn.call_count, 1)
            self.assertEqual(flag, bool(i & 131072))


class Test_flag3(tests.IrisTest):
    def test_invalid(self):
        lbproc = _LBProc(9)
        with self.assertRaises(AttributeError):
            lbproc.flag3


class Test_flag262144(tests.IrisTest):
    def test_invalid(self):
        lbproc = _LBProc(9)
        with self.assertRaises(AttributeError):
            lbproc.flag262144


class Test___int__(tests.IrisTest):
    def test(self):
        self.assertEqual(int(_LBProc(99)), 99)


class Test___eq__(tests.IrisTest):
    def test_equal(self):
        self.assertTrue(_LBProc(17).__eq__(_LBProc(17)))

    def test_equal_int(self):
        self.assertTrue(_LBProc(17).__eq__(17))

    def test_not_equal(self):
        self.assertFalse(_LBProc(17).__eq__(_LBProc(18)))

    def test_not_equal_int(self):
        self.assertFalse(_LBProc(17).__eq__(16))


class Test___ne__(tests.IrisTest):
    def test_equal(self):
        self.assertFalse(_LBProc(7).__ne__(_LBProc(7)))

    def test_equal_int(self):
        self.assertFalse(_LBProc(8).__ne__(8))

    def test_not_equal(self):
        self.assertTrue(_LBProc(9).__ne__(_LBProc(14)))

    def test_not_equal_int(self):
        self.assertTrue(_LBProc(10).__ne__(15))


class Test___iadd__(tests.IrisTest):
    def test(self):
        lbproc = _LBProc(12)
        lbproc += 8
        self.assertEqual(int(lbproc), 20)


class Test___iand__(tests.IrisTest):
    def test(self):
        lbproc = _LBProc(12)
        lbproc &= 8
        self.assertEqual(int(lbproc), 8)


class Test___ior__(tests.IrisTest):
    def test(self):
        lbproc = _LBProc(12)
        lbproc |= 1
        self.assertEqual(int(lbproc), 13)


class Test___repr__(tests.IrisTest):
    def test(self):
        lbproc = _LBProc(8641)
        self.assertEqual(repr(lbproc), '_LBProc(8641)')


class Test___str__(tests.IrisTest):
    def test(self):
        lbproc = _LBProc(8641)
        self.assertEqual(str(lbproc), '8641')


if __name__ == '__main__':
    tests.main()
