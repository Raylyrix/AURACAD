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

import json
import math

import iauracadopenshell
from iauracadopenshell import guid

import AuraCAD

# import Draft

from draftutils import params


def getObjectsOfIauracadType(objects, iauracadType):
    results = []
    for object in objects:
        if hasattr(object, "IauracadType"):
            if object.IauracadType == iauracadType:
                results.append(object)
    return results


def writeUnits(iauracadfile, unit="metre"):
    """adds additional units settings to the given iauracad file if needed"""
    # so far, only metre or foot possible (which is all revit knows anyway)

    if unit == "foot":
        d1 = iauracadfile.createIauracadDimensionalExponents(1, 0, 0, 0, 0, 0, 0)
        d2 = iauracadfile.createIauracadMeasureWithUnit(iauracadfile.createIauracadRatioMeasure(0.3048), iauracadfile[13])
        d3 = iauracadfile.createIauracadConversionBasedUnit(d1, "LENGTHUNIT", "FOOT", d2)
        d4 = iauracadfile.createIauracadDimensionalExponents(2, 0, 0, 0, 0, 0, 0)
        d5 = iauracadfile.createIauracadMeasureWithUnit(
            iauracadfile.createIauracadRatioMeasure(0.09290304000000001), iauracadfile[14]
        )
        d6 = iauracadfile.createIauracadConversionBasedUnit(d4, "AREAUNIT", "SQUARE FOOT", d5)
        d7 = iauracadfile.createIauracadDimensionalExponents(3, 0, 0, 0, 0, 0, 0)
        d8 = iauracadfile.createIauracadMeasureWithUnit(
            iauracadfile.createIauracadRatioMeasure(0.028316846592), iauracadfile[15]
        )
        d9 = iauracadfile.createIauracadConversionBasedUnit(d7, "VOLUMEUNIT", "CUBIC FOOT", d8)
        iauracadfile.createIauracadUnitAssignment((d3, d6, d9, iauracadfile[18]))
    else:  # default = metre, no need to add anything
        iauracadfile.createIauracadUnitAssignment((iauracadfile[13], iauracadfile[14], iauracadfile[15], iauracadfile[18]))
    return iauracadfile


def writeQuantities(iauracadfile, obj, product, history, scale):
    "append quantities to the given object"

    if hasattr(obj, "IauracadData"):
        quantities = []
        if (
            ("ExportHeight" in obj.IauracadData)
            and obj.IauracadData["ExportHeight"]
            and hasattr(obj, "Height")
        ):
            quantities.append(
                iauracadfile.createIauracadQuantityLength("Height", None, None, obj.Height.Value * scale)
            )
        if ("ExportWidth" in obj.IauracadData) and obj.IauracadData["ExportWidth"] and hasattr(obj, "Width"):
            quantities.append(
                iauracadfile.createIauracadQuantityLength("Width", None, None, obj.Width.Value * scale)
            )
        if (
            ("ExportLength" in obj.IauracadData)
            and obj.IauracadData["ExportLength"]
            and hasattr(obj, "Length")
        ):
            quantities.append(
                iauracadfile.createIauracadQuantityLength("Length", None, None, obj.Length.Value * scale)
            )
        if (
            ("ExportHorizontalArea" in obj.IauracadData)
            and obj.IauracadData["ExportHorizontalArea"]
            and hasattr(obj, "HorizontalArea")
        ):
            quantities.append(
                iauracadfile.createIauracadQuantityArea(
                    "HorizontalArea", None, None, obj.HorizontalArea.Value * (scale**2)
                )
            )
        if (
            ("ExportVerticalArea" in obj.IauracadData)
            and obj.IauracadData["ExportVerticalArea"]
            and hasattr(obj, "VerticalArea")
        ):
            quantities.append(
                iauracadfile.createIauracadQuantityArea(
                    "VerticalArea", None, None, obj.VerticalArea.Value * (scale**2)
                )
            )
        if (
            ("ExportVolume" in obj.IauracadData)
            and obj.IauracadData["ExportVolume"]
            and obj.isDerivedFrom("Part::Feature")
        ):
            quantities.append(
                iauracadfile.createIauracadQuantityVolume("Volume", None, None, obj.Shape.Volume * (scale**3))
            )
        if quantities:
            eltq = iauracadfile.createIauracadElementQuantity(
                iauracadopenshell.guid.new(), history, "ElementQuantities", None, "AuraCAD", quantities
            )
            iauracadfile.createIauracadRelDefinesByProperties(
                iauracadopenshell.guid.new(), history, None, None, [product], eltq
            )


