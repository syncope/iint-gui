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


class iintSignalHandling(QtGui.QWidget):
    modelcfg = QtCore.pyqtSignal(str, int)
    removeIndex = QtCore.pyqtSignal(int)
    guesspeak = QtCore.pyqtSignal(int)

    def __init__(self, pDict, parent=None):
        super(iintSignalHandling, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("fitpanel.ui"), self)
        self._hiddencblist = [self.firstModelCB, self.secondModelCB, self.thirdModelCB, self.fourthModelCB]
        self._dummy = True
        self._hiddenuselist = [self._dummy, self.useSecond, self.useThird, self.useFourth]
        self.setParameterDict(pDict)
        self.performFitPushBtn.setDisabled(True)
        self.guessMode.setDisabled(True)
        self.configureFirst.clicked.connect(self.emitfirstmodelconfig)
        self.configureSecond.clicked.connect(self.emitsecondmodelconfig)
        self.configureThird.clicked.connect(self.emitthirdmodelconfig)
        self.configureFourth.clicked.connect(self.emitfourthmodelconfig)
        self.guessMode.stateChanged.connect(self.doGuessing)
        self._inactive = [False, True, True, True]
        self._firstModelDict = {}
        self._secondModelDict = {}
        self._thirdModelDict = {}
        self._fourthModelDict = {}
        self.useSecond.stateChanged.connect(self._toggleSecond)
        self.useThird.stateChanged.connect(self._toggleThird)
        self.useFourth.stateChanged.connect(self._toggleFourth)
        self.firstModelCB.currentIndexChanged.connect(self._checkForGauss)
        self.guessMode.setToolTip("Check to enable guessing of fit start parameters, suited for varying peak positions.\nCurrently only implemented for single gaussian models.\nIf checked no second model can be selected.")
        self.useSecond.setToolTip("Check to activate the options on the line,\nenabling the choice of a model and its configuration.")
        self.useThird.setToolTip("Check to activate the options on the line,\nenabling the choice of a model and its configuration.")
        self.useFourth.setToolTip("Check to activate the options on the line,\nenabling the choice of a model and its configuration.")
        self.firstModelCB.setToolTip("Select a model from the drop down list.")
        self.secondModelCB.setToolTip("Select a model from the drop down list.")
        self.thirdModelCB.setToolTip("Select a model from the drop down list.")
        self.fourthModelCB.setToolTip("Select a model from the drop down list.")
        self.configureFirst.setToolTip("Click here to set the initial values for\nthe chosen model from the drop down list.")
        self.configureSecond.setToolTip("Click here to set the initial values for\nthe chosen model from the drop down list.")
        self.configureThird.setToolTip("Click here to set the initial values for\nthe chosen model from the drop down list.")
        self.configureFourth.setToolTip("Click here to set the initial values for\nthe chosen model from the drop down list.")
        self.performFitPushBtn.setToolTip("Press to run the fitting procedure. All chosen models\nmust be configured first, otherwise fitting is not possible.")

    def reset(self):
        self._firstModelDict = {}
        self._secondModelDict = {}
        self._thirdModelDict = {}
        self._fourthModelDict = {}
        self.performFitPushBtn.setDisabled(True)
        self.configureFirst.setDisabled(True)
        self.guessMode.setDisabled(True)

    def activateConfiguration(self):
        self.firstModelCB.setDisabled(False)
        self.configureFirst.setDisabled(True)
        self.guessMode.setDisabled(False)
        self.useSecond.setDisabled(False)
        self.useThird.setDisabled(False)
        self.useFourth.setDisabled(False)
        self.guessMode.setChecked(True)
        self.performFitPushBtn.setDisabled(False)

    def deactivateConfiguration(self):
        self.firstModelCB.setDisabled(True)
        self.configureFirst.setDisabled(True)
        self.guessMode.setDisabled(True)

    def activateFitting(self):
        self.performFitPushBtn.setDisabled(False)
        self.firstModelCB.setDisabled(False)
        self.useSecond.setDisabled(False)
        self.useThird.setDisabled(False)
        self.useFourth.setDisabled(False)
        self._checkForGauss()

    def deactivateFitting(self):
        self.guessMode.setDisabled(True)
        self.performFitPushBtn.setDisabled(True)
        self.firstModelCB.setDisabled(True)
        self.configureFirst.setDisabled(True)
        self.secondModelCB.setDisabled(True)
        self.configureSecond.setDisabled(True)
        self.thirdModelCB.setDisabled(True)
        self.configureThird.setDisabled(True)
        self.fourthModelCB.setDisabled(True)
        self.configureFourth.setDisabled(True)
        self.useSecond.setDisabled(True)
        self.useThird.setDisabled(True)
        self.useFourth.setDisabled(True)

    def doGuessing(self, state):
        if state is 2:
            self.configureFirst.setDisabled(True)
            self.activateFitting()
            self.guesspeak.emit(1)
            self.useSecond.setDisabled(True)
            self.useThird.setDisabled(True)
            self.useFourth.setDisabled(True)
        elif state is 0:
            self.configureFirst.setDisabled(False)
            self.guesspeak.emit(0)
            self.configureFirst.setDisabled(False)
            self.useSecond.setDisabled(False)
            self.useThird.setDisabled(False)
            self.useFourth.setDisabled(False)
            self.performFitPushBtn.setDisabled(True)

    def _checkForGauss(self):
        # get the model name:
        currentModel = self._modelnames[self.firstModelCB.currentIndex()]
        if currentModel != "gaussianModel":
            self.guessMode.setCheckState(0)
        else:
            if(self.guessMode.isEnabled()):
                self.guessMode.setCheckState(2)

    def _toggleSecond(self):
        self._inactive[1] = not self._inactive[1]
        self.secondModelCB.setDisabled(self._inactive[1])
        self.configureSecond.setDisabled(self._inactive[1])
        if(self._inactive[1]):
            self.removeIndex.emit(1)
        else:
            self.guessMode.setChecked(False)
        self._checkGuessEnabled()

    def _toggleThird(self):
        self._inactive[2] = not self._inactive[2]
        self.thirdModelCB.setDisabled(self._inactive[2])
        self.configureThird.setDisabled(self._inactive[2])
        if(self._inactive[2]):
            self.removeIndex.emit(2)
        else:
            self.guessMode.setChecked(False)
        self._checkGuessEnabled()

    def _toggleFourth(self):
        self._inactive[3] = not self._inactive[3]
        self.fourthModelCB.setDisabled(self._inactive[3])
        self.configureFourth.setDisabled(self._inactive[3])
        if(self._inactive[3]):
            self.removeIndex.emit(3)
        else:
            self.guessMode.setChecked(False)
        self._checkGuessEnabled()

    def _checkGuessEnabled(self):
        if self._inactive[1] and self._inactive[2] and self._inactive[3]:
            self.guessMode.setDisabled(False)
        else:
            self.guessMode.setDisabled(True)

    def setParameterDict(self, pDict):
        self._parDict = pDict

        # set the different scenarios
        names = []
        model = pDict["model"]
        for name in sorted(model.keys()):
            names.append(model[name]['modeltype'])

        for i in range(len(names)):
            name = names[i]
            self._hiddencblist[i].setCurrentIndex(self._hiddencblist[i].findText(name))
            try:
                self._hiddenuselist[i].setDisabled(False)
                self._hiddenuselist[i].setCheckState(2)
            except AttributeError:
                pass

    def passModels(self, modelDict):
        self._modelnames = sorted([key for key in modelDict.keys()])
        self.firstModelCB.addItems(self._modelnames)
        self.secondModelCB.addItems(self._modelnames)
        self.thirdModelCB.addItems(self._modelnames)
        self.fourthModelCB.addItems(self._modelnames)

    def emitfirstmodelconfig(self):
        self.activateFitting()
        index = self.firstModelCB.currentIndex()
        self.modelcfg.emit(self._modelnames[index], 0)

    def emitsecondmodelconfig(self):
        index = self.secondModelCB.currentIndex()
        self.modelcfg.emit(self._modelnames[index], 1)

    def emitthirdmodelconfig(self):
        index = self.thirdModelCB.currentIndex()
        self.modelcfg.emit(self._modelnames[index], 2)

    def emitfourthmodelconfig(self):
        index = self.fourthModelCB.currentIndex()
        self.modelcfg.emit(self._modelnames[index], 3)
