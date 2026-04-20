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

"""This module contains AuraCAD commands for the BIM workbench"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate


class BIM_Reextrude:
    def GetResources(self):
        return {
            "Pixmap": "BIM_Reextrude",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Reextrude", "Re-Extrude"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_Reextrude", "Recreates an extruded structure from a selected face"
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        import Draft
        import Part
        import Arch

        # get selected object and face
        sel = AuraCADGui.Selection.getSelectionEx()

        if (
            (len(sel) == 1)
            and (len(sel[0].SubObjects) == 1)
            and ("Face" in sel[0].SubElementNames[0])
        ):
            sel = sel[0]
            obj = sel.Object
            name = obj.Name
            label = obj.Label

            fac = sel.SubObjects[0]

            # make this undoable
            AuraCAD.ActiveDocument.openTransaction("Reextrude")

            # check if the face has holes or any of the edges is not a line
            wirable = True
            if len(fac.Wires) > 1:
                wirable = False
            else:
                for edge in fac.Edges:
                    if not isinstance(edge, (Part.Line, Part.LineSegment)):
                        # edge can be a spline, but even so be straight. Simple check if tangents are identical at first and last verts...
                        if (
                            edge.tangentAt(edge.FirstParameter).getAngle(
                                edge.tangentAt(edge.LastParameter)
                            )
                            > 0.0001
                        ):
                            wirable = False
                            break
            if wirable:
                # recompose the base wire
                verts = [v.Point for v in fac.Wires[0].OrderedVertexes]
                wir = Draft.makeWire(verts, closed=True)
            else:
                # there are curves. Unable to make a wire. We just use the base face
                wir = AuraCAD.ActiveDocument.addObject("Part::Feature", "Face")
                wir.Shape = fac

            # make the new object
            if Draft.getType(obj) == "Wall":
                newobj = Arch.makeWall(wir)
            elif Draft.getType(obj) == "Panel":
                newobj = Arch.makePanel(wir)
            else:
                newobj = Arch.makeStructure(wir)

            # deduce the normal and extrusion size
            norm = fac.normalAt(0, 0).negative()
            newobj.Normal = norm
            for e in obj.Shape.Edges:
                if abs(e.tangentAt(0).getAngle(norm)) < 0.0001:
                    if hasattr(newobj, "Thickness"):
                        newobj.Thickness = e.Length
                    else:
                        newobj.Height = e.Length

            # set material
            if hasattr(obj, "Material") and obj.Material:
                newobj.Material = obj.Material

            # set role and class
            if hasattr(obj, "IauracadType"):
                newobj.IauracadType = obj.IauracadType
            elif hasattr(obj, "IauracadRole"):
                newobj.IauracadRole = obj.IauracadRole
            if hasattr(obj, "StandardCode"):
                newobj.StandardCode = obj.StandardCode

            # update objects relating to this one
            for parent in obj.InList:
                for prop in parent.PropertiesList:
                    if getattr(parent, prop) == obj:
                        setattr(parent, prop, newobj)
                        AuraCAD.Console.PrintMessage(
                            "Object "
                            + parent.Label
                            + "'s reference to this object has been updated\n"
                        )
                    elif isinstance(getattr(parent, prop), list) and (obj in getattr(parent, prop)):
                        if (prop == "Group") and hasattr(parent, "addObject"):
                            parent.addObject(newobj)
                        else:
                            g = getattr(parent, prop)
                            g.append(newobj)
                            setattr(parent, prop, g)
                        AuraCAD.Console.PrintMessage(
                            "Object "
                            + parent.Label
                            + "'s reference to this object has been updated\n"
                        )
                    # TODO treat PropertyLinkSub / PropertyLinkSubList

            # delete original object
            AuraCAD.ActiveDocument.removeObject(name)
            newobj.Label = label

            # commit changes
            AuraCAD.ActiveDocument.commitTransaction()
            AuraCAD.ActiveDocument.recompute()

        else:
            AuraCAD.Console.PrintError(
                translate("BIM", "Error: Select exactly one base face") + "\n"
            )


AuraCADGui.addCommand("BIM_Reextrude", BIM_Reextrude())
