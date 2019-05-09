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


class iintInspectAnalyze(QtGui.QWidget):

    def __init__(self, parent=None):
        super(iintInspectAnalyze, self).__init__(parent)
        uic.loadUi(getUIFile.getUIFile("inspectAnalyze.ui"), self)
        self.trackedColumnsPlot.setToolTip("Creates and shows a pdf of all scan parameters vs. the tracked columns\nas selected in the data to track dialog.\nWorks only for gaussian/lorentzian fit model!")
        self.showScanFits.setToolTip("Saves a pdf of all scans including the fitted curves\nand opens an external viewer showing this file.")
        self.polAnalysis.setToolTip("Run a polarization analysis on the current data; non-interactive.\nA pdf file and a .stokes file with be created and saved.\nThe pdf file will be opened in an external viewer.")
        self.saveResults.setToolTip("Opens a dialog to allow the saving of the output file.\nThe file automatically contains the scan number, all fit parameters\nand the iint sum including their errors.\nIn addition the data is included that has been selected in the 'Choose data to track' dialog.")

    def activate(self):
        self.trackedColumnsPlot.setDisabled(False)
        self.showScanFits.setDisabled(False)
        self.polAnalysis.setDisabled(False)
        self.saveResults.setDisabled(False)

    def deactivate(self):
        self.trackedColumnsPlot.setDisabled(True)
        self.showScanFits.setDisabled(True)
        self.polAnalysis.setDisabled(True)
        self.saveResults.setDisabled(True)

    def reset(self):
        self.trackedColumnsPlot.setDisabled(True)
        self.showScanFits.setDisabled(True)
        self.polAnalysis.setDisabled(True)
        self.saveResults.setDisabled(True)
