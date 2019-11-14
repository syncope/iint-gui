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

from PyQt4 import QtCore, QtGui, uic
from . import getUIFile


class SelectResultOutput(QtGui.QDialog):
    accept = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(SelectResultOutput, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("selectResultOutput.ui"), self)
        self.cancel.clicked.connect(self.close)
        self.ok.clicked.connect(self._returnOK)
        self.filename.setToolTip("The proposed file name beginning; type here to change it.\nNo string here is allowed, but discouraged.")
        self.ok.setToolTip("Click here to accept the file name.")
        self.cancel.setToolTip("Click here to cancel the save procedure.")

    def _returnOK(self):
        self.accept.emit(self.filename.text())
        self.close()

    def setName(self, filename):
        self.filename.setText(filename)
