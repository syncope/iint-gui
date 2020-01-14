# Copyright (C) 2020  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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

from PyQt4 import QtGui, uic
from . import getUIFile


class BackgroundIntegralDialog(QtGui.QDialog):

    def __init__(self, text, parent=None):
        super(BackgroundIntegralDialog, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("backgroundIntegralInfo.ui"), self)
        self.displaytext.setText(text)
        self.ack.clicked.connect(self.close)
        self.ack.setToolTip("Click to close the dialog.")

