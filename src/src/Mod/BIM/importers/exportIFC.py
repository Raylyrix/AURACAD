# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2014 Yorik van Havre <yorik@uncreated.net>              *
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

__title__ = "AuraCAD Iauracad export"
__author__ = ("Yorik van Havre", "Jonathan Wiedemann", "Bernd Hahnebach")
__url__ = "https://www.AuraCAD.org"

## @package exportIauracad
#  \ingroup ARCH
#  \brief Iauracad file format exporter
#
#  This module provides tools to export Iauracad files.

"""Provide the exporter for Iauracad files used above all in Arch and BIM.

Internally it uses IauracadOpenShell, which must be installed before using.
"""

import math
import os
import time
import tempfile
from builtins import open as pyopen

import AuraCAD
import AuraCADGui
import Arch
import Draft
import DraftVecUtils
import Part
import ArchIauracadSchema

from DraftGeomUtils import vec
from draftutils import params
from draftutils.messages import _msg, _err

from importers import exportIauracadHelper
from importers import exportIauracadStructuralTools
from importers.importIauracadHelper import dd2dms

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")

# Templates and other definitions ****
# Specific AuraCAD <-> Iauracad slang translations
translationtable = {
    "Foundation": "Footing",
    "Floor": "BuildingStorey",
    "Rebar": "ReinforcingBar",
    "HydroEquipment": "SanitaryTerminal",
    "ElectricEquipment": "ElectricAppliance",
    "Furniture": "FurnishingElement",
    "Stair Flight": "StairFlight",
    "Curtain Wall": "CurtainWall",
    "Pipe Segment": "PipeSegment",
    "Pipe Fitting": "PipeFitting",
    "VisGroup": "Group",
    "Undefined": "BuildingElementProxy",
}

