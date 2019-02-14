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
import numpy as np
import pyqtgraph as pg
from . import getUIFile
#~ from adapt.processes import curvefitting


class iintMCADialog(QtGui.QDialog):
    currentIndex = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(iintMCADialog, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("iintMCADialog.ui"), self)
        self.showPreviousBtn.clicked.connect(self.decrementCurrentScanID)
        self.showNextBtn.clicked.connect(self.incrementCurrentScanID)
        self.resetZoom.clicked.connect(self._resetZoom)
        #~ self.logScale.stateChanged.connect(self.plot)
        #~ self.viewPart.scene().sigMouseClicked.connect(self.mouse_click)
        self._currentIndex = 0
        self.currentIndex.emit(self._currentIndex)
        self._tmpFit = None
        self._logScale = False
        self.setGeometry(640, 1, 840, 420)
        #~ self._zoomMarker = pg.LinearRegionItem([0,1])
        #~ self._zoomMarker.setZValue(-10)
        #~ self._zoomMarker.sigRegionChanged.connect(self.update)
        #~ self.viewPart.addItem(self._zoomMarker)
        #~ self.viewPart.sigXRangeChanged.connect(self.updateZoom)
        self.lowerZoom.valueChanged.connect(self.update)
        self.upperZoom.valueChanged.connect(self.update)
        # still missing:
        # a) if zoom marker moved: call updateZoom
        #~ self.showFIT.setToolTip("If fit data is available, checking/unchecking\nthe box will display/hide the fit result as curve.\nThe curve is drawn as solid blue line.")
        #~ self._fitmodels = curvefitting.curvefitting().getFitModels()
        #~ self.handlerPart = self._fitmodels["gaussianModel"]().getWidget(xdata, ydata, index=0)


    def reset(self):
        self._currentIndex = 0
        self.viewPart.clear()
        self.hide()
        self.hidden.emit()

    def update(self, action=None):
        self.viewPart.setXRange(min=self.lowerZoom.value(),max=self.upperZoom.value(), padding=0)
        self.plot()

    #~ def updateZoom(self):
        #~ self._zoomMarker.setRegion(self.viewPart.getViewBox().viewRange()[0])

    def _resetZoom(self):
        self.lowerZoom.setValue(self._zoomStartValues[0])
        self.upperZoom.setValue(self._zoomStartValues[1])
        #~ self._zoomMarker.setRegion(self._zoomStartValues)

    def passData(self, dataDict):
        if len(dataDict) is 1:
            self._dataList = list(dataDict.values())[0]
        else:
            # need some decision what to do here ...!?
            pass
        self._zoomStartValues = (0,len(self._dataList[0]))
        self.lowerZoom.setMinimum(0)
        self.lowerZoom.setMaximum(len(self._dataList[0]))
        self.lowerZoom.setValue(0)
        
        self.upperZoom.setMinimum(0)
        self.upperZoom.setMaximum(len(self._dataList[0]))
        self.upperZoom.setValue(len(self._dataList[0]))
        #~ self._zoomMarker.setRegion(self._zoomStartValues)
        self.update()

    def plot(self):
        datum = self._dataList[self._currentIndex]
        self.mcaID.setText(str(self._currentIndex))
        ydata = datum
        xdata = np.asarray(range(len(datum)))
        #~ if (self._logScale):
            #~ ydata = np.log10(np.clip(ydata, 10e-3, np.inf))
        self.viewPart.clear()
        self.viewPart.plot(xdata, ydata, pen='b')

    #~ def plotFit(self, ydata):
        #~ datum = self._dataList[self._currentIndex]
        #~ xdata = datum.getData(self._motorName)
        #~ if self._tmpFit is not None:
            #~ self._tmpFit.clear()
        #~ self.viewPart.disableAutoRange()
        #~ if (self._logScale):
            #~ ydata = np.log10(np.clip(ydata, 10e-3, np.inf))
        #~ self._tmpFit = self.viewPart.plot(xdata, ydata, pen='r')

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

    def getCurrentIndex(self):
        return self._currentIndex

    def setCurrentIndex(self, index):
        self._currentIndex = index
        self.plot()
