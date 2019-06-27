# Copyright (C) 2017-9  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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


class iintDataPlot(QtGui.QDialog):
    currentIndex = QtCore.pyqtSignal(int)
    blacklist = QtCore.pyqtSignal(list)
    hidden = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(iintDataPlot, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("iintSimplePlot.ui"), self)
        self.showPreviousBtn.clicked.connect(self.decrementCurrentScanID)
        self.showNextBtn.clicked.connect(self.incrementCurrentScanID)
        self.showRAW.stateChanged.connect(self._toggleRAW)
        self.showDES.stateChanged.connect(self._toggleDES)
        self.showBKG.stateChanged.connect(self._toggleBKG)
        self.showSIG.stateChanged.connect(self._toggleSIG)
        self.showFIT.stateChanged.connect(self._toggleFIT)
        self.logScale.stateChanged.connect(self._toggleLOG)
        self.showRAW.stateChanged.connect(self.plot)
        self.showDES.stateChanged.connect(self.plot)
        self.showBKG.stateChanged.connect(self.plot)
        self.showSIG.stateChanged.connect(self.plot)
        self.showFIT.stateChanged.connect(self.plot)
        self.logScale.stateChanged.connect(self.plot)
        self.viewPart.scene().sigMouseClicked.connect(self.mouse_click)
        self.viewPart.enableAutoRange()
        self.viewPart.autoRange()
        self.blacklistButton.clicked.connect(self._blacklisting)
        self._setBLB2Add()
        self._blacklist = []
        self._currentIndex = 0
        self.currentIndex.emit(self._currentIndex)
        self._showraw = True
        self._showdespike = False
        self._showbkg = False
        self._showbkgsubtracted = False
        self._tmpFit = None
        self._logScale = False
        self._showsigfit = False
        self.setGeometry(640, 1, 840, 840)
        self._xaxisname = ''
        self._yaxisname = ''
        self.showID.setToolTip("Shows the number of the currently displayed scan.")
        self.blacklistButton.setToolTip("Click here to toggle between showing or hiding the current scan.\nThis affects ONLY the display of the data, not the processing.")
        self.showPreviousBtn.setToolTip("Show the previous scan of the chosen list.\nIf the first scan is shown, this will show the last entry.")
        self.showNextBtn.setToolTip("Show the next scan of the chosen list.\nIf the last scan is shown, this will show the first entry.")
        self.logScale.setToolTip("Activate the check box to switch to logarithmic scale, an unchecked box means linear scaling.\nThere is a minimum value of 10^-2 for the logarithmic scale.")
        self.xPosition.setToolTip("Indicates the x position of a point if\nit is clicked somewhere in the scan display.")
        self.yPosition.setToolTip("Indicates the y position of a point if\nit is clicked somewhere in the scan display.")
        self.showRAW.setToolTip("If checked, the raw data is shown;as computed from\nthe application of the formula on the input.\nIt is shown as a '+' sign in black.")
        self.showDES.setToolTip("If despiking is performed, the display of the\ndespiked data can be de-/activated with the check box.\nIt is shown as dark green 'x' signs.")
        self.showBKG.setToolTip("If available, the display of the background of the\ndata can be de-/activated with the check box.\nIn case despiking has been applied this is taken as input; otherwise the raw data is taken.\nIt is shown as red diamonds.")
        self.showSIG.setToolTip("If background is available, checking/unchecking\nthe box will display/hide the background subtracted data.\nThis data is shown as blue circles.")
        self.showFIT.setToolTip("If fit data is available, checking/unchecking\nthe box will display/hide the fit result as curve.\nThe curve is drawn as solid blue line.")

    def reset(self):
        self.showRAW.setChecked(True)
        self.showDES.setChecked(False)
        self.showBKG.setChecked(False)
        self.showSIG.setChecked(False)
        self.showFIT.setChecked(False)
        self.showRAW.setDisabled(True)
        self.showDES.setDisabled(True)
        self.showBKG.setDisabled(True)
        self.showSIG.setDisabled(True)
        self.showFIT.setDisabled(True)
        self.viewPart.autoRange()
        self._currentIndex = 0
        self._showraw = True
        self._showdespike = False
        self._showbkg = False
        self._showbkgsubtracted = False
        self._showsigfit = False
        self.viewPart.clear()
        self.hide()
        self.hidden.emit()

    def update(self, action=None):
        self._checkDataAvailability()
        self.viewPart.autoRange()
        if(action == "des"):
            self.showDES.setChecked(True)
        if(action == "bkg"):
            self.showBKG.setChecked(True)
            self.showSIG.setChecked(True)
        if(action == "nobkg"):
            self.showBKG.setChecked(False)
            self.showBKG.setDisabled(True)
            self.showFIT.setChecked(False)
            self.showFIT.setDisabled(True)
            self.showSIG.setChecked(False)
            self.showSIG.setDisabled(True)
        if(action == "plotfit"):
            self.showFIT.setChecked(True)
        if(action == "unplotfit"):
            self.showFIT.setChecked(False)
            self.showFIT.setDisabled(True)
        self.plot()
        self.viewPart.autoRange()

    def passData(self, datalist, motorname, obsname, despobsname, bkgname, signalname, fittedsignalname):
        self._dataList = datalist
        self._motorName = motorname
        self._observableName = obsname
        self._despObservableName = despobsname
        self._backgroundPointsName = bkgname
        self._signalName = signalname
        self._fittedSignalName = fittedsignalname
        self.update()

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
        self.viewPart.autoRange()
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
        self.viewPart.autoRange()
        self._xaxisname = str(self._motorName)
        self.viewPart.setLabel('left', self._yaxisname)
        self.viewPart.setLabel('bottom', self._xaxisname)

    def getPrintData(self):
        # returns straightforward/simple dictionary
        printDict = {}
        datum = self._dataList[self._currentIndex]
        printDict['scannumber'] = datum.getData("scannumber")
        xdata = datum.getData(self._motorName)
        printDict['motor'] = xdata
        rawdata = datum.getData(self._observableName)
        if (self._logScale):
            rawdata = np.log10(np.clip(rawdata, 10e-3, np.inf))
        if(self._showraw): # raw data has black "plus signs"
            printDict['raw'] = rawdata
        if(self._showdespike): # despiked data: green "x"
            despikeData = datum.getData(self._despObservableName)
            if (self._logScale):
                despikeData = np.log10(np.clip(despikeData, 10e-3, np.inf))
            printDict['despike'] = despikeData
            #~ self.viewPart.plot(xdata, despikeData, pen=None, symbolPen=(0,0,80), symbolBrush='g', symbol='x')
        if(self._showbkg):
            bkg = datum.getData(self._backgroundPointsName)
            if (self._logScale):
                bkg = np.log10(np.clip(bkg, 10e-3, np.inf))
            printDict['bkg'] = bkg
            #~ self.viewPart.plot(xdata, bkg, pen=None, symbolPen='r', symbolBrush='r', symbol='d')
        if(self._showbkgsubtracted):
            signal = datum.getData(self._signalName)
            if (self._logScale):
                signal = np.log10(np.clip(signal, 10e-3, np.inf))
            printDict['signal'] = signal
            #~ self.viewPart.plot(xdata, signal, pen=None, symbolPen='b', symbolBrush='b', symbol='o')
        if(self._showsigfit):
            fitdata = datum.getData(self._fittedSignalName)
            if (self._logScale):
                fitdata = np.log10(np.clip(fitdata, 10e-3, np.inf))
            printDict['fit'] = fitdata
        return printDict

    def getAxisNames(self):
        return self._xaxisname, self._yaxisname

    def plotFit(self, ydata):
        datum = self._dataList[self._currentIndex]
        xdata = datum.getData(self._motorName)
        if self._tmpFit is not None:
            self._tmpFit.clear()
        self.viewPart.disableAutoRange()
        if (self._logScale):
            ydata = np.log10(np.clip(ydata, 10e-3, np.inf))
        self._tmpFit = self.viewPart.plot(xdata, ydata, pen='r')

    def removeGuess(self):
        try:
            self._tmpFit.clear()
        except AttributeError:
            # it may happen that the fit object is a NoneType
            pass
        self.viewPart.enableAutoRange()

    def _toggleRAW(self):
        self._showraw = not self._showraw

    def _toggleDES(self):
        self._showdespike = not self._showdespike

    def _toggleBKG(self):
        self._showbkg = not self._showbkg

    def _toggleSIG(self):
        self._showbkgsubtracted = not self._showbkgsubtracted

    def _toggleFIT(self):
        self._showsigfit = not self._showsigfit

    def _toggleLOG(self):
        self._logScale = not self._logScale

    def incrementCurrentScanID(self):
        self._currentIndex += 1
        if (self._currentIndex >= len(self._dataList)):
            self._currentIndex -= len(self._dataList)
        self.currentIndex.emit(self._currentIndex)
        self.plot()

    def decrementCurrentScanID(self):
        self._currentIndex -= 1
        if (self._currentIndex < 0):
            self._currentIndex += len(self._dataList)
        self.currentIndex.emit(self._currentIndex)
        self.plot()

    def mouse_click(self, event):
        position = self._theDrawItem.mapFromScene(event.scenePos())
        self.xPosition.setText("%.3f" % position.x())
        self.yPosition.setText("%.3f" % position.y())

    def getCurrentIndex(self):
        return self._currentIndex

    def setCurrentIndex(self, index):
        self._currentIndex = index
        self.plot()

    def getCurrentSignal(self):
        datum = self._dataList[self._currentIndex]
        # what to do if there is "signal" ?
        # first try despiked data, then try raw .. then bail out
        try:
            return datum.getData(self._motorName), datum.getData(self._signalName)
        except KeyError:
            try:
                return datum.getData(self._motorName), datum.getData(self._despObservableName)
            except KeyError:
                return datum.getData(self._motorName), datum.getData(self._observableName)

    def _blacklisting(self):
        ci = self._currentIndex
        if ci < 0:
            ci = len(self._dataList) + ci
        elif ci > len(self._dataList):
            ci -= len(self._dataList)
        if ci in self._blacklist:
            i = self._blacklist.index(ci)
            del self._blacklist[i]
            self._setBLB2Add()
        else:
            self._blacklist.append(ci)
            self._setBLB2Rm()
        self.blacklist.emit(self._blacklist)

    def _setBLB2Add(self):
        self.blacklistButton.setStyleSheet("color: white;background-color: green;")
        self.blacklistButton.setText("Remove from display")

    def _setBLB2Rm(self):
        self.blacklistButton.setStyleSheet("color: yellow;background-color: red;")
        self.blacklistButton.setText("Add to display again")

    def _blockSignals(self):
        self.showRAW.blockSignals(True)
        self.showDES.blockSignals(True)
        self.showBKG.blockSignals(True)
        self.showSIG.blockSignals(True)
        self.showFIT.blockSignals(True)

    def _unblockSignals(self):
        self.showRAW.blockSignals(False)
        self.showDES.blockSignals(False)
        self.showBKG.blockSignals(False)
        self.showSIG.blockSignals(False)
        self.showFIT.blockSignals(False)
