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


class Arch_Site:
    "the Arch Site command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Site",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Site", "Site"),
            "Accel": "S, I",
            "ToolTip": QT_TRANSLATE_NOOP("Arch_Site", "Creates a site including selected objects"),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Site"))
        AuraCADGui.addModule("Arch")
        AuraCADGui.addModule("Draft")
        AuraCADGui.doCommand("obj = Arch.makeSite()")
        AuraCADGui.doCommand("Draft.autogroup(obj)")
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()


AuraCADGui.addCommand("Arch_Site", Arch_Site())
