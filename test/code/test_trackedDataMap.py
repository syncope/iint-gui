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
        self._testdict = {'a': 1, 'b': 2, 'c': 3}

    def test_initial(self):
        for st in self.tdm.getStatus():
            self.assertFalse(st)

    def test_namesetting(self):
        self.tdm.passNames(self._testdict)
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



#~ from PyQt4 import QtCore, QtGui, uic
#~ from . import getUIFile


#~ class TrackedDataMap(QtGui.QDialog):
    #~ trackeddatatomap = QtCore.pyqtSignal(str, str)

    #~ def __init__(self, parent=None):
        #~ super(TrackedDataMap, self).__init__(parent)
        #~ uic.loadUi(getUIFile.getUIFile("iintTrackedDataMapSelection.ui"), self)
        #~ self._names = []
        #~ self.done.clicked.connect(self.hide)
        #~ self.display.clicked.connect(self.emitNames)

    #~ def reset(self):
        #~ self._names.clear()

    #~ def passNames(self, someDict):
        #~ self.reset()
        #~ # works only in v>=3.5  "unpacking generalization"
        #~ self._names = [*someDict]
        #~ self.firstSelection.clear()
        #~ self.secondSelection.clear()
        #~ self._updateBoxes()

    #~ def _updateBoxes(self):
        #~ self.firstSelection.addItems(self._names)
        #~ self.secondSelection.addItems(self._names)

    #~ def emitNames(self):
        #~ first = self.firstSelection.currentIndex()
        #~ second = self.secondSelection.currentIndex()
        #~ self.trackeddatatomap.emit(self.firstSelection.itemText(first),
                                   #~ self.secondSelection.itemText(second))
