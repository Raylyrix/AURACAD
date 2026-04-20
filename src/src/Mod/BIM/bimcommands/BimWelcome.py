# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2017 Yorik van Havre <yorik@uncreated.net>              *
# *                                                                         *
# *   This file is part of AuraCAD.                                         *
# *                                                                         *
# *   AuraCAD is free software: you can redistribute it and/or modify it    *
# *   under the terms of the GNU Lesser General Public License as           *
# *   published by the Free Software Foundation, either version 2.1 of the  *
# *   License, or (at your option) any later version.                       *
# *                                                                         *
# *   AuraCAD is distributed in the hope that it will be useful, but        *
# *   WITHOUT ANY WARRANTY; without even the implied warranty of            *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      *
# *   Lesser General Public License for more details.                       *
# *                                                                         *
# *   You should have received a copy of the GNU Lesser General Public      *
# *   License along with AuraCAD. If not, see                               *
# *   <https://www.gnu.org/licenses/>.                                      *
# *                                                                         *
# ***************************************************************************

"""This module contains AuraCAD commands for the BIM workbench"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class BIM_Welcome:
    def GetResources(self):
        return {
            "Pixmap": "BIM_Welcome.svg",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Welcome", "BIM Welcome Screen"),
            "ToolTip": QT_TRANSLATE_NOOP("BIM_Welcome", "Shows the BIM workbench welcome screen"),
        }

    def Activated(self):
        self.form = AuraCADGui.PySideUic.loadUi(":ui/dialogWelcome.ui")

        # handle the tutorial links
        self.form.label_4.linkActivated.connect(self.handleLink)
        self.form.label_7.linkActivated.connect(self.handleLink)

        self.form.adjustSize()

        # center the dialog over AuraCAD window
        mw = AuraCADGui.getMainWindow()
        self.form.move(
            mw.frameGeometry().topLeft() + mw.rect().center() - self.form.rect().center()
        )

        # show dialog and run setup dialog afterwards if OK was pressed
        result = self.form.exec_()
        if result:
            AuraCADGui.runCommand("BIM_Setup")

        # remove first time flag
        PARAMS.SetBool("FirstTime", False)

    def handleLink(self, link):
        from PySide import QtCore, QtGui

        if hasattr(self, "form"):
            self.form.hide()
            if "BIM_Start_Tutorial" in link:
                AuraCADGui.runCommand("BIM_Tutorial")
            else:
                # print("Opening link:",link)
                url = QtCore.QUrl(link)
                QtGui.QDesktopServices.openUrl(url)


AuraCADGui.addCommand("BIM_Welcome", BIM_Welcome())