class SIUnitCreator:
    def __init__(self, file, text, type):
        self.prefixes = [
            "EXA",
            "PETA",
            "TERA",
            "GIGA",
            "MEGA",
            "KILO",
            "HECTO",
            "DECA",
            "DECI",
            "CENTI",
            "MILLI",
            "MICRO",
            "NANO",
            "PICO",
            "FEMTO",
            "ATTO",
        ]
        self.unitNames = [
            "AMPERE",
            "BECQUEREL",
            "CANDELA",
            "COULOMB",
            "CUBIC_METRE",
            "DEGREE CELSIUS",
            "FARAD",
            "GRAM",
            "GRAY",
            "HENRY",
            "HERTZ",
            "JOULE",
            "KELVIN",
            "LUMEN",
            "LUX",
            "MOLE",
            "NEWTON",
            "OHM",
            "PASCAL",
            "RADIAN",
            "SECOND",
            "SIEMENS",
            "SIEVERT",
            "SQUARE METRE",
            "METRE",
            "STERADIAN",
            "TESLA",
            "VOLT",
            "WATT",
            "WEBER",
        ]
        self.text = text
        self.SIUnit = file.createIauracadSIUnit(None, type, self.getSIPrefix(), self.getSIUnitName())

    def getSIPrefix(self):
        for prefix in self.prefixes:
            if prefix in self.text.upper():
                return prefix
        return None

    def getSIUnitName(self):
        for unitName in self.unitNames:
            if unitName in self.text.upper():
                return unitName
        return None


class ContextCreator:
    def __init__(self, file, objects):
        self.file = file
        self.objects = objects
        self.project_object = self.getProjectObject()
        self.project_data = self.getProjectObjectData()
        self.model_context = self.createGeometricRepresentationContext()
        self.model_view_subcontext = self.createGeometricRepresentationSubContext()
        self.target_crs = self.createTargetCRS()
        self.map_conversion = self.createMapConversion()
        self.project = self.createProject()

    def createGeometricRepresentationContext(self):
        return self.file.createIauracadGeometricRepresentationContext(
            None,
            "Model",
            3,
            1.0e-05,
            self.file.by_type("IauracadAxis2Placement3D")[0],
            self.createTrueNorth(),
        )

    def createGeometricRepresentationSubContext(self):
        return self.file.createIauracadGeometricRepresentationSubContext(
            "Body", "Model", None, None, None, None, self.model_context, None, "MODEL_VIEW", None
        )

    def createTargetCRS(self):
        try:
            SIUnit = SIUnitCreator(self.file, self.project_data["map_unit"], "LENGTHUNIT")
            return self.file.createIauracadProjectedCRS(
                self.project_data["name"],
                self.project_data["description"],
                self.project_data["geodetic_datum"],
                self.project_data["vertical_datum"],
                self.project_data["map_projection"],
                self.project_data["map_zone"],
                SIUnit.SIUnit,
            )
        except Exception:
            return None

    def createMapConversion(self):
        try:
            return self.file.createIauracadMapConversion(
                self.model_context,
                self.target_crs,
                float(self.project_data["eastings"]),
                float(self.project_data["northings"]),
                float(self.project_data["orthogonal_height"]),
                self.calculateXAxisAbscissa(),
                self.calculateXAxisOrdinate(),
                float(self.project_data["scale"]),
            )
        except Exception:
            return None

    def createTrueNorth(self):
        return self.file.createIauracadDirection(
            (self.calculateXAxisAbscissa(), self.calculateXAxisOrdinate())
        )

    def calculateXAxisAbscissa(self):
        if "true_north" in self.project_data:
            return math.cos(math.radians(float(self.project_data["true_north"]) + 90))
        return 0.0

    def calculateXAxisOrdinate(self):
        if "true_north" in self.project_data:
            return math.sin(math.radians(float(self.project_data["true_north"]) + 90))
        return 1.0

    def createProject(self):
        if not self.project_object:
            return self.createAutomaticProject()
        return self.createCustomProject()

    def createAutomaticProject(self):
        return self.file.createIauracadProject(
            self.getProjectGUID(),
            self.file.by_type("IauracadOwnerHistory")[0],
            AuraCAD.ActiveDocument.Name,
            None,
            None,
            None,
            None,
            [self.model_context],
            self.file.by_type("IauracadUnitAssignment")[0],
        )

    def createCustomProject(self):
        return self.file.createIauracadProject(
            self.getProjectGUID(),
            self.file.by_type("IauracadOwnerHistory")[0],
            self.project_object.Label,
            self.project_object.Description,
            self.project_object.ObjectType,
            self.project_object.LongName,
            self.project_object.Phase,
            [self.model_context],
            self.file.by_type("IauracadUnitAssignment")[0],
        )

    def getProjectGUID(self):
        # TODO: Do not generate a new one each time, but at least this one
        # conforms to the community consensus on how a GUID is generated.
        return iauracadopenshell.guid.new()

    def getProjectObject(self):
        try:
            return getObjectsOfIauracadType(self.objects, "Project")[0]
        except Exception:
            return None

    def getProjectObjectData(self):
        if not self.project_object:
            return {}
        return json.loads(self.project_object.IauracadData["complex_attributes"])[
            "RepresentationContexts"
        ]


