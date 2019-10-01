# Copyright (C) 2019 Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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


'''This is the test for the  module.'''

import unittest
from iintgui import 


class Test(unittest.TestCase):

    def setUp(self):
        '''Create LoggerBox'''
        self. = .()

    def test_bla(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()



#~ from PyQt4 import QtCore, QtGui

#~ # taken from
#~ # expandable/collapsible widget/group box:
#~ # https://stackoverflow.com/questions/52615115/how-to-create-collapsible-box-in-pyqt


#~ class CollapsibleBox(QtGui.QWidget):
    #~ def __init__(self, title="", parent=None):
        #~ super(CollapsibleBox, self).__init__(parent)

        #~ self.toggle_button = QtGui.QToolButton(text=title, checkable=True, checked=False)
        #~ self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        #~ self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        #~ self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        #~ self.toggle_button.pressed.connect(self.on_pressed)

        #~ self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        #~ self.content_area = QtGui.QScrollArea(maximumHeight=0, minimumHeight=0)
        #~ self.content_area.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        #~ self.content_area.setFrameShape(QtGui.QFrame.NoFrame)

        #~ lay = QtGui.QVBoxLayout(self)
        #~ lay.setSpacing(0)
        #~ lay.setContentsMargins(0, 0, 0, 0)
        #~ lay.addWidget(self.toggle_button)
        #~ lay.addWidget(self.content_area)

        #~ self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self, b"minimumHeight"))
        #~ self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self, b"maximumHeight"))
        #~ self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self.content_area, b"maximumHeight"))

    #~ @QtCore.pyqtSlot()
    #~ def on_pressed(self):
        #~ checked = self.toggle_button.isChecked()
        #~ self.toggle_button.setArrowType(QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)
        #~ self.toggle_animation.setDirection(QtCore.QAbstractAnimation.Forward if not checked else QtCore.QAbstractAnimation.Backward)
        #~ self.toggle_animation.start()

    #~ def setContentLayout(self, layout):
        #~ lay = self.content_area.layout()
        #~ del lay
        #~ self.content_area.setLayout(layout)
        #~ collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        #~ content_height = layout.sizeHint().height()
        #~ for i in range(self.toggle_animation.animationCount()):
            #~ animation = self.toggle_animation.animationAt(i)
            #~ animation.setDuration(500)
            #~ animation.setStartValue(collapsed_height)
            #~ animation.setEndValue(collapsed_height + content_height)

        #~ content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        #~ content_animation.setDuration(500)
        #~ content_animation.setStartValue(0)
        #~ content_animation.setEndValue(content_height)
