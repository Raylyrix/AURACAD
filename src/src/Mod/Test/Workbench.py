# ***************************************************************************
# *   Copyright (c) 2006 Werner Mayer <werner.wm.mayer@gmx.de>              *
# *                                                                         *
# *   This file is part of the AuraCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   AuraCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with AuraCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************/

# Workbench test module

import AuraCAD, AuraCADGui, os, unittest
import tempfile

from PySide import QtWidgets, QtCore
from PySide.QtWidgets import QApplication


class CallableCheckWarning:
    def __call__(self):
        diag = QApplication.activeModalWidget()
        if diag:
            QtCore.QTimer.singleShot(0, diag, QtCore.SLOT("accept()"))


class WorkbenchTestCase(unittest.TestCase):
    def setUp(self):
        self.Active = AuraCADGui.activeWorkbench()
        AuraCAD.Console.PrintLog(AuraCADGui.activeWorkbench().name())

    def testActivate(self):
        wbs = AuraCADGui.listWorkbenches()
        # this gives workbenches a possibility to detect that we're under test environment
        AuraCAD.TestEnvironment = True
        for i in wbs:
            try:
                print("Activate workbench '{}'".format(i))
                cobj = CallableCheckWarning()
                QtCore.QTimer.singleShot(500, cobj)
                if AuraCADGui.activeWorkbench().name() != i:
                    success = AuraCADGui.activateWorkbench(i)
                else:
                    # Cannot test activation of an already-active workbench
                    success = True
                AuraCAD.Console.PrintLog(
                    "Active: " + AuraCADGui.activeWorkbench().name() + " Expected: " + i + "\n"
                )
                self.assertTrue(success, "Test on activating workbench {0} failed".format(i))
            except Exception as e:
                self.fail("Loading of workbench '{0}' failed: {1}".format(i, e))
        del AuraCAD.TestEnvironment

    def testHandler(self):
        import __main__

        class UnitWorkbench(__main__.Workbench):
            MenuText = "Unittest"
            ToolTip = "Unittest"

            def Initialize(self):
                cmds = ["Test_Test"]
                self.appendToolbar("My Unittest", cmds)

            def GetClassName(self):
                return "Gui::PythonWorkbench"

        AuraCADGui.addWorkbench(UnitWorkbench())
        wbs = AuraCADGui.listWorkbenches()
        self.assertTrue("UnitWorkbench" in wbs, "Test on adding workbench handler failed")
        AuraCADGui.activateWorkbench("UnitWorkbench")
        AuraCADGui.updateGui()
        self.assertTrue(
            AuraCADGui.activeWorkbench().name() == "UnitWorkbench",
            "Test on loading workbench 'Unittest' failed",
        )
        AuraCADGui.removeWorkbench("UnitWorkbench")
        wbs = AuraCADGui.listWorkbenches()
        self.assertTrue(not "UnitWorkbench" in wbs, "Test on removing workbench handler failed")

    def testInvalidType(self):
        class MyExtWorkbench(AuraCADGui.Workbench):
            def Initialize(self):
                pass

            def GetClassName(self):
                return "App::Extension"

        AuraCADGui.addWorkbench(MyExtWorkbench())
        with self.assertRaises(TypeError):
            AuraCADGui.activateWorkbench("MyExtWorkbench")
        AuraCADGui.removeWorkbench("MyExtWorkbench")

    def tearDown(self):
        AuraCADGui.activateWorkbench(self.Active.name())
        AuraCAD.Console.PrintLog(self.Active.name())


class CommandTestCase(unittest.TestCase):
    def testPR6889(self):
        # Fixes a crash
        TempPath = tempfile.gettempdir()
        macroName = TempPath + os.sep + "testmacro.py"
        macroFile = open(macroName, "w")
        macroFile.write("print ('Hello, World!')")
        macroFile.close()

        name = AuraCADGui.Command.createCustomCommand(macroName)
        cmd = AuraCADGui.Command.get(name)
        cmd.run()


class TestNavigationStyle(unittest.TestCase):
    def setUp(self):
        self.Doc = AuraCAD.newDocument("CreateTest")

    def testInvalidStyle(self):
        AuraCADGui.getDocument(self.Doc).ActiveView.setNavigationType("App::Extension")
        self.assertNotEqual(
            AuraCADGui.getDocument(self.Doc).ActiveView.getNavigationType(), "App::Extension"
        )

    def tearDown(self):
        AuraCAD.closeDocument("CreateTest")
