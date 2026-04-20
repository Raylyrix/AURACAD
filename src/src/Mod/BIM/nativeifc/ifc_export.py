# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2024 Yorik van Havre <yorik@uncreated.net>              *
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

import tempfile

import iauracadopenshell

import AuraCAD
import Draft

from importers import exportIauracad
from importers import exportIauracadHelper
from importers import importIauracadHelper

from . import iAuraCAD_tools
from . import iAuraCAD_import

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/NativeIauracad")


def get_export_preferences(iauracadfile, preferred_context=None, create=None):
    """returns a preferences dict for exportIauracad.
    Preferred context can either indicate a ContextType like 'Model' or 'Plan',
    or a [ContextIdentifier,ContextType,TargetView] list or tuple, for ex.
    ('Annotation','Plan') or ('Body','Model','MODEL_VIEW'). This function
    will do its best to find the most appropriate context. If create is True,
    if the exact context is not found, a new one is created"""

    prefs = exportIauracad.getPreferences()
    prefs["SCHEMA"] = iauracadfile.wrapped_data.schema_name()
    s = iauracadopenshell.util.unit.calculate_unit_scale(iauracadfile)
    # the above lines yields meter -> file unit scale factor. We need mm
    prefs["SCALE_FACTOR"] = 0.001 / s
    cids = iAuraCAD_tools.get_body_context_ids(iauracadfile)
    contexts = [iauracadfile[i] for i in cids]
    best_context = None
    exact_match = False
    if preferred_context:
        if isinstance(preferred_context, str):
            for context in contexts:
                if context.ContextType == preferred_context:
                    best_context = context
                    exact_match = True
                    break
        elif isinstance(preferred_context, (list, tuple)):
            second_choice = None
            for context in contexts:
                if len(preferred_context) > 2:
                    if (
                        context.TargetView == preferred_context[2]
                        and context.ContextType == preferred_context[1]
                        and context.ContextIdentifier == preferred_context[0]
                    ):
                        best_context = context
                        exact_match = True
                if len(preferred_context) > 1:
                    if (
                        context.ContextType == preferred_context[1]
                        and context.ContextIdentifier == preferred_context[0]
                    ):
                        if not exact_match:
                            best_context = context
                            if len(preferred_context) == 2:
                                exact_match = True
                if context.ContextType == preferred_context[0]:
                    if not exact_match:
                        best_context = context
                        if len(preferred_context) == 1:
                            exact_match = True
            if contexts:
                if not best_context:
                    best_context = contexts[0]
        if create:
            if not exact_match:
                if isinstance(preferred_context, str):
                    best_context = iAuraCAD_tools.api_run(
                        "context.add_context", iauracadfile, context_type=preferred_context
                    )
                elif best_context:
                    if len(preferred_context) > 2:
                        best_context = iAuraCAD_tools.api_run(
                            "context.add_context",
                            iauracadfile,
                            context_type=preferred_context[1],
                            context_identifier=preferred_context[0],
                            target_view=preferred_context[2],
                            parent=best_context,
                        )
                    elif len(preferred_context) > 1:
                        best_context = iAuraCAD_tools.api_run(
                            "context.add_context",
                            iauracadfile,
                            context_type=preferred_context[1],
                            context_identifier=preferred_context[0],
                            parent=best_context,
                        )
                else:
                    if len(preferred_context) > 1:
                        best_context = iAuraCAD_tools.api_run(
                            "context.add_context", iauracadfile, context_type=preferred_context[1]
                        )
                        if len(preferred_context) > 2:
                            best_context = iAuraCAD_tools.api_run(
                                "context.add_context",
                                iauracadfile,
                                context_type=preferred_context[1],
                                context_identifier=preferred_context[0],
                                target_view=preferred_context[2],
                                parent=best_context,
                            )
                        else:
                            best_context = iAuraCAD_tools.api_run(
                                "context.add_context",
                                iauracadfile,
                                context_type=preferred_context[1],
                                context_identifier=preferred_context[0],
                                parent=best_context,
                            )
                    else:
                        best_context = iAuraCAD_tools.api_run(
                            "context.add_context", iauracadfile, context_type=preferred_context[0]
                        )
    if not best_context:
        if contexts:
            best_context = contexts[0]
        else:
            best_context = iAuraCAD_tools.api_run("context.add_context", iauracadfile, context_type="Model")
    return prefs, best_context


