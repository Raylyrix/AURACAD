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

"""BIM Schedule command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Stairs:
    "the Arch Stairs command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Stairs",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Stairs", "Stairs"),
            "Accel": "S, R",
            "ToolTip": QT_TRANSLATE_NOOP("Arch_Stairs", "Creates a flight of stairs"),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        import Draft
        from draftutils import params

        AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Stairs"))
        AuraCADGui.addModule("Arch")
        sel = AuraCADGui.Selection.getSelection()
        if sel:
            n = []
            nStr = ""
            for obj in sel:
                if nStr != "":
                    nStr += ","
                nStr += "AuraCAD.ActiveDocument." + obj.Name
            #'obj' in GUI not the same as obj in script,
            # make it 'stairs' to distinguish one from another
            # Create Stairs object with steps numbers in user preference
            AuraCADGui.doCommand(
                "stairs = Arch.makeStairs(baseobj=["
                + nStr
                + "],steps="
                + str(params.get_param_arch("StairsSteps"))
                + ")"
            )
            AuraCADGui.Selection.clearSelection()
            AuraCADGui.doCommand("AuraCADGui.Selection.addSelection(stairs)")

            # ArchSketch Support
            if len(sel) == 1 and Draft.getType(obj) == "ArchSketch":
                # Get ArchSketch.FloorHeight as default and assign to Stairs
                try:
                    height = str(obj.FloorHeight.Value)  # vs obj.FloorHeight
                    # Can only use Value to assign to PropertyLength
                    AuraCADGui.doCommand("stairs.Height = " + height)
                except:
                    pass
                # If base is ArchSketch, ArchSketchObject is already loaded, no
                # need to load again : AuraCADGui.addModule("ArchSketchObject")
                try:
                    AuraCADGui.runCommand("EditStairs")
                except:
                    pass

        else:
            AuraCADGui.doCommand(
                "stairs = Arch.makeStairs(steps=" + str(params.get_param_arch("StairsSteps")) + ")"
            )
        AuraCADGui.addModule("Draft")

        # AuraCADGui.doCommand("Draft.autogroup(obj)")
        AuraCADGui.doCommand("Draft.autogroup(stairs)")

        AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()
        print(" ActiveDocument.recompute, done ")


AuraCADGui.addCommand("Arch_Stairs", Arch_Stairs())
