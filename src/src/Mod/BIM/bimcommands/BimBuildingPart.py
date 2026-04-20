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

"""The BIM Building part-related commands"""

# TODO: Refactor the Site code so it becomes a BuildingPart too


import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Level:
    """The command definition for the Arch workbench's gui tool, Arch Floor"""

    def GetResources(self):

        return {
            "Pixmap": "Arch_Floor",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Level", "Level"),
            "Accel": "L, V",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Level", "Creates a building part object that represents a level"
            ),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Level"))
        AuraCADGui.addModule("Arch")
        AuraCADGui.addModule("Draft")
        AuraCADGui.addModule("WorkingPlane")
        AuraCADGui.doCommand("obj = Arch.makeFloor(AuraCADGui.Selection.getSelection())")
        AuraCADGui.doCommand("obj.Placement = WorkingPlane.get_working_plane().get_placement()")
        AuraCADGui.doCommand("Draft.autogroup(obj)")
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()


class Arch_Building:
    "the Arch Building command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Building",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Building", "Building"),
            "Accel": "B, U",
            "ToolTip": QT_TRANSLATE_NOOP("Arch_Building", "Creates a building object"),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Building"))
        AuraCADGui.addModule("Arch")
        AuraCADGui.addModule("Draft")
        AuraCADGui.doCommand("obj = Arch.makeBuilding()")
        AuraCADGui.doCommand("Draft.autogroup(obj)")
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()


AuraCADGui.addCommand("Arch_Building", Arch_Building())
AuraCADGui.addCommand("Arch_Level", Arch_Level())