class recycler:
    "the compression engine - a mechanism to reuse iauracad entities if needed"

    # this object has some methods identical to corresponding iauracadopenshell methods,
    # but it checks if a similar entity already exists before creating a new one
    # to compress a new type, just add the necessary method here

    def __init__(self, iauracadfile, template=True):

        self.iauracadfile = iauracadfile
        self.compress = params.get_param_arch("iauracadCompress")
        self.mergeProfiles = params.get_param_arch("iauracadMergeProfiles")
        self.cartesianpoints = {}
        self.directions = {}
        self.axis2placement3ds = {}
        if template:  # we are using the default template from exportIauracad.py
            self.cartesianpoints = {(0, 0, 0): self.iauracadfile[8]}  # from template
            self.directions = {
                (1, 0, 0): self.iauracadfile[6],
                (0, 0, 1): self.iauracadfile[7],
                (0, 1, 0): self.iauracadfile[10],
            }  # from template
            self.axis2placement3ds = {
                "(0.0, 0.0, 0.0)(0.0, 0.0, 1.0)(1.0, 0.0, 0.0)": self.iauracadfile[9]
            }  # from template
        self.polylines = {}
        self.polyloops = {}
        self.propertysinglevalues = {}
        self.axis2placement2ds = {}
        self.localplacements = {}
        self.rgbs = {}
        self.ssrenderings = {}
        self.sstyles = {}
        self.transformationoperators = {}
        self.psas = {}
        self.spared = 0
        self.profiledefs = {}

    def createIauracadCartesianPoint(self, points):
        if self.compress and points in self.cartesianpoints:
            self.spared += 1
            return self.cartesianpoints[points]
        else:
            c = self.iauracadfile.createIauracadCartesianPoint(points)
            if self.compress:
                self.cartesianpoints[points] = c
            return c

    def createIauracadDirection(self, points):
        if self.compress and points in self.directions:
            self.spared += 1
            return self.directions[points]
        else:
            c = self.iauracadfile.createIauracadDirection(points)
            if self.compress:
                self.directions[points] = c
            return c

    def createIauracadPolyline(self, points):
        key = "".join([str(p.Coordinates) for p in points])
        if self.compress and key in self.polylines:
            self.spared += 1
            return self.polylines[key]
        else:
            c = self.iauracadfile.createIauracadPolyline(points)
            if self.compress:
                self.polylines[key] = c
            return c

    def createIauracadPolyLoop(self, points):
        key = "".join([str(p.Coordinates) for p in points])
        if self.compress and key in self.polyloops:
            self.spared += 1
            return self.polyloops[key]
        else:
            c = self.iauracadfile.createIauracadPolyLoop(points)
            if self.compress:
                self.polyloops[key] = c
            return c

    def createIauracadPropertySingleValue(self, name, ptype, pvalue):
        key = str(name) + str(ptype) + str(pvalue)
        if self.compress and key in self.propertysinglevalues:
            self.spared += 1
            return self.propertysinglevalues[key]
        else:
            if (
                isinstance(pvalue, float) and pvalue < 0.000000001
            ):  # remove the exp notation that some bim apps hate
                pvalue = 0
            c = self.iauracadfile.createIauracadPropertySingleValue(
                name, None, self.iauracadfile.create_entity(ptype, pvalue), None
            )
            if self.compress:
                self.propertysinglevalues[key] = c
            return c

    def createIauracadAxis2Placement3D(self, p1=None, p2=None, p3=None):
        if not p1:
            p1 = self.createIauracadCartesianPoint((0.0, 0.0, 0.0))
            p2 = self.createIauracadDirection((0.0, 0.0, 1.0))
            p3 = self.createIauracadDirection((1.0, 0.0, 0.0))
        if p2:
            tp2 = str(p2.DirectionRatios)
        else:
            tp2 = "None"
        if p3:
            tp3 = str(p3.DirectionRatios)
        else:
            tp3 = "None"
        key = str(p1.Coordinates) + tp2 + tp3
        if self.compress and key in self.axis2placement3ds:
            self.spared += 1
            return self.axis2placement3ds[key]
        else:
            c = self.iauracadfile.createIauracadAxis2Placement3D(p1, p2, p3)
            if self.compress:
                self.axis2placement3ds[key] = c
            return c

    def createIauracadAxis2Placement2D(self, p1, p2):
        key = str(p1.Coordinates) + str(p2.DirectionRatios)
        if self.compress and key in self.axis2placement2ds:
            self.spared += 1
            return self.axis2placement2ds[key]
        else:
            c = self.iauracadfile.createIauracadAxis2Placement2D(p1, p2)
            if self.compress:
                self.axis2placement2ds[key] = c
            return c

    def createIauracadLocalPlacement(self, gpl=None):
        if not gpl:
            gpl = self.createIauracadAxis2Placement3D()
        key = (
            str(gpl.Location.Coordinates)
            + str(gpl.Axis.DirectionRatios)
            + str(gpl.RefDirection.DirectionRatios)
        )
        if self.compress and key in self.localplacements:
            self.spared += 1
            return self.localplacements[key]
        else:
            c = self.iauracadfile.createIauracadLocalPlacement(None, gpl)
            if self.compress:
                self.localplacements[key] = c
            return c

    def createIauracadColourRgb(self, r, g, b):
        key = (r, g, b)
        if self.compress and key in self.rgbs:
            self.spared += 1
            return self.rgbs[key]
        else:
            c = self.iauracadfile.createIauracadColourRgb(None, r, g, b)
            if self.compress:
                self.rgbs[key] = c
            return c

    def createIauracadSurfaceStyleRendering(self, col, alpha=1):
        key = (col.Red, col.Green, col.Blue, alpha)
        if self.compress and key in self.ssrenderings:
            self.spared += 1
            return self.ssrenderings[key]
        else:
            if alpha == 1:
                alpha = None
            c = self.iauracadfile.createIauracadSurfaceStyleRendering(
                col, alpha, None, None, None, None, None, None, "FLAT"
            )
            if self.compress:
                self.ssrenderings[key] = c
            return c

    def createIauracadCartesianTransformationOperator3D(self, axis1, axis2, origin, scale, axis3):
        key = (
            str(axis1.DirectionRatios)
            + str(axis2.DirectionRatios)
            + str(origin.Coordinates)
            + str(scale)
            + str(axis3.DirectionRatios)
        )
        if self.compress and key in self.transformationoperators:
            self.spared += 1
            return self.transformationoperators[key]
        else:
            c = self.iauracadfile.createIauracadCartesianTransformationOperator3D(
                axis1, axis2, origin, scale, axis3
            )
            if self.compress:
                self.transformationoperators[key] = c
            return c

    def createIauracadSurfaceStyle(self, name, r, g, b, a=1):
        if name:
            key = name + str((r, g, b))
        else:
            key = str((r, g, b))
        if self.compress and key in self.sstyles:
            self.spared += 1
            return self.sstyles[key]
        else:
            col = self.createIauracadColourRgb(r, g, b)
            ssr = self.createIauracadSurfaceStyleRendering(col, a)
            c = self.iauracadfile.createIauracadSurfaceStyle(name, "BOTH", [ssr])
            if self.compress:
                self.sstyles[key] = c
            return c

    def createIauracadPresentationStyleAssignment(self, name, r, g, b, a=1, iauracad4=False):
        if name:
            key = name + str((r, g, b, a))
        else:
            key = str((r, g, b, a))
        if self.compress and key in self.psas:
            self.spared += 1
            return self.psas[key]
        else:
            iss = self.createIauracadSurfaceStyle(name, r, g, b, a)
            if iauracad4:
                c = iss
            else:
                c = self.iauracadfile.createIauracadPresentationStyleAssignment([iss])
            if self.compress:
                self.psas[key] = c
            return c

    def createIauracadRectangleProfileDef(self, name, mode, pt, b, h):
        key = "RECT" + str(name) + str(mode) + str(pt) + str(b) + str(h)
        if self.compress and self.mergeProfiles and key in self.profiledefs:
            return self.profiledefs[key]
        else:
            c = self.iauracadfile.createIauracadRectangleProfileDef(name, mode, pt, b, h)
            if self.compress and self.mergeProfiles:
                self.profiledefs[key] = c
            return c

    def createIauracadCircleProfileDef(self, name, mode, pt, r):
        key = "CIRC" + str(name) + str(mode) + str(pt) + str(r)
        if self.compress and self.mergeProfiles and key in self.profiledefs:
            return self.profiledefs[key]
        else:
            c = self.iauracadfile.createIauracadCircleProfileDef(name, mode, pt, r)
            if self.compress and self.mergeProfiles:
                self.profiledefs[key] = c
            return c

    def createIauracadEllipseProfileDef(self, name, mode, pt, majr, minr):
        key = "ELLI" + str(name) + str(mode) + str(pt) + str(majr) + str(minr)
        if self.compress and self.mergeProfiles and key in self.profiledefs:
            return self.profiledefs[key]
        else:
            c = self.iauracadfile.createIauracadEllipseProfileDef(name, mode, pt, majr, minr)
            if self.compress and self.mergeProfiles:
                self.profiledefs[key] = c
            return c
