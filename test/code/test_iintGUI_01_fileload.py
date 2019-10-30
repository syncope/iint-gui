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

'''This are the tests for iintGUI file loading.'''


import unittest
import os
from iintgui import iintGUI


class TestIintGUI01FileLoad(unittest.TestCase):

    def setUp(self):
        '''Create GUI first'''
        self.ui = iintGUI.iintGUI(testMode=True)
        self.ctrl = self.ui._control

        self.obs = self.ui._obsDef
        self.bkg = self.ui._bkgHandling
        self.sigfit = self.ui._signalFitting
        self.ia = self.ui._inspectAnalyze
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        self.obsfilepath = "../test_configurations/MnCo15_S699E740-obsDef.icfg"
        self.obscfgfile = os.path.join(dir_path, self.obsfilepath)
        self.obsattfilepath = "../test_configurations/MnCo15_S699E740-obsDefAttFac.icfg"
        self.obsattcfgfile = os.path.join(dir_path, self.obsattfilepath)
        self.obsdespfilepath = "../test_configurations/MnCo15_S699E740-obsDefwDes.icfg"
        self.obsdespcfgfile = os.path.join(dir_path, self.obsdespfilepath)
        eupt = "../test_configurations/EuPtIn4_remeasured_clean_S349E391.icfg"
        self.euptfile = os.path.join(dir_path, eupt)
        euptfio = "../test_configurations/EuPtIn4_remeasured_S349E391-FIO.icfg"
        self.euptfiofile = os.path.join(dir_path, euptfio)
        mncoall = "../test_configurations/MnCo15_S699E740-all.icfg"
        self.mncoallfile = os.path.join(dir_path, mncoall)
        mncobkg = "../test_configurations/MnCo15_S699E740-bkg.icfg"
        self.mncobkgfile = os.path.join(dir_path, mncobkg)
        mncoconstbkg = "../test_configurations/MnCo15_S699E740-constBKG.icfg"
        self.mncoconstbkgfile = os.path.join(dir_path, mncoconstbkg)
        rucl = "../test_configurations/rucl3_az_S1179E1258.icfg"
        self.ruclfile = os.path.join(dir_path, rucl)

    def test_load_obs(self):
        self.ui._file = self.obscfgfile
        self.ui.chooseAndLoadConfig()
        # loading should enable all elements...
        self.assertTrue(self.obs.motorCB.isEnabled())
        self.assertTrue(self.obs.observableDetectorCB.isEnabled())
        self.assertTrue(self.obs.observableMonitorCB.isEnabled())
        self.assertTrue(self.obs.observableTimeCB.isEnabled())
        # ... but: the attenuation factor (needs to be checked first!)
        self.assertFalse(self.obs.observableAttFacCB.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isEnabled())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        # after loading the bkg box should be enabled
        self.assertTrue(self.bkg.isEnabled())
        self.assertTrue(self.bkg.groupBox.isEnabled())
        # .. but the rest should be disabled, unless it's checked!
        self.assertFalse(self.bkg.linearBkg.isEnabled())
        self.assertFalse(self.bkg.constBkg.isEnabled())
        self.assertFalse(self.bkg.hyperbolicBkg.isEnabled())
        self.assertFalse(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertFalse(self.bkg.bkgEndPointsSB.isEnabled())

        # it's possible to fit something after loading
        self.assertTrue(self.sigfit.isEnabled())
        self.assertTrue(self.sigfit.autoGaussBox.isEnabled())
        self.assertTrue(self.sigfit.resetButton.isEnabled())
        self.assertTrue(self.sigfit.addButton.isEnabled())
        self.assertTrue(self.sigfit.modelList.isEnabled())
        self.assertFalse(self.sigfit.removeButton.isEnabled())
        self.assertTrue(self.sigfit.configButton.isEnabled())
        self.assertFalse(self.sigfit.fitButton.isEnabled())

        self.assertFalse(self.ia.trackedColumnsPlot.isEnabled())
        self.assertFalse(self.ia.showScanFits.isEnabled())
        self.assertFalse(self.ia.polAnalysis.isEnabled())
        self.assertFalse(self.ia.saveResults.isEnabled())

    def test_load_obsatt(self):
        self.ui._file = self.obsattcfgfile
        self.ui.chooseAndLoadConfig()
        # loading should enable all elements...
        self.assertTrue(self.obs.motorCB.isEnabled())
        self.assertTrue(self.obs.observableDetectorCB.isEnabled())
        self.assertTrue(self.obs.observableMonitorCB.isEnabled())
        self.assertTrue(self.obs.observableTimeCB.isEnabled())
        # ... and! the attenuation factor should be enabled and checked
        self.assertTrue(self.obs.observableAttFacCB.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isChecked())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        # after loading the bkg box should be enabled
        self.assertTrue(self.bkg.isEnabled())
        self.assertTrue(self.bkg.groupBox.isEnabled())
        # .. but the rest should be disabled, unless it's checked!
        self.assertTrue(self.bkg.linearBkg.isEnabled())
        self.assertTrue(self.bkg.constBkg.isEnabled())
        self.assertTrue(self.bkg.hyperbolicBkg.isEnabled())
        self.assertTrue(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertTrue(self.bkg.bkgEndPointsSB.isEnabled())

        # it's possible to fit something after loading
        self.assertTrue(self.sigfit.isEnabled())
        self.assertTrue(self.sigfit.autoGaussBox.isEnabled())
        self.assertTrue(self.sigfit.resetButton.isEnabled())
        self.assertTrue(self.sigfit.addButton.isEnabled())
        self.assertTrue(self.sigfit.modelList.isEnabled())
        self.assertFalse(self.sigfit.removeButton.isEnabled())
        self.assertTrue(self.sigfit.configButton.isEnabled())
        self.assertFalse(self.sigfit.fitButton.isEnabled())

        self.assertFalse(self.ia.trackedColumnsPlot.isEnabled())
        self.assertFalse(self.ia.showScanFits.isEnabled())
        self.assertFalse(self.ia.polAnalysis.isEnabled())
        self.assertFalse(self.ia.saveResults.isEnabled())

    def test_load_obsdesp(self):
        self.ui._file = self.obsdespcfgfile
        self.ui.chooseAndLoadConfig()
        # loading should enable all elements...
        self.assertTrue(self.obs.motorCB.isEnabled())
        self.assertTrue(self.obs.observableDetectorCB.isEnabled())
        self.assertTrue(self.obs.observableMonitorCB.isEnabled())
        self.assertTrue(self.obs.observableTimeCB.isEnabled())
        # ... but: the attenuation factor (needs to be checked first!)
        self.assertFalse(self.obs.observableAttFacCB.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isEnabled())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertTrue(self.obs.despikeCheckBox.isChecked())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        # after loading the bkg box should be enabled
        self.assertTrue(self.bkg.isEnabled())
        self.assertTrue(self.bkg.groupBox.isEnabled())
        # .. but the rest should be disabled, unless it's checked!
        self.assertTrue(self.bkg.linearBkg.isEnabled())
        self.assertTrue(self.bkg.constBkg.isEnabled())
        self.assertTrue(self.bkg.hyperbolicBkg.isEnabled())
        self.assertTrue(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertTrue(self.bkg.bkgEndPointsSB.isEnabled())

        # it's possible to fit something after loading
        self.assertTrue(self.sigfit.isEnabled())
        self.assertTrue(self.sigfit.autoGaussBox.isEnabled())
        self.assertTrue(self.sigfit.resetButton.isEnabled())
        self.assertTrue(self.sigfit.addButton.isEnabled())
        self.assertTrue(self.sigfit.modelList.isEnabled())
        self.assertFalse(self.sigfit.removeButton.isEnabled())
        self.assertTrue(self.sigfit.configButton.isEnabled())
        self.assertFalse(self.sigfit.fitButton.isEnabled())

        self.assertFalse(self.ia.trackedColumnsPlot.isEnabled())
        self.assertFalse(self.ia.showScanFits.isEnabled())
        self.assertFalse(self.ia.polAnalysis.isEnabled())
        self.assertFalse(self.ia.saveResults.isEnabled())

    def test_load_euptfiofile(self):

        self.ui._file = self.euptfiofile
        self.ui.chooseAndLoadConfig()
        # loading should enable all elements...
        self.assertTrue(self.obs.motorCB.isEnabled())
        self.assertTrue(self.obs.observableDetectorCB.isEnabled())
        self.assertTrue(self.obs.observableMonitorCB.isEnabled())
        self.assertTrue(self.obs.observableTimeCB.isEnabled())
        # ... but: the attenuation factor (needs to be checked first!)
        self.assertFalse(self.obs.observableAttFacCB.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isEnabled())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        # after loading the bkg box should be enabled
        self.assertTrue(self.bkg.isEnabled())
        self.assertTrue(self.bkg.groupBox.isEnabled())
        # .. but the rest should be disabled, unless it's checked!
        self.assertFalse(self.bkg.linearBkg.isEnabled())
        self.assertFalse(self.bkg.constBkg.isEnabled())
        self.assertFalse(self.bkg.hyperbolicBkg.isEnabled())
        self.assertFalse(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertFalse(self.bkg.bkgEndPointsSB.isEnabled())

        # it's possible to fit something after loading
        self.assertTrue(self.sigfit.isEnabled())
        self.assertTrue(self.sigfit.autoGaussBox.isEnabled())
        self.assertTrue(self.sigfit.resetButton.isEnabled())
        self.assertTrue(self.sigfit.addButton.isEnabled())
        self.assertTrue(self.sigfit.modelList.isEnabled())
        self.assertFalse(self.sigfit.removeButton.isEnabled())
        self.assertTrue(self.sigfit.configButton.isEnabled())
        self.assertFalse(self.sigfit.fitButton.isEnabled())

        self.assertFalse(self.ia.trackedColumnsPlot.isEnabled())
        self.assertFalse(self.ia.showScanFits.isEnabled())
        self.assertFalse(self.ia.polAnalysis.isEnabled())
        self.assertFalse(self.ia.saveResults.isEnabled())

    def test_load_mncoallfile(self):
        # the full monty: load, desp, bkg, fit, results
        self.ui._file = self.mncoallfile
        self.ui.chooseAndLoadConfig()
        # loading should enable all elements...
        self.assertTrue(self.obs.motorCB.isEnabled())
        self.assertTrue(self.obs.observableDetectorCB.isEnabled())
        self.assertTrue(self.obs.observableMonitorCB.isEnabled())
        self.assertTrue(self.obs.observableTimeCB.isEnabled())
        # ... but: the attenuation factor (needs to be checked first!)
        self.assertFalse(self.obs.observableAttFacCB.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isEnabled())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        # after loading the bkg box should be enabled
        self.assertTrue(self.bkg.isEnabled())
        self.assertTrue(self.bkg.groupBox.isEnabled())
        # .. but the rest should be disabled, unless it's checked!
        self.assertTrue(self.bkg.linearBkg.isEnabled())
        self.assertTrue(self.bkg.constBkg.isEnabled())
        self.assertTrue(self.bkg.hyperbolicBkg.isEnabled())
        self.assertTrue(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertTrue(self.bkg.bkgEndPointsSB.isEnabled())

        # it's possible to fit something after loading
        self.assertTrue(self.sigfit.isEnabled())
        self.assertTrue(self.sigfit.autoGaussBox.isEnabled())
        self.assertTrue(self.sigfit.resetButton.isEnabled())
        self.assertTrue(self.sigfit.addButton.isEnabled())
        self.assertTrue(self.sigfit.modelList.isEnabled())
        self.assertFalse(self.sigfit.removeButton.isEnabled())
        self.assertTrue(self.sigfit.configButton.isEnabled())
        self.assertTrue(self.sigfit.fitButton.isEnabled())

        self.assertTrue(self.ia.trackedColumnsPlot.isEnabled())
        self.assertTrue(self.ia.showScanFits.isEnabled())
        self.assertTrue(self.ia.polAnalysis.isEnabled())
        self.assertTrue(self.ia.saveResults.isEnabled())

    def test_load_mncobkgfile(self):

        self.ui._file = self.mncobkgfile
        self.ui.chooseAndLoadConfig()
        # loading should enable all elements...
        self.assertTrue(self.obs.motorCB.isEnabled())
        self.assertTrue(self.obs.observableDetectorCB.isEnabled())
        self.assertTrue(self.obs.observableMonitorCB.isEnabled())
        self.assertTrue(self.obs.observableTimeCB.isEnabled())
        # ... but: the attenuation factor (needs to be checked first!)
        self.assertFalse(self.obs.observableAttFacCB.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isEnabled())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        # after loading the bkg box should be enabled
        self.assertTrue(self.bkg.isEnabled())
        self.assertTrue(self.bkg.groupBox.isEnabled())
        # .. but the rest should be disabled, unless it's checked!
        self.assertTrue(self.bkg.linearBkg.isEnabled())
        self.assertTrue(self.bkg.constBkg.isEnabled())
        self.assertTrue(self.bkg.hyperbolicBkg.isEnabled())
        self.assertTrue(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertTrue(self.bkg.bkgEndPointsSB.isEnabled())

        # it's possible to fit something after loading
        self.assertTrue(self.sigfit.isEnabled())
        self.assertTrue(self.sigfit.autoGaussBox.isEnabled())
        self.assertTrue(self.sigfit.resetButton.isEnabled())
        self.assertTrue(self.sigfit.addButton.isEnabled())
        self.assertTrue(self.sigfit.modelList.isEnabled())
        self.assertFalse(self.sigfit.removeButton.isEnabled())
        self.assertTrue(self.sigfit.configButton.isEnabled())
        self.assertFalse(self.sigfit.fitButton.isEnabled())

        self.assertFalse(self.ia.trackedColumnsPlot.isEnabled())
        self.assertFalse(self.ia.showScanFits.isEnabled())
        self.assertFalse(self.ia.polAnalysis.isEnabled())
        self.assertFalse(self.ia.saveResults.isEnabled())

    def test_load_mncoconstbkgfile(self):
        # also full monty, different bkg
        self.ui._file = self.mncoconstbkgfile
        self.ui.chooseAndLoadConfig()
        # loading should enable all elements...
        self.assertTrue(self.obs.motorCB.isEnabled())
        self.assertTrue(self.obs.observableDetectorCB.isEnabled())
        self.assertTrue(self.obs.observableMonitorCB.isEnabled())
        self.assertTrue(self.obs.observableTimeCB.isEnabled())
        # ... but: the attenuation factor (needs to be checked first!)
        self.assertFalse(self.obs.observableAttFacCB.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isEnabled())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        # after loading the bkg box should be enabled
        self.assertTrue(self.bkg.isEnabled())
        self.assertTrue(self.bkg.groupBox.isEnabled())
        # .. but the rest should be disabled, unless it's checked!
        self.assertTrue(self.bkg.linearBkg.isEnabled())
        self.assertTrue(self.bkg.constBkg.isEnabled())
        self.assertTrue(self.bkg.hyperbolicBkg.isEnabled())
        self.assertTrue(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertTrue(self.bkg.bkgEndPointsSB.isEnabled())

        # it's possible to fit something after loading
        self.assertTrue(self.sigfit.isEnabled())
        self.assertTrue(self.sigfit.autoGaussBox.isEnabled())
        self.assertTrue(self.sigfit.resetButton.isEnabled())
        self.assertTrue(self.sigfit.addButton.isEnabled())
        self.assertTrue(self.sigfit.modelList.isEnabled())
        self.assertFalse(self.sigfit.removeButton.isEnabled())
        self.assertTrue(self.sigfit.configButton.isEnabled())
        self.assertTrue(self.sigfit.fitButton.isEnabled())

        self.assertTrue(self.ia.trackedColumnsPlot.isEnabled())
        self.assertTrue(self.ia.showScanFits.isEnabled())
        self.assertTrue(self.ia.polAnalysis.isEnabled())
        self.assertTrue(self.ia.saveResults.isEnabled())

    def test_load_ruclfile(self):
        # file contains fitting and usage of 1/x bkg

        self.ui._file = self.ruclfile
        self.ui.chooseAndLoadConfig()
        # loading should enable all elements...
        self.assertTrue(self.obs.motorCB.isEnabled())
        self.assertTrue(self.obs.observableDetectorCB.isEnabled())
        self.assertTrue(self.obs.observableMonitorCB.isEnabled())
        self.assertTrue(self.obs.observableTimeCB.isEnabled())
        # ... but: the attenuation factor (needs to be checked first!)
        self.assertFalse(self.obs.observableAttFacCB.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isEnabled())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        # after loading the bkg box should be enabled
        self.assertTrue(self.bkg.isEnabled())
        self.assertTrue(self.bkg.groupBox.isEnabled())
        # .. but the rest should be disabled, unless it's checked!
        self.assertTrue(self.bkg.linearBkg.isEnabled())
        self.assertTrue(self.bkg.constBkg.isEnabled())
        self.assertTrue(self.bkg.hyperbolicBkg.isEnabled())
        self.assertTrue(self.bkg.hyperbolicBkg.isChecked())
        self.assertTrue(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertTrue(self.bkg.bkgEndPointsSB.isEnabled())

        # it's possible to fit something after loading
        self.assertTrue(self.sigfit.isEnabled())
        self.assertTrue(self.sigfit.autoGaussBox.isEnabled())
        self.assertTrue(self.sigfit.resetButton.isEnabled())
        self.assertTrue(self.sigfit.addButton.isEnabled())
        self.assertTrue(self.sigfit.modelList.isEnabled())
        self.assertFalse(self.sigfit.removeButton.isEnabled())
        self.assertTrue(self.sigfit.configButton.isEnabled())
        self.assertTrue(self.sigfit.fitButton.isEnabled())

        self.assertTrue(self.ia.trackedColumnsPlot.isEnabled())
        self.assertTrue(self.ia.showScanFits.isEnabled())
        self.assertTrue(self.ia.polAnalysis.isEnabled())
        self.assertTrue(self.ia.saveResults.isEnabled())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
