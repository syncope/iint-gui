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


class TrackedDataMap(QtGui.QDialog):
    trackeddatatomap = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(TrackedDataMap, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("iintTrackedDataMapSelection.ui"), self)
        self._names = []
        self.done.clicked.connect(self.hide)
        self.display.clicked.connect(self.emitNames)
        self.done.setDisabled(True)
        self.display.setDisabled(True)
        self._buttonlist = [self.done, self.display]

    def reset(self):
        self._names.clear()
        self.done.setDisabled(True)
        self.display.setDisabled(True)

    def passNames(self, headerList, columnList):
        self.reset()
        self._names = list(set(headerList.copy() + columnList.copy()))
        self.firstSelection.clear()
        self.secondSelection.clear()
        self._updateBoxes()
        if self._names is not None:
            self.done.setDisabled(False)
            self.display.setDisabled(False)

    def _updateBoxes(self):
        self.firstSelection.addItems(self._names)
        self.secondSelection.addItems(self._names)

    def emitNames(self):
        first = self.firstSelection.currentIndex()
        second = self.secondSelection.currentIndex()
        self.trackeddatatomap.emit(self.firstSelection.itemText(first),
                                   self.secondSelection.itemText(second))

    def getStatus(self):
        return [i.isEnabled() for i in self._buttonlist]
