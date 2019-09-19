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


class iintFitConfiguration(QtGui.QDialog):
    def __init__(self, parent=None):
        super(iintFitConfiguration, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("iintFitConfig.ui"), self)
        self.cancelButton.clicked.connect(self._close)
        self.doneButton.clicked.connect(self.close)

    def _close(self):
        self.reset()
        self.close()

    def addWidget(self, widget):
        self.functionlist.addWidget(widget)
        self.update()
        self.show()

    def reset(self):
        for i in reversed(range(self.functionlist.count())): 
            self.functionlist.itemAt(i).widget().setParent(None)