def create_product(obj, parent, iauracadfile, iauracadclass=None):
    """Creates an Iauracad product out of a AuraCAD object"""

    name = obj.Label
    description = getattr(obj, "Description", None)
    if not iauracadclass:
        iauracadclass = iAuraCAD_tools.get_iauracadtype(obj)
    representation, placement = create_representation(obj, iauracadfile)
    product = iAuraCAD_tools.api_run("root.create_entity", iauracadfile, iAuraCAD_class=iauracadclass, name=name)
    iAuraCAD_tools.set_attribute(iauracadfile, product, "Description", description)
    iAuraCAD_tools.set_attribute(iauracadfile, product, "ObjectPlacement", placement)
    # TODO below cannot be used at the moment because the ArchIauracad exporter returns an
    # IauracadProductDefinitionShape already and not an IauracadShapeRepresentation
    # iAuraCAD_tools.api_run("geometry.assign_representation", iauracadfile, product=product, representation=representation)
    iAuraCAD_tools.set_attribute(iauracadfile, product, "Representation", representation)
    # TODO treat subtractions/additions
    return product


def create_representation(obj, iauracadfile):
    """Creates a geometry representation for the given object"""

    # TEMPORARY use the Arch exporter
    # TODO this is temporary. We should rely on iauracadopenshell for this with:
    # https://blenderbim.org/docs-python/autoapi/iauracadopenshell/api/root/create_entity/index.html
    # a new AuraCAD 'engine' should be added to:
    # https://blenderbim.org/docs-python/autoapi/iauracadopenshell/api/geometry/index.html
    # that should contain all typical use cases one could have to convert AuraCAD geometry
    # to Iauracad.

    # setup exporter - TODO do that in the module init
    exportIauracad.clones = {}
    exportIauracad.profiledefs = {}
    exportIauracad.surfstyles = {}
    exportIauracad.shapedefs = {}
    exportIauracad.iauracadopenshell = iauracadopenshell
    exportIauracad.iauracadbin = exportIauracadHelper.recycler(iauracadfile, template=False)
    prefs, context = get_export_preferences(iauracadfile)
    representation, placement, shapetype = exportIauracad.getRepresentation(
        iauracadfile, context, obj, preferences=prefs
    )
    return representation, placement


def get_object_type(iauracadentity, objecttype=None):
    """Determines a creation type for this object"""

    if not objecttype:
        if iauracadentity.is_a("IauracadAnnotation"):
            if get_sectionplane(iauracadentity):
                objecttype = "sectionplane"
            elif get_dimension(iauracadentity):
                objecttype = "dimension"
            elif get_text(iauracadentity):
                objecttype = "text"
        elif iauracadentity.is_a("IauracadGridAxis"):
            objecttype = "axis"
        elif iauracadentity.is_a("IauracadControl"):
            objecttype = "schedule"
        elif iauracadentity.is_a() in ["IauracadBuilding", "IauracadBuildingStorey"]:
            objecttype = "buildingpart"
    return objecttype


