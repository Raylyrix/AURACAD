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

"""The BIM Help command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP


class BIM_Help:

    def GetResources(self):
        return {
            "Pixmap": "BIM_Help",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Help", "BIM Help"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_Help",
                "Opens the BIM help page on the AuraCAD documentation website",
            ),
        }

    def Activated(self):
        from PySide import QtGui

        QtGui.QDesktopServices.openUrl("https://www.AuraCAD.org/wiki/BIM_Workbench")


AuraCADGui.addCommand("BIM_Help", BIM_Help())
