# Copyright (C) 2017-8  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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
from iintgui import resetDialog
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt


class TestResetDialog(unittest.TestCase):

    def setUp(self):
        '''Create LoggerBox'''
        self.dialog = resetDialog.ResetDialog()

    def test_accept(self):
        self.dialog.resetOK.connect(self._ok)
        QTest.mouseClick(self.dialog.okButton, Qt.LeftButton)

    def _ok(self):
        self.assertTrue(True)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()



#~ from PyQt4 import QtCore, QtGui, uic
#~ from . import getUIFile


#~ class ResetDialog(QtGui.QDialog):
    #~ resetOK = QtCore.pyqtSignal(int)

    #~ def __init__(self, parent=None):
        #~ super(ResetDialog, self).__init__(parent)
        #~ uic.loadUi(getUIFile.getUIFile("resetDialog.ui"), self)
        #~ self.cancelButton.clicked.connect(self.close)
        #~ self.okButton.clicked.connect(self._returnOK)
        #~ self.okButton.setToolTip("Click here to reset all processing and stored data.")
        #~ self.cancelButton.setToolTip("Click here to keep all processed data and settings.")

    #~ def _returnOK(self):
        #~ self.resetOK.emit(0)
        #~ self.close()
