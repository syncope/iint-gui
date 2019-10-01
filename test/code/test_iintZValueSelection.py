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


#~ class iintZValueSelection(QtGui.QDialog):
    #~ zvalue = QtCore.pyqtSignal(str)

    #~ def __init__(self, columnnames=None, default=None, parent=None):
        #~ super(iintZValueSelection, self).__init__(parent)
        #~ uic.loadUi(getUIFile.getUIFile("zvalueselect.ui"), self)
        #~ self._fillCB(columnnames, default)
        #~ self.okButton.clicked.connect(self._emitZvalue)
        #~ self.cancelButton.clicked.connect(self.close)
        #~ self.columnNamesCB.setToolTip("The list of column data names.")
        #~ self.okButton.setToolTip("Click 'OK' to chose the current column data.")
        #~ self.cancelButton.setToolTip("Click 'Cancel' to close the dialog.")
        #~ self.show()

    #~ def closeEvent(self, evnt):
        #~ evnt.ignore()
        #~ self.hide()

    #~ def _fillCB(self, columnnames, default):
        #~ self._names = sorted(columnnames)
        #~ self.columnNamesCB.addItem(default)
        #~ self.columnNamesCB.addItems(self._names)

    #~ def reset(self):
        #~ self._names.clear()
        #~ self.close()

    #~ def _emitZvalue(self):
        #~ self.zvalue.emit(self.columnNamesCB.currentText())
        #~ self.hide()
