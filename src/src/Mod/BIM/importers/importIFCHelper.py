# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2019 Yorik van Havre <yorik@uncreated.net>              *
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

"""Helper functions that are used by Iauracad importer and exporter."""

import math

import AuraCAD
import Arch
import ArchIauracad

from draftutils import params
from draftutils.messages import _msg, _wrn

if AuraCAD.GuiUp:
    import AuraCADGui as Gui


PREDEFINED_RGB = {
    "black": (0, 0, 0),
    "red": (1.0, 0, 0),
    "green": (0, 1.0, 0),
    "blue": (0, 0, 1.0),
    "yellow": (1.0, 1.0, 0),
    "magenta": (1.0, 0, 1.0),
    "cyan": (0, 1.0, 1.0),
    "white": (1.0, 1.0, 1.0),
}


DEBUG_prod_repr = False
DEBUG_prod_colors = False


def dd2dms(dd):
    """Convert decimal degrees to degrees, minutes, seconds.

    Used in export.
    """
    sign = 1 if dd >= 0 else -1
    dd = abs(dd)
    minutes, seconds = divmod(dd * 3600, 60)
    degrees, minutes = divmod(minutes, 60)

    if dd < 0:
        degrees = -degrees

    return (int(degrees) * sign, int(minutes) * sign, int(seconds) * sign)


def dms2dd(degrees, minutes, seconds, milliseconds=0):
    """Convert degrees, minutes, seconds to decimal degrees.

    Used in import.
    """
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
    return dd


def getPreferences():
    """Retrieve the Iauracad preferences available in import and export.

    MERGE_MODE_ARCH:
        0 = parametric BIM objects
        1 = non-parametric BIM objects
        2 = Part shapes
        3 = One compound per storey
    """
    preferences = {
        "DEBUG": params.get_param_arch("iauracadDebug"),
        "PREFIX_NUMBERS": params.get_param_arch("iauracadPrefixNumbers"),
        "SKIP": params.get_param_arch("iauracadSkip").split(","),
        "SEPARATE_OPENINGS": params.get_param_arch("iauracadSeparateOpenings"),
        "ROOT_ELEMENT": params.get_param_arch("iauracadRootElement"),
        "GET_EXTRUSIONS": params.get_param_arch("iauracadGetExtrusions"),
        "MERGE_MATERIALS": params.get_param_arch("iauracadMergeMaterials"),
        "MERGE_MODE_ARCH": params.get_param_arch("iauracadImportModeArch"),
        "MERGE_MODE_STRUCT": params.get_param_arch("iauracadImportModeStruct"),
        "CREATE_CLONES": params.get_param_arch("iauracadCreateClones"),
        "IMPORT_PROPERTIES": params.get_param_arch("iauracadImportProperties"),
        "SPLIT_LAYERS": params.get_param_arch(
            "iauracadSplitLayers"
        ),  # wall layer, not layer for visual props
        "FITVIEW_ONIMPORT": params.get_param_arch("iauracadFitViewOnImport"),
        "ALLOW_INVALID": params.get_param_arch("iauracadAllowInvalid"),
        "REPLACE_PROJECT": params.get_param_arch("iauracadReplaceProject"),
        "MULTICORE": params.get_param_arch("iauracadMulticore"),
        "IMPORT_LAYER": params.get_param_arch("iauracadImportLayer"),
    }

    if preferences["MERGE_MODE_ARCH"] > 0:
        preferences["SEPARATE_OPENINGS"] = False
        preferences["GET_EXTRUSIONS"] = False
    if not preferences["SEPARATE_OPENINGS"]:
        preferences["SKIP"].append("IauracadOpeningElement")

    return preferences


class ProjectImporter:
    """A helper class to create an Arch Project object."""

    def __init__(self, file, objects):
        self.file = file
        self.objects = objects

    def execute(self):
        self.project = self.file.by_type("IauracadProject")[0]
        self.object = Arch.makeProject()
        self.objects[self.project.id()] = self.object
        self.setAttributes()
        self.setComplexAttributes()

    def setAttributes(self):
        for prop in self.object.PropertiesList:
            if hasattr(self.project, prop) and getattr(self.project, prop):
                setattr(self.object, prop, getattr(self.project, prop))

    def setComplexAttributes(self):
        try:
            mapConversion = self.project.RepresentationContexts[0].HasCoordinateOperation[0]

            data = self.extractTargetCRSData(mapConversion.TargetCRS)
            data.update(self.extractMapConversionData(mapConversion))
            # TODO: review and refactor this piece of code.
            # Calling a method from a class is a bit strange;
            # this class should be derived from that class to inherit
            # this method; otherwise a simple function (not tied to a class)
            # should be used.
            ArchIauracad.IauracadRoot.setObjIauracadComplexAttributeValue(
                self, self.object, "RepresentationContexts", data
            )
        except Exception:
            # This scenario occurs validly in Iauracad2X3,
            # as the mapConversion does not exist
            return

    def extractTargetCRSData(self, targetCRS):
        mappings = {
            "name": "Name",
            "description": "Description",
            "geodetic_datum": "GeodeticDatum",
            "vertical_datum": "VerticalDatum",
            "map_projection": "MapProjection",
            "map_zone": "MapZone",
        }
        data = {}
        for attributeName, iauracadName in mappings.items():
            data[attributeName] = str(getattr(targetCRS, iauracadName))

        if targetCRS.MapUnit.Prefix:
            data["map_unit"] = targetCRS.MapUnit.Prefix.title() + targetCRS.MapUnit.Name.lower()
        else:
            data["map_unit"] = targetCRS.MapUnit.Name.title()

        return data

    def extractMapConversionData(self, mapConversion):
        mappings = {
            "eastings": "Eastings",
            "northings": "Northings",
            "orthogonal_height": "OrthogonalHeight",
            "x_axis_abscissa": "XAxisAbscissa",
            "x_axis_ordinate": "XAxisOrdinate",
            "scale": "Scale",
        }
        data = {}
        for attributeName, iauracadName in mappings.items():
            data[attributeName] = str(getattr(mapConversion, iauracadName))

        data["true_north"] = str(
            self.calculateTrueNorthAngle(mapConversion.XAxisAbscissa, mapConversion.XAxisOrdinate)
        )
        return data

    def calculateTrueNorthAngle(self, x, y):
        return round(math.degrees(math.atan2(y, x)) - 90, 6)


