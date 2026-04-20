# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2017 Yorik van Havre <yorik@uncreated.net>              *
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

"""The BIM Ungroup command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP


class BIM_Ungroup:

    def GetResources(self):
        return {
            "Pixmap": "Draft_AddToGroup",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Convert", "Remove From Group"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_Convert", "Removes this object from its parent group"
            ),
        }

    def Activated(self):
        sel = AuraCADGui.Selection.getSelection()
        first = True
        if sel:
            for obj in sel:
                for parent in obj.InList:
                    if parent.isDerivedFrom("App::DocumentObjectGroup") or parent.hasExtension(
                        "App::GroupExtension"
                    ):
                        if obj in parent.Group:
                            if first:
                                AuraCAD.ActiveDocument.openTransaction("Ungroup")
                                first = False
                            if hasattr(parent, "removeObject"):
                                parent.removeObject(obj)
                            else:
                                g = parent.Group
                                g.remove(obj)
                                parent.Group = g
        if not first:
            AuraCAD.ActiveDocument.commitTransaction()
            AuraCAD.ActiveDocument.recompute()


AuraCADGui.addCommand("BIM_Ungroup", BIM_Ungroup())
