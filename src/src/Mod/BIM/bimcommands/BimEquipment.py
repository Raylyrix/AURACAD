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

"""BIM equipment commands"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Equipment:
    "the Arch Equipment command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Equipment",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Equipment", "Equipment"),
            "Accel": "E, Q",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Equipment", "Creates an equipment from a selected object (Part or Mesh)"
            ),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        s = AuraCADGui.Selection.getSelection()
        if not s:
            AuraCAD.Console.PrintError(
                translate("Arch", "Select a base shape object and optionally a mesh object")
            )
        else:
            base = ""
            mesh = ""
            if len(s) == 2:
                if hasattr(s[0], "Shape"):
                    base = s[0].Name
                elif s[0].isDerivedFrom("Mesh::Feature"):
                    mesh = s[0].Name
                if hasattr(s[1], "Shape"):
                    if mesh:
                        base = s[1].Name
                elif s[1].isDerivedFrom("Mesh::Feature"):
                    if base:
                        mesh = s[1].Name
            else:
                if hasattr(s[0], "Shape"):
                    base = s[0].Name
                elif s[0].isDerivedFrom("Mesh::Feature"):
                    mesh = s[0].Name
            AuraCAD.ActiveDocument.openTransaction(str(translate("Arch", "Create Equipment")))
            AuraCADGui.addModule("Arch")
            if base:
                base = "AuraCAD.ActiveDocument." + base
            AuraCADGui.doCommand("obj = Arch.makeEquipment(" + base + ")")
            if mesh:
                AuraCADGui.doCommand("obj.HiRes = AuraCAD.ActiveDocument." + mesh)
            AuraCADGui.addModule("Draft")
            AuraCADGui.doCommand("Draft.autogroup(obj)")
            AuraCAD.ActiveDocument.commitTransaction()
            AuraCAD.ActiveDocument.recompute()
            # get diffuse color info from base object
            if base and hasattr(s[0].ViewObject, "DiffuseColor"):
                AuraCADGui.doCommand(
                    "AuraCAD.ActiveDocument.Objects[-1].ViewObject.DiffuseColor = "
                    + base
                    + ".ViewObject.DiffuseColor"
                )
        return


AuraCADGui.addCommand("Arch_Equipment", Arch_Equipment())
