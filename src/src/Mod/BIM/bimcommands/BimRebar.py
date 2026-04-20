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

"""BIM Rebar command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Rebar:
    "the Arch Rebar command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Rebar",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Rebar", "Custom Rebar"),
            "Accel": "R, B",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Rebar",
                "Creates a reinforcement bar from the selected face of solid object and/or a sketch",
            ),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        import ArchComponent

        sel = AuraCADGui.Selection.getSelectionEx()
        if sel:
            obj = sel[0].Object
            if hasattr(obj, "Shape") and obj.Shape.Solids:
                # this is our host object
                if len(sel) > 1:
                    sk = sel[1].Object
                    if hasattr(sk, "Shape"):
                        if len(sk.Shape.Wires) == 1:
                            # we have a structure and a wire: create the rebar now
                            AuraCAD.ActiveDocument.openTransaction(
                                translate("Arch", "Create Rebar")
                            )
                            AuraCADGui.addModule("Arch")
                            AuraCADGui.doCommand(
                                "Arch.makeRebar(AuraCAD.ActiveDocument."
                                + obj.Name
                                + ",AuraCAD.ActiveDocument."
                                + sk.Name
                                + ")"
                            )
                            AuraCAD.ActiveDocument.commitTransaction()
                            AuraCAD.ActiveDocument.recompute()
                            return
                else:
                    # we have only a structure: open the sketcher
                    AuraCADGui.activateWorkbench("SketcherWorkbench")
                    AuraCADGui.runCommand("Sketcher_NewSketch")
                    AuraCAD.ArchObserver = ArchComponent.ArchSelectionObserver(
                        obj,
                        AuraCAD.ActiveDocument.Objects[-1],
                        hide=False,
                        nextCommand="Arch_Rebar",
                    )
                    AuraCADGui.Selection.addObserver(AuraCAD.ArchObserver)
                    return
            elif hasattr(obj, "Shape"):
                if len(obj.Shape.Wires) == 1:
                    # we have only a wire: extract its support object, if available, and make the rebar
                    support = "None"
                    if hasattr(obj, "AttachmentSupport"):
                        if obj.AttachmentSupport:
                            if len(obj.AttachmentSupport) != 0:
                                support = (
                                    "AuraCAD.ActiveDocument." + obj.AttachmentSupport[0][0].Name
                                )
                    AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Rebar"))
                    AuraCADGui.addModule("Arch")
                    AuraCADGui.doCommand(
                        "Arch.makeRebar(" + support + ",AuraCAD.ActiveDocument." + obj.Name + ")"
                    )
                    AuraCAD.ActiveDocument.commitTransaction()
                    AuraCAD.ActiveDocument.recompute()
                    return

        AuraCAD.Console.PrintMessage(
            translate("Arch", "Select a base face on a structural object") + "\n"
        )
        AuraCADGui.Control.closeDialog()
        AuraCADGui.Control.showDialog(ArchComponent.SelectionTaskPanel())
        AuraCAD.ArchObserver = ArchComponent.ArchSelectionObserver(nextCommand="Arch_Rebar")
        AuraCADGui.Selection.addObserver(AuraCAD.ArchObserver)


AuraCADGui.addCommand("Arch_Rebar", Arch_Rebar())