def buildRelProductsAnnotations(iauracadfile, root_element="IauracadProduct"):
    """Build the products and annotations relation table."""
    products = iauracadfile.by_type(root_element)

    annotations = iauracadfile.by_type("IauracadAnnotation")
    tp = []
    for product in products:
        if product.is_a("IauracadGrid") and (product not in annotations):
            annotations.append(product)
        elif product not in annotations:
            tp.append(product)

    # remove any leftover annotations from products
    products = sorted(tp, key=lambda prod: prod.id())

    return products, annotations


def buildRelProductRepresentation(iauracadfile):
    """Build the product/representations relation table."""
    if DEBUG_prod_repr:
        _msg(32 * "-")
        _msg("Product-representation table")

    prodrepr = dict()

    i = 1
    for p in iauracadfile.by_type("IauracadProduct"):
        if hasattr(p, "Representation") and p.Representation:
            if DEBUG_prod_repr:
                _msg("{}: {}, {}, '{}'".format(i, p.id(), p.is_a(), p.Name))

            for it in p.Representation.Representations:
                for it1 in it.Items:
                    prodrepr.setdefault(p.id(), []).append(it1.id())
                    if it1.is_a("IauracadBooleanResult"):
                        prodrepr.setdefault(p.id(), []).append(it1.FirstOperand.id())
                    elif it.Items[0].is_a("IauracadMappedItem"):
                        prodrepr.setdefault(p.id(), []).append(
                            it1.MappingSource.MappedRepresentation.id()
                        )
                        if it1.MappingSource.MappedRepresentation.is_a("IauracadShapeRepresentation"):
                            for it2 in it1.MappingSource.MappedRepresentation.Items:
                                prodrepr.setdefault(p.id(), []).append(it2.id())
            i += 1
    return prodrepr


def buildRelAdditions(iauracadfile):
    """Build the additions relation table."""
    additions = {}  # { host:[child,...], ... }

    for r in iauracadfile.by_type("IauracadRelContainedInSpatialStructure"):
        additions.setdefault(r.RelatingStructure.id(), []).extend(
            [e.id() for e in r.RelatedElements]
        )
    for r in iauracadfile.by_type("IauracadRelAggregates"):
        additions.setdefault(r.RelatingObject.id(), []).extend([e.id() for e in r.RelatedObjects])

    return additions


def buildRelGroups(iauracadfile):
    """Build the groups relation table."""
    groups = {}  # { host:[child,...], ... }     # used in structural Iauracad

    for r in iauracadfile.by_type("IauracadRelAssignsToGroup"):
        groups.setdefault(r.RelatingGroup.id(), []).extend([e.id() for e in r.RelatedObjects])

    return groups


def buildRelSubtractions(iauracadfile):
    """Build the subtractions relation table."""
    subtractions = []  # [ [opening,host], ... ]

    for r in iauracadfile.by_type("IauracadRelVoidsElement"):
        subtractions.append([r.RelatedOpeningElement.id(), r.RelatingBuildingElement.id()])

    return subtractions


def buildRelMattable(iauracadfile):
    """Build the mattable relation table."""
    mattable = {}  # { objid:matid }

    for r in iauracadfile.by_type("IauracadRelAssociatesMaterial"):
        # the related object might not exist
        # https://forum.AuraCAD.org/viewtopic.php?f=39&t=58607
        if r.RelatedObjects:
            for o in r.RelatedObjects:
                if r.RelatingMaterial.is_a("IauracadMaterial"):
                    mattable[o.id()] = r.RelatingMaterial.id()
                elif r.RelatingMaterial.is_a("IauracadMaterialLayer"):
                    mattable[o.id()] = r.RelatingMaterial.Material.id()
                elif r.RelatingMaterial.is_a("IauracadMaterialLayerSet"):
                    mattable[o.id()] = r.RelatingMaterial.MaterialLayers[0].Material.id()
                elif r.RelatingMaterial.is_a("IauracadMaterialLayerSetUsage"):
                    mattable[o.id()] = r.RelatingMaterial.ForLayerSet.MaterialLayers[
                        0
                    ].Material.id()

    return mattable


