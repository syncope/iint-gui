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
        self.dialog.resetOK.connect(self._ok)
        self.dialog.cancelButton.clicked.connect(self._cancel)

    def test_acceptReset(self):
        QTest.mouseClick(self.dialog.okButton, Qt.LeftButton)

    def test_cancelReset(self):
        QTest.mouseClick(self.dialog.cancelButton, Qt.LeftButton)

    def _ok(self):
        self.assertTrue(True)

    def _cancel(self):
        self.assertTrue(True)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
