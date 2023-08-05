# (C) British Crown Copyright 2010 - 2020, Met Office
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
Provides testing capabilities for installed copies of Iris.

"""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Because this file is imported by setup.py, there may be additional runtime
# imports later in the file.
import multiprocessing
import os
import sys


# NOTE: Do not inherit from object as distutils does not like it.
class TestRunner():
    """Run the Iris tests under nose and multiprocessor for performance"""

    description = ('Run tests under nose and multiprocessor for performance. '
                   'Default behaviour is to run all non-example tests. '
                   'Specifying one or more test flags will run *only* those '
                   'tests.')
    user_options = [
        ('no-data', 'n', 'Override the paths to the data repositories so it '
                         'appears to the tests that it does not exist.'),
        ('stop', 'x', 'Stop running tests after the first error or failure.'),
        ('system-tests', 's', 'Run the limited subset of system tests.'),
        ('example-tests', 'e', 'Run the example code tests.'),
        ('default-tests', 'd', 'Run the default tests.'),
        ('coding-tests', 'c', 'Run the coding standards tests. (These are a '
                              'subset of the default tests.)'),
        ('num-processors=', 'p', 'The number of processors used for running '
                                 'the tests.'),
        ('create-missing', 'm', 'Create missing test result files.'),
    ]
    boolean_options = ['no-data', 'system-tests', 'stop', 'example-tests',
                       'default-tests', 'coding-tests', 'create-missing']

    def initialize_options(self):
        self.no_data = False
        self.stop = False
        self.system_tests = False
        self.example_tests = False
        self.default_tests = False
        self.coding_tests = False
        self.num_processors = None
        self.create_missing = False

    def finalize_options(self):
        # These enviroment variables will be propagated to all the
        # processes that nose.run creates.
        if self.no_data:
            print('Running tests in no-data mode...')
            import iris.config
            iris.config.TEST_DATA_DIR = None
        if self.create_missing:
            os.environ['IRIS_TEST_CREATE_MISSING'] = 'true'

        tests = []
        if self.system_tests:
            tests.append('system')
        if self.default_tests:
            tests.append('default')
        if self.coding_tests:
            tests.append('coding')
        if self.example_tests:
            tests.append('example')
        if not tests:
            tests.append('default')
        print('Running test suite(s): {}'.format(', '.join(tests)))
        if self.stop:
            print('Stopping tests after the first error or failure')
        if self.num_processors is None:
            # Choose a magic number that works reasonably well for the default
            # number of processes.
            self.num_processors = (multiprocessing.cpu_count() + 1) // 4 + 1
        else:
            self.num_processors = int(self.num_processors)

    def run(self):
        import nose

        if hasattr(self, 'distribution') and self.distribution.tests_require:
            self.distribution.fetch_build_eggs(self.distribution.tests_require)

        tests = []
        if self.system_tests:
            tests.append('iris.tests.system_test')
        if self.default_tests:
            tests.append('iris.tests')
        if self.coding_tests:
            tests.append('iris.tests.test_coding_standards')
        if self.example_tests:
            import iris.config
            default_doc_path = os.path.join(sys.path[0], 'docs', 'iris')
            doc_path = iris.config.get_option('Resources', 'doc_dir',
                                              default=default_doc_path)
            example_path = os.path.join(doc_path, 'example_tests')
            if os.path.exists(example_path):
                tests.append(example_path)
            else:
                print('WARNING: Example path %s does not exist.' %
                      (example_path))
        if not tests:
            tests.append('iris.tests')

        regexp_pat = r'--match=^([Tt]est(?![Mm]ixin)|[Ss]ystem)'

        n_processors = max(self.num_processors, 1)

        args = ['', None, '--processes=%s' % n_processors,
                '--verbosity=2', regexp_pat,
                '--process-timeout=180']
        try:
            import gribapi
        except ImportError:
            args.append('--exclude=^grib$')
        if self.stop:
            args.append('--stop')

        result = True
        for test in tests:
            args[1] = test
            print()
            print('Running test discovery on %s with %s processors.' %
                  (test, n_processors))
            # run the tests at module level i.e. my_module.tests
            # - test must start with test/Test and must not contain the
            #   word Mixin.
            result &= nose.run(argv=args)
        if result is False:
            exit(1)
