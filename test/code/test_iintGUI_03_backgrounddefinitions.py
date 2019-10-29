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

'''This are the tests for iintGUI background definitions.'''


import unittest
import os
from iintgui import iintGUI


class TestIintGUI03BackgroundDefinitions(unittest.TestCase):

    def setUp(self):
        '''Create GUI for starters'''
        self.ui = iintGUI.iintGUI(testMode=True)
        self.ctrl = self.ui._control

        self.obs = self.ui._obsDef
        self.bkg = self.ui._bkgHandling
        self.sigfit = self.ui._signalFitting
        self.ia = self.ui._inspectAnalyze
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        mncoall = "../test_configurations/MnCo15_S699E740-all.icfg"
        self.mncoallfile = os.path.join(dir_path, mncoall)
        mncoconstbkg = "../test_configurations/MnCo15_S699E740-constBKG.icfg"
        self.mncoconstbkgfile = os.path.join(dir_path, mncoconstbkg)
        rucl = "../test_configurations/rucl3_az_S1179E1258.icfg"
        self.ruclfile = os.path.join(dir_path, rucl)


    def test_linear_bkg(self):
        self.ui._file = self.mncoallfile
        self.ui.chooseAndLoadConfig()
        # loading should enable all elements...

        # after loading the bkg box should be enabled
        self.assertTrue(self.bkg.isEnabled())
        self.assertTrue(self.bkg.groupBox.isEnabled())
        self.assertTrue(self.bkg.linearBkg.isEnabled())
        self.assertTrue(self.bkg.constBkg.isEnabled())
        self.assertTrue(self.bkg.hyperbolicBkg.isEnabled())
        self.assertTrue(self.bkg.linearBkg.isChecked())
        self.assertTrue(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertTrue(self.bkg.bkgEndPointsSB.isEnabled())

    def test_const_bkg(self):
        # also full monty, different bkg
        self.ui._file = self.mncoconstbkgfile
        self.ui.chooseAndLoadConfig()

        # after loading the bkg box should be enabled
        self.assertTrue(self.bkg.isEnabled())
        self.assertTrue(self.bkg.groupBox.isEnabled())
        self.assertTrue(self.bkg.linearBkg.isEnabled())
        self.assertTrue(self.bkg.constBkg.isEnabled())
        self.assertTrue(self.bkg.hyperbolicBkg.isEnabled())
        self.assertTrue(self.bkg.constBkg.isChecked())
        self.assertTrue(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertTrue(self.bkg.bkgEndPointsSB.isEnabled())

    def test_hyperbolic_bkg(self):
        # file contains fitting and usage of 1/x bkg

        self.ui._file = self.ruclfile
        self.ui.chooseAndLoadConfig()

        # after loading the bkg box should be enabled
        self.assertTrue(self.bkg.isEnabled())
        self.assertTrue(self.bkg.groupBox.isEnabled())
        self.assertTrue(self.bkg.linearBkg.isEnabled())
        self.assertTrue(self.bkg.constBkg.isEnabled())
        self.assertTrue(self.bkg.hyperbolicBkg.isEnabled())
        self.assertTrue(self.bkg.hyperbolicBkg.isChecked())
        self.assertTrue(self.bkg.bkgStartPointsSB.isEnabled())
        self.assertTrue(self.bkg.bkgEndPointsSB.isEnabled())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
