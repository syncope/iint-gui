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
import numpy as np
from . import getUIFile


class iintOverlayPlot(QtGui.QDialog):

    def __init__(self, parent=None):
        super(iintOverlayPlot, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("iintOverlayPlot.ui"), self)
        self.logScale.stateChanged.connect(self._toggleLOG)
        self.logScale.stateChanged.connect(self.plot)
        self.viewPart.scene().sigMouseClicked.connect(self.mouse_click)
        #~ self.scanSelectBtn.clicked.connect(print)
        self.rawradio.clicked.connect(self.plot)
        self.desradio.clicked.connect(self.plot)
        self.bkgradio.clicked.connect(self.plot)
        self.sigradio.clicked.connect(self.plot)
        self.fitradio.clicked.connect(self.plot)
        self._logScale = False
        self.setGeometry(640, 1, 840, 840)
        self._xaxisname = ''
        self._yaxisname = ''
        self.logScale.setToolTip("Activate the check box to switch to logarithmic scale, an unchecked box means linear scaling.\nThere is a minimum value of 10^-2 for the logarithmic scale.")
        self.xPosition.setToolTip("Indicates the x position of a point if\nit is clicked somewhere in the scan display.")
        self.yPosition.setToolTip("Indicates the y position of a point if\nit is clicked somewhere in the scan display.")
        self.rawradio.setToolTip("Activate to display the raw data. Is disabled if data not present.")
        self.desradio.setToolTip("Activate to display the despiked data. Is disabled if data not present.")
        self.bkgradio.setToolTip("Activate to display the background. Is disabled if data not present.")
        self.sigradio.setToolTip("Activate to display the signal. Is disabled if data not present.")
        self.fitradio.setToolTip("Activate to display the fitted signal. Is disabled if data not present.")

    def reset(self):
        self._dataList = []
        self._selection = []
        self._indexList = []

    def passData(self, selection, datalist, motorname, obsname, despobsname, bkgname, signalname, fittedsignalname):
        self._selection = selection
        self._dataList = datalist
        self._motorName = motorname
        self._observableName = obsname
        self._despObservableName = despobsname
        self._backgroundPointsName = bkgname
        self._signalName = signalname
        self._fittedSignalName = fittedsignalname
        self._indexList = []
        self._generateIndexList()
        self._checkDataAvailability()

    def _generateIndexList(self):
        for datum in self._dataList:
            number = datum.getData("scannumber")
            index = self._dataList.index(datum)
            if str(number) in self._selection:
                self._indexList.append(index)

    def _toggleLOG(self):
        self._logScale = not self._logScale

    def _checkDataAvailability(self):
        datum = self._dataList[0]
        try:
            datum.getData(self._observableName)
            self.rawradio.setDisabled(False)
        except KeyError:
            self.rawradio.setDisabled(True)
        try:
            if(self._despObservableName == self._observableName):
                self.desradio.setDisabled(True)
            else:
                datum.getData(self._despObservableName)
                self.desradio.setDisabled(False)
        except KeyError:
            self.desradio.setDisabled(True)
        try:
            datum.getData(self._backgroundPointsName)
            self.bkgradio.setDisabled(False)
        except KeyError:
            self.bkgradio.setDisabled(True)
        try:
            datum.getData(self._signalName)
            self.sigradio.setDisabled(False)
        except KeyError:
            self.sigradio.setDisabled(True)
        try:
            datum.getData(self._fittedSignalName)
            self.fitradio.setDisabled(False)
        except KeyError:
            self.fitradio.setDisabled(True)

    def plot(self):
        self.viewPart.clear()

        for index in self._indexList:
            datum = self._dataList[index]

            xdata = datum.getData(self._motorName)

            if self.rawradio.isChecked():
                ydata = datum.getData(self._observableName)
                spen = 'k'
            elif self.desradio.isChecked():
                ydata = datum.getData(self._despObservableName)
                spen = (0,0,80)
            elif self.bkgradio.isChecked():
                ydata = datum.getData(self._backgroundPointsName)
                spen = 'r'
            elif self.sigradio.isChecked():
                ydata = datum.getData(self._signalName)
                spen = 'b'
            elif self.fitradio.isChecked():
                ydata = datum.getData(self._fittedSignalName)
                spen = 'b'

            if (self._logScale):
                ydata = np.log10(np.clip(ydata, 10e-3, np.inf))

            try:
                self._theDrawItem = self.viewPart.plot(xdata, ydata, pen=spen)
            except:
                pass

        if self._logScale:
            self._yaxisname = "Signal intensity (log-Scale)"
        else:
            self._yaxisname = "Signal intensity"
        self._xaxisname = str(self._motorName)
        self.viewPart.setLabel('left', self._yaxisname)
        self.viewPart.setLabel('bottom', self._yaxisname)

    def mouse_click(self, event):
        position = self._theDrawItem.mapFromScene(event.scenePos())
        self.xPosition.setText("%.3f" % position.x())
        self.yPosition.setText("%.3f" % position.y())
