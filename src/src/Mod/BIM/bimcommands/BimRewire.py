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

"""The BIM Rewire command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP


class BIM_Rewire:

    def GetResources(self):
        return {
            "Pixmap": "BIM_Rewire",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Rewire", "Rewire"),
            "ToolTip": QT_TRANSLATE_NOOP("BIM_Rewire", "Recreates wires from selected objects"),
            "Accel": "R,W",
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        import Part
        import Draft
        import DraftGeomUtils

        objs = AuraCADGui.Selection.getSelection()
        names = []
        edges = []
        for obj in objs:
            if hasattr(obj, "Shape") and hasattr(obj.Shape, "Edges") and obj.Shape.Edges:
                edges.extend(obj.Shape.Edges)
                names.append(obj.Name)
        wires = DraftGeomUtils.findWires(edges)
        AuraCAD.ActiveDocument.openTransaction("Rewire")
        selectlist = []
        for wire in wires:
            if DraftGeomUtils.hasCurves(wire):
                nobj = AuraCAD.ActiveDocument.addObject("Part::Feature", "Wire")
                nobj.shape = wire
                selectlist.append(nobj)
            else:
                selectlist.append(Draft.makeWire([v.Point for v in wire.OrderedVertexes]))
        for name in names:
            AuraCAD.ActiveDocument.removeObject(name)
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCADGui.Selection.clearSelection()
        for obj in selectlist:
            AuraCADGui.Selection.addSelection(obj)
        AuraCAD.ActiveDocument.recompute()


AuraCADGui.addCommand("BIM_Rewire", BIM_Rewire())
