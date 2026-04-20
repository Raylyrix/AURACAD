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
import DraftTools

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP


class BIM_Clone(DraftTools.Draft_Clone):

    def __init__(self):
        DraftTools.Draft_Clone.__init__(self)
        self.moveAfterCloning = True

    def GetResources(self):
        return {
            "Pixmap": "BIM_Clone",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Clone", "Clone"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_Clone", "Clones selected objects to another location"
            ),
            "Accel": "C,L",
        }


AuraCADGui.addCommand("BIM_Clone", BIM_Clone())
