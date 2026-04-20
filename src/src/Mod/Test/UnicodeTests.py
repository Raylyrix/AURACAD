# ***************************************************************************
# *   Copyright (c) 2007 Juergen Riegel <juergen.riegel@web.de>             *
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

# Open and edit only in UTF-8 !!!!!!

import AuraCAD, os, unittest, tempfile

# ---------------------------------------------------------------------------
# define the functions to test the AuraCAD Document code
# ---------------------------------------------------------------------------


class UnicodeBasicCases(unittest.TestCase):
    def setUp(self):
        self.Doc = AuraCAD.newDocument("CreateTest")

    def testUnicodeLabel(self):
        L1 = self.Doc.addObject("App::FeatureTest", "Label_1")
        L1.Label = "à¤¹à¤¿à¤¨à¥à¤¦à¥€"
        self.assertTrue(L1.Label == "à¤¹à¤¿à¤¨à¥à¤¦à¥€")

    def tearDown(self):
        # closing doc
        AuraCAD.closeDocument("CreateTest")


class DocumentSaveRestoreCases(unittest.TestCase):
    def setUp(self):
        self.Doc = AuraCAD.newDocument("SaveRestoreTests")
        L1 = self.Doc.addObject("App::FeatureTest", "Label_1")
        L1.Label = "à¤¹à¤¿à¤¨à¥à¤¦à¥€"
        self.TempPath = tempfile.gettempdir()
        AuraCAD.Console.PrintLog("  Using temp path: " + self.TempPath + "\n")

    def testSaveAndRestore(self):
        # saving and restoring
        SaveName = self.TempPath + os.sep + "UnicodeTest.auracadStd"
        self.Doc.saveAs(SaveName)
        AuraCAD.closeDocument("SaveRestoreTests")
        self.Doc = AuraCAD.open(SaveName)
        self.assertTrue(self.Doc.Label_1.Label == "à¤¹à¤¿à¤¨à¥à¤¦à¥€")
        AuraCAD.closeDocument("UnicodeTest")
        AuraCAD.newDocument("SaveRestoreTests")

    def tearDown(self):
        # closing doc
        AuraCAD.closeDocument("SaveRestoreTests")
