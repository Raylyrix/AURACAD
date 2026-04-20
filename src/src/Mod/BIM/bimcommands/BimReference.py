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


class Arch_Reference:
    "the Arch Reference command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Reference",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Reference", "External Reference"),
            "Accel": "E, X",
            "ToolTip": QT_TRANSLATE_NOOP("Arch_Reference", "Creates an external reference object"),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        AuraCADGui.Control.closeDialog()
        AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create external reference"))
        AuraCADGui.addModule("Arch")
        AuraCADGui.addModule("Draft")
        AuraCADGui.doCommand("obj = Arch.makeReference()")
        AuraCADGui.doCommand("Draft.autogroup(obj)")
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCADGui.doCommand("obj.ViewObject.Document.setEdit(obj.ViewObject, 0)")


AuraCADGui.addCommand("Arch_Reference", Arch_Reference())
