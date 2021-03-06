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


class FileInfo(QtGui.QWidget):
    newspecfile = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(FileInfo, self).__init__(parent)
        self.setWindowTitle("File Display")
        uic.loadUi(getUIFile.getUIFile("fileInfo.ui"), self)
        self.fileLabel.setToolTip("If a SPEC file has been selected, the name is shown here.")
        self.scanSelectionDisplay.setToolTip("The actual selection of scans in the given SPEC file.")
        self._defaulttext = "No File"
        self._defaultselection = "No Selection"

    def reset(self):
        self.fileLabel.setText(self._defaulttext)
        self.fileLabel.setToolTip(self._defaulttext)
        self.scanSelectionDisplay.setText(self._defaultselection)

    def setNames(self, f, s):
        import os.path
        self.fileLabel.setText(os.path.basename(f))
        self.fileLabel.setToolTip(f)
        self.scanSelectionDisplay.setText(s)
