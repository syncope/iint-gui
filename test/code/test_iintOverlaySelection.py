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
from iintgui import 


class Test(unittest.TestCase):

    def setUp(self):
        '''Create LoggerBox'''
        self. = .()

    def test_bla(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()



#~ from PyQt4 import QtCore, QtGui, uic
#~ from . import getUIFile


#~ class iintOverlaySelection(QtGui.QWidget):
    #~ overlayscanlist = QtCore.pyqtSignal(list)

    #~ def __init__(self, datalist=None, parent=None):
        #~ super(iintOverlaySelection, self).__init__(parent)
        #~ uic.loadUi(getUIFile.getUIFile("chooseOverlayScans.ui"), self)
        #~ self._datalist = list(map(str, datalist))
        #~ self._fillLists()
        #~ self.okButton.clicked.connect(self._emitOverlayScans)
        #~ self.cancelButton.clicked.connect(self.close)
        #~ self.addToOverlay.setDisabled(False)
        #~ self.addToOverlay.clicked.connect(self._moveToOverlay)
        #~ self.removeFromOverlay.setDisabled(False)
        #~ self.removeFromOverlay.clicked.connect(self._removeFromOverlay)

        #~ self.listScans.setToolTip("List of scans not included in the overlay.\n Select by double-clicking or by selecting via single mouse click and then using the button '>>'.")
        #~ self.listOverlayScans.setToolTip("The list of already selected scans to overlay.\n De-select by double-clicking or by selecting via single mouse click and then using the button '<<'.")
        #~ self.okButton.setToolTip("Click 'OK' to use the current choice of overlay scans.")
        #~ self.cancelButton.setToolTip("Click 'Cancel' to disregard the current selection.")
        #~ self.show()

    #~ def closeEvent(self, evnt):
        #~ evnt.ignore()
        #~ self.hide()

    #~ def reset(self):
        #~ self._currentItemScans.clear()
        #~ self._currentItemOverlays.clear()
        #~ self._updateDisplay()
        #~ self._datalist.clear()
        #~ self.close()

    #~ def passData(self, datalist):
        #~ self._datalist = list(map(str, datalist))
        #~ self._fillLists()

    #~ def _fillLists(self):
        #~ # two lists: scans and overlays
        #~ self._currentItemScans = sorted(self._datalist)
        #~ self._currentItemOverlays = []
        #~ self.listScans.addItems(self._currentItemScans)

    #~ def _updateDisplay(self):
        #~ self.listScans.clear()
        #~ self.listOverlayScans.clear()
        #~ self.listScans.addItems(sorted(self._currentItemScans))
        #~ self.listOverlayScans.addItems(sorted(self._currentItemOverlays))

    #~ def _moveToOverlay(self):
        #~ for index in self.listScans.selectedIndexes():
            #~ self._currentItemOverlays.append(index.data())
            #~ self._currentItemScans = [i for i in self._currentItemScans if i != index.data()]
        #~ self._updateDisplay()

    #~ def _removeFromOverlay(self):
        #~ for index in self.listOverlayScans.selectedIndexes():
            #~ self._currentItemScans.append(index.data())
            #~ self._currentItemOverlays = [i for i in self._currentItemOverlays if i != index.data()]
        #~ self._updateDisplay()

    #~ def _emitOverlayScans(self):
        #~ self.overlayscanlist.emit(self._currentItemOverlays)
        #~ self.hide()
