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
        eupt = "../test_configurations/EuPtIn4_remeasured_clean_S349E391.icfg"
        self.euptfile = os.path.join(dir_path, eupt)
        rucl = "../test_configurations/rucl3_az_S1179E1258.icfg"
        self.ruclfile = os.path.join(dir_path, rucl)

    def test_bla(self):
        self.assertTrue(True)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
