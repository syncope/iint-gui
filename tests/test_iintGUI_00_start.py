# Copyright (C) 2017-19  Christoph Rosemann
#  DESY, Notkestr. 85, D-22607 Hamburg
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

'''This are the tests for iintGUI startup and reset.'''


import unittest
from iintgui import iintGUI


class TestIintGUI00Start(unittest.TestCase):

    def setUp(self):
        '''Create GUI'''
        self.ui = iintGUI.iintGUI()
        self.ctrl = self.ui._control

        self.obs = self.ui._obsDef
        self.bkg = self.ui._bkgHandling
        self.sigfit = self.ui._signalFitting
        self.ia = self.ui._inspectAnalyze

    def test_start(self):
        self.assertFalse(self.obs.motorCB.isEnabled())
        self.assertFalse(self.obs.observableDetectorCB.isEnabled())
        self.assertFalse(self.obs.observableMonitorCB.isEnabled())
        self.assertFalse(self.obs.observableTimeCB.isEnabled())
        self.assertFalse(self.obs.observableAttFacCB.isEnabled())
        self.assertFalse(self.obs.observableAttFaccheck.isEnabled())
        self.assertFalse(self.obs.despikeCheckBox.isEnabled())
        self.assertFalse(self.obs.trackData.isEnabled())
        self.assertFalse(self.obs.showScanProfile.isEnabled())
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertFalse(self.obs.overlayBtn.isEnabled())

        self.assertFalse(self.bkg.groupBox.isEnabled())
        self.assertFalse(self.bkg.linearBkg.isEnabled())
        self.assertFalse(self.bkg.constBkg.isEnabled())
        self.assertFalse(self.bkg.hyperbolicBkg.isEnabled())
        self.assertFalse(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertFalse(self.bkg.bkgEndPointsSB.isEnabled())

        self.assertFalse(self.sigfit.autoGaussBox.isEnabled())
        self.assertFalse(self.sigfit.resetButton.isEnabled())
        self.assertFalse(self.sigfit.addButton.isEnabled())
        self.assertFalse(self.sigfit.modelList.isEnabled())
        self.assertFalse(self.sigfit.removeButton.isEnabled())
        self.assertFalse(self.sigfit.configButton.isEnabled())
        self.assertFalse(self.sigfit.fitButton.isEnabled())

        self.assertFalse(self.ia.trackedColumnsPlot.isEnabled())
        self.assertFalse(self.ia.showScanFits.isEnabled())
        self.assertFalse(self.ia.polAnalysis.isEnabled())
        self.assertFalse(self.ia.saveResults.isEnabled())

    def test_reset(self):
        self.ui._resetAll()
        self.assertFalse(self.obs.motorCB.isEnabled())
        self.assertFalse(self.obs.observableDetectorCB.isEnabled())
        self.assertFalse(self.obs.observableMonitorCB.isEnabled())
        self.assertFalse(self.obs.observableTimeCB.isEnabled())
        self.assertFalse(self.obs.observableAttFacCB.isEnabled())
        self.assertFalse(self.obs.observableAttFaccheck.isEnabled())
        self.assertFalse(self.obs.despikeCheckBox.isEnabled())
        self.assertFalse(self.obs.trackData.isEnabled())
        self.assertFalse(self.obs.showScanProfile.isEnabled())
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertFalse(self.obs.overlayBtn.isEnabled())

        self.assertFalse(self.bkg.groupBox.isEnabled())
        self.assertFalse(self.bkg.linearBkg.isEnabled())
        self.assertFalse(self.bkg.constBkg.isEnabled())
        self.assertFalse(self.bkg.hyperbolicBkg.isEnabled())
        self.assertFalse(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertFalse(self.bkg.bkgEndPointsSB.isEnabled())

        self.assertFalse(self.sigfit.autoGaussBox.isEnabled())
        self.assertFalse(self.sigfit.resetButton.isEnabled())
        self.assertFalse(self.sigfit.addButton.isEnabled())
        self.assertFalse(self.sigfit.modelList.isEnabled())
        self.assertFalse(self.sigfit.removeButton.isEnabled())
        self.assertFalse(self.sigfit.configButton.isEnabled())
        self.assertFalse(self.sigfit.fitButton.isEnabled())

        self.assertFalse(self.ia.trackedColumnsPlot.isEnabled())
        self.assertFalse(self.ia.showScanFits.isEnabled())
        self.assertFalse(self.ia.polAnalysis.isEnabled())
        self.assertFalse(self.ia.saveResults.isEnabled())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
