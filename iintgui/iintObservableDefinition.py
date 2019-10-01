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
from . import getUIFile


class iintObservableDefinition(QtGui.QWidget):
    motorName = QtCore.pyqtSignal(str)
    observableDicts = QtCore.pyqtSignal(dict, dict)
    doDespike = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(iintObservableDefinition, self).__init__(parent)
        self.setWindowTitle("Intensity definition")
        uic.loadUi(getUIFile.getUIFile("iintSignalDefinition.ui"), self)
        self._obsDict = {}
        self._despikeDict = {}
        self._trapintDict = {}
        self.motorCB.currentIndexChanged.connect(self.setMotor)
        self.observableDetectorCB.currentIndexChanged.connect(self.setObservable)
        self.observableMonitorCB.currentIndexChanged.connect(self.setMonitor)
        self.observableTimeCB.currentIndexChanged.connect(self.setTime)
        self._useAttenuationFactor = False
        self.observableAttFaccheck.stateChanged.connect(self.toggleAttFac)
        self.observableAttFacCB.currentIndexChanged.connect(self.setAttFac)
        self.observableAttFacCB.setDisabled(True)
        self.despikeCheckBox.stateChanged.connect(self.toggleDespiking)
        self._despike = False
        self._notEnabled(True)
        self._observableName = 'intensity'
        self.motorCB.setToolTip("Choose the independent axis of the scan display (the 'motor'), e.g. from the scan command.")
        self.label.setToolTip("The shorthand notation for the used formula to calculate\nthe number of counts at the given motor position.")
        self.observableDetectorCB.setToolTip("Chose the detector entry from the scan file information.")
        self.observableMonitorCB.setToolTip("Chose the monitor name from the scan file information.")
        self.observableTimeCB.setToolTip("Chose the time entry from the scan file information.")
        self.observableAttFaccheck.setToolTip("Chose the entry from the scan file information for an attenuation factor.")
        self.observableAttFacCB.setToolTip("Check the box to enable the choice of an attenuation factor entry.")
        self.despikeCheckBox.setToolTip("Check the box to run a despiking/filtering algorithm\non the scan data to dampen spikes/noise fluctuation.")
        self.overlayBtn.setToolTip("Open an overlay plot window to select scans to view at the same time.")
        self.showScanProfile.setToolTip("Creates a stack of all scans as matrix, creating an image.\nThe result is stored in a file, which is shown in an external viewer.")
        self.trackData.setToolTip("Open a dialog to select column and header\ndata to be included in the output file.")
        self.maptracks.setToolTip("After tracked data has been selected, choose data to map.")
        # infrastructure for testing whether a value has already been set
        self._default = "Not set"
        self.motorCB.currentIndexChanged.connect(self._checkStatus)
        self.observableDetectorCB.currentIndexChanged.connect(self._checkStatus)
        self.observableMonitorCB.currentIndexChanged.connect(self._checkStatus)
        self.observableTimeCB.currentIndexChanged.connect(self._checkStatus)
        self.observableAttFacCB.currentIndexChanged.connect(self._checkStatus)
        # introduce a "memory" object for setting initial values for the combo boxes
        self._previousObsDict = {}
        self._previousDespDict = {}

    def _defaultSettings(self):
        self._obsDict = {}
        self._despikeDict = {}
        self._trapintDict = {}
        self._previousObsDict = {}
        self._previousDespDict = {}
        self._useAttenuationFactor = False
        self.observableAttFacCB.setDisabled(True)
        self.despikeCheckBox.setChecked(False)
        self._despike = False
        self._notEnabled(True)
        self._observableName = 'intensity'
        self.deactivateShowScanProfile()
        self.trackData.setDisabled(True)
        self.doDespike.emit(False)

    def _checkStatus(self):
        # automatic check for the values in the combo boxes, run at every change
        # will fail if *any* relevant combo box value is invalid
        # at fail: no display/overlay/despike button is available
        # at success: enables all actions and draw the current selection!
        comboboxes = [self.motorCB, self.observableDetectorCB, self.observableMonitorCB,
                      self.observableTimeCB]
        if self._useAttenuationFactor:
            comboboxes.append(self.observableAttFacCB)
        check = True
        for box in comboboxes:
            if box.currentText() == self._default:
                check = False
        if check:
            self.despikeCheckBox.setDisabled(False)
            self.overlayBtn.setDisabled(False)
            self.emittit()
        else:
            self.despikeCheckBox.setDisabled(True)
            self.overlayBtn.setDisabled(True)

    def reset(self):
        self._blockSignals()
        self._defaultSettings()
        self._unblockSignals()

    def activate(self):
        self._notEnabled(False)

    def activateMapTrack(self):
        self.maptracks.setDisabled(False)

    def deactivateMapTrack(self):
        self.maptracks.setDisabled(True)

    def passInfo(self, dataobject, defaultmotor=None):
        if dataobject is None:
            self._notEnabled(True)
            return
        else:
            self._notEnabled(False)

        self._currentdataLabels = dataobject.getLabels()
        self.scantype.setText(dataobject.getScanType())
        self.scantype.setStyleSheet("color: red;")
        self._scanmotorname = dataobject.getMotorName()

        # now set the texts and labels
        self._blockSignals()
        self.motorCB.clear()
        self.observableDetectorCB.clear()
        self.observableMonitorCB.clear()
        self.observableTimeCB.clear()
        self.observableAttFacCB.clear()
        # place the default value first
        self.motorCB.addItem(self._default)
        self.observableDetectorCB.addItem(self._default)
        self.observableMonitorCB.addItem(self._default)
        self.observableTimeCB.addItem(self._default)
        self.observableAttFacCB.addItem(self._default)
        # and now insert the other labels
        self.motorCB.addItems(self._currentdataLabels)
        self.observableDetectorCB.addItems(self._currentdataLabels)
        self.observableMonitorCB.addItems(self._currentdataLabels)
        self.observableTimeCB.addItems(self._currentdataLabels)
        self.observableAttFacCB.addItems(self._currentdataLabels)
        self._unblockSignals()
        if not self._useAttenuationFactor:
            self.observableAttFacCB.setDisabled(True)
            self._useAttenuationFactor = False
            self.observableAttFaccheck.setChecked(False)
        if defaultmotor is not None:
            index = self.motorCB.findText(defaultmotor, QtCore.Qt.MatchExactly)
            if index >= 0:
                self.motorCB.setCurrentIndex(index)

        if self._previousObsDict != {}:
            self.setParameterDicts(self._previousObsDict, self._previousDespDict)

    def _notEnabled(self, state):
        self.motorCB.setDisabled(state)
        self.observableDetectorCB.setDisabled(state)
        self.observableMonitorCB.setDisabled(state)
        self.observableTimeCB.setDisabled(state)
        self.observableAttFaccheck.setDisabled(state)
        self.observableAttFacCB.setDisabled(state)
        self.despikeCheckBox.setDisabled(state)
        self.overlayBtn.setDisabled(state)
        self.trackData.setDisabled(state)

    def activateShowScanProfile(self):
        self.showScanProfile.setDisabled(False)

    def deactivateShowScanProfile(self):
        self.showScanProfile.setDisabled(True)

    def toggleAttFac(self):
        # creates trouble at reset
        self.observableAttFacCB.setDisabled(self._useAttenuationFactor)
        self._useAttenuationFactor = not self._useAttenuationFactor

    def setMotor(self, motorindex):
        self._motorname = self._currentdataLabels[self._correctIndex(motorindex)]
        self.motorName.emit(self._motorname)

    def setObservable(self, obsindex):
        self._detname = self._currentdataLabels[self._correctIndex(obsindex)]

    def setMonitor(self, monindex):
        self._monname = self._currentdataLabels[self._correctIndex(monindex)]

    def setTime(self, timeindex):
        self._timename = self._currentdataLabels[self._correctIndex(timeindex)]

    def setAttFac(self, attfacindex):
        # need to sort out the pre-condition
        self._attenfname = self._currentdataLabels[self._correctIndex(attfacindex)]

    def _correctIndex(self, index):
        # since a default element was added in front of the list
        # the correct index in the list of names is one larger
        # than the value returned from the combobox
        return index - 1

    def toggleDespiking(self):
        self._despike = not self._despike
        self.doDespike.emit(self._despike)
        if self._obsDict != {}:
            self.emittit()

    def emittit(self):
        self.activateShowScanProfile()
        self._obsDict["type"] = "iintdefinition"
        self._obsDict["input"] = "rawdata"
        self._obsDict["motor_column"] = self._motorname
        self._obsDict["detector_column"] = self._detname
        self._obsDict["monitor_column"] = self._monname
        self._obsDict["exposureTime_column"] = self._timename
        self._obsDict["output"] = self._observableName
        self._obsDict["id"] = "scannumber"
        if(self._useAttenuationFactor):
            self._obsDict["attenuationFactor_column"] = self._attenfname
        else:
            try:
                del self._obsDict["attenuationFactor_column"]
            except KeyError:
                # maybe it doesn't exist yet
                pass

        if(self._despike):
            self._despikeDict["type"] = "filter1d"
            self._despikeDict["method"] = "p09despiking"
            self._despikeDict["input"] = "intensity"
            self._despikeDict["output"] = "despikedIntensity"
        else:
            self._despikeDict = {}
        self._trapintDict["type"] = "trapezoidintegration"
        self._trapintDict["motor"] = self._motorname
        self._trapintDict["observable"] = "signalIntensity"
        self._trapintDict["output"] = "trapezoidIntegral"

        self._previousObsDict = self._obsDict.copy()
        self._previousDespDict = self._despikeDict.copy()
        self.observableDicts.emit(self._obsDict, self._despikeDict)

    def setParameterDicts(self, obsDict, despDict):
        index = self.motorCB.findText(obsDict["motor_column"], QtCore.Qt.MatchExactly)
        if index >= 0:
            self.motorCB.setCurrentIndex(index)

        # first get index of element
        index = self.observableDetectorCB.findText(obsDict["detector_column"], QtCore.Qt.MatchExactly)
        if index >= 0:
            self.observableDetectorCB.setCurrentIndex(index)

        index = self.observableMonitorCB.findText(obsDict["monitor_column"], QtCore.Qt.MatchExactly)
        if index >= 0:
            self.observableMonitorCB.setCurrentIndex(index)

        index = self.observableTimeCB.findText(obsDict["exposureTime_column"], QtCore.Qt.MatchExactly)
        if index >= 0:
            self.observableTimeCB.setCurrentIndex(index)

        try:
            index = self.observableAttFacCB.findText(obsDict["attenuationFactor_column"], QtCore.Qt.MatchExactly)
            if index >= 0:
                self.observableAttFacCB.setCurrentIndex(index)
                self.observableAttFaccheck.setChecked(True)
                self.observableAttFacCB.setDisabled(False)
        except KeyError:
            # there is no attenuation factor column
            self._useAttenuationFactor = False
            self.observableAttFacCB.setDisabled(True)
            pass

        if (despDict != {}):
            self.despikeCheckBox.setChecked(True)

    def _blockSignals(self):
        self.motorCB.blockSignals(True)
        self.observableDetectorCB.blockSignals(True)
        self.observableMonitorCB.blockSignals(True)
        self.observableTimeCB.blockSignals(True)
        self.observableAttFacCB.blockSignals(True)
        self.observableAttFaccheck.blockSignals(True)
        self.despikeCheckBox.blockSignals(True)

    def _unblockSignals(self):
        self.motorCB.blockSignals(False)
        self.observableDetectorCB.blockSignals(False)
        self.observableMonitorCB.blockSignals(False)
        self.observableTimeCB.blockSignals(False)
        self.observableAttFacCB.blockSignals(False)
        self.observableAttFaccheck.blockSignals(False)
        self.despikeCheckBox.blockSignals(False)