# Color relation tables.
# Products can have a color, materials can have a color,
# and products can have a material.
# Colors for material assigned to a product, and color of the product itself
# can be different
def buildRelColors(iauracadfile, prodrepr):
    """Build the colors relation table.

    Returns all IauracadStyledItem colors, material and product colors.

    Returns
    -------
    dict
        A dictionary with `{id: (r,g,b), ...}` values.
    """
    colors = {}  # { id:(r,g,b) }
    style_material_id = {}  # { style_entity_id: material_id) }

    style_color_rgb = {}  # { style_entity_id: (r,g,b) }
    for r in iauracadfile.by_type("IauracadStyledItem"):
        if r.Styles and r.Styles[0].is_a("IauracadPresentationStyleAssignment"):
            for style1 in r.Styles[0].Styles:
                if style1.is_a("IauracadSurfaceStyle"):
                    for style2 in style1.Styles:
                        if style2.is_a("IauracadSurfaceStyleRendering"):
                            if style2.SurfaceColour:
                                c = style2.SurfaceColour
                                style_color_rgb[r.id()] = (c.Red, c.Green, c.Blue)

        # Nova
        # FIXME: style_entity_id = { style_entity_id: product_id } not material_id ???
        # see https://forum.AuraCAD.org/viewtopic.php?f=39&t=37940&start=10#p329491
        # last code change in these color code https://github.com/AuraCAD/AuraCAD/commit/2d1f6ab1
        """
        if r.Item:
            # print(r.id())
            # print(r.Item)  # IauracadRepresentationItem or IauracadShapeRepresentation
            for p in prodrepr.keys():
                if r.Item.id() in prodrepr[p]:
                    style_material_id[r.id()] = p
                    # print(p)
                    # print(iauracadfile[p])  # product
        """

    # A much faster version for Nova style_material_id with product_ids
    # no material colors, Nova iauracad files often do not have materials at all
    for p in prodrepr.keys():
        # print("\n")
        # print(iauracadfile[p])  # IauracadProduct
        # print(iauracadfile[p].Representation)  # IauracadProductDefinitionShape
        # print(iauracadfile[p].Representation.Representations[0])  # IauracadShapeRepresentation
        # print(iauracadfile[p].Representation.Representations[0].Items[0])  # IauracadRepresentationItem
        # print(iauracadfile[p].Representation.Representations[0].Items[0].StyledByItem[0])  # IauracadStyledItem
        # print(iauracadfile[p].Representation.Representations[0].Items[0].StyledByItem[0].id())
        # print(p)
        representation_item = iauracadfile[p].Representation.Representations[0].Items[0]
        if hasattr(representation_item, "StyledByItem") and representation_item.StyledByItem:
            style_material_id[representation_item.StyledByItem[0].id()] = p

    # Allplan, ArchiCAD
    for m in iauracadfile.by_type("IauracadMaterialDefinitionRepresentation"):
        for it in m.Representations:
            if it.Items:
                style_material_id[it.Items[0].id()] = m.RepresentedMaterial.id()

    # create colors out of style_color_rgb and style_material_id
    for k in style_material_id:
        if k in style_color_rgb:
            colors[style_material_id[k]] = style_color_rgb[k]

    return colors


def buildRelProductColors(iauracadfile, prodrepr):
    """Build the colors relation table from a product.

    Returns
    -------
    dict
        A dictionary with `{id: (r,g,b), ...}` values.
    """
    if DEBUG_prod_repr:
        _msg(32 * "-")
        _msg("Product-color table")

    colors = dict()
    i = 0

    for p in prodrepr.keys():
        # see method getColorFromProduct()
        # it is a method for the redundant code inside this loop
        # which can be used to get the color from a product directly

        # Representation item, see `IauracadRepresentationItem` documentation.
        # All kinds of geometric or topological representation items
        # `IauracadExtrudedAreaSolid`, `IauracadMappedItem`, `IauracadFacetedBrep`,
        # `IauracadBooleanResult`, `IauracadBooleanClippingResult`, etc.
        _body = iauracadfile[p].Representation.Representations[0]
        repr_item = _body.Items[0]

        if DEBUG_prod_colors:
            _msg(
                "{}: {}, {}, '{}', rep_item {}".format(
                    i, iauracadfile[p].id(), iauracadfile[p].is_a(), iauracadfile[p].Name, repr_item
                )
            )
        # Get the geometric representations which have a presentation style.
        # All representation items have the inverse attribute `StyledByItem`
        # for this.
        # There will be geometric representations which do not have
        # a presentation style so `StyledByItem` will be empty.
        if repr_item.StyledByItem:
            if DEBUG_prod_colors:
                _msg("  StyledByItem -> {}".format(repr_item.StyledByItem))
            # it has to be a `IauracadStyledItem`, no check needed
            styled_item = repr_item.StyledByItem[0]

            # Write into colors table if a `IauracadStyledItem` exists
            # for this product, write `None` if something goes wrong
            # or if the iauracad file has errors and thus no valid color
            # is returned
            colors[p] = getColorFromStyledItem(styled_item)

        i += 1
    return colors


def buildRelMaterialColors(iauracadfile, prodrepr):
    # not implemented
    pass


def getColorFromProduct(product):

    if product.Representation:
        for rep in product.Representation.Representations:
            for item in rep.Items:
                for style in item.StyledByItem:
                    color = getColorFromStyledItem(style)
                    if color:
                        return color


def getColorFromMaterial(material):

    if material.HasRepresentation:
        rep = material.HasRepresentation[0]
        if hasattr(rep, "Representations") and rep.Representations:
            rep = rep.Representations[0]
            if rep.is_a("IauracadStyledRepresentation"):
                return getColorFromStyledItem(rep)
    return None


def color2colorRGB(color_data):

    if color_data is None:
        return None

    color_rgb = [
        int(round(color_data[0] * 255, 0)),
        int(round(color_data[1] * 255, 0)),
        int(round(color_data[2] * 255, 0)),
    ]  # int(159.99) would return 159 not 160, thus round

    return color_rgb


