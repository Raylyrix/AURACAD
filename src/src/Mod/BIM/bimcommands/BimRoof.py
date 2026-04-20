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

"""BIM Roof command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Roof:
    """the Arch Roof command definition"""

    def GetResources(self):
        return {
            "Pixmap": "Arch_Roof",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Roof", "Roof"),
            "Accel": "R, F",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Roof", "Creates a roof object from the selected wire."
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        import ArchComponent

        sel = AuraCADGui.Selection.getSelectionEx()
        if sel:
            sel = sel[0]
            obj = sel.Object
            AuraCADGui.Control.closeDialog()
            if sel.HasSubObjects:
                if "Face" in sel.SubElementNames[0]:
                    i = int(sel.SubElementNames[0][4:])
                    AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Roof"))
                    AuraCADGui.addModule("Arch")
                    AuraCADGui.doCommand(
                        "obj = Arch.makeRoof(AuraCAD.ActiveDocument."
                        + obj.Name
                        + ","
                        + str(i)
                        + ")"
                    )
                    AuraCADGui.addModule("Draft")
                    AuraCADGui.doCommand("Draft.autogroup(obj)")
                    AuraCAD.ActiveDocument.commitTransaction()
                    AuraCAD.ActiveDocument.recompute()
                    return
            if hasattr(obj, "Shape"):
                if obj.Shape.Wires:
                    AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Roof"))
                    AuraCADGui.addModule("Arch")
                    AuraCADGui.doCommand(
                        "obj = Arch.makeRoof(AuraCAD.ActiveDocument." + obj.Name + ")"
                    )
                    AuraCADGui.addModule("Draft")
                    AuraCADGui.doCommand("Draft.autogroup(obj)")
                    AuraCAD.ActiveDocument.commitTransaction()
                    AuraCAD.ActiveDocument.recompute()
                    return
            else:
                AuraCAD.Console.PrintMessage(translate("Arch", "Unable to create a roof"))
        else:
            AuraCAD.Console.PrintMessage(translate("Arch", "Please select a base object") + "\n")
            AuraCADGui.Control.showDialog(ArchComponent.SelectionTaskPanel())
            AuraCAD.ArchObserver = ArchComponent.ArchSelectionObserver(nextCommand="Arch_Roof")
            AuraCADGui.Selection.addObserver(AuraCAD.ArchObserver)


AuraCADGui.addCommand("Arch_Roof", Arch_Roof())
