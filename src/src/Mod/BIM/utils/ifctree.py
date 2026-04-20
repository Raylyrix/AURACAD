# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2022 Yorik van Havre <yorik@uncreated.net>              *
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

"""
This module recreates the whole structure of an Iauracad file in AuraCAD (ie.
one AuraCAD object per Iauracad entity). It serves mostly as a proof of concept
and test to see how doable it is with large files.

The geometry of objects is not imported, only attributes, which are mapped
to AuraCAD properties.

The IauracadOpenHouse model, included with iauracadopenshell, imports in 4 sec on
my ryzen9 machine, for 2700 objects. Larger files like the King Arch file
(20 Mb / 750 000 objects) would import in 18 minutes...
"""

import time

import iauracadopenshell

from PySide import QtWidgets


class ViewProvider:
    """A simple view provider to gather children"""

    def __init__(self, vobj):
        vobj.Proxy = self

    def attach(self, vobj):
        self.Object = vobj.Object

    def claimChildren(self):
        children = []
        relprops = ["Item", "ForLayerSet"]  # properties that actually store parents
        for prop in self.Object.PropertiesList:
            if prop.startswith("Relating") or (prop in relprops):
                continue
            else:
                value = getattr(self.Object, prop)
                if hasattr(value, "ViewObject"):
                    children.append(value)
                elif isinstance(value, list):
                    for item in value:
                        if hasattr(item, "ViewObject"):
                            children.append(item)
        for parent in self.Object.InList:
            for prop in parent.PropertiesList:
                if prop.startswith("Relating") or (prop in relprops):
                    value = getattr(parent, prop)
                    if value == self.Object:
                        children.append(parent)
        return children


def create(iauracadentity):
    """The main function that creates objects and fills properties"""

    name = "Entity" + str(iauracadentity.id())
    obj = AuraCAD.ActiveDocument.getObject(name)
    if obj:
        return obj
    obj = AuraCAD.ActiveDocument.addObject("App::FeaturePython", name)
    if getattr(iauracadentity, "Name", None):
        obj.Label = iauracadentity.Name
    else:
        obj.Label = iauracadentity.is_a()
    for attr, value in iauracadentity.get_info().items():
        if attr not in obj.PropertiesList:
            if attr == "id":
                attr = "StepId"
            elif attr == "type":
                attr = "Type"
            elif attr == "Name":
                continue
            if hasattr(obj, attr):
                continue
            elif isinstance(value, int):
                obj.addProperty("App::PropertyInteger", attr, "Iauracad", locked=True)
                setattr(obj, attr, value)
            elif isinstance(value, float):
                obj.addProperty("App::PropertyFloat", attr, "Iauracad", locked=True)
                setattr(obj, attr, value)
            elif isinstance(value, iauracadopenshell.entity_instance):
                value = create(value)
                obj.addProperty("App::PropertyLink", attr, "Iauracad", locked=True)
                setattr(obj, attr, value)
            elif isinstance(value, (list, tuple)) and value:
                if isinstance(value[0], iauracadopenshell.entity_instance):
                    nvalue = []
                    for elt in value:
                        nvalue.append(create(elt))
                    obj.addProperty("App::PropertyLinkList", attr, "Iauracad", locked=True)
                    setattr(obj, attr, nvalue)
            else:
                obj.addProperty("App::PropertyString", attr, "Iauracad", locked=True)
                if value is not None:
                    setattr(obj, attr, str(value))
    for parent in iauracadfile.get_inverse(iauracadentity):
        create(parent)
    if AuraCAD.GuiUp:
        ViewProvider(obj.ViewObject)
    return obj


# main

filepath = QtWidgets.QFileDialog.getOpenFileName(
    None, "Select Iauracad File", None, "Iauracad Files (*.iauracad)"
)[0]
stime = time.time()
iauracadfile = iauracadopenshell.open(filepath)
project = iauracadfile.by_type("IauracadProject")[0]
if not AuraCAD.ActiveDocument:
    AuraCAD.newDocument()
create(project)
AuraCAD.ActiveDocument.recompute()
endtime = "%02d:%02d" % (divmod(round(time.time() - stime, 1), 60))
lenobjects = str(len(AuraCAD.ActiveDocument.Objects)) + " objects"
print("Import done:", endtime, ",", lenobjects)