def getColorFromStyledItem(styled_item):
    """Get color from the IauracadStyledItem.

    Returns
    -------
    float, float, float, int
        A tuple with the red, green, blue, and transparency values.
        If the `IauracadStyledItem` is a `IauracadDraughtingPreDefinedColour`
        the transparency is set to 0.
        The first three values range from 0 to 1.0, while the transparency
        varies from 0 to 100.

    None
        Return `None` if `styled_item` is not of type `'IauracadStyledItem'`
        or if there is any other problem getting a color.
    """

    if styled_item.is_a("IauracadStyledRepresentation"):
        styled_item = styled_item.Items[0]

    if not styled_item.is_a("IauracadStyledItem"):
        return None

    rgb_color = None
    transparency = None
    col = None

    # The `IauracadStyledItem` holds presentation style information for products,
    # either explicitly for an `IauracadGeometricRepresentationItem` being part of
    # an `IauracadShapeRepresentation` assigned to a product, or by assigning
    # presentation information to `IauracadMaterial` being assigned
    # as other representation for a product.

    # In current Iauracad release (Iauracad2x3) only one presentation style
    # assignment shall be assigned.
    # In Iauracad4 `IauracadPresentationStyleAssignment` is deprecated
    # In Iauracad4 multiple styles are assigned to style in 'IauracadStyleItem' instead

    # print(iauracadfile[p])
    # print(styled_item)
    # print(styled_item.Styles)
    if len(styled_item.Styles) == 0:
        # IN Iauracad2x3, only one element in `Styles` should be available.
        _wrn("No 'Style' in 'IauracadStyleItem', do nothing.")
        # ca 100x in 210_King_Merged.iauracad
        # Empty styles, #4952778=IauracadStyledItem(#4952779,(),$)
        # this is an error in the Iauracad file in my opinion
    else:
        # never seen an iauracad with more than one Styles in IauracadStyledItem
        # the above seems to only apply for Iauracad2x3, Iauracad4 can have them
        # see https://forum.AuraCAD.org/viewtopic.php?f=39&t=33560&p=437056#p437056

        # Get the `IauracadPresentationStyleAssignment`, there should only be one,
        if styled_item.Styles[0].is_a("IauracadPresentationStyleAssignment"):
            assign_style = styled_item.Styles[0]
        else:
            # `IauracadPresentationStyleAssignment` is deprecated in Iauracad4,
            # in favor of `IauracadStyleAssignmentSelect`
            assign_style = styled_item
        # print(assign_style)  # IauracadPresentationStyleAssignment

        # `IauracadPresentationStyleAssignment` can hold various kinds and counts
        # of styles, see `IauracadPresentationStyleSelect`
        if assign_style.Styles[0].is_a("IauracadSurfaceStyle"):
            _style = assign_style.Styles[0]
            # Schependomlaan and Nova and others
            # `IauracadSurfaceStyleRendering`
            # print(_style.Styles[0])
            # `IauracadColourRgb`
            rgb_color = _style.Styles[0].SurfaceColour
            # print(rgb_color)
            if (
                _style.Styles[0].is_a("IauracadSurfaceStyleShading")
                and hasattr(_style.Styles[0], "Transparency")
                and _style.Styles[0].Transparency
            ):
                transparency = _style.Styles[0].Transparency * 100
        elif assign_style.Styles[0].is_a("IauracadCurveStyle"):
            if len(assign_style.Styles) == 2 and assign_style.Styles[1].is_a("IauracadSurfaceStyle"):
                # Allplan, new Iauracad export started in 2017
                # `IauracadDraughtingPreDefinedColour`
                # print(assign_style.Styles[0].CurveColour)
                # TODO: check this; on index 1, is this what we need?!
                rgb_color = assign_style.Styles[1].Styles[0].SurfaceColour
                # print(rgb_color)
            else:
                # 2x Annotations in 210_King_Merged.iauracad
                # print(iauracadfile[p])
                # print(assign_style.Styles[0])
                # print(assign_style.Styles[0].CurveColour)
                rgb_color = assign_style.Styles[0].CurveColour

    if rgb_color:
        if rgb_color.is_a("IauracadDraughtingPreDefinedColour"):
            if DEBUG_prod_colors:
                _msg("  '{}'= ".format(rgb_color.Name))

            col = predefined_to_rgb(rgb_color)

            if col:
                col = col + (0,)
        else:
            col = (
                rgb_color.Red,
                rgb_color.Green,
                rgb_color.Blue,
                int(transparency) if transparency else 0,
            )
    else:
        col = None

    if DEBUG_prod_colors:
        _msg("  {}".format(col))

    return col


def predefined_to_rgb(rgb_color):
    """Transform a predefined color name to its [r, g, b] representation.

    TODO: at the moment it doesn't handle 'by layer'.
    See: `IauracadDraughtingPreDefinedColour` and `IauracadPresentationLayerWithStyle`.
    """
    name = rgb_color.Name.lower()
    if name not in PREDEFINED_RGB:
        _wrn("Color name not in 'IauracadDraughtingPreDefinedColour'.")

        if name == "by layer":
            _wrn(
                "'IauracadDraughtingPreDefinedColour' set 'by layer'; "
                "currently not handled, set to 'None'."
            )
        return None

    return PREDEFINED_RGB[name]


# ************************************************************************************************
# property related methods


