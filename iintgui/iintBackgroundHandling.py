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


class iintBackgroundHandling(QtGui.QWidget):
    bkgDicts = QtCore.pyqtSignal(dict, dict, dict, dict)
    bkgmodel = QtCore.pyqtSignal(str)
    noBKG= QtCore.pyqtSignal(int)

    def __init__(self, pDicts, parent=None):
        super(iintBackgroundHandling, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("iintbackground.ui"), self)
        self.bkgStartPointsSB.setMinimum(0)
        self.bkgStartPointsSB.setMaximum(10)
        self.bkgEndPointsSB.setMinimum(0)
        self.bkgEndPointsSB.setMaximum(10)
        self._selectParDict = {}
        self._fitParDict = {}
        self._calcParDict = {}
        self._subtractParDict = {}
        # if there are just two options, only one toggle needs to be connected
        self.constBkg.clicked.connect(self._setModel)
        self.linearBkg.clicked.connect(self._setModel)
        self.hyperbolicBkg.clicked.connect(self._setModel)
        # there used to be a button to fit the background
        #~ self.fitBkg.clicked.connect(self.emittem)
        self._noBKG = True
        self.groupBox.clicked.connect(self._clicktoggle)
        #~ self.useBkg.stateChanged.connect(self._toggle)
        self.setParameterDicts(pDicts)
        #~ self.fitBkg.setDisabled(True)
        self.groupBox.setToolTip("If data is available, check this box to enable the\nsetting and execution of background calculation.")
        self.linearBkg.setToolTip("Active to chose a linear background model.")
        self.constBkg.setToolTip("Activate to select a constant background model.")
        self.bkgStartPointsSB.setToolTip("Select the number of points at the low end\nof the motor positions to be included in the background estimation.")
        self.bkgEndPointsSB.setToolTip("Select the number of points at the upper end\nof the motor positions to be included in the background estimation.")
        #~ self.fitBkg.setToolTip("Perform the background fitting procedure.")

    def reset(self):
        self._selectParDict = {}
        self._fitParDict = {}
        self._calcParDict = {}
        self._subtractParDict = {}
        self.bkgStartPointsSB.setValue(3)
        self.bkgEndPointsSB.setValue(3)
        #~ self.fitBkg.setDisabled(True)
        self.bkgEndPointsSB.setDisabled(True)
        self.bkgStartPointsSB.setDisabled(True)
        self.linearBkg.setDisabled(True)
        self.constBkg.setDisabled(True)
        self.hyperbolicBkg.setDisabled(True)
        self.groupBox.setDisabled(True)
        #~ self.groupBox.setChecked(False)

    def activate(self):
        self.bkgEndPointsSB.setDisabled(False)
        self.bkgStartPointsSB.setDisabled(False)
        self.linearBkg.setDisabled(False)
        self.constBkg.setDisabled(False)
        self.hyperbolicBkg.setDisabled(False)
        self.groupBox.setDisabled(False)
        #~ self.fitBkg.setDisabled(False)
        # if it is already active, then do the magic
        self._clicktoggle(self.groupBox.isChecked())

    def _clicktoggle(self, checked):
        if checked:
            self._noBKG = False
            self.noBKG.emit(0)
            self.emittem()
        elif not checked:
            self._noBKG = True
            self.noBKG.emit(1)

    def _setModel(self):
        if self.linearBkg.isChecked():
            self._model = "linearModel"
        elif self.constBkg.isChecked():
            self._model = "constantModel"
        elif self.hyperbolicBkg.isChecked():
            self._model = "shiftedhyperbolaModel"
        self.bkgmodel.emit(self._model)
        if self._noBKG is False:
            self.emittem()

    def setParameterDicts(self, dicts, active=False):
        self._selectParDict = dicts[0]
        self.bkgStartPointsSB.setValue(self._selectParDict["startpointnumber"])
        self.bkgEndPointsSB.setValue(self._selectParDict["endpointnumber"])
        self._fitParDict = dicts[1]
        model = self._fitParDict["model"]
        modeltype = None
        for k in model.keys():
            try:
                modeltype = model[k]['modeltype']
            except:
                pass
        if modeltype == 'linearModel':
            self.linearBkg.setChecked(True)
        elif modeltype == 'constantModel':
            self.constBkg.setChecked(True)
        elif modeltype == 'shiftedhyperbolaModel':
            self.hyperbolicBkg.setChecked(True)

        self._calcParDict = dicts[2]
        self._subtractParDict = dicts[3]
        # previous check if bkg is enabled
        #~ if dicts[0] != {} and dicts[1] != {} and dicts[2] != {} and dicts[3] != {}:
        # now only activate when done from config!
        if active:
            self.groupBox.setChecked(True)

    def emittem(self):
        self._selectParDict["startpointnumber"] = self.bkgStartPointsSB.value()
        self._selectParDict["endpointnumber"] = self.bkgEndPointsSB.value()
        self.bkgDicts.emit(self._selectParDict, self._fitParDict, self._calcParDict, self._subtractParDict)
