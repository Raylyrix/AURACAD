# SPDX-License-Identifier: LGPL-2.1-or-later

import sys

# sys.path.append("")

from PySide import QtCore, QtGui
import AuraCAD, AuraCADGui
import ctypes

from ui_mainwindow import Ui_MainWindow


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        from PySide import QtNetwork

        QtNetwork.QNetworkConfigurationManager()

    @QtCore.Slot()
    def on_actionEmbed_triggered(self):
        AuraCADGui.showMainWindow()
        hwnd = self.winId()
        PyCObject_AsVoidPtr = ctypes.PYFUNCTYPE(ctypes.c_void_p, ctypes.py_object)(
            ("PyCObject_AsVoidPtr", ctypes.pythonapi)
        )
        addr = PyCObject_AsVoidPtr(hwnd)
        AuraCADGui.embedToWindow(hex(addr))

        # Need version >= 0.16.5949
        class BlankWorkbench(AuraCADGui.Workbench):
            MenuText = "Blank"
            ToolTip = "Blank workbench"

            def Initialize(self):
                return

            def GetClassName(self):
                return "Gui::BlankWorkbench"

        AuraCADGui.addWorkbench(BlankWorkbench)
        AuraCADGui.activateWorkbench("BlankWorkbench")

    @QtCore.Slot()
    def on_actionDocument_triggered(self):
        AuraCAD.newDocument()

    @QtCore.Slot()
    def on_actionCube_triggered(self):
        AuraCAD.ActiveDocument.addObject("Part::Box")
        AuraCAD.ActiveDocument.recompute()
        AuraCADGui.ActiveDocument.ActiveView.fitAll()


app = QtGui.QApplication(sys.argv)
ui = Ui_MainWindow()
mw = MainWindow()
ui.setupUi(mw)
mw.resize(1200, 800)
mw.show()
app.exec_()
