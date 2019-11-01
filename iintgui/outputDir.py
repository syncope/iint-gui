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


class OutputDir(QtGui.QWidget):
    newdirectory = QtCore.pyqtSignal(str)

    def __init__(self, initialDir, parent=None):
        super(OutputDir, self).__init__(parent)
        self.setWindowTitle("Output Directory")
        uic.loadUi(getUIFile.getUIFile("outputDirectory.ui"), self)
        self.outdir.setToolTip("Displays the current directory, in which any output is stored.")
        self.selectDirBtn.setToolTip("Select the output directory for storing result files.")
        self.selectDirBtn.clicked.connect(self._dirSelectDialog)
        self.outdir.setText(initialDir)

    def _dirSelectDialog(self):
        newname = QtGui.QFileDialog.getExistingDirectory(self, 'Choose output directory', '.')
        if newname:
            self.outdir.setText(newname)
            self.newdirectory.emit(newname)

    def setOutputDirectory(self, name):
        self.outdir.setText(name)

    def getOutputDirectory(self):
        return self.outdir.text()
