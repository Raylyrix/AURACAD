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

"""The BIM Clone command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP


class BIM_ResetCloneColors:

    def GetResources(self):
        return {
            "Pixmap": "BIM_ResetCloneColors",
            "MenuText": QT_TRANSLATE_NOOP("BIM_ResetCloneColors", "Reset Colors"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_ResetCloneColors",
                "Resets the colors of this object from its cloned original",
            ),
            "Accel": "D,O",
        }

    def Activated(self):
        for obj in AuraCADGui.Selection.getSelection():
            if hasattr(obj, "CloneOf") and obj.CloneOf:
                obj.ViewObject.DiffuseColor = obj.CloneOf.ViewObject.DiffuseColor


AuraCADGui.addCommand("BIM_ResetCloneColors", BIM_ResetCloneColors())