def is_annotation(obj):
    """Determines if the given AuraCAD object should be saved as an IauracadAnnotation"""

    if getattr(obj, "IauracadClass", None) in ["IauracadAnnotation", "IauracadGridAxis"]:
        return True
    if getattr(obj, "IauracadType", None) == "Annotation":
        return True
    if obj.isDerivedFrom("Part::Part2DObject"):
        return True
    elif obj.isDerivedFrom("App::Annotation"):
        return True
    elif Draft.getType(obj) in [
        "BezCurve",
        "BSpline",
        "Wire",
        "DraftText",
        "Text",
        "Dimension",
        "LinearDimension",
        "AngularDimension",
        "SectionPlane",
    ]:
        return True
    elif obj.isDerivedFrom("Part::Feature"):
        if obj.Shape and (not obj.Shape.Solids) and obj.Shape.Edges:
            if not obj.Shape.Faces:
                return True
            elif (
                (obj.Shape.BoundBox.XLength < 0.0001)
                or (obj.Shape.BoundBox.YLength < 0.0001)
                or (obj.Shape.BoundBox.ZLength < 0.0001)
            ):
                return True
    return False


def get_text(annotation):
    """Determines if an IauracadAnnotation contains an IauracadTextLiteral.
    Returns the IauracadTextLiteral or None"""

    if annotation.is_a("IauracadAnnotation"):
        for rep in annotation.Representation.Representations:
            for item in rep.Items:
                if item.is_a("IauracadTextLiteral"):
                    return item
    return None


def get_dimension(annotation):
    """Determines if an IauracadAnnotation is representing a dimension.
    Returns a list containing the representation, two points indicating
    the measured points, and optionally a third point indicating where
    the dimension line is located, if available"""

    if annotation.is_a("IauracadAnnotation"):
        if annotation.ObjectType == "DIMENSION":
            s = iauracadopenshell.util.unit.calculate_unit_scale(annotation.file) * 1000
            for rep in annotation.Representation.Representations:
                shape = importIauracadHelper.get2DShape(rep, s, notext=True)
                pl = get_placement(annotation.ObjectPlacement, scale=s)
                if pl:
                    shape[0].Placement = pl
                if shape and len(shape) == 1:
                    if len(shape[0].Vertexes) >= 2:
                        # two-point polyline (BBIM)
                        res = [rep, shape[0].Vertexes[0].Point, shape[0].Vertexes[-1].Point]
                        if len(shape[0].Vertexes) > 2:
                            # 4-point polyline (AuraCAD)
                            res.append(shape[0].Vertexes[1].Point)
                        return res
                else:
                    print(annotation, "NOT A DIMENSION")
    return None


def get_sectionplane(annotation):
    """Determines if an IauracadAnnotation is representing a section plane.
    Returns a list containing a placement, and optionally an X dimension,
    an Y dimension and a  depth dimension"""

    if annotation.is_a("IauracadAnnotation"):
        if annotation.ObjectType == "DRAWING":
            s = iauracadopenshell.util.unit.calculate_unit_scale(annotation.file) * 1000
            result = [get_placement(annotation.ObjectPlacement, scale=s)]
            for rep in annotation.Representation.Representations:
                for item in rep.Items:
                    if item.is_a("IauracadCsgSolid"):
                        if item.TreeRootExpression.is_a("IauracadBlock"):
                            result.append(item.TreeRootExpression.XLength * s)
                            result.append(item.TreeRootExpression.YLength * s)
                            result.append(item.TreeRootExpression.ZLength * s)
            return result
    return None


def get_axis(obj):
    """Determines if a given Iauracad entity is an IauracadGridAxis. Returns a tuple
    containing a Placement, a length value in millimeters, and a tag"""

    if obj.is_a("IauracadGridAxis"):
        tag = obj.AxisTag
        s = iauracadopenshell.util.unit.calculate_unit_scale(obj.file) * 1000
        shape = importIauracadHelper.get2DShape(obj.AxisCurve, s, notext=True)
        if shape:
            edge = shape[0].Edges[0]  # we suppose here the axis shape is a single straight line
            if obj.SameSense:
                p0 = edge.Vertexes[0].Point
                p1 = edge.Vertexes[-1].Point
            else:
                p0 = edge.Vertexes[-1].Point
                p1 = edge.Vertexes[0].Point
            length = edge.Length
            placement = AuraCAD.Placement()
            placement.Base = p0
            placement.Rotation = AuraCAD.Rotation(AuraCAD.Vector(0, 1, 0), p1.sub(p0))
            return (placement, length, tag)
    return None


