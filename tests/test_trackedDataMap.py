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


'''This is the test for the TrackedDataMap module.'''

import unittest
from iintgui import trackedDataMap


class TrackedDataMapTest(unittest.TestCase):

    def setUp(self):
        '''Create TrackedDataMap'''
        self.tdm = trackedDataMap.TrackedDataMap()
        self._testlist = ['1','2','3','4','5']
        self._testlist2 = ['6','7','8']

    def test_initial(self):
        for st in self.tdm.getStatus():
            self.assertFalse(st)

    def test_namesetting(self):
        self.tdm.passNames(self._testlist, self._testlist2)
        for st in self.tdm.getStatus():
            self.assertTrue(st)

    def test_resetting(self):
        self.tdm.reset()
        for st in self.tdm.getStatus():
            self.assertFalse(st)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
