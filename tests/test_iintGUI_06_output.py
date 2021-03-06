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

'''This are the tesst for iintGUI config files.'''


import unittest
import os
import numpy as np
from iintgui import iintGUI


class TestIintGUI06Output(unittest.TestCase):

    def setUp(self):
        '''Create GUI for starters'''
        self.ui = iintGUI.iintGUI(testMode=True)
        self.ctrl = self.ui._control

        self.obs = self.ui._obsDef
        self.bkg = self.ui._bkgHandling
        self.sigfit = self.ui._signalFitting
        self.ia = self.ui._inspectAnalyze

        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        mnco = "test_configurations/MnCo15_S699E740-all.icfg"
        self.mncoallfile = os.path.join(dir_path, mnco)
        self.mnconames = ["testing_MNCO-all.iint",
                          "testing_MNCO-all_scanControlPlots.pdf",
                          "testing_MNCO-all_scanProfiles.pdf",
                          "testing_MNCO-all_trackedColumnsPlots.pdf"]

        egonn = "test_configurations/egonnd2_S63E231.icfg"
        self.egonnfile =  os.path.join(dir_path, egonn)
        self.egonnames = ["testing_egonn.iint",
                          "testing_egonn_scanControlPlots.pdf",
                          "testing_egonn_scanProfiles.pdf",
                          "testing_egonn_trackedColumnsPlots.pdf"]
        

    def test_mncooutput(self):
        # test case for command line argument
        self.ui._file = self.mncoallfile
        self.ui.chooseAndLoadConfig()
        self.ui._control.setResultFilename("testing_MNCO-all")
        self.ui.runOutputSaving()
        for f in self.mnconames:
            self.assertTrue(os.path.isfile(f))
        # test if arrays are non-zero:
        darr = np.loadtxt("testing_MNCO-all.iint", unpack=True)
        for k in darr:
            self.assertTrue(np.any(k))

    def test_egonn(self):
        self.ui._file = self.egonnfile
        self.ui.chooseAndLoadConfig()
        self.ui._control.setResultFilename("testing_egonn")
        self.ui.runOutputSaving()
        for f in self.egonnames:
            self.assertTrue(os.path.isfile(f))

    def tearDown(self):
        for f in self.mnconames:
            if os.path.isfile(f):
                os.remove(f)
        for f in self.egonnames:
            if os.path.isfile(f):
                os.remove(f)


if __name__ == '__main__':
    unittest.main()
