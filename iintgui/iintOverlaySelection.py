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

from PyQt4 import QtCore, QtGui, uic
from . import getUIFile


class iintOverlaySelection(QtGui.QWidget):
    overlayscanlist = QtCore.pyqtSignal(list)

    def __init__(self, datalist=None, parent=None):
        super(iintOverlaySelection, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("chooseOverlayScans.ui"), self)
        self._datalist = datalist

        self.okButton.clicked.connect(self._emitOverlayScans)
        self.cancelButton.clicked.connect(self.close)

        self.addToOverlay.setDisabled(True)
        #~ self.addToOverlay.clicked.connect(self._moveButtonToSelectedScans)
        self.removeFromOverlay.setDisabled(True)
        #~ self.removeFromOverlay.clicked.connect(self._moveButtonToUnselectedScans)

        self._currentUnSelectedItemScans = 0
        self._currentSelectedItemScans = 0

        self.listScans.setToolTip("List of scans not included in the overlay.\n Select by double-clicking or by selecting via single mouse click and then using the button '>>'.")
        self.listOverlayScans.setToolTip("The list of already selected scans to overlay.\n De-select by double-clicking or by selecting via single mouse click and then using the button '<<'.")
        self.okButton.setToolTip("Click 'OK' to use the current choice of overlay scans.")
        self.cancelButton.setToolTip("Click 'Cancel' to disregard the current selection.")
        self.show()

    def closeEvent(self, evnt):
        evnt.ignore()
        self.hide()

    def reset(self):
        #~ self.listScans.clear()
        #~ self.listOverlayScans.clear()
        self.close()

    #~ def _pickedUnselectedItemScans(self, item):
        #~ self._currentUnSelectedItemScans = item
        #~ self.addToListScans.setDisabled(False)

    #~ def _pickedSelectedItemScans(self, item):
        #~ self._currentSelectedItemScans = item
        #~ self.removeFromListScans.setDisabled(False)

    #~ def _addToOverlayScans(self):
        #~ self._moveToSelectedScans(self.listAllScans.selectedItems())

    #~ def _removeFromOverlayScans(self):
        #~ self.listSelectedScans.addItems(self.listSelectedScans.selectedItems())
        #~ for elem in self.listSelectedScans.selectedItems():
            #~ self.listSelectedScans.takeItem(self.listSelectedScans.row(elem))

    def _emitOverlayScans(self):
        #~ emitterData = self._trackedDataColumns + self._trackedDataScans
        #~ self.trackedData.emit(emitterData)
        self.hide()
