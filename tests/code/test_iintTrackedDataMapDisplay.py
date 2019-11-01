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
#~ import numpy as np
#~ from . import getUIFile


#~ class iintTrackedDataMapDisplay(QtGui.QDialog):
    #~ maperror = QtCore.pyqtSignal(str)

    #~ def __init__(self, xname='', xdata=None, yname='', ydata=None, parent=None):
        #~ super(iintTrackedDataMapDisplay, self).__init__(parent)
        #~ uic.loadUi(getUIFile.getUIFile("iintTrackedDataMap.ui"), self)
        #~ self.viewPart.scene().sigMouseClicked.connect(self.mouse_click)
        #~ self.setGeometry(640, 1, 840, 840)
        #~ self._xaxisname = xname
        #~ self._xdata = np.asarray(xdata)
        #~ self._yaxisname = yname
        #~ self._ydata = np.asarray(ydata)
        #~ self.xPosition.setToolTip("Indicates the x position of a point if\nit is clicked somewhere in the display.")
        #~ self.yPosition.setToolTip("Indicates the y position of a point if\nit is clicked somewhere in the display.")

    #~ def reset(self):
        #~ self._dataList = []
        #~ self._selection = []
        #~ self._indexList = []

    #~ def plot(self):
        #~ self.viewPart.clear()

        #~ try:
            #~ self._theDrawItem = self.viewPart.plot(self._xdata, self._ydata, pen=None, symbolPen=None, symbolSize=8, symbolBrush='k')
        #~ except:
            #~ self.maperror.emit("Could not map the current selection, plotting failed.")
            #~ self.close()
        #~ self.viewPart.setLabel('left', self._yaxisname)
        #~ self.viewPart.setLabel('bottom', self._xaxisname)

    #~ def mouse_click(self, event):
        #~ try:
            #~ position = self._theDrawItem.mapFromScene(event.scenePos())
            #~ self.xPosition.setText("%.3f" % position.x())
            #~ self.yPosition.setText("%.3f" % position.y())
        #~ except AttributeError:
            #~ pass
