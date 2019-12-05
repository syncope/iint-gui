# Copyright (C) 2017-9  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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


class iintTrackedDataChoice(QtGui.QWidget):
    trackedData = QtCore.pyqtSignal(list,list)

    def __init__(self, dataelement=None, headerlist=None, columnlist=None, parent=None):
        super(iintTrackedDataChoice, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("chooseTrackedData.ui"), self)
        self._data = dataelement
        self._initialNamesColumns = self._data.getLabels()
        self._initialNamesHeaders = []
        for elem in list(self._data.getCustomKeys()):
            self._initialNamesHeaders.append(elem)
        self._fillLists(headerlist, columnlist)
        self.okButton.clicked.connect(self._emitTrackedData)
        self.cancelButton.clicked.connect(self.close)
        self.addToListColumns.setDisabled(True)
        self.addToListHeaders.setDisabled(True)
        self.addToListColumns.clicked.connect(self._moveButtonToSelectedColumns)
        self.addToListHeaders.clicked.connect(self._moveButtonToSelectedHeaders)
        self.removeFromListColumns.clicked.connect(self._moveButtonToUnselectedColumns)
        self.removeFromListHeaders.clicked.connect(self._moveButtonToUnselectedHeaders)
        self.removeFromListColumns.setDisabled(True)
        self.removeFromListHeaders.setDisabled(True)
        self.listAllColumns.itemClicked.connect(self._pickedUnselectedItemColumns)
        self.listAllColumns.itemDoubleClicked.connect(self._moveToSelectedColumns)
        self.listSelectedColumns.itemClicked.connect(self._pickedSelectedItemColumns)
        self.listSelectedColumns.itemDoubleClicked.connect(self._moveToUnselectedColumns)
        self.listAllHeaders.itemClicked.connect(self._pickedUnselectedItemHeaders)
        self.listAllHeaders.itemDoubleClicked.connect(self._moveToSelectedHeaders)
        self.listSelectedHeaders.itemClicked.connect(self._pickedSelectedItemHeaders)
        self.listSelectedHeaders.itemDoubleClicked.connect(self._moveToUnselectedHeaders)
        self._currentUnSelectedItemColumns = 0
        self._currentSelectedItemColumns = 0
        self._currentUnSelectedItemHeaders = 0
        self._currentSelectedItemHeaders = 0
        self.listAllColumns.setToolTip("A list of available column data that has not yet been selected for tracking.\n Select by double-clicking or by selecting via single mouse click and then using the button '>>'.")
        self.listSelectedColumns.setToolTip("The list of already selected column data to be included in the output file.\n De-select by double-clicking or by selecting via single mouse click and then using the button '<<'.")
        self.listAllHeaders.setToolTip("A list of available header data that has not yet been selected for tracking.\n Select by double-clicking or by selecting via single mouse click and then using the button '>>'.")
        self.listSelectedHeaders.setToolTip("The list of already selected header data to be included in the output file.\n De-select by double-clicking or by selecting via single mouse click and then using the button '<<'.")
        self.okButton.setToolTip("Click 'OK' to store the current choice of tracked data.")
        self.cancelButton.setToolTip("Click 'Cancel' to disregard the current changes in tracked data.")
        self.show()

    def closeEvent(self, evnt):
        evnt.ignore()
        self.hide()

    def _fillLists(self, headerlist, columnlist):
        self._untrackedDataColumns = sorted(self._initialNamesColumns[:])
        self._untrackedDataHeaders = sorted(self._initialNamesHeaders[:])
        self._trackedDataColumns = []
        self._trackedDataHeaders = []
        if headerlist is not None:
            for header in headerlist:
                try:
                    self._untrackedDataHeaders.remove(header)
                    self._trackedDataHeaders.append(header)
                except ValueError:
                    pass
        if columnlist is not None:
            for column in columnlist:
                try:
                    self._untrackedDataColumns.remove(column)
                    self._trackedDataColumns.append(column)
                except ValueError:
                    pass
        self.listSelectedColumns.addItems(sorted(self._trackedDataColumns))
        self.listSelectedHeaders.addItems(sorted(self._trackedDataHeaders))
        self.listAllColumns.addItems(self._untrackedDataColumns)
        self.listAllHeaders.addItems(self._untrackedDataHeaders)

    def reset(self):
        self.listAllColumns.clear()
        self._untrackedDataColumns.clear()
        self._trackedDataColumns.clear()
        self.listAllHeaders.clear()
        self._untrackedDataHeaders.clear()
        self._trackedDataHeaders.clear()
        del self._trackedDataColumns[:]
        del self._trackedDataHeaders[:]
        del self._untrackedDataColumns[:]
        del self._untrackedDataHeaders[:]
        self.close()

    def _pickedUnselectedItemColumns(self, item):
        self._currentUnSelectedItemColumns = item
        self.addToListColumns.setDisabled(False)

    def _pickedUnselectedItemHeaders(self, item):
        self._currentUnSelectedItemHeaders = item
        self.addToListHeaders.setDisabled(False)

    def _pickedSelectedItemColumns(self, item):
        self._currentSelectedItemColumns = item
        self.removeFromListColumns.setDisabled(False)

    def _pickedSelectedItemHeaders(self, item):
        self._currentSelectedItemHeaders = item
        self.removeFromListHeaders.setDisabled(False)

    def _moveButtonToSelectedColumns(self):
        index = self._untrackedDataColumns.index(self._currentUnSelectedItemColumns.text())
        self._trackedDataColumns.append(self._untrackedDataColumns.pop(index))
        self.listSelectedColumns.addItem(self.listAllColumns.takeItem(self.listAllColumns.row(self._currentUnSelectedItemColumns)))
        self.listAllColumns.setCurrentRow(-1)
        self.addToListColumns.setDisabled(True)

    def _moveButtonToSelectedHeaders(self):
        index = self._untrackedDataHeaders.index(self._currentUnSelectedItemHeaders.text())
        self._trackedDataHeaders.append(self._untrackedDataHeaders.pop(index))
        self.listSelectedHeaders.addItem(self.listAllHeaders.takeItem(self.listAllHeaders.row(self._currentUnSelectedItemHeaders)))
        self.listAllHeaders.setCurrentRow(-1)
        self.addToListHeaders.setDisabled(True)

    def _moveButtonToUnselectedColumns(self):
        index = self._trackedDataColumns.index(self._currentSelectedItemColumns.text())
        self._untrackedDataColumns.append(self._trackedDataColumns.pop(index))
        self.listAllColumns.addItem(self.listSelectedColumns.takeItem(self.listSelectedColumns.row(self._currentSelectedItemColumns)))
        self.listSelectedColumns.setCurrentRow(-1)
        self.removeFromListColumns.setDisabled(True)

    def _moveButtonToUnselectedHeaders(self):
        index = self._trackedDataHeaders.index(self._currentSelectedItemHeaders.text())
        self._untrackedDataHeaders.append(self._trackedDataHeaders.pop(index))
        self.listAllHeaders.addItem(self.listSelectedHeaders.takeItem(self.listSelectedHeaders.row(self._currentSelectedItemHeaders)))
        self.listSelectedHeaders.setCurrentRow(-1)
        self.removeFromListHeaders.setDisabled(True)

    def _moveToSelectedColumns(self, item):
        index = self._untrackedDataColumns.index(item.text())
        self._trackedDataColumns.append(self._untrackedDataColumns.pop(index))
        self.listSelectedColumns.addItem(self.listAllColumns.takeItem(self.listAllColumns.row(item)))
        self.listAllColumns.clearSelection()
        self.addToListColumns.setDisabled(True)

    def _moveToSelectedHeaders(self, item):
        index = self._untrackedDataHeaders.index(item.text())
        self._trackedDataHeaders.append(self._untrackedDataHeaders.pop(index))
        self.listSelectedHeaders.addItem(self.listAllHeaders.takeItem(self.listAllHeaders.row(item)))
        self.listAllHeaders.clearSelection()
        self.addToListHeaders.setDisabled(True)

    def _moveToUnselectedColumns(self, item):
        index = self._trackedDataColumns.index(item.text())
        self._untrackedDataColumns.append(self._trackedDataColumns.pop(index))
        self.listAllColumns.addItem(self.listSelectedColumns.takeItem(self.listSelectedColumns.row(item)))
        self.listSelectedColumns.clearSelection()
        self.removeFromListColumns.setDisabled(True)

    def _moveToUnselectedHeaders(self, item):
        index = self._trackedDataHeaders.index(item.text())
        self._untrackedDataHeaders.append(self._trackedDataHeaders.pop(index))
        self.listAllHeaders.addItem(self.listSelectedHeaders.takeItem(self.listSelectedHeaders.row(item)))
        self.listSelectedHeaders.clearSelection()
        self.removeFromListHeaders.setDisabled(True)

    def _addToListColumns(self):
        self._moveToSelectedColumns(self.listAllColumns.selectedItems())

    def _addToListHeaders(self):
        self._moveToSelectedHeaders(self.listAllHeaders.selectedItems())

    def _removeFromListColumns(self):
        self.listSelectedColumns.addItems(self.listSelectedColumns.selectedItems())
        for elem in self.listSelectedColumns.selectedItems():
            self.listSelectedColumns.takeItem(self.listSelectedColumns.row(elem))

    def _removeFromListHeaders(self):
        self.listSelectedHeaders.addItems(self.listSelectedHeaders.selectedItems())
        for elem in self.listSelectedHeaders.selectedItems():
            self.listSelectedHeaders.takeItem(self.listSelectedHeaders.row(elem))

    def _emitTrackedData(self):
        self.trackedData.emit(self._trackedDataHeaders, self._trackedDataColumns)
        self.hide()
