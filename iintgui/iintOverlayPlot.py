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
    currentIndex = QtCore.pyqtSignal(int)
    blacklist = QtCore.pyqtSignal(list)
    hidden = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(iintOverlayPlot, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("iintOverlayPlot.ui"), self)
        self.logScale.stateChanged.connect(self._toggleLOG)
        self.logScale.stateChanged.connect(self.plot)
        self.viewPart.scene().sigMouseClicked.connect(self.mouse_click)
        self.scanSelectBtn.clicked.connect(print)
        self._logScale = False
        self.setGeometry(640, 1, 840, 840)
        self._xaxisname = ''
        self._yaxisname = ''
        self.logScale.setToolTip("Activate the check box to switch to logarithmic scale, an unchecked box means linear scaling.\nThere is a minimum value of 10^-2 for the logarithmic scale.")
        self.xPosition.setToolTip("Indicates the x position of a point if\nit is clicked somewhere in the scan display.")
        self.yPosition.setToolTip("Indicates the y position of a point if\nit is clicked somewhere in the scan display.")

    def reset(self):
        pass

    def update(self, action=None):
        self._checkDataAvailability()

    def passData(self, datalist, motorname, obsname, despobsname, bkgname, signalname, fittedsignalname):
        self._dataList = datalist
        self._motorName = motorname
        self._observableName = obsname
        self._despObservableName = despobsname
        self._backgroundPointsName = bkgname
        self._signalName = signalname
        self._fittedSignalName = fittedsignalname

    def _toggleLOG(self):
        self._logScale = not self._logScale

    def _checkDataAvailability(self):
        datum = self._dataList[0]
        try:
            datum.getData(self._observableName)
            self.showRAW.setDisabled(False)
        except KeyError:
            self.showRAW.setDisabled(True)
        try:
            if(self._despObservableName == self._observableName):
                self.showDES.setDisabled(True)
            else:
                datum.getData(self._despObservableName)
                self.showDES.setDisabled(False)
        except KeyError:
            self.showDES.setDisabled(True)
        try:
            datum.getData(self._backgroundPointsName)
            self.showBKG.setDisabled(False)
        except KeyError:
            self.showBKG.setDisabled(True)
            self.showBKG.setChecked(False)
        try:
            datum.getData(self._signalName)
            self.showSIG.setDisabled(False)
        except KeyError:
            self.showSIG.setDisabled(True)
            self.showSIG.setChecked(False)
        try:
            datum.getData(self._fittedSignalName)
            self.showFIT.setDisabled(False)
        except KeyError:
            self.showFIT.setDisabled(True)
            self.showFIT.setChecked(False)

    def plot(self):
        datum = self._dataList[self._currentIndex]
        if(self._currentIndex in self._blacklist):
            self._setBLB2Rm()
        else:
            self._setBLB2Add()

        self.showID.setText(str(datum.getData("scannumber")))
        xdata = datum.getData(self._motorName)
        ydata = datum.getData(self._observableName)
        if (self._logScale):
            ydata = np.log10(np.clip(ydata, 10e-3, np.inf))
        self.viewPart.clear()
        if(self._showraw): # raw data has black "plus signs"
            self._theDrawItem = self.viewPart.plot(xdata, ydata, pen=None, symbolPen='k', symbolBrush='k', symbol='+')
        if(self._showdespike): # despiked data: green "x"
            despikeData = datum.getData(self._despObservableName)
            if (self._logScale):
                despikeData = np.log10(np.clip(despikeData, 10e-3, np.inf))
            self.viewPart.plot(xdata, despikeData, pen=None, symbolPen=(0,0,80), symbolBrush='g', symbol='x')
        if(self._showbkg):
            bkg = datum.getData(self._backgroundPointsName)
            if (self._logScale):
                bkg = np.log10(np.clip(bkg, 10e-3, np.inf))
            self.viewPart.plot(xdata, bkg, pen=None, symbolPen='r', symbolBrush='r', symbol='d')
        if(self._showbkgsubtracted):
            signal = datum.getData(self._signalName)
            if (self._logScale):
                signal = np.log10(np.clip(signal, 10e-3, np.inf))
            self.viewPart.plot(xdata, signal, pen=None, symbolPen='b', symbolBrush='b', symbol='o')
        if(self._showsigfit):
            fitdata = datum.getData(self._fittedSignalName)
            if (self._logScale):
                fitdata = np.log10(np.clip(fitdata, 10e-3, np.inf))
            self.viewPart.plot(xdata, fitdata, pen='b')
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
