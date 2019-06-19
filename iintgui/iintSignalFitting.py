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


class iintSignalFitting(QtGui.QWidget):
    #~ modelcfg = QtCore.pyqtSignal(str, int)
    #~ removeIndex = QtCore.pyqtSignal(int)
    #~ guesspeak = QtCore.pyqtSignal(int)

    def __init__(self, pDict, modellist parent=None):
        super(iintSignalFitting, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("fitpanel2.ui"), self)
        #~ self._hiddencblist = [self.firstModelCB, self.secondModelCB, self.thirdModelCB, self.fourthModelCB]
        #~ self._dummy = True
        #~ self._hiddenuselist = [self._dummy, self.useSecond, self.useThird, self.useFourth]
        self.setParameterDict(pDict)
        #~ self.performFitPushBtn.setDisabled(True)
        #~ self.guessMode.setDisabled(True)
        #~ self.guessMode.stateChanged.connect(self.doGuessing)
        #~ self._inactive = [False, True, True, True]
        self.currentModelList.setToolTip("The current model by its constituents, only the name and type of function are indicated.")
        self.modelList.setToolTip("Select a function for addition to the current fit mdel.")
        self.addButton.setToolTip("If a function is selected in the drop down list next to this button, clicking it will add this function to the current model.")
        self.removeButton.setToolTip("If a function is selection in the view of the current model, clicking this button will remove it from the current model.")
        self.fitButton.setToolTip("Perform the fit with the current model. Might trigger the display of a configuration dialog if further details need to be provided.")

    def reset(self):
        self.currentModelList.setDisabled(True)
        self.modelList.setDisabled(True)
        self.addButton.setDisabled(True)
        self.removeButton.setDisabled(True)
        self.fitButton.setDisabled(True)

    #~ def activateConfiguration(self):
        #~ self.firstModelCB.setDisabled(False)
        #~ self.configureFirst.setDisabled(True)
        #~ self.guessMode.setDisabled(False)
        #~ self.useSecond.setDisabled(False)
        #~ self.useThird.setDisabled(False)
        #~ self.useFourth.setDisabled(False)
        #~ self.guessMode.setChecked(True)
        #~ self.performFitPushBtn.setDisabled(False)

    #~ def deactivateConfiguration(self):
        #~ self.firstModelCB.setDisabled(True)
        #~ self.configureFirst.setDisabled(True)
        #~ self.guessMode.setDisabled(True)

    def setParameterDict(self, pDict):
        self._parDict = pDict

    def activateFitting(self):
        self.currentModelList.setDisabled(False)
        self.modelList.setDisabled(False)
        self.addButton.setDisabled(False)
        self.fitButton.setDisabled(False)

        #~ self._checkForGauss()

    def deactivateFitting(self):
        #~ self.guessMode.setDisabled(True)
        self.currentModelList.setDisabled(True)
        self.modelList.setDisabled(True)
        self.addButton.setDisabled(True)
        self.removeButton.setDisabled(True)
        self.fitButton.setDisabled(True)

    #~ def doGuessing(self, state):
        #~ if state is 2:
            #~ self.configureFirst.setDisabled(True)
            #~ self.activateFitting()
            #~ self.guesspeak.emit(1)
            #~ self.useSecond.setDisabled(True)
            #~ self.useThird.setDisabled(True)
            #~ self.useFourth.setDisabled(True)
        #~ elif state is 0:
            #~ self.configureFirst.setDisabled(False)
            #~ self.guesspeak.emit(0)
            #~ self.configureFirst.setDisabled(False)
            #~ self.useSecond.setDisabled(False)
            #~ self.useThird.setDisabled(False)
            #~ self.useFourth.setDisabled(False)
            #~ self.performFitPushBtn.setDisabled(True)

    #~ def _checkForGauss(self):
        #~ # get the model name:
        #~ currentModel = self._modelnames[self.firstModelCB.currentIndex()]
        #~ if currentModel != "gaussianModel":
            #~ self.guessMode.setCheckState(0)
        #~ else:
            #~ if( self.guessMode.isEnabled()):
                #~ self.guessMode.setCheckState(2)
  
    #~ def _checkGuessEnabled(self):
        #~ if self._inactive[1] and self._inactive[2] and self._inactive[3]:
            #~ self.guessMode.setDisabled(False)
        #~ else:
            #~ self.guessMode.setDisabled(True)

    #~ def passModels(self, modelDict):
        #~ self._modelnames = sorted([key for key in modelDict.keys()])
        #~ self.firstModelCB.addItems(self._modelnames)
        #~ self.secondModelCB.addItems(self._modelnames)
        #~ self.thirdModelCB.addItems(self._modelnames)
        #~ self.fourthModelCB.addItems(self._modelnames)