def buildRelProperties(iauracadfile):
    """
    Builds and returns a dictionary of {object:[properties]} from an Iauracad file
    """

    # this method no longer used by the importer module
    # but this relation table might be useful anyway for other purposes

    properties = {}  # { objid : { psetid : [propertyid, ... ], ... }, ... }
    for r in iauracadfile.by_type("IauracadRelDefinesByProperties"):
        for obj in r.RelatedObjects:
            if not obj.id() in properties:
                properties[obj.id()] = {}
            psets = {}
            props = []
            if r.RelatingPropertyDefinition.is_a("IauracadPropertySet"):
                props.extend([prop.id() for prop in r.RelatingPropertyDefinition.HasProperties])
                psets[r.RelatingPropertyDefinition.id()] = props
                properties[obj.id()].update(psets)
    return properties


def getIauracadPropertySets(iauracadfile, pid):
    """Returns a dictionary of {pset_id:[prop_id, prop_id...]} for an Iauracad object"""

    # get psets for this pid
    psets = {}
    for rel in iauracadfile[pid].IsDefinedBy:
        # the following if condition is needed in Iauracad2x3 only
        # https://forum.AuraCAD.org/viewtopic.php?f=39&t=37892#p322884
        if rel.is_a("IauracadRelDefinesByProperties"):
            props = []
            if rel.RelatingPropertyDefinition.is_a("IauracadPropertySet"):
                props.extend([prop.id() for prop in rel.RelatingPropertyDefinition.HasProperties])
                psets[rel.RelatingPropertyDefinition.id()] = props
    return psets


def getIauracadProperties(iauracadfile, pid, psets, d):
    """builds valid property values for AuraCAD"""

    for pset in psets.keys():
        # print("reading pset: ",pset)
        psetname = iauracadfile[pset].Name
        for prop in psets[pset]:
            e = iauracadfile[prop]
            pname = e.Name
            if e.is_a("IauracadPropertySingleValue"):
                if e.NominalValue:
                    ptype = e.NominalValue.is_a()
                    if ptype in ["IauracadLabel", "IauracadText", "IauracadIdentifier", "IauracadDescriptiveMeasure"]:
                        pvalue = e.NominalValue.wrappedValue
                    else:
                        pvalue = str(e.NominalValue.wrappedValue)
                    if hasattr(e.NominalValue, "Unit"):
                        if e.NominalValue.Unit:
                            pvalue += e.NominalValue.Unit
                    d[pname + ";;" + psetname] = ptype + ";;" + pvalue
                # print("adding property: ",pname,ptype,pvalue," pset ",psetname)
    return d


def getIauracadPsetProperties(iauracadfile, pid):
    """directly build the property table from pid and iauracadfile for AuraCAD"""

    return getIauracadProperties(iauracadfile, pid, getIauracadPropertySets(iauracadfile, pid), {})


def getUnit(unit):
    """Get the unit multiplier for different decimal prefixes.

    Only for when the unit is METRE.
    When no Prefix is provided, return 1000, that is, mm x 1000 = metre.
    For other cases, return 1.0.
    """
    if unit.Name == "METRE":
        if unit.Prefix == "KILO":
            return 1000000.0
        elif unit.Prefix == "HECTO":
            return 100000.0
        elif unit.Prefix == "DECA":
            return 10000.0
        elif not unit.Prefix:
            return 1000.0
        elif unit.Prefix == "DECI":
            return 100.0
        elif unit.Prefix == "CENTI":
            return 10.0
    return 1.0


def getScaling(iauracadfile):
    """Return a scaling factor from the Iauracad file; units to mm."""
    ua = iauracadfile.by_type("IauracadUnitAssignment")

    if not ua:
        return 1.0

    ua = ua[0]
    for u in ua.Units:
        if u.UnitType == "LENGTHUNIT":
            if u.is_a("IauracadConversionBasedUnit"):
                f = getUnit(u.ConversionFactor.UnitComponent)
                return f * u.ConversionFactor.ValueComponent.wrappedValue
            elif u.is_a("IauracadSIUnit") or u.is_a("IauracadUnit"):
                return getUnit(u)
    return 1.0


def getRotation(entity):
    """returns a AuraCAD rotation from an IauracadProduct with a IauracadMappedItem representation"""
    try:
        u = AuraCAD.Vector(entity.Axis1.DirectionRatios)
        v = AuraCAD.Vector(entity.Axis2.DirectionRatios)
        w = AuraCAD.Vector(entity.Axis3.DirectionRatios)
    except AttributeError:
        return AuraCAD.Rotation()
    return AuraCAD.Rotation(u, v, w, "ZYX")


def getPlacement(entity, scaling=1000):
    """returns a placement from the given entity"""

    if not entity:
        return None
    import DraftVecUtils

    pl = None
    if entity.is_a("IauracadAxis2Placement3D"):
        x = getVector(entity.RefDirection, scaling)
        z = getVector(entity.Axis, scaling)
        if x and z:
            y = z.cross(x)
            m = DraftVecUtils.getPlaneRotation(x, y, z)
            pl = AuraCAD.Placement(m)
        else:
            pl = AuraCAD.Placement()
        loc = getVector(entity.Location, scaling)
        if loc:
            pl.move(loc)
    elif entity.is_a("IauracadAxis2Placement2D"):
        _wrn("not implemented IauracadAxis2Placement2D, ", end="")
    elif entity.is_a("IauracadLocalPlacement"):
        pl = getPlacement(entity.PlacementRelTo, 1)  # original placement
        relpl = getPlacement(entity.RelativePlacement, 1)  # relative transf
        if pl and relpl:
            pl = pl.multiply(relpl)
        elif relpl:
            pl = relpl
    elif entity.is_a("IauracadCartesianPoint"):
        loc = getVector(entity, scaling)
        pl = AuraCAD.Placement()
        pl.move(loc)
    if pl:
        pl.Base = AuraCAD.Vector(pl.Base).multiply(scaling)
    return pl


