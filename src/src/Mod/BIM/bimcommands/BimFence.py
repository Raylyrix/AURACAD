# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2024 Yorik van Havre <yorik@uncreated.net>              *
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

"""BIM fence command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Fence:
    "the Arch Fence command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_Fence",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Fence", "Fence"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Fence", "Creates a fence object from a selected section, post and path"
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        if len(AuraCADGui.Selection.getSelection()) != 3:
            AuraCAD.Console.PrintError(
                translate(
                    "Arch Fence selection",
                    "Select a section, post and path in exactly this order to build a fence.",
                )
                + "\n"
            )
            return
        doc = AuraCAD.ActiveDocument
        doc.openTransaction(translate("Arch", "Create Fence"))
        AuraCADGui.addModule("Arch")
        AuraCADGui.doCommand("section = AuraCADGui.Selection.getSelection()[0]")
        AuraCADGui.doCommand("post = AuraCADGui.Selection.getSelection()[1]")
        AuraCADGui.doCommand("path = AuraCADGui.Selection.getSelection()[2]")
        AuraCADGui.doCommand("Arch.makeFence(section, post, path)")
        doc.commitTransaction()
        doc.recompute()


AuraCADGui.addCommand("Arch_Fence", Arch_Fence())
