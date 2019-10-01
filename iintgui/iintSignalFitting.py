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
    models = QtCore.pyqtSignal(list)
    autogauss = QtCore.pyqtSignal(int)

    def __init__(self, modellist, parent=None):
        super(iintSignalFitting, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("fitpanel2.ui"), self)
        self.modelList.addItems(sorted(modellist))
        self.currentModelList.itemClicked.connect(self._currentFunctionClicked)
        self.removeButton.clicked.connect(self._removeCurrentFunction)
        self.addButton.clicked.connect(self._addFunction)
        self.configButton.clicked.connect(self._getModels)
        self.resetButton.clicked.connect(self._reset)
        self.resetButton.setToolTip("Resets the complete fit information to its initial values.")
        self.currentModelList.setToolTip("The current model by its constituents, only the name and type of function are indicated.")
        self.modelList.setToolTip("Select a function for addition to the current fit mdel.")
        self.addButton.setToolTip("If a function is selected in the drop down list next to this button, clicking it will add this function to the current model.")
        self.removeButton.setToolTip("If a function is selection in the view of the current model, clicking this button will remove it from the current model.")
        self.fitButton.setToolTip("Perform the fit with the current model. Might trigger the display of a configuration dialog if further details need to be provided.")
        self.deactivateFitting()
        self.autoGaussBox.setToolTip("Enable to choose single gaussian fit with automatic guessing of parameters.\nDisables all other options.")
        self.autoGaussBox.stateChanged.connect(self._toggleGaussGuess)

    def _toggleGaussGuess(self, state):
        if state is 2:
            self.autogauss.emit(1)
            self._hideMost(True)
            self.allowFitButton()
        elif state is 0:
            self.autogauss.emit(0)
            self._hideMost(False)
            self.disallowFitButton()

    def _hideMost(self, hide):
        if hide:
            self.currentModelList.hide()
            self.modelList.hide()
            self.addButton.hide()
            self.removeButton.hide()
            self.configButton.hide()
        else:
            self.currentModelList.show()
            self.modelList.show()
            self.addButton.show()
            self.removeButton.show()
            self.configButton.show()

    def _reset(self):
        self.removeButton.setDisabled(True)
        self.fitButton.setDisabled(True)
        self.activateConfiguration()

    def reset(self):
        self.currentModelList.setDisabled(True)
        self.modelList.setDisabled(True)
        self.addButton.setDisabled(True)
        self.removeButton.setDisabled(True)
        self.disallowFitButton()
        self.resetButton.setDisabled(True)
        self.autoGaussBox.setDisabled(True)
        self.deactivateConfiguration()

    def activateFitting(self):
        self.currentModelList.setDisabled(False)
        self.modelList.setDisabled(False)
        self.addButton.setDisabled(False)
        self.resetButton.setDisabled(False)
        self.autoGaussBox.setDisabled(False)
        self.activateConfiguration()

    def deactivateFitting(self):
        self.currentModelList.setDisabled(True)
        self.modelList.setDisabled(True)
        self.addButton.setDisabled(True)
        self.removeButton.setDisabled(True)
        self.configButton.setDisabled(True)
        self.fitButton.setDisabled(True)
        self.resetButton.setDisabled(True)
        self.autoGaussBox.setDisabled(True)

    def _currentFunctionClicked(self, item):
        self._currentSelected = item
        self.removeButton.setDisabled(False)

    def _removeCurrentFunction(self):
        self.removeButton.setDisabled(True)
        # figure out how to remove the stupid item
        self.currentModelList.takeItem(self.currentModelList.row(self._currentSelected))
        self.currentModelList.clearSelection()
        self._currentSelected = None
        self.removeButton.setDisabled(True)
        if self.currentModelList.count() < 1:
            self.deactivateConfiguration()
            self.disallowFitButton()

    def allowFitButton(self, state=True):
        self.fitButton.setDisabled(False)

    def disallowFitButton(self, state=True):
        self.fitButton.setDisabled(True)

    def activateConfiguration(self):
        self.configButton.setDisabled(False)

    def deactivateConfiguration(self):
        self.configButton.setDisabled(True)

    def _addFunction(self):
        self.currentModelList.addItem(self.modelList.currentText())
        self.activateConfiguration()

    def _getModels(self):
        modellist = []
        for i in range(self.currentModelList.count()):
            modellist.append(str(self.currentModelList.item(i).text()))
        self.models.emit(modellist)