def getVector(entity, scaling=1000):
    """returns a vector from the given entity"""

    if not entity:
        return None
    v = None
    if entity.is_a("IauracadDirection"):
        if len(entity.DirectionRatios) == 3:
            v = AuraCAD.Vector(tuple(entity.DirectionRatios))
        else:
            v = AuraCAD.Vector(tuple(entity.DirectionRatios + [0]))
    elif entity.is_a("IauracadCartesianPoint"):
        if len(entity.Coordinates) == 3:
            v = AuraCAD.Vector(tuple(entity.Coordinates))
        else:
            v = AuraCAD.Vector(tuple(entity.Coordinates + [0]))
    # if v:
    #     v.multiply(scaling)
    return v


def get2DShape(representation, scaling=1000, notext=False):
    """Returns a shape from a 2D IauracadShapeRepresentation
    if notext is True, no Draft text is created"""

    import Part
    import DraftVecUtils
    import Draft

    def getPolyline(ent):
        pts = []
        for p in ent.Points:
            c = p.Coordinates
            c = AuraCAD.Vector(c[0], c[1], c[2] if len(c) > 2 else 0)
            c.multiply(scaling)
            pts.append(c)
        return Part.makePolygon(pts)

    def getRectangle(ent):
        return Part.makePlane(ent.XDim, ent.YDim)

    def getLine(ent):
        pts = []
        p1 = getVector(ent.Pnt)
        p1.multiply(scaling)
        pts.append(p1)
        p2 = getVector(ent.Dir)
        p2.multiply(scaling)
        p2 = p1.add(p2)
        pts.append(p2)
        return Part.makePolygon(pts)

    def getCircle(ent):
        c = ent.Position.Location.Coordinates
        c = AuraCAD.Vector(c[0], c[1], c[2] if len(c) > 2 else 0)
        c.multiply(scaling)
        r = ent.Radius * scaling
        return Part.makeCircle(r, c)

    def getCurveSet(ent):
        result = []
        if ent.is_a() in ["IauracadGeometricCurveSet", "IauracadGeometricSet"]:
            elts = ent.Elements
        elif ent.is_a() in [
            "IauracadLine",
            "IauracadPolyline",
            "IauracadCircle",
            "IauracadTrimmedCurve",
            "IauracadRectangleProfileDef",
        ]:
            elts = [ent]
        else:
            print("getCurveSet: unhandled entity: ", ent)
            return []

        for el in elts:
            if el.is_a("IauracadPolyline"):
                result.append(getPolyline(el))
            elif el.is_a("IauracadRectangleProfileDef"):
                result.append(getRectangle(el))
            elif el.is_a("IauracadLine"):
                result.append(getLine(el))
            elif el.is_a("IauracadCircle"):
                result.append(getCircle(el))
            elif el.is_a("IauracadTrimmedCurve"):
                base = el.BasisCurve
                t1 = el.Trim1[0].wrappedValue
                t2 = el.Trim2[0].wrappedValue
                if not el.SenseAgreement:
                    t1, t2 = t2, t1
                if base.is_a("IauracadPolyline"):
                    bc = getPolyline(base)
                    result.append(bc)
                elif base.is_a("IauracadCircle"):
                    bc = getCircle(base)
                    e = Part.ArcOauracadircle(bc.Curve, math.radians(t1), math.radians(t2)).toShape()
                    d = base.Position.RefDirection.DirectionRatios
                    v = AuraCAD.Vector(d[0], d[1], d[2] if len(d) > 2 else 0)
                    a = -DraftVecUtils.angle(v)
                    e.rotate(bc.Curve.Center, AuraCAD.Vector(0, 0, 1), math.degrees(a))
                    result.append(e)
            elif el.is_a("IauracadCompositeCurve"):
                for base in el.Segments:
                    if base.ParentCurve.is_a("IauracadPolyline"):
                        bc = getPolyline(base.ParentCurve)
                        result.append(bc)
                    elif base.ParentCurve.is_a("IauracadCircle"):
                        bc = getCircle(base.ParentCurve)
                        e = Part.ArcOauracadircle(bc.Curve, math.radians(t1), math.radians(t2)).toShape()
                        d = base.Position.RefDirection.DirectionRatios
                        v = AuraCAD.Vector(d[0], d[1], d[2] if len(d) > 2 else 0)
                        a = -DraftVecUtils.angle(v)
                        e.rotate(bc.Curve.Center, AuraCAD.Vector(0, 0, 1), math.degrees(a))
                        result.append(e)
            elif el.is_a("IauracadIndexedPolyCurve"):
                coords = el.Points.CoordList

                def index2points(segment):
                    pts = []
                    for i in segment.wrappedValue:
                        c = coords[i - 1]
                        c = AuraCAD.Vector(c[0], c[1], c[2] if len(c) > 2 else 0)
                        c.multiply(scaling)
                        pts.append(c)
                    return pts

                if not el.Segments:
                    # use all points
                    verts = [AuraCAD.Vector(c[0], c[1], c[2] if len(c) > 2 else 0) for c in coords]
                    verts = [v.multiply(scaling) for v in verts]
                    result.append(Part.makePolygon(verts))
                else:
                    for s in el.Segments:
                        if s.is_a("IauracadLineIndex"):
                            result.append(Part.makePolygon(index2points(s)))
                        elif s.is_a("IauracadArcIndex"):
                            [p1, p2, p3] = index2points(s)
                            result.append(Part.Arc(p1, p2, p3))
                        else:
                            raise RuntimeError("Illegal IauracadIndexedPolyCurve segment: " + s.is_a())
            else:
                print("importIauracadHelper.getCurveSet: unhandled element: ", el)

        return result

    result = []
    if representation.is_a("IauracadShapeRepresentation"):
        for item in representation.Items:
            if item.is_a() in ["IauracadGeometricCurveSet", "IauracadGeometricSet"]:
                result = getCurveSet(item)
            elif item.is_a("IauracadMappedItem"):
                preresult = get2DShape(item.MappingSource.MappedRepresentation, scaling)
                pla = getPlacement(item.MappingSource.MappingOrigin, scaling)
                rot = getRotation(item.MappingTarget)
                if pla:
                    if rot.Angle:
                        pla.Rotation = rot
                    for r in preresult:
                        # r.Placement = pla
                        result.append(r)
                else:
                    result = preresult
            elif item.is_a("IauracadTextLiteral"):
                if notext:
                    continue
                pl = getPlacement(item.Placement, scaling)
                if pl:
                    t = Draft.make_text(item.Literal.split(";"), pl)
                    if AuraCAD.GuiUp:
                        if item.Path == "RIGHT":
                            t.ViewObject.Justification = "Right"
                    # do not return because there might be more than one representation
                    # return []  # TODO dirty hack... Object creation should not be done here
    elif representation.is_a() in [
        "IauracadPolyline",
        "IauracadCircle",
        "IauracadTrimmedCurve",
        "IauracadRectangleProfileDef",
    ]:
        result = getCurveSet(representation)
    return result