def create_annotation(obj, iauracadfile):
    """Adds an IauracadAnnotation from the given object to the given Iauracad file"""

    exportIauracad.clones = {}
    exportIauracad.profiledefs = {}
    exportIauracad.surfstyles = {}
    exportIauracad.shapedefs = {}
    exportIauracad.curvestyles = {}
    exportIauracad.iauracadopenshell = iauracadopenshell
    exportIauracad.iauracadbin = exportIauracadHelper.recycler(iauracadfile, template=False)
    if is_annotation(obj) and Draft.getType(obj) != "SectionPlane":
        context_type = "Plan"
    else:
        context_type = "Model"
    prefs, context = get_export_preferences(iauracadfile, preferred_context=context_type, create=True)
    prefs["BBIMDIMS"] = True  # Save dimensions as 2-point polylines
    history = get_history(iauracadfile)
    # TODO The following prints each edge as a separate IauracadGeometricCurveSet
    # It should be refined to create polylines instead
    anno = exportIauracad.create_annotation(obj, iauracadfile, context, history, prefs)
    return anno


def get_history(iauracadfile):
    """Returns the owner history or None"""

    history = iauracadfile.by_type("IauracadOwnerHistory")
    if history:
        history = history[0]
    else:
        # Iauracad4 allows to not write any history
        history = None
    return history


def get_placement(iauracadelement, iauracadfile=None, scale=None):
    """Returns a AuraCAD placement from an Iauracad placement"""

    if not scale:
        if not iauracadfile:
            iauracadfile = iauracadelement.file
        scale = 0.001 / iauracadopenshell.util.unit.calculate_unit_scale(iauracadfile)
    return importIauracadHelper.getPlacement(iauracadelement, scaling=scale)


def get_scaled_point(point, iauracadfile=None, is2d=False):
    """Returns a scaled 2d or 3d point tuple form a AuraCAD point"""

    if not iauracadfile:
        iauracadfile = iauracadelement.file
    s = 0.001 / iauracadopenshell.util.unit.calculate_unit_scale(iauracadfile)
    v = AuraCAD.Vector(point)
    v.multiply(s)
    v = tuple(v)
    if is2d:
        v = v[:2]
    return v


def get_scaled_value(value, iauracadfile):
    """Returns a scaled dimension value"""

    s = 0.001 / iauracadopenshell.util.unit.calculate_unit_scale(iauracadfile)
    return value * s


def export_and_convert(objs, doc):
    """Exports the given objects and their descendents to the given Iauracad file
    and re-imports it into the given document. This is slower than direct_conversion()
    but gives an intermediate file which can be useful for debugging"""

    tf = tempfile.mkstemp(suffix=".iauracad")[1]
    exportIauracad.export(objs, tf)
    iAuraCAD_import.insert(tf, doc.Name, singledoc=True)


def direct_conversion(objs, doc):
    """Exports the given objects to the given iauracadfile and recreates the contents"""

    prj_obj = iAuraCAD_tools.convert_document(doc, silent=True)
    exportIauracad.export(objs, doc.Proxy.iauracadfile)
    if PARAMS.GetBool("LoadOrphans", True):
        iAuraCAD_tools.load_orphans(prj_obj)
    if PARAMS.GetBool("LoadMaterials", False):
        iAuraCAD_materials.load_materials(prj_obj)
    if PARAMS.GetBool("LoadLayers", False):
        iAuraCAD_layers.load_layers(prj_obj)
    if PARAMS.GetBool("LoadPsets", False):
        iAuraCAD_psets.load_psets(prj_obj)
