# SPDX-License-Identifier: LGPL-2.1-or-later

import sys
from PySide2 import QtWidgets
import AuraCADGui


class MainWindow(QtWidgets.QMainWindow):
    def showEvent(self, event):
        AuraCADGui.showMainWindow()
        self.setCentralWidget(AuraCADGui.getMainWindow())


app = QtWidgets.QApplication(sys.argv)
mw = MainWindow()
mw.resize(1200, 800)
mw.show()

# must be done a few times to update the GUI
app.processEvents()
app.processEvents()
app.processEvents()

import Part

cube = Part.makeBox(2, 2, 2)
# creates a document and a Part feature with the cube
Part.show(cube)
app.processEvents()
app.processEvents()