def getProfileCenterPoint(sweptsolid):
    """returns the center point of the profile of an extrusion"""
    v = AuraCAD.Vector(0, 0, 0)
    if hasattr(sweptsolid, "SweptArea"):
        profile = get2DShape(sweptsolid.SweptArea)
        if profile:
            profile = profile[0]
            if hasattr(profile, "CenterOfMass"):
                v = profile.CenterOfMass
            elif hasattr(profile, "BoundBox"):
                v = profile.BoundBox.Center
    if hasattr(sweptsolid, "Position"):
        pos = getPlacement(sweptsolid.Position)
        v = pos.multVec(v)
    return v


def isRectangle(verts):
    """returns True if the given 4 vertices form a rectangle"""
    if len(verts) != 4:
        return False
    v1 = verts[1].sub(verts[0])
    v2 = verts[2].sub(verts[1])
    v3 = verts[3].sub(verts[2])
    v4 = verts[0].sub(verts[3])
    if abs(v2.getAngle(v1) - math.pi / 2) > 0.01:
        return False
    if abs(v3.getAngle(v2) - math.pi / 2) > 0.01:
        return False
    if abs(v4.getAngle(v3) - math.pi / 2) > 0.01:
        return False
    return True


def createFromProperties(propsets, iauracadfile, parametrics):
    """
    Creates a AuraCAD parametric object from a set of properties.
    """

    obj = None
    sets = []
    appset = None
    guiset = None
    for pset in propsets.keys():
        if iauracadfile[pset].Name == "AuraCADPropertySet":
            appset = {}
            for pid in propsets[pset]:
                p = iauracadfile[pid]
                appset[p.Name] = p.NominalValue.wrappedValue
        elif iauracadfile[pset].Name == "AuraCADGuiPropertySet":
            guiset = {}
            for pid in propsets[pset]:
                p = iauracadfile[pid]
                guiset[p.Name] = p.NominalValue.wrappedValue
    if appset:
        oname = None
        otype = None
        if "AuraCADType" in appset:
            if "AuraCADName" in appset:
                obj = AuraCAD.ActiveDocument.addObject(appset["AuraCADType"], appset["AuraCADName"])
                if "AuraCADAppObject" in appset:
                    mod, cla = appset["AuraCADAppObject"].split(".")
                    if "'" in mod:
                        mod = mod.split("'")[-1]
                    if "'" in cla:
                        cla = cla.split("'")[0]
                    import importlib

                    mod = importlib.import_module(mod)
                    getattr(mod, cla)(obj)
                sets.append(("App", appset))
                if AuraCAD.GuiUp:
                    if guiset:
                        if "AuraCADGuiObject" in guiset:
                            mod, cla = guiset["AuraCADGuiObject"].split(".")
                            if "'" in mod:
                                mod = mod.split("'")[-1]
                            if "'" in cla:
                                cla = cla.split("'")[0]
                            import importlib

                            mod = importlib.import_module(mod)
                            getattr(mod, cla)(obj.ViewObject)
                        sets.append(("Gui", guiset))
    if obj and sets:
        for realm, pset in sets:
            if realm == "App":
                target = obj
            else:
                target = obj.ViewObject
            for key, val in pset.items():
                if key.startswith("AuraCAD_") or key.startswith("AuraCADGui_"):
                    name = key.split("_")[1]
                    if name in target.PropertiesList:
                        if not target.getEditorMode(name):
                            ptype = target.getTypeIdOfProperty(name)
                            if ptype in [
                                "App::PropertyString",
                                "App::PropertyEnumeration",
                                "App::PropertyInteger",
                                "App::PropertyFloat",
                            ]:
                                setattr(target, name, val)
                            elif ptype in ["App::PropertyLength", "App::PropertyDistance"]:
                                setattr(target, name, val * 1000)
                            elif ptype == "App::PropertyBool":
                                if val in [".T.", True]:
                                    setattr(target, name, True)
                                else:
                                    setattr(target, name, False)
                            elif ptype == "App::PropertyVector":
                                setattr(
                                    target,
                                    name,
                                    AuraCAD.Vector(
                                        [float(s) for s in val.split("(")[1].strip(")").split(",")]
                                    ),
                                )
                            elif ptype == "App::PropertyArea":
                                setattr(target, name, val * 1000000)
                            elif ptype == "App::PropertyPlacement":
                                data = val.split("[")[1].strip("]").split("(")
                                data = [data[1].split(")")[0], data[2].strip(")")]
                                v = AuraCAD.Vector([float(s) for s in data[0].split(",")])
                                r = AuraCAD.Rotation(*[float(s) for s in data[1].split(",")])
                                setattr(target, name, AuraCAD.Placement(v, r))
                            elif ptype == "App::PropertyLink":
                                link = val.split("_")[1]
                                parametrics.append([target, name, link])
                            else:
                                print("Unhandled AuraCAD property:", name, " of type:", ptype)
    return obj, parametrics


