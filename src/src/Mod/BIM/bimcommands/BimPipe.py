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

"""BIM Panel-related Arch_"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Pipe:
    "the Arch Pipe command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Pipe",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Pipe", "Pipe"),
            "Accel": "P, I",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Pipe", "Creates a pipe object from a given wire or line"
            ),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        s = AuraCADGui.Selection.getSelection()
        if s:
            for obj in s:
                if hasattr(obj, "Shape"):
                    if len(obj.Shape.Wires) == 1:
                        AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Pipe"))
                        AuraCADGui.addModule("Arch")
                        AuraCADGui.addModule("Draft")
                        AuraCADGui.doCommand(
                            "obj = Arch.makePipe(AuraCAD.ActiveDocument." + obj.Name + ")"
                        )
                        AuraCADGui.doCommand("Draft.autogroup(obj)")
                        AuraCAD.ActiveDocument.commitTransaction()
        else:
            AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Pipe"))
            AuraCADGui.addModule("Arch")
            AuraCADGui.addModule("Draft")
            AuraCADGui.doCommand("obj = Arch.makePipe()")
            AuraCADGui.doCommand("Draft.autogroup(obj)")
            AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()


class Arch_PipeConnector:
    "the Arch Pipe command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_PipeConnector",
            "MenuText": QT_TRANSLATE_NOOP("Arch_PipeConnector", "Connector"),
            "Accel": "P, C",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_PipeConnector", "Creates a connector between 2 or 3 selected pipes"
            ),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        import Draft

        s = AuraCADGui.Selection.getSelection()
        if not (len(s) in [2, 3]):
            AuraCAD.Console.PrintError(
                translate("Arch", "Select exactly 2 or 3 pipe objects") + "\n"
            )
            return
        o = "["
        for obj in s:
            if Draft.getType(obj) != "Pipe":
                AuraCAD.Console.PrintError(translate("Arch", "Select only pipe objects") + "\n")
                return
            o += "AuraCAD.ActiveDocument." + obj.Name + ","
        o += "]"
        AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Connector"))
        AuraCADGui.addModule("Arch")
        AuraCADGui.addModule("Draft")
        AuraCADGui.doCommand("obj = Arch.makePipeConnector(" + o + ")")
        AuraCADGui.doCommand("Draft.autogroup(obj)")
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()


class Arch_PipeGroupCommand:

    def GetCommands(self):
        return tuple(["Arch_Pipe", "Arch_PipeConnector"])

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("Arch_PipeTools", "Pipe Tools"),
            "ToolTip": QT_TRANSLATE_NOOP("Arch_PipeTools", "Pipe tools"),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v


AuraCADGui.addCommand("Arch_Pipe", Arch_Pipe())
AuraCADGui.addCommand("Arch_PipeConnector", Arch_PipeConnector())
AuraCADGui.addCommand("Arch_PipeTools", Arch_PipeGroupCommand())