# The base Iauracad template for export, the $variables will be substituted
# by specific information
iauracadtemplate = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
FILE_NAME('$filename','$timestamp',('$owner','$email'),('$company'),'IauracadOpenShell','IauracadOpenShell','');
FILE_SCHEMA(('$iauracadschema'));
ENDSEC;
DATA;
#1=IauracadPERSON($,$,'$owner',$,$,$,$,$);
#2=IauracadORGANIZATION($,'$company',$,$,$);
#3=IauracadPERSONANDORGANIZATION(#1,#2,$);
#4=IauracadAPPLICATION(#2,'$version','AuraCAD','118df2cf_ed21_438e_a41');
#5=IauracadOWNERHISTORY(#3,#4,$,.ADDED.,$now,#3,#4,$now);
#6=IauracadDIRECTION((1.,0.,0.));
#7=IauracadDIRECTION((0.,0.,1.));
#8=IauracadCARTESIANPOINT((0.,0.,0.));
#9=IauracadAXIS2PLACEMENT3D(#8,#7,#6);
#10=IauracadDIRECTION((0.,1.,0.));
#12=IauracadDIMENSIONALEXPONENTS(0,0,0,0,0,0,0);
#13=IauracadSIUNIT(*,.LENGTHUNIT.,$,.METRE.);
#14=IauracadSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);
#15=IauracadSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);
#16=IauracadSIUNIT(*,.PLANEANGLEUNIT.,$,.RADIAN.);
#17=IauracadMEASUREWITHUNIT(IauracadPLANEANGLEMEASURE(0.017453292519943295),#16);
#18=IauracadCONVERSIONBASEDUNIT(#12,.PLANEANGLEUNIT.,'DEGREE',#17);
ENDSEC;
END-ISO-10303-21;
"""


def _prepare_export_list_skipping_std_groups(initial_export_list, preferences_dict):
    """
    Builds the list of objects for Iauracad export. This function is called when the preference to skip
    standard groups is active. Standard AuraCAD groups (App::DocumentObjectGroup that would become
    IauracadGroup) are omitted from the returned list, and their children are processed. This includes
    children from their .Group property and also architecturally hosted elements (like windows in
    walls) if a child of the skipped group is a host.

    The re-parenting of children of a skipped AuraCAD group in the resulting Iauracad file is achieved
    implicitly:

    1. The skipped AuraCAD group itself is not converted into an Iauracad product. It will not exist as
        an IauracadGroup or IauracadElementAssembly in the Iauracad file.
    2. Children of the skipped group (and architecturally hosted elements like windows within walls
       that were part of the skipped group's content) are processed and converted into their
       respective Iauracad products.
    3. These Iauracad products, initially "orphaned" from the skipped AuraCAD group's potential Iauracad
       representation, are then handled by the exporter's subsequent spatial relationship logic.
       This logic typically assigns such "untreated" elements to the current or default Iauracad spatial
       container (e.g., an IauracadBuildingStorey if the skipped group was under a Level).

    The net effect is that the children appear directly contained within the Iauracad representation of
    the skipped group's parent container.
    """
    all_potential_objects = Arch.get_architectural_contents(
        initial_export_list,
        recursive=True,
        discover_hosted_elements=True,
        include_components_from_additions=True,
        include_initial_objects_in_result=True,
    )

    final_objects_for_processing = []

    for obj in all_potential_objects:
        is_std_group_to_skip = False
        # Determine if the current object is a standard AuraCAD group that should be skipped
        if obj.isDerivedFrom("App::DocumentObjectGroup"):
            # Check its potential Iauracad type; only skip if it would become a generic IauracadGroup
            potential_iAuraCAD_type = getIauracadTypeFromObj(obj)
            if potential_iAuraCAD_type == "IauracadGroup":
                is_std_group_to_skip = True

        if not is_std_group_to_skip:
            if obj not in final_objects_for_processing:  # Ensure uniqueness
                final_objects_for_processing.append(obj)
        elif preferences_dict["DEBUG"]:
            print(
                f"DEBUG: Iauracad Exporter: StdGroup '{obj.Label}' ({obj.Name}) "
                "was identified by get_architectural_contents but is now being filtered out."
            )

    return final_objects_for_processing


def getPreferences():
    """Retrieve the Iauracad preferences available in import and export."""

    import iauracadopenshell

    iauracadunit = params.get_param_arch("iauracadUnit")

    # Factor to multiply the dimension in millimeters
    # mm x 0.001 = metre
    # mm x 0.00328084 = foot
    # mm x 0.03937008 = inch

    # The only real use of these units is to make Revit choose which mode
    # to work with.
    #
    # Inch is not yet implemented, and I don't even know if it is actually
    # desired

    f = 0.001
    u = "metre"

    if iauracadunit == 1:
        f = 0.00328084
        u = "foot"

    # if iauracadunit == 2:
    #     f = 0.03937008
    #     u = "inch"

    # Be careful with setting ADD_DEFAULT_SITE, ADD_DEFAULT_BUILDING,
    # and ADD_DEFAULT_STOREY to False. If this is done the spatial structure
    # may no longer be fully connected to the `IauracadProject`. This means
    # some objects may be "unreferenced" and won't belong to the `IauracadProject`.
    # Some applications may fail at importing these unreferenced objects.
    preferences = {
        "DEBUG": params.get_param_arch("iauracadDebug"),
        "CREATE_CLONES": params.get_param_arch("iauracadCreateClones"),
        "FORCE_BREP": params.get_param_arch("iauracadExportAsBrep"),
        "STORE_UID": params.get_param_arch("iauracadStoreUid"),
        "SERIALIZE": params.get_param_arch("iauracadSerialize"),
        "EXPORT_2D": params.get_param_arch("iauracadExport2D"),
        "FULL_PARAMETRIC": params.get_param_arch("IauracadExportAuraCADProperties"),
        "ADD_DEFAULT_SITE": params.get_param_arch("IauracadAddDefaultSite"),
        "ADD_DEFAULT_BUILDING": params.get_param_arch("IauracadAddDefaultBuilding"),
        "ADD_DEFAULT_STOREY": params.get_param_arch("IauracadAddDefaultStorey"),
        "IAuraCAD_UNIT": u,
        "SCALE_FACTOR": f,
        "GET_STANDARD": params.get_param_arch("getStandardType"),
        "EXPORT_MODEL": ["arch", "struct", "hybrid"][params.get_param_arch("iauracadExportModel")],
        "GROUPS_AS_ASSEMBLIES": params.get_param_arch("IauracadGroupsAsAssemblies"),
        "IGNORE_STD_GROUPS": not params.get_param_arch("IauracadExportStdGroups"),
    }

    # get iauracadopenshell version
    iauracados_version = 0.0
    if hasattr(iauracadopenshell, "version"):
        if iauracadopenshell.version.startswith("0"):
            iauracados_version = float(iauracadopenshell.version[:3])  # < 0.6
        elif iauracadopenshell.version.startswith("v"):
            iauracados_version = float(iauracadopenshell.version[1:4])  # 0.7
        else:
            print(
                "Could not retrieve IauracadOpenShell version. Version is set to {}".format(
                    iauracados_version
                )
            )
    else:
        print("Could not retrieve IauracadOpenShell version. Version is set to {}".format(iauracados_version))

    # set schema
    if hasattr(iauracadopenshell, "schema_identifier"):
        schema = iauracadopenshell.schema_identifier
    else:
        # v0.6 onwards allows one to set our own schema
        schema = PARAMS.GetString("DefaultIauracadExportVersion", "Iauracad4")
    preferences["SCHEMA"] = schema

    return preferences


def export(exportList, filename, colors=None, preferences=None):
    """Export the selected objects to Iauracad format.

    Parameters
    ----------
    colors:
        It defaults to `None`.
        It is an optional dictionary of `objName:shapeColorTuple`
        or `objName:diffuseColorList` elements to be used in non-GUI mode
        if you want to be able to export colors.
    """
    try:
        global iauracadopenshell
        import iauracadopenshell
    except ModuleNotFoundError:
        _err(
            "IauracadOpenShell was not found on this system. "
            "Iauracad support is disabled.\n"
            "Visit https://wiki.AuraCAD.org/IauracadOpenShell "
            "to learn about installing it."
        )
        return
    from iauracadopenshell import guid

    if str(filename).lower().endswith("json"):
        import json

        try:
            from iauracadjson import iauracad2json5a
        except Exception:
            try:
                import iauracad2json5a
            except Exception:
                _err("Error: Unable to locate iauracad2json5a module. Aborting.")
                return

    starttime = time.time()

    global iauracadfile, surfstyles, clones, sharedobjects, profiledefs, shapedefs, uids, template, curvestyles

    if preferences is None:
        preferences = getPreferences()

    existing_file = False
    if isinstance(filename, iauracadopenshell.file):
        iauracadfile = filename
        existing_file = True
    else:
        # process template

        version = AuraCAD.Version()
        owner = AuraCAD.ActiveDocument.CreatedBy
        email = ""
        if ("@" in owner) and ("<" in owner):
            s = owner.split("<")
            owner = s[0].strip()
            email = s[1].strip(">")

        template = iauracadtemplate.replace(
            "$version", version[0] + "." + version[1] + " build " + version[2]
        )
        if preferences["DEBUG"]:
            print("Exporting an", preferences["SCHEMA"], "file...")
        template = template.replace("$iauracadschema", preferences["SCHEMA"])
        template = template.replace("$owner", owner)
        template = template.replace("$company", AuraCAD.ActiveDocument.Company)
        template = template.replace("$email", email)
        template = template.replace("$now", str(int(time.time())))
        template = template.replace("$filename", os.path.basename(filename))
        template = template.replace(
            "$timestamp", str(time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()))
        )
        if hasattr(iauracadopenshell, "version"):
            template = template.replace("IauracadOpenShell", "IauracadOpenShell " + iauracadopenshell.version)
        templatefilehandle, templatefile = tempfile.mkstemp(suffix=".iauracad")
        of = pyopen(templatefile, "w")

        of.write(template)
        of.close()
        os.close(templatefilehandle)

        # create Iauracad file

        iauracadfile = iauracadopenshell.open(templatefile)
        iauracadfile = exportIauracadHelper.writeUnits(iauracadfile, preferences["IAuraCAD_UNIT"])

    history = iauracadfile.by_type("IauracadOwnerHistory")
    if history:
        history = history[0]
    else:
        # Iauracad4 allows one to not write any history
        history = None

    if preferences["IGNORE_STD_GROUPS"]:
        if preferences["DEBUG"]:
            print("Iauracad Export: Skipping standard AuraCAD groups and processing their children.")
        objectslist = _prepare_export_list_skipping_std_groups(exportList, preferences)
    else:
        objectslist = Draft.get_group_contents(exportList, walls=True, addgroups=True)

    # separate 2D and special objects. Special objects provide their own Iauracad export method

    annotations = []
    specials = []
    for obj in objectslist:
        if (
            obj.isDerivedFrom("Part::Part2DObject")
            or obj.isDerivedFrom("App::Annotation")
            or Draft.getType(obj)
            in [
                "BezCurve",
                "BSpline",
                "Wire",
                "DraftText",
                "Text",
                "Dimension",
                "LinearDimension",
                "AngularDimension",
            ]
        ):
            annotations.append(obj)
        elif hasattr(obj, "Proxy") and hasattr(obj.Proxy, "export_iauracad"):
            specials.append(obj)
        elif obj.isDerivedFrom("Part::Feature"):
            if obj.Shape and (not obj.Shape.Solids) and obj.Shape.Edges:
                if not obj.Shape.Faces:
                    annotations.append(obj)
                elif (
                    (obj.Shape.BoundBox.XLength < 0.0001)
                    or (obj.Shape.BoundBox.YLength < 0.0001)
                    or (obj.Shape.BoundBox.ZLength < 0.0001)
                ):
                    annotations.append(obj)

    # clean objects list of unwanted types

    objectslist = [obj for obj in objectslist if obj not in annotations]
    objectslist = [obj for obj in objectslist if obj not in specials]
    objectslist = Arch.pruneIncluded(objectslist, strict=True)
    objectslist = [
        obj
        for obj in objectslist
        if Draft.getType(obj)
        not in ["Dimension", "Material", "MaterialContainer", "WorkingPlaneProxy"]
    ]

    # Note that the Draft.get_group_contents() function used later will also find children.
    # Duplicate processing is avoided with the treated list.
    if preferences["FULL_PARAMETRIC"]:
        objectslist = Arch.getAllChildren(objectslist)

    # create project, context and geodata settings

    if existing_file:
        project = iauracadfile.by_type("IauracadProject")[0]
        body_contexts = [
            c
            for c in iauracadfile.by_type("IauracadGeometricRepresentationSubContext")
            if c.ContextIdentifier in ["Body", "Facetation"]
        ]
        body_contexts.extend(
            [
                c
                for c in iauracadfile.by_type(
                    "IauracadGeometricRepresentationContext", include_subtypes=False
                )
                if c.ContextType == "Model"
            ]
        )
        context = body_contexts[
            0
        ]  # we take the first one (subcontext if existing, or context if not)
    else:
        contextCreator = exportIauracadHelper.ContextCreator(iauracadfile, objectslist)
        context = contextCreator.model_view_subcontext
        project = contextCreator.project
        objectslist = [obj for obj in objectslist if obj != contextCreator.project_object]

        if Draft.getObjectsOfType(
            objectslist, "Site"
        ):  # we assume one site and one representation context only
            decl = Draft.getObjectsOfType(objectslist, "Site")[0].Declination.getValueAs(
                AuraCAD.Units.Radian
            )
            contextCreator.model_context.TrueNorth.DirectionRatios = (
                math.cos(decl + math.pi / 2),
                math.sin(decl + math.pi / 2),
            )

    # reusable entity system

    global iauracadbin
    iauracadbin = exportIauracadHelper.recycler(iauracadfile, template=not existing_file)

    # setup analytic model

    if preferences["EXPORT_MODEL"] in ["struct", "hybrid"]:
        exportIauracadStructuralTools.setup(iauracadfile, iauracadbin, preferences["SCALE_FACTOR"])

    # define holders for the different types we create

    products = {}  # { Name: IauracadEntity, ... }
    subproducts = (
        {}
    )  # { Name: IauracadEntity, ... } for storing additions/subtractions and other types of subcomponents of a product
    surfstyles = {}  # { (r,g,b): IauracadEntity, ... }
    clones = {}  # { Basename:[Clonename1,Clonename2,...] }
    sharedobjects = {}  # { BaseName: IauracadRepresentationMap }
    count = 1
    groups = {}  # { Host: [Child,Child,...] }
    profiledefs = {}  # { ProfileDefString:profiledef,...}
    shapedefs = {}  # { ShapeDefString:[shapes],... }
    spatialelements = {}  # {Name:IauracadEntity, ... }
    uids = (
        []
    )  # store used UIDs to avoid reuse (some AuraCAD objects might have same Iauracad UID, ex. copy/pasted objects
    classifications = {}  # {Name:IauracadEntity, ... }
    curvestyles = {}

    # build clones table

    if preferences["CREATE_CLONES"]:
        for o in objectslist:
            b = Draft.getCloneBase(o, strict=True)
            if b:
                clones.setdefault(b.Name, []).append(o.Name)

    # print("clones table: ",clones)
    # print(objectslist)

    # testing if more than one site selected (forbidden in Iauracad)
    # TODO: Moult: This is not forbidden in Iauracad.

    if len(Draft.getObjectsOfType(objectslist, "Site")) > 1:
        AuraCAD.Console.PrintError(
            "More than one site is selected, which is forbidden by Iauracad standards. Please export only one site by Iauracad file.\n"
        )
        return

    # products

    for obj in objectslist:

        if obj.Name in products:
            # never export same product twice
            continue

        # structural analysis object

        structobj = None
        if preferences["EXPORT_MODEL"] in ["struct", "hybrid"]:
            structobj = exportIauracadStructuralTools.createStructuralMember(iauracadfile, iauracadbin, obj)
            if preferences["EXPORT_MODEL"] == "struct":
                continue

        # getting generic data

        name = getText("Name", obj)
        description = getText("Description", obj)
        uid = getUID(obj, preferences)
        iauracadtype = getIauracadTypeFromObj(obj)
        # print(iauracadtype)

        # handle assemblies (arrays, app::parts, references, etc...)

        assemblyElements = []
        assemblyTypes = ["IauracadApp::Part", "IauracadPart::Compound", "IauracadElementAssembly"]
        is_nested_group = False
        if preferences["GROUPS_AS_ASSEMBLIES"] and iauracadtype == "IauracadGroup":
            for p in obj.InListRecursive:
                if not p.isDerivedFrom("App::DocumentObjectGroup"):
                    is_nested_group = True

        if iauracadtype == "IauracadArray":
            clonedeltas = []
            if obj.ArrayType == "ortho":
                for i in range(obj.NumberX):
                    clonedeltas.append(obj.Placement.Base + (i * obj.IntervalX))
                    for j in range(obj.NumberY):
                        if j > 0:
                            clonedeltas.append(
                                obj.Placement.Base + (i * obj.IntervalX) + (j * obj.IntervalY)
                            )
                        for k in range(obj.NumberZ):
                            if k > 0:
                                clonedeltas.append(
                                    obj.Placement.Base
                                    + (i * obj.IntervalX)
                                    + (j * obj.IntervalY)
                                    + (k * obj.IntervalZ)
                                )
            if clonedeltas:
                iauracadtype = "IauracadElementAssembly"
                for delta in clonedeltas:
                    # print("delta: {}".format(delta))
                    representation, placement, shapetype = getRepresentation(
                        iauracadfile,
                        context,
                        obj.Base,
                        forcebrep=(getBrepFlag(obj.Base, preferences)),
                        colors=colors,
                        preferences=preferences,
                        forceclone=delta,
                    )
                    subproduct = createProduct(
                        iauracadfile,
                        obj.Base,
                        getIauracadTypeFromObj(obj.Base),
                        getUID(obj.Base, preferences),
                        history,
                        getText("Name", obj.Base),
                        getText("Description", obj.Base),
                        placement,
                        representation,
                        preferences,
                    )
                    products[obj.Base.Name] = subproduct
                    assemblyElements.append(subproduct)
                    exportIauracadHelper.writeQuantities(
                        iauracadfile, obj.Base, subproduct, history, preferences["SCALE_FACTOR"]
                    )

        elif iauracadtype in assemblyTypes or is_nested_group:
            if hasattr(obj, "Group"):
                group = obj.Group
            elif hasattr(obj, "Links"):
                group = obj.Links
            else:
                group = [AuraCAD.ActiveDocument.getObject(n[:-1]) for n in obj.getSubObjects()]
            for subobj in group:
                if subobj.Name in products:
                    subproduct = products[subobj.Name]
                else:
                    representation, placement, shapetype = getRepresentation(
                        iauracadfile,
                        context,
                        subobj,
                        forcebrep=(getBrepFlag(subobj, preferences)),
                        colors=colors,
                        preferences=preferences,
                    )
                    subproduct = createProduct(
                        iauracadfile,
                        subobj,
                        getIauracadTypeFromObj(subobj),
                        getUID(subobj, preferences),
                        history,
                        getText("Name", subobj),
                        getText("Description", subobj),
                        placement,
                        representation,
                        preferences,
                    )
                    products[subobj.Name] = subproduct
                assemblyElements.append(subproduct)
            iauracadtype = "IauracadElementAssembly"

        # export grids

        if iauracadtype in ["IauracadAxis", "IauracadAxisSystem", "IauracadGrid"]:
            iauracadaxes = []
            iauracadpols = []
            if iauracadtype == "IauracadAxis":
                # make sure this axis is not included in something else already
                standalone = True
                for p in obj.InList:
                    if hasattr(p, "Axes") and (obj in p.Axes):
                        if p in objectslist:
                            axgroups = []
                            standalone = False
                            break
                if standalone:
                    axgroups = [obj.Proxy.getAxisData(obj)]
            else:
                axgroups = obj.Proxy.getAxisData(obj)
            if not axgroups:
                if preferences["DEBUG"]:
                    print(
                        "Warning! Axis system object found '{}', but no axis data found.".format(
                            obj.Label
                        )
                    )
                continue
            iauracadtype = "IauracadGrid"
            for axg in axgroups:
                iauracadaxg = []
                for ax in axg:
                    p1 = iauracadbin.createIauracadCartesianPoint(
                        tuple(AuraCAD.Vector(ax[0]).multiply(preferences["SCALE_FACTOR"])[:2])
                    )
                    p2 = iauracadbin.createIauracadCartesianPoint(
                        tuple(AuraCAD.Vector(ax[1]).multiply(preferences["SCALE_FACTOR"])[:2])
                    )
                    pol = iauracadbin.createIauracadPolyline([p1, p2])
                    iauracadpols.append(pol)
                    axis = iauracadfile.createIauracadGridAxis(ax[2], pol, True)
                    iauracadaxg.append(axis)
                if len(iauracadaxes) < 3:
                    iauracadaxes.append(iauracadaxg)
                else:
                    iauracadaxes[2] = iauracadaxes[2] + iauracadaxg  # IauracadGrid can have max 3 axes systems
            u = None
            v = None
            w = None
            if iauracadaxes:
                u = iauracadaxes[0]
            if len(iauracadaxes) > 1:
                v = iauracadaxes[1]
            if len(iauracadaxes) > 2:
                w = iauracadaxes[2]
            if u and v:
                if preferences["DEBUG"]:
                    print(
                        str(count).ljust(3),
                        " : ",
                        iauracadtype,
                        " (",
                        str(len(iauracadpols)),
                        "axes ) : ",
                        name,
                    )
                xvc = iauracadbin.createIauracadDirection((1.0, 0.0, 0.0))
                zvc = iauracadbin.createIauracadDirection((0.0, 0.0, 1.0))
                ovc = iauracadbin.createIauracadCartesianPoint((0.0, 0.0, 0.0))
                gpl = iauracadbin.createIauracadAxis2Placement3D(ovc, zvc, xvc)
                plac = iauracadbin.createIauracadLocalPlacement(gpl)
                cset = iauracadfile.createIauracadGeometricCurveSet(iauracadpols)
                # subc = iauracadfile.createIauracadGeometricRepresentationSubContext('FootPrint','Model',context,None,"MODEL_VIEW",None,None,None,None,None)
                srep = iauracadfile.createIauracadShapeRepresentation(
                    context, "FootPrint", "GeometricCurveSet", iauracadpols
                )
                pdef = iauracadfile.createIauracadProductDefinitionShape(None, None, [srep])
                grid = iauracadfile.createIauracadGrid(
                    uid, history, name, description, None, plac, pdef, u, v, w
                )
                products[obj.Name] = grid
                count += 1
            else:
                if preferences["DEBUG"]:
                    print(
                        "Warning! Axis system object '{}' only contains one set of axis but at least two are needed for a IauracadGrid to be added to Iauracad.".format(
                            obj.Label
                        )
                    )
            continue

        # gather groups

        if iauracadtype == "IauracadGroup":
            groups[obj.Name] = [o.Name for o in obj.Group]
            continue

        if iauracadtype not in ArchIauracadSchema.IauracadProducts:
            iauracadtype = "IauracadBuildingElementProxy"

        # getting the representation

        # ignore the own shape for assembly objects
        skipshape = False
        if assemblyElements:
            # print("Assembly object: {}, thus own Shape will have no representation.".format(obj.Name))
            skipshape = True

        representation, placement, shapetype = getRepresentation(
            iauracadfile,
            context,
            obj,
            forcebrep=(getBrepFlag(obj, preferences)),
            colors=colors,
            preferences=preferences,
            skipshape=skipshape,
        )
        if preferences["GET_STANDARD"]:
            if isStandardCase(obj, iauracadtype):
                iauracadtype += "StandardCase"

        if preferences["DEBUG"]:
            print(str(count).ljust(3), " : ", iauracadtype, " (", shapetype, ") : ", name)

        # creating the product

        product = createProduct(
            iauracadfile,
            obj,
            iauracadtype,
            uid,
            history,
            name,
            description,
            placement,
            representation,
            preferences,
        )

        products[obj.Name] = product
        if iauracadtype in ["IauracadBuilding", "IauracadBuildingStorey", "IauracadSite", "IauracadSpace"]:
            spatialelements[obj.Name] = product

        # associate with structural analysis object if any

        if structobj:
            exportIauracadStructuralTools.associates(iauracadfile, product, structobj)

        # gather assembly subelements

        if assemblyElements:
            if is_nested_group:
                aname = "AuraCADGroup"
            else:
                aname = "Assembly"
            iauracadfile.createIauracadRelAggregates(
                iauracadopenshell.guid.new(), history, aname, "", products[obj.Name], assemblyElements
            )
            if preferences["DEBUG"]:
                print("      aggregating", len(assemblyElements), "object(s)")

        # additions

        if hasattr(obj, "Additions") and (shapetype in ["extrusion", "no shape"]):
            for o in obj.Additions:
                r2, p2, c2 = getRepresentation(
                    iauracadfile, context, o, colors=colors, preferences=preferences
                )
                if preferences["DEBUG"]:
                    print("      adding ", c2, " : ", o.Label)
                l = o.Label
                prod2 = iauracadfile.createIauracadBuildingElementProxy(
                    iauracadopenshell.guid.new(), history, l, None, None, p2, r2, None, "ELEMENT"
                )
                subproducts[o.Name] = prod2
                iauracadfile.createIauracadRelAggregates(
                    iauracadopenshell.guid.new(), history, "Addition", "", product, [prod2]
                )

        # subtractions

        guests = []
        for o in obj.InList:
            if hasattr(o, "Hosts"):
                for co in o.Hosts:
                    if co == obj:
                        if o not in guests:
                            guests.append(o)
        if hasattr(obj, "Subtractions") and (shapetype in ["extrusion", "no shape"]):
            for o in obj.Subtractions + guests:
                r2, p2, c2 = getRepresentation(
                    iauracadfile, context, o, subtraction=True, colors=colors, preferences=preferences
                )
                if preferences["DEBUG"]:
                    print("      subtracting ", c2, " : ", o.Label)
                l = o.Label
                prod2 = iauracadfile.createIauracadOpeningElement(
                    iauracadopenshell.guid.new(), history, l, None, None, p2, r2, None
                )
                subproducts[o.Name] = prod2
                iauracadfile.createIauracadRelVoidsElement(
                    iauracadopenshell.guid.new(), history, "Subtraction", "", product, prod2
                )

        # properties

        iauracadprop = False
        if hasattr(obj, "IauracadProperties"):

            if obj.IauracadProperties:

                iauracadprop = True

                if isinstance(obj.IauracadProperties, dict):

                    # IauracadProperties is a dictionary (AuraCAD 0.18)

                    psets = {}
                    for key, value in obj.IauracadProperties.items():
                        pset, pname, ptype, pvalue = getPropertyData(key, value, preferences)
                        if pvalue is None:
                            if preferences["DEBUG"]:
                                print("      property ", pname, " ignored because no value found.")
                            continue
                        p = iauracadbin.createIauracadPropertySingleValue(str(pname), str(ptype), pvalue)
                        psets.setdefault(pset, []).append(p)
                    for pname, props in psets.items():
                        pset = iauracadfile.createIauracadPropertySet(
                            iauracadopenshell.guid.new(), history, pname, None, props
                        )
                        iauracadfile.createIauracadRelDefinesByProperties(
                            iauracadopenshell.guid.new(), history, None, None, [product], pset
                        )

                elif obj.IauracadProperties.TypeId == "Spreadsheet::Sheet":

                    # IauracadProperties is a spreadsheet (deprecated)

                    sheet = obj.IauracadProperties
                    propertiesDic = {}
                    categories = []
                    n = 2
                    cell = True
                    while cell is True:
                        if hasattr(sheet, "A" + str(n)):
                            cat = sheet.get("A" + str(n))
                            key = sheet.get("B" + str(n))
                            tp = sheet.get("C" + str(n))
                            if hasattr(sheet, "D" + str(n)):
                                val = sheet.get("D" + str(n))
                            else:
                                val = ""
                            key = str(key)
                            tp = str(tp)
                            if tp in [
                                "IauracadLabel",
                                "IauracadText",
                                "IauracadIdentifier",
                                "IauracadDescriptiveMeasure",
                            ]:
                                val = val.encode("utf8")
                            elif tp == "IauracadBoolean":
                                if val == "True":
                                    val = True
                                else:
                                    val = False
                            elif tp == "IauracadInteger":
                                val = int(val)
                            else:
                                val = float(val)
                            unit = None
                            # unit = sheet.get('E'+str(n))
                            if cat in categories:
                                propertiesDic[cat].append(
                                    {"key": key, "tp": tp, "val": val, "unit": unit}
                                )
                            else:
                                propertiesDic[cat] = [
                                    {"key": key, "tp": tp, "val": val, "unit": unit}
                                ]
                                categories.append(cat)
                            n += 1
                        else:
                            cell = False
                    for cat in propertiesDic:
                        props = []
                        for prop in propertiesDic[cat]:
                            if preferences["DEBUG"]:
                                print("key", prop["key"], type(prop["key"]))
                                print("tp", prop["tp"], type(prop["tp"]))
                                print("val", prop["val"], type(prop["val"]))
                            if tp.lower().startswith("iauracad"):
                                props.append(
                                    iauracadbin.createIauracadPropertySingleValue(
                                        prop["key"], prop["tp"], prop["val"]
                                    )
                                )
                            else:
                                print("Unable to create a property of type:", tp)
                        if props:
                            pset = iauracadfile.createIauracadPropertySet(
                                iauracadopenshell.guid.new(), history, cat, None, props
                            )
                            iauracadfile.createIauracadRelDefinesByProperties(
                                iauracadopenshell.guid.new(), history, None, None, [product], pset
                            )

        if hasattr(obj, "IauracadData"):

            if obj.IauracadData:
                iauracadprop = True
                # if preferences['DEBUG'] : print("      adding iauracad attributes")
                props = []
                for key in obj.IauracadData:
                    if not (
                        key
                        in [
                            "attributes",
                            "complex_attributes",
                            "IauracadUID",
                            "FlagForceBrep",
                            "ExportHeight",
                            "ExportWidth",
                            "ExportLength",
                            "ExportHorizontalArea",
                            "ExportVerticalArea",
                            "ExportVolume",
                        ]
                    ):

                        # (deprecated) properties in IauracadData dict are stored as "key":"type(value)"

                        r = obj.IauracadData[key].strip(")").split("(")
                        if len(r) == 1:
                            tp = "IauracadText"
                            val = r[0]
                        else:
                            tp = r[0]
                            val = "(".join(r[1:])
                            val = val.strip("'")
                            val = val.strip('"')
                            # if preferences['DEBUG']: print("      property ",key," : ",val.encode("utf8"), " (", str(tp), ")")
                            if tp in [
                                "IauracadLabel",
                                "IauracadText",
                                "IauracadIdentifier",
                                "IauracadDescriptiveMeasure",
                            ]:
                                pass
                            elif tp == "IauracadBoolean":
                                if val == ".T.":
                                    val = True
                                else:
                                    val = False
                            elif tp == "IauracadInteger":
                                val = int(val)
                            else:
                                val = float(val)
                        props.append(iauracadbin.createIauracadPropertySingleValue(str(key), str(tp), val))
                if props:
                    pset = iauracadfile.createIauracadPropertySet(
                        iauracadopenshell.guid.new(), history, "PropertySet", None, props
                    )
                    iauracadfile.createIauracadRelDefinesByProperties(
                        iauracadopenshell.guid.new(), history, None, None, [product], pset
                    )

        if not iauracadprop:
            # if preferences['DEBUG'] : print("no iauracad properties to export")
            pass

        # Quantities

        exportIauracadHelper.writeQuantities(iauracadfile, obj, product, history, preferences["SCALE_FACTOR"])

        if preferences["FULL_PARAMETRIC"]:

            # exporting all the object properties

            AuraCADProps = []
            AuraCADGuiProps = []
            AuraCADProps.append(
                iauracadbin.createIauracadPropertySingleValue("AuraCADType", "IauracadText", obj.TypeId)
            )
            AuraCADProps.append(
                iauracadbin.createIauracadPropertySingleValue("AuraCADName", "IauracadText", obj.Name)
            )
            sets = [("App", obj)]
            if hasattr(obj, "Proxy"):
                if obj.Proxy:
                    AuraCADProps.append(
                        iauracadbin.createIauracadPropertySingleValue(
                            "AuraCADAppObject", "IauracadText", str(obj.Proxy.__class__)
                        )
                    )
            if AuraCAD.GuiUp:
                if obj.ViewObject:
                    sets.append(("Gui", obj.ViewObject))
                    if hasattr(obj.ViewObject, "Proxy"):
                        if obj.ViewObject.Proxy:
                            AuraCADGuiProps.append(
                                iauracadbin.createIauracadPropertySingleValue(
                                    "AuraCADGuiObject",
                                    "IauracadText",
                                    str(obj.ViewObject.Proxy.__class__),
                                )
                            )
            for realm, ctx in sets:
                if ctx:
                    for prop in ctx.PropertiesList:
                        if not (
                            prop
                            in [
                                "IauracadProperties",
                                "IauracadData",
                                "Shape",
                                "Proxy",
                                "ExpressionEngine",
                                "AngularDeflection",
                                "BoundingBox",
                            ]
                        ):
                            try:
                                ptype = ctx.getTypeIdOfProperty(prop)
                            except AttributeError:
                                ptype = "Unknown"
                            itype = None
                            ivalue = None
                            if ptype in ["App::PropertyString", "App::PropertyEnumeration"]:
                                itype = "IauracadText"
                                ivalue = getattr(ctx, prop)
                            elif ptype == "App::PropertyInteger":
                                itype = "IauracadInteger"
                                ivalue = getattr(ctx, prop)
                            elif ptype == "App::PropertyFloat":
                                itype = "IauracadReal"
                                ivalue = float(getattr(ctx, prop))
                            elif ptype == "App::PropertyBool":
                                itype = "IauracadBoolean"
                                ivalue = getattr(ctx, prop)
                            elif ptype in ["App::PropertyVector", "App::PropertyPlacement"]:
                                itype = "IauracadText"
                                ivalue = str(getattr(ctx, prop))
                            elif ptype in ["App::PropertyLength", "App::PropertyDistance"]:
                                itype = "IauracadReal"
                                ivalue = float(getattr(ctx, prop).getValueAs("m"))
                            elif ptype == "App::PropertyArea":
                                itype = "IauracadReal"
                                ivalue = float(getattr(ctx, prop).getValueAs("m^2"))
                            elif ptype == "App::PropertyLink":
                                t = getattr(ctx, prop)
                                if t:
                                    itype = "IauracadText"
                                    ivalue = "AuraCADLink_" + t.Name
                            else:
                                if preferences["DEBUG"]:
                                    print("Unable to encode property ", prop, " of type ", ptype)
                            if itype:
                                # TODO add description
                                if realm == "Gui":
                                    AuraCADGuiProps.append(
                                        iauracadbin.createIauracadPropertySingleValue(
                                            "AuraCADGui_" + prop, itype, ivalue
                                        )
                                    )
                                else:
                                    AuraCADProps.append(
                                        iauracadbin.createIauracadPropertySingleValue(
                                            "AuraCAD_" + prop, itype, ivalue
                                        )
                                    )
            if AuraCADProps:
                pset = iauracadfile.createIauracadPropertySet(
                    iauracadopenshell.guid.new(), history, "AuraCADPropertySet", None, AuraCADProps
                )
                iauracadfile.createIauracadRelDefinesByProperties(
                    iauracadopenshell.guid.new(), history, None, None, [product], pset
                )
            if AuraCADGuiProps:
                pset = iauracadfile.createIauracadPropertySet(
                    iauracadopenshell.guid.new(), history, "AuraCADGuiPropertySet", None, AuraCADGuiProps
                )
                iauracadfile.createIauracadRelDefinesByProperties(
                    iauracadopenshell.guid.new(), history, None, None, [product], pset
                )

        # Classifications

        classification = getattr(obj, "StandardCode", "")
        if classification:
            name, code = classification.split(" ", 1)
            if name in classifications:
                system = classifications[name]
            else:
                system = iauracadfile.createIauracadClassification(None, None, None, name)
                classifications[name] = system
            for ref in getattr(system, "HasReferences", []):
                if code.startswith(ref.Name):
                    break
            else:
                ref = iauracadfile.createIauracadClassificationReference(None, code, None, system)
            if getattr(ref, "ClassificationRefForObjects", None):
                rel = ref.ClassificationRefForObjects[0]
                rel.RelatedObjects = rel.RelatedObjects + [product]
            else:
                rel = iauracadfile.createIauracadRelAssociatesClassification(
                    iauracadopenshell.guid.new(),
                    history,
                    "AuraCADClassificationRel",
                    None,
                    [product],
                    ref,
                )

        count += 1

    # relate structural analysis objects to the struct model

    if preferences["EXPORT_MODEL"] in ["struct", "hybrid"]:
        exportIauracadStructuralTools.createStructuralGroup(iauracadfile)

    # relationships

    sites = []
    buildings = []
    floors = []
    treated = []
    defaulthost = []

    # buildingParts can be exported as any "normal" Iauracad type. In that case, gather their elements first
    # if iauracad type is "Undefined" gather elements too

    for bp in Draft.getObjectsOfType(objectslist, "BuildingPart"):
        if bp.IauracadType not in ["Site", "Building", "Building Storey", "Space"]:
            if bp.Name in products:
                subs = []
                for c in bp.Group:
                    if c.Name in products:
                        subs.append(products[c.Name])
                        treated.append(c.Name)
                if subs:
                    iauracadfile.createIauracadRelAggregates(
                        iauracadopenshell.guid.new(), history, "Assembly", "", products[bp.Name], subs
                    )

    # storeys

    for floor in Draft.getObjectsOfType(objectslist, "Floor") + Draft.getObjectsOfType(
        objectslist, "BuildingPart"
    ):
        if (Draft.getType(floor) == "Floor") or (
            hasattr(floor, "IauracadType") and floor.IauracadType == "Building Storey"
        ):
            f = products[floor.Name]
            floors.append(f)
            defaulthost = f
            treated.append(floor.Name)

            # objs will include the floor itself, we avoid duplicate processing with the treated list.
            objs = Draft.get_group_contents(floor, walls=True, addgroups=True)
            objs = Arch.pruneIncluded(objs)
            buildingelements = []
            spaces = []
            for c in objs:
                if c.Name not in treated and c.Name in products:
                    prod = products[c.Name]
                    if prod.is_a() == "IauracadSpace":
                        spaces.append(prod)
                    else:
                        buildingelements.append(prod)
                    treated.append(c.Name)
            if buildingelements:
                iauracadfile.createIauracadRelContainedInSpatialStructure(
                    iauracadopenshell.guid.new(), history, "StoreyLink", "", buildingelements, f
                )
            if spaces:
                iauracadfile.createIauracadRelAggregates(
                    iauracadopenshell.guid.new(), history, "StoreyLink", "", f, spaces
                )

    # buildings

    for building in Draft.getObjectsOfType(objectslist, "Building") + Draft.getObjectsOfType(
        objectslist, "BuildingPart"
    ):
        if (Draft.getType(building) == "Building") or (
            hasattr(building, "IauracadType") and building.IauracadType == "Building"
        ):
            b = products[building.Name]
            buildings.append(b)
            if not defaulthost and not preferences["ADD_DEFAULT_STOREY"]:
                defaulthost = b
            treated.append(building.Name)

            # objs will include the building itself, we avoid duplicate processing with the treated list.
            objs = Draft.get_group_contents(building, walls=True, addgroups=True)
            objs = Arch.pruneIncluded(objs)
            children = []
            childfloors = []
            for c in objs:
                if c.Name not in treated and c.Name in products:
                    if Draft.getType(c) in ["Floor", "BuildingPart", "Space"]:
                        childfloors.append(products[c.Name])
                        treated.append(c.Name)
                    else:
                        children.append(products[c.Name])
                        treated.append(c.Name)
            if children:
                iauracadfile.createIauracadRelContainedInSpatialStructure(
                    iauracadopenshell.guid.new(), history, "BuildingLink", "", children, b
                )
            if childfloors:
                iauracadfile.createIauracadRelAggregates(
                    iauracadopenshell.guid.new(), history, "BuildingLink", "", b, childfloors
                )

    # sites

    for site in exportIauracadHelper.getObjectsOfIauracadType(objectslist, "Site"):
        sites.append(products[site.Name])
        treated.append(site.Name)

        # objs will include the site itself, we avoid duplicate processing with the treated list.
        objs = Draft.get_group_contents(site, walls=True, addgroups=True)
        objs = Arch.pruneIncluded(objs)
        children = []
        childbuildings = []
        for c in objs:
            if c.Name not in treated and c.Name in products:
                if Draft.getType(c) == "Building":
                    childbuildings.append(products[c.Name])
                    treated.append(c.Name)

    # add default site, building and storey as required

    if not sites:
        if preferences["ADD_DEFAULT_SITE"] and not existing_file:
            if preferences["DEBUG"]:
                print("No site found. Adding default site")
            sites = [
                iauracadfile.createIauracadSite(
                    iauracadopenshell.guid.new(),
                    history,
                    "Default Site",
                    "",
                    None,
                    None,
                    None,
                    None,
                    "ELEMENT",
                    None,
                    None,
                    None,
                    None,
                    None,
                )
            ]
    if sites:
        iauracadfile.createIauracadRelAggregates(
            iauracadopenshell.guid.new(), history, "ProjectLink", "", project, sites
        )
    if not buildings:
        if preferences["ADD_DEFAULT_BUILDING"] and not existing_file:
            if preferences["DEBUG"]:
                print("No building found. Adding default building")
            buildings = [
                iauracadfile.createIauracadBuilding(
                    iauracadopenshell.guid.new(),
                    history,
                    "Default Building",
                    "",
                    None,
                    None,
                    None,
                    None,
                    "ELEMENT",
                    None,
                    None,
                    None,
                )
            ]
    if buildings and (not sites):
        iauracadfile.createIauracadRelAggregates(
            iauracadopenshell.guid.new(), history, "ProjectLink", "", project, buildings
        )
    if floors and buildings:
        iauracadfile.createIauracadRelAggregates(
            iauracadopenshell.guid.new(), history, "BuildingLink", "", buildings[0], floors
        )
    if sites and buildings:
        iauracadfile.createIauracadRelAggregates(
            iauracadopenshell.guid.new(), history, "SiteLink", "", sites[0], buildings
        )

    # treat objects that are not related to any site, building or storey

    untreated = []
    for k, v in products.items():
        if not (k in treated):
            if (not buildings) or (k != buildings[0].Name):
                if not (
                    Draft.getType(AuraCAD.ActiveDocument.getObject(k))
                    in ["Site", "Building", "Floor", "BuildingPart"]
                ):
                    untreated.append(v)
                elif Draft.getType(AuraCAD.ActiveDocument.getObject(k)) == "BuildingPart":
                    if not (
                        AuraCAD.ActiveDocument.getObject(k).IauracadType
                        in ["Building", "Building Storey", "Site", "Space"]
                    ):
                        # if iauracad type is "Undefined" the object is added to untreated
                        untreated.append(v)
    if untreated:
        if not defaulthost:
            if preferences["ADD_DEFAULT_STOREY"] and not existing_file:
                if preferences["DEBUG"]:
                    print("No floor found. Adding default floor")
                defaulthost = iauracadfile.createIauracadBuildingStorey(
                    iauracadopenshell.guid.new(),
                    history,
                    "Default Storey",
                    "",
                    None,
                    None,
                    None,
                    None,
                    "ELEMENT",
                    None,
                )
                # if preferences['ADD_DEFAULT_STOREY'] is on, we need a building
                # to host it, regardless of preferences['ADD_DEFAULT_BUILDING']
                if not buildings:
                    if preferences["DEBUG"]:
                        print("No building found. Adding default building")
                    buildings = [
                        iauracadfile.createIauracadBuilding(
                            iauracadopenshell.guid.new(),
                            history,
                            "Default Building",
                            "",
                            None,
                            None,
                            None,
                            None,
                            "ELEMENT",
                            None,
                            None,
                            None,
                        )
                    ]
                    if sites:
                        iauracadfile.createIauracadRelAggregates(
                            iauracadopenshell.guid.new(), history, "SiteLink", "", sites[0], buildings
                        )
                    else:
                        iauracadfile.createIauracadRelAggregates(
                            iauracadopenshell.guid.new(), history, "ProjectLink", "", project, buildings
                        )
                iauracadfile.createIauracadRelAggregates(
                    iauracadopenshell.guid.new(),
                    history,
                    "DefaultStoreyLink",
                    "",
                    buildings[0],
                    [defaulthost],
                )
            elif buildings:
                defaulthost = buildings[0]
        if defaulthost:
            spaces, buildingelements = [], []
            for entity in untreated:
                if entity.is_a() == "IauracadSpace":
                    spaces.append(entity)
                else:
                    buildingelements.append(entity)
            if spaces:
                iauracadfile.createIauracadRelAggregates(
                    iauracadopenshell.guid.new(),
                    history,
                    "UnassignedObjectsLink",
                    "",
                    defaulthost,
                    spaces,
                )
            if buildingelements:
                iauracadfile.createIauracadRelContainedInSpatialStructure(
                    iauracadopenshell.guid.new(),
                    history,
                    "UnassignedObjectsLink",
                    "",
                    buildingelements,
                    defaulthost,
                )
        else:
            # no default host: aggregate unassigned objects directly under the IauracadProject - WARNING: NON STANDARD
            if preferences["DEBUG"]:
                print(
                    "WARNING - Default building generation is disabled. You are producing a non-standard file."
                )
            iauracadfile.createIauracadRelAggregates(
                iauracadopenshell.guid.new(), history, "ProjectLink", "", project, untreated
            )

    # materials

    materials = {}
    for m in Arch.getDocumentMaterials():
        relobjs = []
        for o in m.InList:
            if hasattr(o, "Material"):
                if o.Material:
                    if o.Material.isDerivedFrom("App::MaterialObject"):
                        # TODO : support multimaterials too
                        if o.Material.Name == m.Name:
                            if o.Name in products:
                                relobjs.append(products[o.Name])
                            elif o.Name in subproducts:
                                relobjs.append(subproducts[o.Name])
        if relobjs:
            l = m.Label
            mat = iauracadfile.createIauracadMaterial(l)
            materials[m.Label] = mat
            rgb = None
            if hasattr(m, "Color"):
                rgb = m.Color[:3]
            else:
                for colorslot in ["Color", "DiffuseColor", "ViewColor"]:
                    if colorslot in m.Material:
                        if m.Material[colorslot]:
                            if m.Material[colorslot][0] == "(":
                                rgb = tuple(
                                    [float(f) for f in m.Material[colorslot].strip("()").split(",")]
                                )
                                break
            if rgb:
                psa = iauracadbin.createIauracadPresentationStyleAssignment(
                    l, rgb[0], rgb[1], rgb[2], iauracad4=(preferences["SCHEMA"] == "Iauracad4")
                )
                isi = iauracadfile.createIauracadStyledItem(None, [psa], None)
                isr = iauracadfile.createIauracadStyledRepresentation(context, "Style", "Material", [isi])
                imd = iauracadfile.createIauracadMaterialDefinitionRepresentation(None, None, [isr], mat)
            iauracadfile.createIauracadRelAssociatesMaterial(
                iauracadopenshell.guid.new(), history, "MaterialLink", "", relobjs, mat
            )

    # 2D objects

    annos = {}
    if preferences["EXPORT_2D"]:
        curvestyles = {}
        if annotations and preferences["DEBUG"]:
            print("exporting 2D objects...")
        for anno in annotations:
            ann = create_annotation(anno, iauracadfile, context, history, preferences)
            annos[anno.Name] = ann

    # specials. Specials should take care of register themselves where needed under the project

    specs = {}
    for spec in specials:
        if preferences["DEBUG"]:
            print("exporting special object:", spec.Label)
        elt = spec.Proxy.export_iauracad(spec, iauracadfile)
        specs[spec.Name] = elt

    # groups

    sortedgroups = []
    swallowed = []
    while groups:
        for g in groups.keys():
            okay = True
            for c in groups[g]:
                if Draft.getType(AuraCAD.ActiveDocument.getObject(c)) in ["Group", "VisGroup"]:
                    okay = False
                    for s in sortedgroups:
                        if s[0] == c:
                            okay = True
            if okay:
                sortedgroups.append([g, groups[g]])
        for g in sortedgroups:
            if g[0] in groups:
                del groups[g[0]]
    # print("sorted groups:",sortedgroups)
    containers = {}
    for g in sortedgroups:
        if g[1]:
            children = []
            for o in g[1]:
                if o in products:
                    children.append(products[o])
                elif o in annos:
                    children.append(annos[o])
                    swallowed.append(annos[o])
            if children:
                name = AuraCAD.ActiveDocument.getObject(g[0]).Label
                grp = iauracadfile.createIauracadGroup(iauracadopenshell.guid.new(), history, name, "", None)
                products[g[0]] = grp
                spatialelements[g[0]] = grp
                ass = iauracadfile.createIauracadRelAssignsToGroup(
                    iauracadopenshell.guid.new(), history, "GroupLink", "", children, None, grp
                )

    # stack groups inside containers

    stack = {}
    for g in sortedgroups:
        go = AuraCAD.ActiveDocument.getObject(g[0])
        for parent in go.InList:
            if hasattr(parent, "Group") and (go in parent.Group):
                if (parent.Name in spatialelements) and (g[0] in spatialelements):
                    stack.setdefault(parent.Name, []).append(spatialelements[g[0]])
    for k, v in stack.items():
        iauracadfile.createIauracadRelAggregates(
            iauracadopenshell.guid.new(), history, "GroupStackLink", "", spatialelements[k], v
        )

    # add remaining 2D objects to default host

    if annos:
        remaining = [anno for anno in annos.values() if anno not in swallowed]
        if remaining:
            if not defaulthost:
                if preferences["ADD_DEFAULT_STOREY"]:
                    if preferences["DEBUG"]:
                        print("No floor found. Adding default floor")
                    defaulthost = iauracadfile.createIauracadBuildingStorey(
                        iauracadopenshell.guid.new(),
                        history,
                        "Default Storey",
                        "",
                        None,
                        None,
                        None,
                        None,
                        "ELEMENT",
                        None,
                    )
                    # if preferences['ADD_DEFAULT_STOREY'] is on, we need a
                    # building to host it, regardless of
                    # preferences['ADD_DEFAULT_BUILDING']
                    if not buildings:
                        buildings = [
                            iauracadfile.createIauracadBuilding(
                                iauracadopenshell.guid.new(),
                                history,
                                "Default Building",
                                "",
                                None,
                                None,
                                None,
                                None,
                                "ELEMENT",
                                None,
                                None,
                                None,
                            )
                        ]
                        if sites:
                            iauracadfile.createIauracadRelAggregates(
                                iauracadopenshell.guid.new(),
                                history,
                                "SiteLink",
                                "",
                                sites[0],
                                buildings,
                            )
                        else:
                            iauracadfile.createIauracadRelAggregates(
                                iauracadopenshell.guid.new(),
                                history,
                                "ProjectLink",
                                "",
                                project,
                                buildings,
                            )
                    iauracadfile.createIauracadRelAggregates(
                        iauracadopenshell.guid.new(),
                        history,
                        "DefaultStoreyLink",
                        "",
                        buildings[0],
                        [defaulthost],
                    )
                elif preferences["ADD_DEFAULT_BUILDING"]:
                    if not buildings:
                        defaulthost = iauracadfile.createIauracadBuilding(
                            iauracadopenshell.guid.new(),
                            history,
                            "Default Building",
                            "",
                            None,
                            None,
                            None,
                            None,
                            "ELEMENT",
                            None,
                            None,
                            None,
                        )
                        if sites:
                            iauracadfile.createIauracadRelAggregates(
                                iauracadopenshell.guid.new(),
                                history,
                                "SiteLink",
                                "",
                                sites[0],
                                [defaulthost],
                            )
                        else:
                            iauracadfile.createIauracadRelAggregates(
                                iauracadopenshell.guid.new(),
                                history,
                                "ProjectLink",
                                "",
                                project,
                                [defaulthost],
                            )
            if defaulthost:
                iauracadfile.createIauracadRelContainedInSpatialStructure(
                    iauracadopenshell.guid.new(), history, "AnnotationsLink", "", remaining, defaulthost
                )
            else:
                iauracadfile.createIauracadRelAggregates(
                    iauracadopenshell.guid.new(), history, "ProjectLink", "", project, remaining
                )

    if not existing_file:
        if preferences["DEBUG"]:
            print("writing ", filename, "...")

        if filename.lower().endswith("json"):
            writeJson(filename, iauracadfile)
        else:
            iauracadfile.write(filename)

        if preferences["STORE_UID"]:
            # some properties might have been changed
            AuraCAD.ActiveDocument.recompute()

        os.remove(templatefile)

        if preferences["DEBUG"] and iauracadbin.compress and (not filename.lower().endswith("json")):
            f = pyopen(filename, "r")
            s = len(f.read().split("\n"))
            f.close()
            print(
                "Compression ratio:", int((float(iauracadbin.spared) / (s + iauracadbin.spared)) * 100), "%"
            )
    del iauracadbin

    if existing_file:
        return products | spatialelements

    endtime = time.time() - starttime

    _msg("Finished exporting in {} seconds".format(int(endtime)))


# ************************************************************************************************
# ********** helper for export Iauracad **************


def getPropertyData(key, value, preferences):

    # in 0.18, properties in IauracadProperties dict are stored as "key":"pset;;type;;value" or "key":"type;;value"
    # in 0.19, key = name;;pset, value = ptype;;value (because there can be several props with same name)

    pset = None
    pname = key
    if ";;" in pname:
        pname = key.split(";;")[0]
        pset = key.split(";;")[-1]
    value = value.split(";;")
    if len(value) == 3:
        pset = value[0]
        ptype = value[1]
        pvalue = value[2]
    elif len(value) == 2:
        if not pset:
            pset = "Default property set"
        ptype = value[0]
        pvalue = value[1]
    else:
        if preferences["DEBUG"]:
            print("      unable to export property:", pname, value)
        return pset, pname, ptype, None

    # if preferences['DEBUG']: print("      property ",pname," : ",pvalue.encode("utf8"), " (", str(ptype), ") in ",pset)
    if pvalue == "":
        return pset, pname, ptype, None
    if ptype in ["IauracadLabel", "IauracadText", "IauracadIdentifier", "IauracadDescriptiveMeasure"]:
        pass
    elif ptype == "IauracadBoolean":
        if pvalue == "True":
            pvalue = True
        elif pvalue == ".T.":
            pvalue = True
        else:
            pvalue = False
    elif ptype == "IauracadLogical":
        if pvalue == "True":
            pvalue = True
        elif pvalue.upper() == "TRUE":
            pvalue = True
        else:
            pvalue = False
    elif ptype == "IauracadInteger":
        pvalue = int(pvalue)
    else:
        try:
            pvalue = float(pvalue)
        except Exception:
            try:
                pvalue = AuraCAD.Units.Quantity(pvalue).Value
            except Exception:
                if preferences["DEBUG"]:
                    print(
                        "      warning: unable to export property as numeric value:", pname, pvalue
                    )

    # print('pset: {}, pname: {}, ptype: {}, pvalue: {}'.format(pset, pname, ptype, pvalue))
    return pset, pname, ptype, pvalue


def isStandardCase(obj, iauracadtype):

    if iauracadtype.endswith("StandardCase"):
        return False  # type is already standard case, return False so "StandardCase" is not added twice
    if hasattr(obj, "Proxy") and hasattr(obj.Proxy, "isStandardCase"):
        return obj.Proxy.isStandardCase(obj)
    return False


def getIauracadTypeFromObj(obj):

    dtype = Draft.getType(obj)
    if (dtype == "BuildingPart") and hasattr(obj, "IauracadType") and (obj.IauracadType == "Undefined"):
        iauracadtype = "IauracadBuildingElementPart"
        obj.IauracadType = "Building Element Part"
        # export BuildingParts as Building Element Parts if their type wasn't explicitly set
        # set IauracadType in the object as well
        # https://forum.AuraCAD.org/viewtopic.php?p=662934#p662927
    elif hasattr(obj, "IauracadType"):
        iauracadtype = obj.IauracadType.replace(" ", "")
    elif dtype in ["App::Part", "Part::Compound"]:
        iauracadtype = "IauracadElementAssembly"
    elif dtype in ["App::DocumentObjectGroup"]:
        iauracadtype = "IauracadGroup"
    else:
        iauracadtype = dtype

    if iauracadtype in translationtable:
        iauracadtype = translationtable[iauracadtype]
    if not iauracadtype.startswith("Iauracad"):
        iauracadtype = "Iauracad" + iauracadtype
    if "::" in iauracadtype:
        # it makes no sense to return IauracadPart::Cylinder for a Part::Cylinder
        # this is not a iauracadtype at all
        iauracadtype = "IauracadBuildingElementPRoxy"

    # print("Return value of getIauracadTypeFromObj: {}".format(iauracadtype))
    return iauracadtype


def exportIauracad2X3Attributes(obj, kwargs, scale=0.001):

    iauracadtype = getIauracadTypeFromObj(obj)
    if iauracadtype in ["IauracadSlab", "IauracadFooting"]:
        kwargs.update({"PredefinedType": "NOTDEFINED"})
    elif iauracadtype == "IauracadBuilding":
        kwargs.update({"CompositionType": "ELEMENT"})
    elif iauracadtype == "IauracadBuildingStorey":
        kwargs.update({"CompositionType": "ELEMENT"})
    elif iauracadtype == "IauracadBuildingElementProxy":
        kwargs.update({"CompositionType": "ELEMENT"})
    elif iauracadtype == "IauracadSpace":
        internal = "NOTDEFINED"
        if hasattr(obj, "Internal"):
            if obj.Internal:
                internal = "INTERNAL"
            else:
                internal = "EXTERNAL"
        kwargs.update(
            {
                "CompositionType": "ELEMENT",
                "InteriorOrExteriorSpace": internal,
                "ElevationWithFlooring": obj.Shape.BoundBox.ZMin * scale,
            }
        )
    elif iauracadtype == "IauracadReinforcingBar":
        kwargs.update({"NominalDiameter": obj.Diameter.Value, "BarLength": obj.Length.Value})
    elif iauracadtype == "IauracadBuildingStorey":
        kwargs.update({"Elevation": obj.Placement.Base.z * scale})
    return kwargs


def exportIauracadAttributes(obj, kwargs, scale=0.001):

    iauracadtype = getIauracadTypeFromObj(obj)
    for property in obj.PropertiesList:
        if obj.getGroupOfProperty(property) == "Iauracad Attributes" and obj.getPropertyByName(property):
            value = obj.getPropertyByName(property)
            if isinstance(value, AuraCAD.Units.Quantity):
                value = float(value)
                if "Elevation" in property:
                    value = value * scale  # some properties must be changed to meters
            if (iauracadtype == "IauracadFurnishingElement") and (property == "PredefinedType"):
                pass  # Iauracad2x3 Furniture objects get converted to IauracadFurnishingElement and have no PredefinedType anymore
            else:
                kwargs.update({property: value})
    return kwargs


def buildAddress(obj, iauracadfile):

    a = obj.Address or None
    p = obj.PostalCode or None
    t = obj.City or None
    r = obj.Region or None
    c = obj.Country or None
    if a or p or t or r or c:
        addr = iauracadfile.createIauracadPostalAddress(
            "SITE", "Site Address", "", None, [a], None, t, r, p, c
        )
    else:
        addr = None
    return addr


def createCurve(iauracadfile, wire, scaling=1.0):
    """creates an IauracadIndexdPolyCurve from a wire
    if possible, or defects to createCurveWithArcs"""

    if wire.ShapeType != "Wire":
        return createCurveWithArcs(iauracadfile, wire, scaling)
    for e in wire.Edges:
        if isinstance(e.Curve, Part.Circle):
            return createCurveWithArcs(iauracadfile, wire, scaling)
    verts = [v.Point for v in wire.Vertexes]
    if scaling != 1:
        verts = [v.multiply(scaling) for v in verts]
    verts = tuple([tuple(v) for v in verts])
    pts = iauracadfile.createIauracadCartesianPointList3D(verts)
    idc = iauracadfile.createIauracadIndexedPolyCurve(pts, None, None)
    return idc


def createCurveWithArcs(iauracadfile, wire, scaling=1.0):
    "creates an IauracadCompositeCurve from a shape"

    segments = []
    pol = None
    last = None
    if wire.ShapeType == "Edge":
        edges = [wire]
    else:
        edges = Part.__sortEdges__(wire.Edges)
    for e in edges:
        if scaling not in (0, 1):
            e.scale(scaling)
        if isinstance(e.Curve, Part.Circle):
            xaxis = e.Curve.XAxis
            zaxis = e.Curve.Axis
            follow = True
            if last:
                if not DraftVecUtils.equals(last, e.Vertexes[0].Point):
                    follow = False
                    last = e.Vertexes[0].Point
                    prev = e.Vertexes[-1].Point
                else:
                    last = e.Vertexes[-1].Point
                    prev = e.Vertexes[0].Point
            else:
                last = e.Vertexes[-1].Point
                prev = e.Vertexes[0].Point
            p1 = math.degrees(-DraftVecUtils.angle(prev.sub(e.Curve.Center), xaxis, zaxis))
            p2 = math.degrees(-DraftVecUtils.angle(last.sub(e.Curve.Center), xaxis, zaxis))
            da = DraftVecUtils.angle(
                e.valueAt(e.FirstParameter + 0.1).sub(e.Curve.Center), prev.sub(e.Curve.Center)
            )
            # print("curve params:",p1,",",p2,"da=",da)
            if p1 < 0:
                p1 = 360 + p1
            if p2 < 0:
                p2 = 360 + p2
            if da > 0:
                # follow = not(follow) # now we always draw segments in the correct order, so follow is always true
                pass
            # print("  circle from",prev,"to",last,"a1=",p1,"a2=",p2)
            ovc = iauracadbin.createIauracadCartesianPoint(tuple(e.Curve.Center))
            zvc = iauracadbin.createIauracadDirection(tuple(zaxis))
            xvc = iauracadbin.createIauracadDirection(tuple(xaxis))
            plc = iauracadbin.createIauracadAxis2Placement3D(ovc, zvc, xvc)
            cir = iauracadfile.createIauracadCircle(plc, e.Curve.Radius)
            curve = iauracadfile.createIauracadTrimmedCurve(
                cir,
                [iauracadfile.createIauracadParameterValue(p1)],
                [iauracadfile.createIauracadParameterValue(p2)],
                follow,
                "PARAMETER",
            )
        else:
            verts = [vertex.Point for vertex in e.Vertexes]
            if last:
                if not DraftVecUtils.equals(last, verts[0]):
                    verts.reverse()
                    last = e.Vertexes[0].Point
                else:
                    last = e.Vertexes[-1].Point
            else:
                last = e.Vertexes[-1].Point
            # print("  polyline:",verts)
            pts = [iauracadbin.createIauracadCartesianPoint(tuple(v)) for v in verts]
            curve = iauracadbin.createIauracadPolyline(pts)
        segment = iauracadfile.createIauracadCompositeCurveSegment("CONTINUOUS", True, curve)
        segments.append(segment)
    if segments:
        pol = iauracadfile.createIauracadCompositeCurve(segments, False)
    return pol


def getEdgesAngle(edge1, edge2):
    """getEdgesAngle(edge1, edge2): returns a angle between two edges."""

    vec1 = vec(edge1)
    vec2 = vec(edge2)
    angle = vec1.getAngle(vec2)
    angle = math.degrees(angle)
    return angle


def checkRectangle(edges):
    """checkRectangle(edges=[]): This function checks whether the given form is a rectangle
    or not. It will return True when edges form a rectangular shape or return False
    when edges do not form a rectangular shape."""

    if params.get_param_arch("DisableIauracadRectangleProfileDef"):
        return False
    if len(edges) != 4:
        return False
    angles = [
        round(getEdgesAngle(edges[0], edges[1])),
        round(getEdgesAngle(edges[0], edges[2])),
        round(getEdgesAngle(edges[0], edges[3])),
    ]
    if angles.count(90) == 2 and (angles.count(180) == 1 or angles.count(0) == 1):
        return True
    return False


def getProfile(iauracadfile, p):
    """returns an Iauracad profile definition from a shape"""

    import Part
    import DraftGeomUtils

    profile = None
    if len(p.Edges) == 1:
        pxvc = iauracadbin.createIauracadDirection((1.0, 0.0))
        povc = iauracadbin.createIauracadCartesianPoint((0.0, 0.0))
        pt = iauracadbin.createIauracadAxis2Placement2D(povc, pxvc)
        if isinstance(p.Edges[0].Curve, Part.Circle):
            # extruded circle
            profile = iauracadbin.createIauracadCircleProfileDef("AREA", None, pt, p.Edges[0].Curve.Radius)
        elif isinstance(p.Edges[0].Curve, Part.Ellipse):
            # extruded ellipse
            profile = iauracadbin.createIauracadEllipseProfileDef(
                "AREA", None, pt, p.Edges[0].Curve.MajorRadius, p.Edges[0].Curve.MinorRadius
            )
    elif checkRectangle(p.Edges):
        # arbitrarily use the first edge as the rectangle orientation
        d = vec(p.Edges[0])
        d.normalize()
        pxvc = iauracadbin.createIauracadDirection(tuple(d)[:2])
        # profile must be located at (0,0) because placement gets added later
        # povc = iauracadbin.createIauracadCartesianPoint((0.0,0.0))
        # the above statement appears wrong, so the line below has been uncommented for now
        # TODO we must sort this out at some point... For now the line below seems to work
        if getattr(p, "CenterOfMass", None):
            povc = iauracadbin.createIauracadCartesianPoint(tuple(p.CenterOfMass[:2]))
        else:
            povc = iauracadbin.createIauracadCartesianPoint((0.0, 0.0))
        pt = iauracadbin.createIauracadAxis2Placement2D(povc, pxvc)
        # semiPerimeter = p.Length/2
        # diff = math.sqrt(semiPerimeter**2 - 4*p.Area)
        # b = max(abs((semiPerimeter + diff)/2),abs((semiPerimeter - diff)/2))
        # h = min(abs((semiPerimeter + diff)/2),abs((semiPerimeter - diff)/2))
        b = p.Edges[0].Length
        h = p.Edges[1].Length
        if h == b:
            # are these edges unordered? To be on the safe side, check the next one
            h = p.Edges[2].Length
        profile = iauracadbin.createIauracadRectangleProfileDef("AREA", "rectangular", pt, b, h)
    elif (len(p.Faces) == 1) and (len(p.Wires) > 1):
        # face with holes
        f = p.Faces[0]
        if DraftGeomUtils.hasCurves(f.OuterWire):
            outerwire = createCurve(iauracadfile, f.OuterWire)
        else:
            w = Part.Wire(Part.__sortEdges__(f.OuterWire.Edges))
            pts = [
                iauracadbin.createIauracadCartesianPoint(tuple(v.Point)[:2])
                for v in w.Vertexes + [w.Vertexes[0]]
            ]
            outerwire = iauracadbin.createIauracadPolyline(pts)
        innerwires = []
        for w in f.Wires:
            if w.hashCode() != f.OuterWire.hashCode():
                if DraftGeomUtils.hasCurves(w):
                    innerwires.append(createCurve(iauracadfile, w))
                else:
                    w = Part.Wire(Part.__sortEdges__(w.Edges))
                    pts = [
                        iauracadbin.createIauracadCartesianPoint(tuple(v.Point)[:2])
                        for v in w.Vertexes + [w.Vertexes[0]]
                    ]
                    innerwires.append(iauracadbin.createIauracadPolyline(pts))
        profile = iauracadfile.createIauracadArbitraryProfileDefWithVoids("AREA", None, outerwire, innerwires)
    else:
        if DraftGeomUtils.hasCurves(p):
            # extruded composite curve
            pol = createCurve(iauracadfile, p)
        else:
            # extruded polyline
            w = Part.Wire(Part.__sortEdges__(p.Wires[0].Edges))
            pts = [
                iauracadbin.createIauracadCartesianPoint(tuple(v.Point)[:2])
                for v in w.Vertexes + [w.Vertexes[0]]
            ]
            pol = iauracadbin.createIauracadPolyline(pts)
        profile = iauracadfile.createIauracadArbitraryClosedProfileDef("AREA", None, pol)
    return profile


def getRepresentation(
    iauracadfile,
    context,
    obj,
    forcebrep=False,
    subtraction=False,
    tessellation=1,
    colors=None,
    preferences=None,
    forceclone=False,
    skipshape=False,
):
    """returns an IauracadShapeRepresentation object or None. forceclone can be False (does nothing),
    "store" or True (stores the object as clone base) or a Vector (creates a clone)"""

    import Part
    import DraftGeomUtils
    import DraftVecUtils

    shapes = []
    placement = None
    productdef = None
    shapetype = "no shape"
    tostore = False
    subplacement = None

    # enable forcebrep for non-solids
    if hasattr(obj, "Shape"):
        if obj.Shape:
            if not obj.Shape.Solids:
                forcebrep = True

    # check for clones

    if ((not subtraction) and (not forcebrep)) or forceclone:
        if forceclone:
            if obj.Name not in clones:
                clones[obj.Name] = []
        for k, v in clones.items():
            if (obj.Name == k) or (obj.Name in v):
                if k in sharedobjects:
                    # base shape already exists
                    repmap = sharedobjects[k]
                    pla = obj.getGlobalPlacement()
                    pos = AuraCAD.Vector(pla.Base)
                    if isinstance(forceclone, AuraCAD.Vector):
                        pos += forceclone
                    axis1 = iauracadbin.createIauracadDirection(
                        tuple(pla.Rotation.multVec(AuraCAD.Vector(1, 0, 0)))
                    )
                    axis2 = iauracadbin.createIauracadDirection(
                        tuple(pla.Rotation.multVec(AuraCAD.Vector(0, 1, 0)))
                    )
                    axis3 = iauracadbin.createIauracadDirection(
                        tuple(pla.Rotation.multVec(AuraCAD.Vector(0, 0, 1)))
                    )
                    origin = iauracadbin.createIauracadCartesianPoint(
                        tuple(pos.multiply(preferences["SCALE_FACTOR"]))
                    )
                    transf = iauracadbin.createIauracadCartesianTransformationOperator3D(
                        axis1, axis2, origin, 1.0, axis3
                    )
                    mapitem = iauracadfile.createIauracadMappedItem(repmap, transf)
                    shapes = [mapitem]
                    solidType = "MappedRepresentation"
                    shapetype = "clone"
                else:
                    # base shape not yet created
                    tostore = k

    # unhandled case: object is duplicated because of Axis
    if (
        obj.isDerivedFrom("Part::Feature")
        and (len(obj.Shape.Solids) > 1)
        and hasattr(obj, "Axis")
        and obj.Axis
    ):
        forcebrep = True

    if (not shapes) and (not forcebrep) and (not skipshape):
        profile = None
        ev = AuraCAD.Vector()
        if hasattr(obj, "Proxy"):
            if hasattr(obj.Proxy, "getRebarData"):
                # export rebars as IauracadSweptDiskSolid
                rdata = obj.Proxy.getRebarData(obj)
                if rdata:
                    # convert to meters
                    r = rdata[1] * preferences["SCALE_FACTOR"]
                    for w in rdata[0]:
                        w.Placement = w.Placement.multiply(obj.getGlobalPlacement())
                        w.scale(preferences["SCALE_FACTOR"])
                        cur = createCurve(iauracadfile, w)
                        shape = iauracadfile.createIauracadSweptDiskSolid(cur, r)
                        shapes.append(shape)
                        solidType = "SweptSolid"
                        shapetype = "extrusion"
            if (not shapes) and hasattr(obj.Proxy, "getExtrusionData"):
                extdata = obj.Proxy.getExtrusionData(obj)
                if extdata:
                    # print(extdata)
                    # convert to meters
                    p = extdata[0]
                    if not isinstance(p, list):
                        p = [p]
                    ev = extdata[1]
                    if not isinstance(ev, list):
                        ev = [ev]
                    pl = extdata[2]
                    if not isinstance(pl, list):
                        pl = [pl]
                    simpleExtrusion = True
                    for evi in ev:
                        if not isinstance(evi, AuraCAD.Vector):
                            simpleExtrusion = False
                    if simpleExtrusion:
                        for i in range(len(p)):
                            pi = p[i]
                            pi.scale(preferences["SCALE_FACTOR"])
                            if i < len(ev):
                                evi = AuraCAD.Vector(ev[i])
                            else:
                                evi = AuraCAD.Vector(ev[-1])
                            evi.multiply(preferences["SCALE_FACTOR"])
                            if i < len(pl):
                                pli = pl[i].copy()
                            else:
                                pli = pl[-1].copy()
                            pli.Base = pli.Base.multiply(preferences["SCALE_FACTOR"])
                            pstr = str([v.Point for v in p[i].Vertexes])
                            if pstr in profiledefs:
                                profile = profiledefs[pstr]
                                profiles = [profile]
                                shapetype = "reusing profile"
                            else:
                                # Fix bug in Forum Discussion
                                # https://forum.AuraCAD.org/viewtopic.php?p=771954#p771954
                                if not isinstance(pi, Part.Compound):
                                    profile = getProfile(iauracadfile, pi)
                                    if profile:
                                        profiledefs[pstr] = profile
                                        profiles = [profile]
                                else:  # i.e. Part.Compound
                                    profiles = []
                                    for pif in pi.Faces:
                                        profile = getProfile(iauracadfile, pif)
                                        if profile:
                                            profiledefs[pstr] = profile
                                            profiles.append(profile)
                            if profiles and not (DraftVecUtils.isNull(evi)):
                                for profile in profiles:
                                    # ev = pl.Rotation.inverted().multVec(evi)
                                    # print("evi:",evi)
                                    if not tostore:
                                        # add the object placement to the profile placement. Otherwise it'll be done later at map insert
                                        pl2 = obj.getGlobalPlacement()
                                        pl2.Base = pl2.Base.multiply(preferences["SCALE_FACTOR"])
                                        pli = pl2.multiply(pli)
                                    xvc = iauracadbin.createIauracadDirection(
                                        tuple(pli.Rotation.multVec(AuraCAD.Vector(1, 0, 0)))
                                    )
                                    zvc = iauracadbin.createIauracadDirection(
                                        tuple(pli.Rotation.multVec(AuraCAD.Vector(0, 0, 1)))
                                    )
                                    ovc = iauracadbin.createIauracadCartesianPoint(tuple(pli.Base))
                                    lpl = iauracadbin.createIauracadAxis2Placement3D(ovc, zvc, xvc)
                                    edir = iauracadbin.createIauracadDirection(
                                        tuple(AuraCAD.Vector(evi).normalize())
                                    )
                                    shape = iauracadfile.createIauracadExtrudedAreaSolid(
                                        profile, lpl, edir, evi.Length
                                    )
                                    shapes.append(shape)
                                    solidType = "SweptSolid"
                                    shapetype = "extrusion"
        if (not shapes) and obj.isDerivedFrom("Part::Extrusion"):
            import ArchComponent

            pstr = str([v.Point for v in obj.Base.Shape.Vertexes])
            profile, pl = ArchComponent.Component.rebase(obj, obj.Base.Shape)
            profile.scale(preferences["SCALE_FACTOR"])
            pl.Base = pl.Base.multiply(preferences["SCALE_FACTOR"])
            profile = getProfile(iauracadfile, profile)
            if profile:
                profiledefs[pstr] = profile
            ev = AuraCAD.Vector(obj.Dir)
            l = obj.LengthFwd.Value
            if l:
                ev = ev.normalize()  # new since 0.20 - obj.Dir length is ignored
                ev.multiply(l)
            ev.multiply(preferences["SCALE_FACTOR"])
            ev = pl.Rotation.inverted().multVec(ev)
            xvc = iauracadbin.createIauracadDirection(tuple(pl.Rotation.multVec(AuraCAD.Vector(1, 0, 0))))
            zvc = iauracadbin.createIauracadDirection(tuple(pl.Rotation.multVec(AuraCAD.Vector(0, 0, 1))))
            ovc = iauracadbin.createIauracadCartesianPoint(tuple(pl.Base))
            lpl = iauracadbin.createIauracadAxis2Placement3D(ovc, zvc, xvc)
            edir = iauracadbin.createIauracadDirection(tuple(AuraCAD.Vector(ev).normalize()))
            shape = iauracadfile.createIauracadExtrudedAreaSolid(profile, lpl, edir, ev.Length)
            shapes.append(shape)
            solidType = "SweptSolid"
            shapetype = "extrusion"

    if (not shapes) and (not skipshape):

        # check if we keep a null shape (additions-only object)

        if (
            (hasattr(obj, "Base") and hasattr(obj, "Width") and hasattr(obj, "Height"))
            and (not obj.Base)
            and obj.Additions
            and (not obj.Width.Value)
            and (not obj.Height.Value)
        ):
            shapes = None

        else:

            # brep representation

            auracadshape = None
            solidType = "Brep"
            if subtraction:
                if hasattr(obj, "Proxy"):
                    if hasattr(obj.Proxy, "getSubVolume"):
                        auracadshape = obj.Proxy.getSubVolume(obj)
            if not auracadshape:
                if obj.isDerivedFrom("Part::Feature"):
                    # if hasattr(obj,"Base") and hasattr(obj,"Additions")and hasattr(obj,"Subtractions"):
                    if False:  # above is buggy. No way to duplicate shapes that way?
                        if obj.Base and not obj.Additions and not obj.Subtractions:
                            if obj.Base.isDerivedFrom("Part::Feature"):
                                if obj.Base.Shape:
                                    if obj.Base.Shape.Solids:
                                        auracadshape = obj.Base.Shape
                                        subplacement = AuraCAD.Placement(obj.Placement)
                    if not auracadshape:
                        if obj.Shape:
                            if not obj.Shape.isNull():
                                auracadshape = obj.Shape.copy()
                                auracadshape.Placement = obj.getGlobalPlacement()
            if auracadshape:
                shapedef = str([v.Point for v in auracadshape.Vertexes])
                if shapedef in shapedefs:
                    shapes = shapedefs[shapedef]
                    shapetype = "reusing brep"
                else:

                    # new iauracadopenshell serializer

                    from iauracadopenshell import geom

                    serialized = False
                    if (
                        hasattr(geom, "serialise")
                        and obj.isDerivedFrom("Part::Feature")
                        and preferences["SERIALIZE"]
                    ):
                        if obj.Shape.Faces:
                            sh = obj.Shape.copy()
                            sh.Placement = obj.getGlobalPlacement()
                            sh.scale(preferences["SCALE_FACTOR"])  # to meters
                            # clean shape and moves placement away from the outer element level
                            # https://forum.AuraCAD.org/viewtopic.php?p=675760#p675760
                            brep_data = sh.removeSplitter().exportBrepToString()
                            try:
                                p = geom.serialise(brep_data)
                            except TypeError:
                                # IauracadOpenShell v0.6.0
                                # Serialization.cpp:IauracadUtil::IauracadBaseClass* IauracadGeom::serialise(const std::string& schema_name, const TopoDS_Shape& shape, bool advanced)
                                p = geom.serialise(preferences["SCHEMA"], brep_data)
                            if p:
                                productdef = iauracadfile.add(p)
                                for rep in productdef.Representations:
                                    rep.ContextOfItems = context
                                placement = iauracadbin.createIauracadLocalPlacement()
                                shapetype = "advancedbrep"
                                shapes = None
                                serialized = True
                            else:
                                if preferences["DEBUG"]:
                                    print(
                                        "Warning! IauracadOS serializer did not return a iauracad-geometry for object {}. "
                                        "The shape will be exported with triangulation.".format(
                                            obj.Label
                                        )
                                    )

                    if not serialized:

                        # old method

                        solids = []

                        # if this is a clone, place back the shape in null position
                        if tostore:
                            auracadshape.Placement = AuraCAD.Placement()

                        if auracadshape.Solids:
                            dataset = auracadshape.Solids
                        elif auracadshape.Shells:
                            dataset = auracadshape.Shells
                            # if preferences['DEBUG']: print("Warning! object contains no solids")
                        else:
                            if preferences["DEBUG"]:
                                print(
                                    "Warning! object " + obj.Label + " contains no solids or shells"
                                )
                            dataset = [auracadshape]
                        for auracadsolid in dataset:
                            auracadsolid.scale(preferences["SCALE_FACTOR"])  # to meters
                            faces = []
                            curves = False
                            shapetype = "brep"
                            for auracadface in auracadsolid.Faces:
                                for e in auracadface.Edges:
                                    if DraftGeomUtils.geomType(e) != "Line":
                                        from AuraCAD import Base

                                        try:
                                            if (
                                                e.curvatureAt(
                                                    e.FirstParameter
                                                    + (e.LastParameter - e.FirstParameter) / 2
                                                )
                                                > 0.0001
                                            ):
                                                curves = True
                                                break
                                        except Part.OCCError:
                                            pass
                                        except Base.AuraCADError:
                                            pass
                            if curves:
                                joinfacets = params.get_param_arch("iauracadJoinCoplanarFacets")
                                usedae = params.get_param_arch("iauracadUseDaeOptions")
                                if joinfacets:
                                    result = Arch.removeCurves(auracadsolid, dae=usedae)
                                    if result:
                                        auracadsolid = result
                                    else:
                                        # fall back to standard triangulation
                                        joinfacets = False
                                if not joinfacets:
                                    shapetype = "triangulated"
                                    if usedae:
                                        from importers import importDAE

                                        tris = importDAE.triangulate(auracadsolid)
                                    else:
                                        tris = auracadsolid.tessellate(tessellation)
                                    for tri in tris[1]:
                                        pts = [
                                            iauracadbin.createIauracadCartesianPoint(tuple(tris[0][i]))
                                            for i in tri
                                        ]
                                        loop = iauracadbin.createIauracadPolyLoop(pts)
                                        bound = iauracadfile.createIauracadFaceOuterBound(loop, True)
                                        face = iauracadfile.createIauracadFace([bound])
                                        faces.append(face)
                                        auracadsolid = (
                                            Part.Shape()
                                        )  # empty shape so below code is not executed

                            for auracadface in auracadsolid.Faces:
                                loops = []
                                verts = [v.Point for v in auracadface.OuterWire.OrderedVertexes]
                                c = auracadface.CenterOfMass
                                if len(verts) < 1:
                                    print(
                                        "Warning: OuterWire returned no ordered Vertexes in ",
                                        obj.Label,
                                    )
                                    # Part.show(auracadface)
                                    # Part.show(auracadsolid)
                                    continue
                                v1 = verts[0].sub(c)
                                v2 = verts[1].sub(c)
                                try:
                                    n = auracadface.normalAt(0, 0)
                                except Part.OCCError:
                                    continue  # this is a very wrong face, it probably shouldn't be here...
                                if DraftVecUtils.angle(v2, v1, n) >= 0:
                                    verts.reverse()  # inverting verts order if the direction is couterclockwise
                                pts = [iauracadbin.createIauracadCartesianPoint(tuple(v)) for v in verts]
                                loop = iauracadbin.createIauracadPolyLoop(pts)
                                bound = iauracadfile.createIauracadFaceOuterBound(loop, True)
                                loops.append(bound)
                                for wire in auracadface.Wires:
                                    if wire.hashCode() != auracadface.OuterWire.hashCode():
                                        verts = [v.Point for v in wire.OrderedVertexes]
                                        if len(verts) > 1:
                                            v1 = verts[0].sub(c)
                                            v2 = verts[1].sub(c)
                                            if (
                                                DraftVecUtils.angle(v2, v1, DraftVecUtils.neg(n))
                                                >= 0
                                            ):
                                                verts.reverse()
                                            pts = [
                                                iauracadbin.createIauracadCartesianPoint(tuple(v))
                                                for v in verts
                                            ]
                                            loop = iauracadbin.createIauracadPolyLoop(pts)
                                            bound = iauracadfile.createIauracadFaceBound(loop, True)
                                            loops.append(bound)
                                        else:
                                            print("Warning: wire with one/no vertex in ", obj.Label)
                                face = iauracadfile.createIauracadFace(loops)
                                faces.append(face)

                            if faces:
                                shell = iauracadfile.createIauracadClosedShell(faces)
                                shape = iauracadfile.createIauracadFacetedBrep(shell)
                                shapes.append(shape)

                        shapedefs[shapedef] = shapes

    if shapes:

        colorshapes = shapes  # to keep track of individual shapes for coloring below
        if tostore:
            subrep = iauracadfile.createIauracadShapeRepresentation(context, "Body", solidType, shapes)
            gpl = iauracadbin.createIauracadAxis2Placement3D()
            repmap = iauracadfile.createIauracadRepresentationMap(gpl, subrep)
            pla = obj.getGlobalPlacement()
            if isinstance(forceclone, AuraCAD.Vector):
                pla.Base += forceclone
            axis1 = iauracadbin.createIauracadDirection(tuple(pla.Rotation.multVec(AuraCAD.Vector(1, 0, 0))))
            axis2 = iauracadbin.createIauracadDirection(tuple(pla.Rotation.multVec(AuraCAD.Vector(0, 1, 0))))
            origin = iauracadbin.createIauracadCartesianPoint(
                tuple(AuraCAD.Vector(pla.Base).multiply(preferences["SCALE_FACTOR"]))
            )
            axis3 = iauracadbin.createIauracadDirection(tuple(pla.Rotation.multVec(AuraCAD.Vector(0, 0, 1))))
            transf = iauracadbin.createIauracadCartesianTransformationOperator3D(
                axis1, axis2, origin, 1.0, axis3
            )
            mapitem = iauracadfile.createIauracadMappedItem(repmap, transf)
            shapes = [mapitem]
            sharedobjects[tostore] = repmap
            solidType = "MappedRepresentation"

        # set surface style

        shapecolor = None
        diffusecolor = None
        transparency = 0.0
        if colors:
            # color dict is given
            if obj.Name in colors:
                color = colors[obj.Name]
                shapecolor = color
                if isinstance(color[0], tuple):
                    # this is a diffusecolor. For now, use the first color - #TODO: Support per-face colors
                    diffusecolor = color
                    shapecolor = color[0]
        elif AuraCAD.GuiUp and (not subtraction) and hasattr(obj.ViewObject, "ShapeColor"):
            # every object gets a surface style. If the obj has a material, the surfstyle
            # is named after it. Revit will treat surfacestyles as materials (and discard
            # actual iauracadmaterial)
            shapecolor = obj.ViewObject.ShapeColor[:3]
            transparency = obj.ViewObject.Transparency / 100.0
            if transparency == 1:
                # fix buggy fully transparent materials
                # TODO there is some problem somewhere in ShapeAppearance that needs solving.
                transparency = 0.0
            if hasattr(obj.ViewObject, "DiffuseColor"):
                diffusecolor = obj.ViewObject.DiffuseColor
        if shapecolor and (shapetype != "clone"):  # cloned objects are already colored
            key = None
            rgbt = [shapecolor + (transparency,)] * len(shapes)
            if (
                diffusecolor
                and (len(diffusecolor) == len(obj.Shape.Faces))
                and (len(obj.Shape.Solids) == len(colorshapes))
            ):
                i = 0
                rgbt = []
                for sol in obj.Shape.Solids:
                    if i < len(diffusecolor):
                        rgbt.append(diffusecolor[i])
                    else:
                        rgbt.append(diffusecolor[0])
                    i += len(sol.Faces)
            for i, shape in enumerate(colorshapes):
                # TODO handle multimaterials
                if i >= len(rgbt):
                    i = 0
                key = rgbt[i]
                mat = None
                if getattr(obj, "Material", None):
                    mat = obj.Material.Label
                    if hasattr(obj.Material, "Transparency"):
                        # Can obj.Material.Transparency (single material) really
                        # be different from obj.ViewObject.Transparency?
                        key = key[:3] + (obj.Material.Transparency / 100.0,)
                if key in surfstyles:
                    psa = surfstyles[key]
                else:
                    psa = iauracadbin.createIauracadPresentationStyleAssignment(mat, *key)
                    surfstyles[key] = psa
                isi = iauracadfile.createIauracadStyledItem(shape, [psa], None)

        placement = iauracadbin.createIauracadLocalPlacement()
        representation = [iauracadfile.createIauracadShapeRepresentation(context, "Body", solidType, shapes)]
        # additional representations?
        if Draft.getType(obj) in ["Wall", "Structure"]:
            addrepr = createAxis(iauracadfile, obj, preferences, forceclone)
            if addrepr:
                representation = representation + [addrepr]
        productdef = iauracadfile.createIauracadProductDefinitionShape(None, None, representation)

    return productdef, placement, shapetype


def getBrepFlag(obj, preferences):
    """returns True if the object must be exported as BREP"""
    brepflag = False
    if preferences["FORCE_BREP"]:
        return True
    if hasattr(obj, "IauracadData"):
        if "FlagForceBrep" in obj.IauracadData:
            if obj.IauracadData["FlagForceBrep"] == "True":
                brepflag = True
    return brepflag


def createProduct(
    iauracadfile, obj, iauracadtype, uid, history, name, description, placement, representation, preferences
):
    """creates a product in the given Iauracad file"""

    kwargs = {
        "GlobalId": uid,
        "OwnerHistory": history,
        "Name": name,
        "Description": description,
        "ObjectPlacement": placement,
        "Representation": representation,
    }
    if iauracadtype == "IauracadSite":
        kwargs.update(
            {
                "RefLatitude": dd2dms(obj.Latitude),
                "RefLongitude": dd2dms(obj.Longitude),
                "RefElevation": obj.Elevation.Value * preferences["SCALE_FACTOR"],
                "SiteAddress": buildAddress(obj, iauracadfile),
                "CompositionType": "ELEMENT",
            }
        )
    if preferences["SCHEMA"] == "Iauracad2X3":
        kwargs = exportIauracad2X3Attributes(obj, kwargs, preferences["SCALE_FACTOR"])
    else:
        kwargs = exportIauracadAttributes(obj, kwargs, preferences["SCALE_FACTOR"])
    # in some cases object have wrong iauracadtypes, thus set it
    # https://forum.AuraCAD.org/viewtopic.php?f=39&t=50085
    if iauracadtype not in ArchIauracadSchema.IauracadProducts:
        # print("Wrong IauracadType: IauracadBuildingElementProxy is used. {}".format(iauracadtype))
        iauracadtype = "IauracadBuildingElementProxy"
    # print("createProduct: {}".format(iauracadtype))
    # print(kwargs)
    product = getattr(iauracadfile, "create" + iauracadtype)(**kwargs)
    return product


def getUID(obj, preferences):
    """gets or creates an UUID for an object"""

    global uids
    uid = None
    if hasattr(obj, "IauracadData"):
        if "IauracadUID" in obj.IauracadData:
            uid = str(obj.IauracadData["IauracadUID"])
            if uid in uids:
                # this UID  has already been used in another object
                uid = None
    if not uid:
        uid = iauracadopenshell.guid.new()
        # storing the uid for further use
        if preferences["STORE_UID"]:
            if hasattr(obj, "IauracadData"):
                d = obj.IauracadData
                d["IauracadUID"] = uid
                obj.IauracadData = d
            if hasattr(obj, "GlobalId"):
                obj.GlobalId = uid
    if "uids" in globals():
        uids.append(uid)
    return uid


def getText(field, obj):
    """Returns the value of a text property of an object"""

    result = ""
    if field == "Name":
        field = "Label"
    if hasattr(obj, field):
        result = getattr(obj, field)
    return result


def getAxisContext(iauracadfile):
    """gets or creates an axis context"""

    contexts = iauracadfile.by_type("IauracadGeometricRepresentationContext")
    # filter out subcontexts
    subcontexts = [c for c in contexts if c.is_a() == "IauracadGeometricRepresentationSubContext"]
    contexts = [c for c in contexts if c.is_a() == "IauracadGeometricRepresentationContext"]
    for ctx in subcontexts:
        if ctx.ContextIdentifier == "Axis":
            return ctx
    ctx = contexts[0]  # arbitrarily take the first one...
    nctx = iauracadfile.createIauracadGeometricRepresentationSubContext(
        "Axis", "Model", None, None, None, None, ctx, None, "MODEL_VIEW", None
    )
    return nctx


def createAxis(iauracadfile, obj, preferences, delta=None):
    """Creates an axis for a given wall, if applicable"""

    shape = None
    pla = AuraCAD.Placement(obj.Placement)
    if isinstance(delta, AuraCAD.Vector):
        pla.Base += delta
    if getattr(obj, "Nodes", None):
        shape = Part.makePolygon([pla.multVec(v) for v in obj.Nodes])
    elif hasattr(obj, "Base") and hasattr(obj.Base, "Shape") and obj.Base.Shape:
        shape = obj.Base.Shape
    if shape:
        if shape.ShapeType in ["Wire", "Edge"]:
            curve = createCurve(iauracadfile, shape, preferences["SCALE_FACTOR"])
            if curve:
                ctx = getAxisContext(iauracadfile)
                axis = iauracadfile.createIauracadShapeRepresentation(ctx, "Axis", "Curve2D", [curve])
                return axis
    return None


def writeJson(filename, iauracadfile):
    """writes an .iauracadjson file"""

    import json

    try:
        from iauracadjson import iauracad2json5a
    except Exception:
        try:
            import iauracad2json5a
        except Exception:
            print("Error: Unable to locate iauracad2json5a module. Aborting.")
            return
    print("Converting Iauracad to JSON...")
    jsonfile = iauracad2json5a.Iauracad2JSON5a(iauracadfile).spf2Json()
    f = pyopen(filename, "w")
    s = json.dumps(jsonfile, indent=4)
    # print("json:",s)
    f.write(s)
    f.close()


def create_annotation(anno, iauracadfile, context, history, preferences):
    """Creates an annotation object"""

    global curvestyles, iauracadbin
    reps = []
    repid = "Annotation"
    reptype = "Annotation2D"
    description = getattr(anno, "Description", None)
    # uses global iauracadbin, curvestyles
    objectType = None
    ovc = None
    zvc = None
    xvc = None
    reps = []
    repid = "Annotation"
    reptype = "Annotation2D"
    if anno.isDerivedFrom("Part::Feature"):
        if Draft.getType(anno) == "Hatch":
            objectType = "HATCH"
        elif getattr(anno.ViewObject, "EndArrow", False):
            objectType = "LEADER"
        elif anno.Shape.Faces:
            objectType = "AREA"
        elif Draft.getType(anno) == "Axis":
            axdata = anno.Proxy.getAxisData(anno)
            axes = []
            for ax in axdata:
                p1 = iauracadbin.createIauracadCartesianPoint(
                    tuple(AuraCAD.Vector(ax[0]).multiply(preferences["SCALE_FACTOR"])[:2])
                )
                p2 = iauracadbin.createIauracadCartesianPoint(
                    tuple(AuraCAD.Vector(ax[1]).multiply(preferences["SCALE_FACTOR"])[:2])
                )
                pol = iauracadbin.createIauracadPolyline([p1, p2])
                axis = iauracadfile.createIauracadGridAxis(ax[2], pol, True)
                axes.append(axis)
            if axes:
                if len(axes) > 1:
                    print(
                        "DEBUG: exportIauracad.create_annotation: Cannot create more than one axis",
                        anno.Label,
                    )
                return axes[0]
            else:
                print("Unable to handle object", anno.Label)
                return None
        else:
            objectType = "LINEWORK"
        sh = anno.Shape.copy()
        sh.scale(preferences["SCALE_FACTOR"])  # to meters
        ehc = []
        curves = []
        for w in sh.Wires:
            curves.append(createCurve(iauracadfile, w))
            for e in w.Edges:
                ehc.append(e.hashCode())
        if curves:
            reps.append(iauracadfile.createIauracadGeometricCurveSet(curves))
        curves = []
        for e in sh.Edges:
            if e.hashCode not in ehc:
                curves.append(createCurve(iauracadfile, e))
        if curves:
            reps.append(iauracadfile.createIauracadGeometricCurveSet(curves))
    elif anno.isDerivedFrom("App::Annotation"):
        objectType = "TEXT"
        l = AuraCAD.Vector(anno.Position).multiply(preferences["SCALE_FACTOR"])
        pos = iauracadbin.createIauracadCartesianPoint((0.0, 0.0, 0.0))
        tpl = iauracadbin.createIauracadAxis2Placement3D(pos, None, None)
        ovc = iauracadbin.createIauracadCartesianPoint((l.x, l.y, l.z))
        s = ";".join(anno.LabelText)
        txt = iauracadfile.createIauracadTextLiteral(s, tpl, "LEFT")
        reps = [txt]
    elif Draft.getType(anno) in ["DraftText", "Text"]:
        objectType = "TEXT"
        l = AuraCAD.Vector(anno.Placement.Base).multiply(preferences["SCALE_FACTOR"])
        pos = iauracadbin.createIauracadCartesianPoint((0.0, 0.0, 0.0))
        tpl = iauracadbin.createIauracadAxis2Placement3D(pos, None, None)
        ovc = iauracadbin.createIauracadCartesianPoint((l.x, l.y, l.z))
        zvc = iauracadbin.createIauracadDirection(
            tuple(anno.Placement.Rotation.multVec(AuraCAD.Vector(0, 0, 1)))
        )
        xvc = iauracadbin.createIauracadDirection(
            tuple(anno.Placement.Rotation.multVec(AuraCAD.Vector(1, 0, 0)))
        )
        alg = "LEFT"
        if AuraCAD.GuiUp and hasattr(anno.ViewObject, "Justification"):
            if anno.ViewObject.Justification == "Right":
                alg = "RIGHT"
        s = ";".join(anno.Text)
        txt = iauracadfile.createIauracadTextLiteral(s, tpl, alg)
        reps = [txt]
    elif Draft.getType(anno) in ["Dimension", "LinearDimension", "AngularDimension"]:
        if AuraCAD.GuiUp:
            objectType = "DIMENSION"
            vp = anno.ViewObject.Proxy
            if "BBIMDIMS" in preferences and preferences["BBIMDIMS"]:
                sh = Part.makePolygon([vp.p2, vp.p3])
            else:
                sh = Part.makePolygon([vp.p1, vp.p2, vp.p3, vp.p4])
            sh.scale(preferences["SCALE_FACTOR"])  # to meters
            curve = createCurve(iauracadfile, sh)
            reps = [iauracadfile.createIauracadGeometricCurveSet([curve])]
            # Append text
            l = AuraCAD.Vector(vp.tbase).multiply(preferences["SCALE_FACTOR"])
            zdir = None
            xdir = None
            if hasattr(vp, "trot"):
                r = AuraCAD.Rotation(vp.trot[0], vp.trot[1], vp.trot[2], vp.trot[3])
                zdir = iauracadbin.createIauracadDirection(tuple(r.multVec(AuraCAD.Vector(0, 0, 1))))
                xdir = iauracadbin.createIauracadDirection(tuple(r.multVec(AuraCAD.Vector(1, 0, 0))))
            pos = iauracadbin.createIauracadCartesianPoint((l.x, l.y, l.z))
            tpl = iauracadbin.createIauracadAxis2Placement3D(pos, zdir, xdir)
            txt = iauracadfile.createIauracadTextLiteral(vp.string, tpl, "LEFT")
            reps.append(txt)
    elif Draft.getType(anno) == "SectionPlane":
        p = AuraCAD.Vector(anno.Placement.Base).multiply(preferences["SCALE_FACTOR"])
        ovc = iauracadbin.createIauracadCartesianPoint((p.x, p.y, p.z))
        zvc = iauracadbin.createIauracadDirection(
            tuple(anno.Placement.Rotation.multVec(AuraCAD.Vector(0, 0, 1)))
        )
        xvc = iauracadbin.createIauracadDirection(
            tuple(anno.Placement.Rotation.multVec(AuraCAD.Vector(1, 0, 0)))
        )
        objectType = "DRAWING"
        l = w = h = 1000
        if anno.ViewObject:
            if anno.ViewObject.DisplayLength.Value:
                l = anno.ViewObject.DisplayLength.Value
            if anno.ViewObject.DisplayHeight.Value:
                w = anno.ViewObject.DisplayHeight.Value
        if anno.Depth.Value:
            h = anno.Depth.Value
        l = AuraCAD.Vector(l, w, h).multiply(preferences["SCALE_FACTOR"])
        zdir = iauracadbin.createIauracadDirection((0.0, 0.0, 1.0))
        xdir = iauracadbin.createIauracadDirection((1.0, 0.0, 0.0))
        pos = iauracadbin.createIauracadCartesianPoint((-l.x / 2, -l.y / 2, -l.z))
        tpl = iauracadbin.createIauracadAxis2Placement3D(pos, zdir, xdir)
        blk = iauracadfile.createIauracadBlock(tpl, l.x, l.y, l.z)
        csg = iauracadfile.createIauracadCsgSolid(blk)
        reps = [csg]
        repid = "Body"
        reptype = "CSG"
    else:
        print("Unable to handle object", anno.Label)
        return None

    for coldef in ["LineColor", "TextColor", "ShapeColor"]:
        if hasattr(anno.ViewObject, coldef):
            rgb = getattr(anno.ViewObject, coldef)[:3]
            if rgb in curvestyles:
                psa = curvestyles[rgb]
            else:
                col = iauracadbin.createIauracadColourRgb(rgb[0], rgb[1], rgb[2])
                cvf = iauracadfile.createIauracadDraughtingPredefinedCurveFont("continuous")
                ics = iauracadfile.createIauracadCurveStyle("Line", cvf, None, col)
                psa = iauracadfile.createIauracadPresentationStyleAssignment([ics])
                curvestyles[rgb] = psa
            for rep in reps:
                isi = iauracadfile.createIauracadStyledItem(rep, [psa], None)
            break
    if not xvc:
        xvc = iauracadbin.createIauracadDirection((1.0, 0.0, 0.0))
    if not zvc:
        zvc = iauracadbin.createIauracadDirection((0.0, 0.0, 1.0))
    if not ovc:
        ovc = iauracadbin.createIauracadCartesianPoint((0.0, 0.0, 0.0))
    gpl = iauracadbin.createIauracadAxis2Placement3D(ovc, zvc, xvc)
    placement = iauracadbin.createIauracadLocalPlacement(gpl)
    shp = iauracadfile.createIauracadShapeRepresentation(context, "Annotation", "Annotation2D", reps)
    rep = iauracadfile.createIauracadProductDefinitionShape(None, None, [shp])
    label = anno.Label
    description = getattr(anno, "Description", "")
    ann = iauracadfile.createIauracadAnnotation(
        iauracadopenshell.guid.new(), history, label, description, objectType, placement, rep
    )
    return ann