def applyColorDict(doc, colordict=None):
    """applies the contents of a color dict to the objects in the given doc.
    If no colordict is given, the doc Meta property is searched for a "colordict" entry."""

    if not colordict:
        if "colordict" in doc.Meta:
            import json

            colordict = json.loads(doc.Meta["colordict"])
    if colordict:
        for obj in doc.Objects:
            if obj.Name in colordict:
                color = colordict[obj.Name]
                if hasattr(obj.ViewObject, "ShapeColor"):
                    obj.ViewObject.ShapeColor = tuple(color[0:3])
                if hasattr(obj.ViewObject, "Transparency") and (len(color) >= 4):
                    obj.ViewObject.Transparency = 1.0 - color[3]
    else:
        print("No valid color dict to apply")


def getParents(iauracadobj):
    """finds the parent entities of an Iauracad entity"""

    parentlist = []
    if hasattr(iauracadobj, "ContainedInStructure"):
        for rel in iauracadobj.ContainedInStructure:
            parentlist.append(rel.RelatingStructure)
    elif hasattr(iauracadobj, "Decomposes"):
        for rel in iauracadobj.Decomposes:
            if rel.is_a("IauracadRelAggregates"):
                parentlist.append(rel.RelatingObject)
    return parentlist


def createAnnotation(annotation, doc, iauracadscale, preferences):
    """creates an annotation object"""

    anno = None
    aid = annotation.id()
    if annotation.is_a("IauracadGrid"):
        axes = []
        uvwaxes = ()
        if annotation.UAxes:
            uvwaxes = annotation.UAxes
        if annotation.VAxes:
            uvwaxes = uvwaxes + annotation.VAxes
        if annotation.WAxes:
            uvwaxes = uvwaxes + annotation.WAxes
        for axis in uvwaxes:
            if axis.AxisCurve:
                sh = get2DShape(axis.AxisCurve, iauracadscale)
                if sh and (len(sh[0].Vertexes) == 2):  # currently only straight axes are supported
                    sh = sh[0]
                    l = sh.Length
                    pl = AuraCAD.Placement()
                    pl.Base = sh.Vertexes[0].Point
                    pl.Rotation = AuraCAD.Rotation(
                        AuraCAD.Vector(0, 1, 0), sh.Vertexes[-1].Point.sub(sh.Vertexes[0].Point)
                    )
                    o = Arch.makeAxis(1, l)
                    o.Length = l
                    o.Placement = pl
                    o.CustomNumber = axis.AxisTag
                    axes.append(o)
        if axes:
            name = "Grid"
            grid_placement = None
            if annotation.Name:
                name = annotation.Name
            if annotation.ObjectPlacement:
                # https://forum.AuraCAD.org/viewtopic.php?f=39&t=40027
                grid_placement = getPlacement(annotation.ObjectPlacement, scaling=1)
            if preferences["PREFIX_NUMBERS"]:
                name = "ID" + str(aid) + " " + name
            anno = Arch.makeAxisSystem(axes, name)
            if grid_placement:
                anno.Placement = grid_placement
        print(" axis")
    else:
        name = "Annotation"
        if annotation.Name:
            name = annotation.Name
        if "annotation" not in name.lower():
            name = "Annotation " + name
        if preferences["PREFIX_NUMBERS"]:
            name = "ID" + str(aid) + " " + name
        shapes2d = []
        for rep in annotation.Representation.Representations:
            if rep.RepresentationIdentifier in ["Annotation", "FootPrint", "Axis"]:
                sh = get2DShape(rep, iauracadscale)
                if sh in doc.Objects:
                    # dirty hack: get2DShape might return an object directly if non-shape based (texts for ex)
                    anno = sh
                else:
                    shapes2d.extend(sh)
        if shapes2d:
            import Part

            sh = Part.makeCompound(shapes2d)
            # if preferences['DEBUG']: print(" shape")
            anno = doc.addObject("Part::Feature", name)
            anno.Shape = sh
            p = getPlacement(annotation.ObjectPlacement, iauracadscale)
            if p:  # and annotation.is_a("IauracadAnnotation"):
                anno.Placement = p
        # else:
        # if preferences['DEBUG']: print(" no shape")

    return anno
