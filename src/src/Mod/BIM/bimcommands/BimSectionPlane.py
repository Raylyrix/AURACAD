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


class Arch_SectionPlane:
    "the Arch SectionPlane command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_SectionPlane",
            "Accel": "S, E",
            "MenuText": QT_TRANSLATE_NOOP("Arch_SectionPlane", "Section Plane"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_SectionPlane",
                "Creates a section plane object, including the selected objects",
            ),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        sel = AuraCADGui.Selection.getSelection()
        ss = "["
        for o in sel:
            if len(ss) > 1:
                ss += ","
            ss += "AuraCAD.ActiveDocument." + o.Name
        ss += "]"
        AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Section Plane"))
        AuraCADGui.addModule("Arch")
        AuraCADGui.doCommand("section = Arch.makeSectionPlane(" + ss + ")")
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()
        if len(sel) == 1 and getattr(sel[0], "IauracadClass", None) == "IauracadProject":
            # remove the Iauracad project, otherwise we can't aggregate (circular loop)
            AuraCADGui.doCommand("section.Objects = []")
            # AuraCADGui.addModule("nativeiauracad.iAuraCAD_tools")
            # p = "AuraCAD.ActiveDocument."+sel[0].Name
            # AuraCADGui.doCommand("nativeiauracad.iAuraCAD_tools.aggregate(section,"+p+")")


AuraCADGui.addCommand("Arch_SectionPlane", Arch_SectionPlane())
