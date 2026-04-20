# ***************************************************************************
# *   Copyright (c) 2005 Werner Mayer <werner.wm.mayer@gmx.de>              *
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
# *   Werner Mayer 2005                                                     *
# ***************************************************************************/

# Menu test module

import AuraCAD, os, unittest, AuraCADGui

# ---------------------------------------------------------------------------
# define the functions to test the AuraCAD base code
# ---------------------------------------------------------------------------

# def suite():
#    suite = unittest.TestSuite()
#    suite.addTest(DocTestCase("DocumentProperties"))
#    suite.addTest(DocTestCase("DocumentLabels"))
#    suite.addTest(DocTestCase("DocumentSaveAndRestore"))
#    return suite


class MenuCreateCases(unittest.TestCase):
    def setUp(self):
        AuraCADGui.activateWorkbench("TestWorkbench")
        AuraCAD.Console.PrintLog("Setup Test menu...\n")
        list = ["Test_TestAll", "Test_TestDoc", "Test_TestBase", "Test_TestWork"]
        w = AuraCADGui.getWorkbench("TestWorkbench")
        w.appendMenu("TestMenu", list)

    def testMenu(self):
        # check menu for items
        AuraCAD.Console.PrintLog("Checking Test menu...\n")
        w = AuraCADGui.getWorkbench("TestWorkbench")
        list = w.listMenus()
        self.b = False
        for i in list:
            if i == "TestMenu":
                self.b = True
        self.assertTrue(self.b, "Test menu not found")

    def tearDown(self):
        if self.b:
            AuraCAD.Console.PrintLog("Test menu successfully added\n")
        else:
            AuraCAD.Console.PrintLog("Adding Test menu failed\n")


class MenuDeleteCases(unittest.TestCase):
    def setUp(self):
        AuraCADGui.activateWorkbench("TestWorkbench")
        AuraCAD.Console.PrintLog("Remove Test menu...\n")
        w = AuraCADGui.getWorkbench("TestWorkbench")
        w.removeMenu("TestMenu")

    def testMenu(self):
        # check menu for items
        AuraCAD.Console.PrintLog("Checking Test menu...\n")
        w = AuraCADGui.getWorkbench("TestWorkbench")
        list = w.listMenus()
        self.b = True
        for i in list:
            if i == "TestMenu":
                self.b = False
        self.assertTrue(self.b == True, "Test menu still added")

    def tearDown(self):
        if self.b:
            AuraCAD.Console.PrintLog("Test menu successfully removed\n")
        else:
            AuraCAD.Console.PrintLog("Removing Test menu failed\n")
