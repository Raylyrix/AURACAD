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

"""This module contains Iauracad object definitions"""

import AuraCAD
import AuraCADGui

translate = AuraCAD.Qt.translate


# the property groups below should not be treated as psets
NON_PSETS = [
    "Base",
    "Iauracad",
    "",
    "Geometry",
    "Dimension",
    "Linear/radial dimension",
    "SectionPlane",
    "Axis",
    "PhysicalProperties",
    "BuildingPart",
    "Iauracad Attributes",
]


class iAuraCAD_object:
    """Base class for all Iauracad-based objects"""

    def __init__(self, otype=None):
        self.cached = True  # this marks that the object is freshly created and its shape should be taken from cache
        self.virgin_placement = True  # this allows one to set the initial placement without triggering any placement change
        if otype:
            self.Type = otype[0].upper() + otype[1:]  # capitalize to match Draft standard
        else:
            self.Type = "IauracadObject"

    def onBeforeChange(self, obj, prop):
        if prop == "Schema":
            self.old_schema = obj.Schema
        elif prop == "Placement":
            self.old_placement = obj.Placement

    def onChanged(self, obj, prop):
        # link class property to its hidder IauracadClass counterpart
        if prop == "IauracadClass" and hasattr(obj, "Class") and obj.Class != obj.IauracadClass:
            obj.Class = obj.IauracadClass
            self.rebuild_classlist(obj, setprops=True)
        elif prop == "Class" and hasattr(obj, "IauracadClass") and obj.Class != obj.IauracadClass:
            obj.IauracadClass = obj.Class
            self.rebuild_classlist(obj, setprops=True)
        elif prop == "Schema":
            self.edit_schema(obj, obj.Schema)
        elif prop == "Type":
            self.edit_type(obj)
            self.assign_classification(obj)
        elif prop == "Classification":
            self.edit_classification(obj)
        elif prop == "Group":
            self.edit_group(obj)
        elif hasattr(obj, prop) and obj.getGroupOfProperty(prop) == "Iauracad":
            if prop not in ["StepId"]:
                self.edit_attribute(obj, prop)
        elif prop == "Label":
            self.edit_attribute(obj, "Name", obj.Label)
        elif prop == "Text":
            self.edit_annotation(obj, "Text", "\n".join(obj.Text))
        elif prop in ["Start", "End"]:
            self.edit_annotation(obj, prop)
        elif prop in ["DisplayLength", "DisplayHeight", "Depth"]:
            self.edit_annotation(obj, prop)
        elif prop == "Placement":
            if getattr(self, "virgin_placement", False):
                self.virgin_placement = False
            elif obj.Placement != getattr(self, "old_placement", None):
                # print("placement changed for",obj.Label,"to",obj.Placement)
                self.edit_placement(obj)
        elif prop == "Modified":
            if obj.ViewObject:
                obj.ViewObject.signalChangeIcon()
        elif hasattr(obj, prop) and obj.getGroupOfProperty(prop) == "Geometry":
            self.edit_geometry(obj, prop)
        elif hasattr(obj, prop) and obj.getGroupOfProperty(prop) == "Quantities":
            self.edit_quantity(obj, prop)
        elif hasattr(obj, prop) and obj.getGroupOfProperty(prop) not in NON_PSETS:
            # Treat all property groups outside the default ones as Psets
            # print("DEBUG: editinog pset prop",prop)
            self.edit_pset(obj, prop)

    def onDocumentRestored(self, obj):
        self.rebuild_classlist(obj)
        if hasattr(obj, "IauracadFilePath"):
            # once we have loaded the project, recalculate child coin nodes
            from PySide import QtCore  # lazy loading

            if obj.OutListRecursive:
                for child in obj.OutListRecursive:
                    if getattr(child, "ShapeMode", None) == "Coin":
                        child.Proxy.cached = True
                        child.touch()
            else:
                obj.Proxy.cached = True
                QtCore.QTimer.singleShot(100, obj.touch)
            QtCore.QTimer.singleShot(100, obj.Document.recompute)
            QtCore.QTimer.singleShot(100, self.fit_all)

    def assign_classification(self, obj):
        """
        Assigns Classification to an Iauracad object in a case where
        the object references a Type that has a Classification property,
        so we move copy the Type's property to our actual object.
        """

        if not getattr(obj, "Type", None):
            return

        type_obj = obj.Type
        if getattr(type_obj, "Classification", None):
            # Check if there is Classification already, since user can just change
            # the Iauracad type, but there could be one previously assigned which had
            # Classification
            if getattr(obj, "Classification", None) is None:
                obj.addProperty("App::PropertyString", "Classification", "Iauracad")
            obj.Classification = type_obj.Classification
            obj.recompute()
        elif getattr(obj, "Classification", None):
            # This means user has assigned type that has no classification, so clear
            # the one that they have currently selected
            obj.Classification = ""
            obj.recompute()

    def fit_all(self):
        """Fits the view"""

        if AuraCAD.GuiUp:
            AuraCADGui.SendMsgToActiveView("ViewFit")

    def rebuild_classlist(self, obj, setprops=False):
        """rebuilds the list of Class enum property according to current class"""

        from . import iAuraCAD_tools  # lazy import

        obj.Class = [obj.IauracadClass]
        obj.Class = iAuraCAD_tools.get_iAuraCAD_classes(obj, obj.IauracadClass)
        obj.Class = obj.IauracadClass
        if setprops:
            iAuraCAD_tools.remove_unused_properties(obj)
            iAuraCAD_tools.add_properties(obj)

    def __getstate__(self):
        return getattr(self, "Type", None)

    def __setstate__(self, state):
        self.loads(state)

    def dumps(self):
        return getattr(self, "Type", None)

    def loads(self, state):
        if state:
            self.Type = state

    def execute(self, obj):
        from . import iAuraCAD_generator  # lazy import

        if obj.isDerivedFrom("Part::Feature"):
            cached = getattr(self, "cached", False)
            iAuraCAD_generator.generate_geometry(obj, cached=cached)
            self.cached = False
            self.rebuild_classlist(obj)

    def addObject(self, obj, child):
        if child not in obj.Group:
            g = obj.Group
            g.append(child)
            obj.Group = g

    def removeObject(self, obj, child):
        if child in obj.Group:
            g = obj.Group
            g.remove(child)
            obj.Group = g

    def edit_attribute(self, obj, attribute, value=None):
        """Edits an attribute of an underlying Iauracad object"""

        from . import iAuraCAD_tools  # lazy import

        if not value:
            value = obj.getPropertyByName(attribute)
        iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
        elt = iAuraCAD_tools.get_iAuraCAD_element(obj, iauracadfile)
        if elt:
            result = iAuraCAD_tools.set_attribute(iauracadfile, elt, attribute, value)
            if result:
                if hasattr(result, "id") and (result.id() != obj.StepId):
                    obj.StepId = result.id()

    def edit_annotation(self, obj, attribute, value=None):
        """Edits an attribute of an underlying Iauracad annotation"""

        from . import iAuraCAD_tools  # lazy import
        from . import iAuraCAD_export

        if not value:
            if hasattr(obj, attribute):
                value = obj.getPropertyByName(attribute)
        iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
        elt = iAuraCAD_tools.get_iAuraCAD_element(obj, iauracadfile)
        if elt:
            if attribute == "Text":
                text = iAuraCAD_export.get_text(elt)
                if text:
                    iAuraCAD_tools.set_attribute(iauracadfile, text, "Literal", value)
            elif attribute in ["Start", "End"]:
                dim = iAuraCAD_export.get_dimension(elt)
                if dim:
                    rep = dim[0]
                    for curve in rep.Items:
                        if not hasattr(curve, "Elements"):
                            # this is a TextLiteral for the dimension text - skip it
                            continue
                        for sub in curve.Elements:
                            if sub.is_a("IauracadIndexedPolyCurve"):
                                points = sub.Points
                                value = list(points.CoordList)
                                is2d = "2D" in points.is_a()
                                if attribute == "Start":
                                    value[0] = iAuraCAD_export.get_scaled_point(obj.Start, iauracadfile, is2d)
                                else:
                                    value[-1] = iAuraCAD_export.get_scaled_point(obj.End, iauracadfile, is2d)
                                iAuraCAD_tools.set_attribute(iauracadfile, points, "CoordList", value)
                            else:
                                print("DEBUG: unknown dimension curve type:", sub)
            elif attribute in ["DisplayLength", "DisplayHeight", "Depth"]:
                l = w = h = 1000.0
                if obj.ViewObject:
                    if obj.ViewObject.DisplayLength.Value:
                        l = iAuraCAD_export.get_scaled_value(obj.ViewObject.DisplayLength.Value, iauracadfile)
                    if obj.ViewObject.DisplayHeight.Value:
                        w = iAuraCAD_export.get_scaled_value(obj.ViewObject.DisplayHeight.Value, iauracadfile)
                if obj.Depth.Value:
                    h = iAuraCAD_export.get_scaled_value(obj.Depth.Value, iauracadfile)
                if elt.Representation.Representations:
                    for rep in elt.Representation.Representations:
                        for item in rep.Items:
                            if item.is_a("IauracadCsgSolid"):
                                if item.TreeRootExpression.is_a("IauracadBlock"):
                                    block = item.TreeRootExpression
                                    loc = block.Position.Location
                                    iAuraCAD_tools.set_attribute(iauracadfile, block, "XLength", l)
                                    iAuraCAD_tools.set_attribute(iauracadfile, block, "YLength", w)
                                    iAuraCAD_tools.set_attribute(iauracadfile, block, "ZLength", h)
                                    iAuraCAD_tools.set_attribute(
                                        iauracadfile, loc, "Coordinates", (-l / 2, -h / 2, -h)
                                    )

    def edit_geometry(self, obj, prop):
        """Edits a geometry property of an object"""

        from . import iAuraCAD_geometry  # lazy loading
        from . import iAuraCAD_tools  # lazy import

        result = iAuraCAD_geometry.set_geom_property(obj, prop)
        if result:
            obj.touch()

    def edit_schema(self, obj, schema):
        """Changes the schema of an Iauracad document"""

        from . import iAuraCAD_tools  # lazy import

        iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
        if not iauracadfile:
            return
        if not getattr(self, "old_schema", None):
            return
        if schema != iauracadfile.wrapped_data.schema_name():
            # set obj.Proxy.silent = True to disable the schema change warning
            if obj.ViewObject and not getattr(self, "silent", False):
                if not obj.ViewObject.Proxy.schema_warning():
                    return
            iauracadfile, migration_table = iAuraCAD_tools.migrate_schema(iauracadfile, schema)
            self.iauracadfile = iauracadfile
            for old_id, new_id in migration_table.items():
                child = [o for o in obj.OutListRecursive if getattr(o, "StepId", None) == old_id]
                if len(child) == 1:
                    child[0].StepId = new_id

    def edit_placement(self, obj):
        """Syncs the internal Iauracad placement"""

        from . import iAuraCAD_tools  # lazy import

        iAuraCAD_tools.set_placement(obj)

    def edit_pset(self, obj, prop):
        """Edits a Pset value"""

        from . import iAuraCAD_psets  # lazy import

        iAuraCAD_psets.edit_pset(obj, prop)

    def edit_group(self, obj):
        """Edits the children list"""

        from . import iAuraCAD_tools  # lazy import
        from . import iAuraCAD_layers

        if obj.Class in [
            "IauracadPresentationLayerAssignment",
            "IauracadPresentationLayerWithStyle",
        ]:
            iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
            if not iauracadfile:
                return
            newlist = []
            for child in obj.Group:
                if not getattr(child, "StepId", None) or iAuraCAD_tools.get_iauracadfile(child) != iauracadfile:
                    print(
                        "DEBUG: Not an Iauracad object. Removing",
                        child.Label,
                        "from layer",
                        obj.Label,
                    )
                else:
                    # print("DEBUG: adding", child.Label, "to layer", obj.Label)
                    newlist.append(child)
                    iAuraCAD_layers.add_to_layer(child, obj)
            if newlist != obj.Group:
                obj.Group = newlist

    def edit_type(self, obj):
        """Edits the type of this object"""

        from . import iAuraCAD_types  # lazy import

        iAuraCAD_types.edit_type(obj)

    def edit_quantity(self, obj, prop):
        """Edits the given quantity"""
        pass  # TODO implement

    def get_section_data(self, obj):
        """Returns two things: a list of objects and a cut plane"""

        from . import iAuraCAD_tools  # lazy import
        import Part

        if not obj.IauracadClass == "IauracadAnnotation":
            return [], None
        if obj.ObjectType != "DRAWING":
            return [], None
        objs = getattr(obj, "Objects", [])
        if not objs:
            # no object defined, we automatically use the project
            objs = []
            proj = iAuraCAD_tools.get_project(obj)
            if isinstance(proj, AuraCAD.DocumentObject):
                objs.append(proj)
            objs.extend(iAuraCAD_tools.get_AuraCAD_children(proj))
        if objs:
            s = []
            for o in objs:
                # TODO print a better message
                if o.ShapeMode != "Shape":
                    s.append(o)
            if s:
                AuraCAD.Console.PrintLog("DEBUG: Generating shapes. This might take some time...\n")
                for o in s:
                    o.ShapeMode = "Shape"
                    o.recompute()
            l = 1
            h = 1
            if obj.ViewObject:
                if hasattr(obj.ViewObject, "DisplayLength"):
                    l = obj.ViewObject.DisplayLength.Value
                    h = obj.ViewObject.DisplayHeight.Value
            plane = Part.makePlane(l, h, AuraCAD.Vector(l / 2, -h / 2, 0), AuraCAD.Vector(0, 0, 1))
            plane.Placement = obj.Placement
            return objs, plane
        else:
            print("DEBUG: Section plane returned no objects")
            return [], None

    def edit_classification(self, obj):
        """Edits the classification of this object"""

        from . import iAuraCAD_classification  # lazy loading

        iAuraCAD_classification.edit_classification(obj)


class document_object:
    """Holder for the document's Iauracad objects"""

    def __init__(self):
        pass
