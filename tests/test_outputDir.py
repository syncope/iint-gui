# Copyright (C) 2019  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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


'''This is the test for the  module.'''

import unittest
from iintgui import outputDir


class TestOutputDir(unittest.TestCase):

    def setUp(self):
        self._name1 = "asdhfkljHJKL"
        self._name2 = "fsafIPUIPUIAHJKHD"
        self.mtt = outputDir.OutputDir(self._name1)

    def test_initial(self):
        self.assertEqual(self.mtt.getOutputDirectory(), self._name1)

    def test_setting(self):
        self.mtt.setOutputDirectory(self._name2)
        self.assertEqual(self.mtt.getOutputDirectory(), self._name2)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
