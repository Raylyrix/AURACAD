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

"""The BIM Background command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP


class BIM_Background:

    def GetResources(self):
        return {
            "Pixmap": "BIM_Background",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Background", "Toggle Background"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_Background",
                "Toggles the 3D View background between simple and gradient",
            ),
        }

    def Activated(self):
        param = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/View")
        if param.GetBool("Simple", True):
            param.SetBool("Simple", False)
            param.SetBool("Gradient", True)
            param.SetBool("RadialGradient", False)
        elif param.GetBool("Gradient", True):
            param.SetBool("Simple", False)
            param.SetBool("Gradient", False)
            param.SetBool("RadialGradient", True)
        else:
            param.SetBool("Simple", True)
            param.SetBool("Gradient", False)
            param.SetBool("RadialGradient", False)
        AuraCADGui.updateGui()


AuraCADGui.addCommand("BIM_Background", BIM_Background())
