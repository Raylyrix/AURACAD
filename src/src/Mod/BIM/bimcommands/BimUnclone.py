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

"""The BIM UnClone command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate


class BIM_Unclone:

    def GetResources(self):
        return {
            "Pixmap": "BIM_Unclone",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Unclone", "Unclone"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_Unclone",
                "Creates a selected clone object independent from its original",
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        import Arch
        import Draft

        # get selected object and face
        sel = AuraCADGui.Selection.getSelection()

        if len(sel) == 1:
            # make this undoable
            AuraCAD.ActiveDocument.openTransaction("Reextrude")
            obj = sel[0]

            # check that types are identical
            if hasattr(obj, "CloneOf") and obj.CloneOf:
                cloned = obj.CloneOf
                placement = AuraCAD.Placement(obj.Placement)
                if Draft.getType(obj) != Draft.getType(cloned):
                    # wrong type - we need to create a new object
                    newobj = getattr(Arch, "make" + Draft.getType(cloned))()
                else:
                    newobj = obj
                    newobj.CloneOf = None
                    if hasattr(newobj, "ViewObject") and newobj.ViewObject:
                        newobj.ViewObject.signalChangeIcon()

                # copy properties over, except special ones
                for prop in cloned.PropertiesList:
                    if not prop in [
                        "Objects",
                        "CloneOf",
                        "ExpressionEngine",
                        "HorizontalArea",
                        "Area",
                        "VerticalArea",
                        "PerimeterLength",
                        "Placement",
                        "Proxy",
                        "Shape",
                    ]:
                        setattr(newobj, prop, getattr(cloned, prop))
                newobj.Placement = placement
                AuraCAD.ActiveDocument.recompute()

                # update/reset view properties too? no i think...
                # for prop in cloned.ViewObject.PropertiesList:
                #    if not prop in ["Proxy"]:
                #        setattr(newobj.ViewObject,prop,getattr(cloned.ViewObject,prop))

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
                        elif isinstance(getattr(parent, prop), list) and (
                            obj in getattr(parent, prop)
                        ):
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
                        # TODO treat PropertyLinkSub / PropertyLinkSubList DANGEROUS - toponaming

                # remove old object if needed, and relabel new object
                if newobj != obj:
                    name = obj.Name
                    label = obj.Label

                    AuraCAD.ActiveDocument.removeObject(name)
                    newobj.Label = label

                # commit changes
                AuraCAD.ActiveDocument.commitTransaction()
                AuraCAD.ActiveDocument.recompute()

            elif Draft.getType(obj) == "Clone":
                AuraCAD.Console.PrintError(
                    translate("BIM", "Draft clones are not supported yet!") + "\n"
                )
            else:
                AuraCAD.Console.PrintError(
                    translate("BIM", "The selected object is not a clone") + "\n"
                )
        else:
            AuraCAD.Console.PrintError(translate("BIM", "Select exactly one object") + "\n")


AuraCADGui.addCommand("BIM_Unclone", BIM_Unclone())
