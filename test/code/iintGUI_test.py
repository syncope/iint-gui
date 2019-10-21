# Copyright (C) 2018-9 Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
# email contact: christoph.rosemann@desy.de
#
# iintgui is an application for the ADAPT framework
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation in  version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.


'''Code and gui testing for iintGUI.'''

import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

# still to write: include all test cases into a test suite
from . import test_loggerBox
from . import test_selectResultOutput
from . import test_resetDialog
from . import test_trackedDataMap
from . import test_outputDir

# general tests
from . import test_iintGUI_00_start
from . import test_iintGUI_01_fileload
from . import test_iintGUI_02_signaldefinitions
from . import test_iintGUI_03_backgrounddefinitions
from . import test_iintGUI_04_fitting
from . import test_iintGUI_05_configurations

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

app = QApplication(sys.argv)

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_loggerBox))
suite.addTests(loader.loadTestsFromModule(test_selectResultOutput))
suite.addTests(loader.loadTestsFromModule(test_resetDialog))
suite.addTests(loader.loadTestsFromModule(test_trackedDataMap))
suite.addTests(loader.loadTestsFromModule(test_outputDir))

suite.addTests(loader.loadTestsFromModule(test_iintGUI_00_start))
suite.addTests(loader.loadTestsFromModule(test_iintGUI_01_fileload))
suite.addTests(loader.loadTestsFromModule(test_iintGUI_02_signaldefinitions))
suite.addTests(loader.loadTestsFromModule(test_iintGUI_03_backgrounddefinitions))
suite.addTests(loader.loadTestsFromModule(test_iintGUI_04_fitting))
suite.addTests(loader.loadTestsFromModule(test_iintGUI_05_configurations))


def run(verbosity=3):
    # initialize a runner, pass it your suite and run it
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

def run_tests(verbosity=3):
    run(verbosity)

if __name__ == "__main__":
    unittest.main()
