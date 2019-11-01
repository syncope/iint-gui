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

'''This are the tests for iintGUI signal definitions.'''


import unittest
import os
from iintgui import iintGUI


class TestIintGUI02SignalDefinitions(unittest.TestCase):

    def setUp(self):
        '''Create GUI for starters'''
        self.ui = iintGUI.iintGUI(testMode=True)
        self.ctrl = self.ui._control

        self.obs = self.ui._obsDef
        self.bkg = self.ui._bkgHandling
        self.sigfit = self.ui._signalFitting
        self.ia = self.ui._inspectAnalyze
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        mnco = "../test_configurations/MnCo15_S699E740-obsDef.icfg"
        self.obscfgfile = os.path.join(dir_path, mnco)
        mncodes = "../test_configurations/MnCo15_S699E740-obsDefwDes.icfg"
        self.mncodesfile = os.path.join(dir_path, mncodes)
        mncoatt = "../test_configurations/MnCo15_S699E740-obsDefAttFac.icfg"
        self.mncoattfile = os.path.join(dir_path, mncoatt)
        eupt = "../test_configurations/EuPtIn4_remeasured_clean_S349E391.icfg"
        self.euptfile = os.path.join(dir_path, eupt)
        rucl = "../test_configurations/rucl3_az_S1179E1258.icfg"
        self.ruclfile = os.path.join(dir_path, rucl)

    def test_obsdef_mnco4(self):
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
        self.assertFalse(self.obs.observableAttFaccheck.isChecked())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertFalse(self.obs.despikeCheckBox.isChecked())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        self.assertEqual(self.obs.motorCB.currentText(), 'pth')
        self.assertEqual(self.obs.observableDetectorCB.currentText(), 'exp_c01')
        self.assertEqual(self.obs.observableMonitorCB.currentText(), 'sumvfcs_counts')
        self.assertEqual(self.obs.observableTimeCB.currentText(), 'exp_t01')

    def test_obsdef_mnco4att(self):
        self.ui._file = self.mncoattfile
        self.ui.chooseAndLoadConfig()
        # loading should enable all elements...
        self.assertTrue(self.obs.motorCB.isEnabled())
        self.assertTrue(self.obs.observableDetectorCB.isEnabled())
        self.assertTrue(self.obs.observableMonitorCB.isEnabled())
        self.assertTrue(self.obs.observableTimeCB.isEnabled())
        # ... but: the attenuation factor (needs to be checked first!)
        self.assertTrue(self.obs.observableAttFacCB.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isChecked())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertFalse(self.obs.despikeCheckBox.isChecked())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        self.assertEqual(self.obs.motorCB.currentText(), 'pth')
        self.assertEqual(self.obs.observableDetectorCB.currentText(), 'exp_c01')
        self.assertEqual(self.obs.observableMonitorCB.currentText(), 'sumvfcs_counts')
        self.assertEqual(self.obs.observableTimeCB.currentText(), 'exp_t01')
        self.assertEqual(self.obs.observableAttFacCB.currentText(), 'abs_attenfactor')

    def test_obsdef_mnco4des(self):
        self.ui._file = self.mncodesfile
        self.ui.chooseAndLoadConfig()
        # loading should enable all elements...
        self.assertTrue(self.obs.motorCB.isEnabled())
        self.assertTrue(self.obs.observableDetectorCB.isEnabled())
        self.assertTrue(self.obs.observableMonitorCB.isEnabled())
        self.assertTrue(self.obs.observableTimeCB.isEnabled())
        # ... but: the attenuation factor (needs to be checked first!)
        self.assertFalse(self.obs.observableAttFacCB.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isEnabled())
        self.assertFalse(self.obs.observableAttFaccheck.isChecked())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertTrue(self.obs.despikeCheckBox.isChecked())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        self.assertEqual(self.obs.motorCB.currentText(), 'pth')
        self.assertEqual(self.obs.observableDetectorCB.currentText(), 'exp_c01')
        self.assertEqual(self.obs.observableMonitorCB.currentText(), 'sumvfcs_counts')
        self.assertEqual(self.obs.observableTimeCB.currentText(), 'exp_t01')

    def test_obsdef_eupt(self):

        self.ui._file = self.euptfile
        self.ui.chooseAndLoadConfig()
        # loading should enable all elements...
        self.assertTrue(self.obs.motorCB.isEnabled())
        self.assertTrue(self.obs.observableDetectorCB.isEnabled())
        self.assertTrue(self.obs.observableMonitorCB.isEnabled())
        self.assertTrue(self.obs.observableTimeCB.isEnabled())
        # ... but: the attenuation factor (needs to be checked first!)
        self.assertFalse(self.obs.observableAttFacCB.isEnabled())
        self.assertTrue(self.obs.observableAttFaccheck.isEnabled())
        self.assertFalse(self.obs.observableAttFaccheck.isChecked())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertFalse(self.obs.despikeCheckBox.isChecked())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        self.assertEqual(self.obs.motorCB.currentText(), 'del')
        self.assertEqual(self.obs.observableDetectorCB.currentText(), 'exp_c03')
        self.assertEqual(self.obs.observableMonitorCB.currentText(), 'sumvfcs_counts')
        self.assertEqual(self.obs.observableTimeCB.currentText(), 'exp_t01')

    def test_obsdef_rucl(self):
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
        self.assertFalse(self.obs.observableAttFaccheck.isChecked())
        self.assertTrue(self.obs.despikeCheckBox.isEnabled())
        self.assertFalse(self.obs.despikeCheckBox.isChecked())
        self.assertTrue(self.obs.trackData.isEnabled())
        self.assertTrue(self.obs.showScanProfile.isEnabled())
        # ... and but: the map tracks, unless something has been chosen for tracking
        self.assertFalse(self.obs.maptracks.isEnabled())
        self.assertTrue(self.obs.overlayBtn.isEnabled())

        self.assertEqual(self.obs.motorCB.currentText(), 'del')
        self.assertEqual(self.obs.observableDetectorCB.currentText(), 'exp_c01')
        self.assertEqual(self.obs.observableMonitorCB.currentText(), 'exp_vfc02')
        self.assertEqual(self.obs.observableTimeCB.currentText(), 'dt')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
