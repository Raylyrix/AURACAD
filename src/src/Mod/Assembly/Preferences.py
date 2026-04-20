# SPDX-License-Identifier: LGPL-2.1-or-later
# /**************************************************************************
#                                                                           *
#    Copyright (c) 2023 Ondsel <development@ondsel.com>                     *
#                                                                           *
#    This file is part of AuraCAD.                                          *
#                                                                           *
#    AuraCAD is free software: you can redistribute it and/or modify it     *
#    under the terms of the GNU Lesser General Public License as            *
#    published by the Free Software Foundation, either version 2.1 of the   *
#    License, or (at your option) any later version.                        *
#                                                                           *
#    AuraCAD is distributed in the hope that it will be useful, but         *
#    WITHOUT ANY WARRANTY; without even the implied warranty of             *
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU       *
#    Lesser General Public License for more details.                        *
#                                                                           *
#    You should have received a copy of the GNU Lesser General Public       *
#    License along with AuraCAD. If not, see                                *
#    <https://www.gnu.org/licenses/>.                                       *
#                                                                           *
# **************************************************************************/

import AuraCAD
import AuraCADGui

translate = AuraCAD.Qt.translate


def preferences():
    return AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Assembly")


class PreferencesPage:
    def __init__(self, parent=None):
        self.form = AuraCADGui.PySideUic.loadUi(":preferences/Assembly.ui")

    def saveSettings(self):
        pref = preferences()
        pref.SetBool("LeaveEditWithEscape", self.form.checkBoxEnableEscape.isChecked())
        pref.SetBool("LogSolverDebug", self.form.checkBoxSolverDebug.isChecked())
        pref.SetInt("GroundFirstPart", self.form.groundFirstPart.currentIndex())

    def loadSettings(self):
        pref = preferences()
        self.form.checkBoxEnableEscape.setChecked(pref.GetBool("LeaveEditWithEscape", True))
        self.form.checkBoxSolverDebug.setChecked(pref.GetBool("LogSolverDebug", False))
        self.form.groundFirstPart.clear()
        self.form.groundFirstPart.addItem(translate("Assembly", "Ask"))
        self.form.groundFirstPart.addItem(translate("Assembly", "Always"))
        self.form.groundFirstPart.addItem(translate("Assembly", "Never"))
        self.form.groundFirstPart.setCurrentIndex(pref.GetInt("GroundFirstPart", 0))
