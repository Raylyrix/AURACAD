# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2020 Werner Mayer <wmayer[at]users.sourceforge.net>     *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__title__ = "BasicShapes.CommandShapes"
__author__ = "Werner Mayer"
__url__ = "https://www.AuraCAD.org"
__doc__ = "Basic shapes"


import AuraCAD
from AuraCAD import Qt
import AuraCADGui

import Part
from . import Shapes
from . import ViewProviderShapes
import math
import sys


class CommandTube:
    """Command for creating Tube."""

    def GetResources(self):
        return {
            "MenuText": Qt.QT_TRANSLATE_NOOP("Part_Tube", "Tube"),
            "Accel": "",
            "CmdType": "AlterDoc:Alter3DView:AlterSelection",
            "Pixmap": "Part_Tube_Parametric",
            "ToolTip": Qt.QT_TRANSLATE_NOOP("Part_Tube", "Creates a tube"),
        }

    def Activated(self):
        text = AuraCAD.Qt.translate("QObject", "Create tube")
        AuraCAD.ActiveDocument.openTransaction(text)
        tube = AuraCAD.ActiveDocument.addObject("Part::FeaturePython", "Tube")
        Shapes.TubeFeature(tube)
        vp = ViewProviderShapes.ViewProviderTube(tube.ViewObject)
        activePart = AuraCADGui.activeView().getActiveObject("part")
        if activePart:
            activePart.addObject(tube)
        AuraCAD.ActiveDocument.recompute()
        vp.startDefaultEditMode(tube.ViewObject)

    def IsActive(self):
        return not AuraCAD.ActiveDocument is None


AuraCADGui.addCommand("Part_Tube", CommandTube())
