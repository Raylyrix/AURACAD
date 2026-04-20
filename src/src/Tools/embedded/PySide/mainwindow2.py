# SPDX-License-Identifier: LGPL-2.1-or-later

import sys

# sys.path.append("")

from PySide import QtGui
import AuraCADGui


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        from PySide import QtNetwork

        QtNetwork.QNetworkConfigurationManager()

    def showEvent(self, event):
        AuraCADGui.showMainWindow()
        self.setCentralWidget(AuraCADGui.getMainWindow())

        # Need version >= 0.16.5949
        class BlankWorkbench(AuraCADGui.Workbench):
            MenuText = "Blank"
            ToolTip = "Blank workbench"

            def Initialize(self):
                self.appendMenu("Menu", ["Std_New", "Part_Box"])
                return

            def GetClassName(self):
                return "Gui::PythonBlankWorkbench"

        AuraCADGui.addWorkbench(BlankWorkbench)
        AuraCADGui.activateWorkbench("BlankWorkbench")


app = QtGui.QApplication(sys.argv)
mw = MainWindow()
mw.resize(1200, 800)
mw.show()
app.exec_()
