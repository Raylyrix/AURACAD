# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2011 Yorik van Havre <yorik@uncreated.net>              *
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

# WARNING ##################################################################
#                                                                          #
#    This module is deprecated and will be removed in a future version     #
#                                                                          #
############################################################################

__title__ = "AuraCAD Iauracad importer"
__author__ = "Yorik van Havre"
__url__ = "https://www.AuraCAD.org"

import math
import os
import re
import time
import uuid

from builtins import open as pyopen

import AuraCAD
import Arch
import Draft
import DraftVecUtils
import Part

from draftutils import params
from draftutils.translate import translate

# config
subtractiveTypes = ["IauracadOpeningElement"]  # elements that must be subtracted from their parents
SCHEMA = "http://www.steptools.com/support/stdev_docs/iauracadbim/iauracad4.exp"  # only for internal parser
MAKETEMPFILES = False  # if True, shapes are passed from iauracadopenshell to AuraCAD through temp files
DEBUG = True  # this is only for the python console, this value is overridden when importing through the GUI
SKIP = [
    "IauracadBuildingElementProxy",
    "IauracadFlowTerminal",
    "IauracadFurnishingElement",
]  # default. overwritten by the GUI options
IauracadLINE_RE = re.compile(r"#(\d+)[ ]?=[ ]?(.*?)\((.*)\);[\\r]?$")
APPLYFIX = True  # if true, the iauracadopenshell bug-fixing function is applied when saving files
# end config

# supported iauracad products (export only):
supportedIauracadTypes = [
    "IauracadSite",
    "IauracadBuilding",
    "IauracadBuildingStorey",
    "IauracadBeam",
    "IauracadBeamStandardCase",
    "IauracadChimney",
    "IauracadColumn",
    "IauracadColumnStandardCase",
    "IauracadCovering",
    "IauracadCurtainWall",
    "IauracadDoor",
    "IauracadDoorStandardCase",
    "IauracadMember",
    "IauracadMemberStandardCase",
    "IauracadPlate",
    "IauracadPlateStandardCase",
    "IauracadRailing",
    "IauracadRamp",
    "IauracadRampFlight",
    "IauracadRoof",
    "IauracadSlab",
    "IauracadStair",
    "IauracadStairFlight",
    "IauracadWall",
    "IauracadSpace",
    "IauracadWallStandardCase",
    "IauracadWindow",
    "IauracadWindowStandardCase",
    "IauracadBuildingElementProxy",
    "IauracadPile",
    "IauracadFooting",
    "IauracadReinforcingBar",
    "IauracadTendon",
]
# TODO : shading device not supported?


def open(filename, skip=None):
    "called when AuraCAD opens a file"
    docname = os.path.splitext(os.path.basename(filename))[0]
    doc = AuraCAD.newDocument(docname)
    doc.Label = docname
    AuraCAD.ActiveDocument = doc
    getConfig()
    read(filename, skip)
    return doc


def insert(filename, docname, skip=None):
    "called when AuraCAD wants to import a file"
    try:
        doc = AuraCAD.getDocument(docname)
    except NameError:
        doc = AuraCAD.newDocument(docname)
    AuraCAD.ActiveDocument = doc
    getConfig()
    read(filename, skip)
    return doc


def getConfig():
    "Gets Arch Iauracad import preferences"
    global SKIP, CREATE_IAuraCAD_GROUPS, ASMESH, PREFIX_NUMBERS, FORCE_PYTHON_PARSER, SEPARATE_OPENINGS, SEPARATE_PLACEMENTS, JOINSOLIDS, AGGREGATE_WINDOWS
    IMPORT_IAuraCAD_FURNITURE = False
    ASMESH = ["IauracadFurnishingElement"]
    CREATE_IAuraCAD_GROUPS = params.get_param_arch("createIauracadGroups")
    FORCE_PYTHON_PARSER = params.get_param_arch("forceIauracadPythonParser")
    DEBUG = params.get_param_arch("iauracadDebug")
    SEPARATE_OPENINGS = params.get_param_arch("iauracadSeparateOpenings")
    SEPARATE_PLACEMENTS = params.get_param_arch("iauracadSeparatePlacements")
    PREFIX_NUMBERS = params.get_param_arch("iauracadPrefixNumbers")
    JOINSOLIDS = params.get_param_arch("iauracadJoinSolids")
    AGGREGATE_WINDOWS = params.get_param_arch("iauracadAggregateWindows")
    skiplist = params.get_param_arch("iauracadSkip")
    if skiplist:
        SKIP = skiplist.split(",")
    asmeshlist = params.get_param_arch("iauracadAsMesh")
    if asmeshlist:
        ASMESH = asmeshlist.split(",")


def getIauracadOpenShell():
    "locates and imports iauracadopenshell"
    global IauracadOPENSHELL5
    global IauracadImport
    IauracadOPENSHELL5 = False
    try:
        import IauracadImport
    except ImportError:
        try:
            import iAuraCAD_wrapper as IauracadImport
        except ImportError:
            AuraCAD.Console.PrintMessage(translate("Arch", "Could not locate IauracadOpenShell") + "\n")
            return False
        else:
            IauracadOPENSHELL5 = True
            return True
    else:
        if hasattr(IauracadImport, "IauracadFile"):
            IauracadOPENSHELL5 = True
        return True


def read(filename, skip=None):
    "Parses an Iauracad file"

    # parsing the Iauracad file
    t1 = time.time()

    processedIds = []
    skipIds = skip
    if not skipIds:
        skipIds = []
    elif isinstance(skipIds, int):
        skipIds = [skipIds]

    if getIauracadOpenShell() and not FORCE_PYTHON_PARSER:
        # use the IauracadOpenShell parser

        # preparing IauracadOpenShell
        if DEBUG:
            global iauracadObjects, iauracadParents
        iauracadObjects = {}  # a table to relate iauracad id with AuraCAD object
        iauracadParents = {}  # a table to relate iauracad id with parent id
        if SEPARATE_OPENINGS:
            if not IauracadOPENSHELL5:
                if hasattr(IauracadImport, "DISABLE_OPENING_SUBTRACTIONS"):
                    IauracadImport.Settings(IauracadImport.DISABLE_OPENING_SUBTRACTIONS, True)
        else:
            SKIP.append("IauracadOpeningElement")
        useShapes = False
        if IauracadOPENSHELL5:
            useShapes = True
            if hasattr(IauracadImport, "clean"):
                IauracadImport.clean()
        elif hasattr(IauracadImport, "USE_BREP_DATA"):
            IauracadImport.Settings(IauracadImport.USE_BREP_DATA, True)
            useShapes = True
        else:
            if DEBUG:
                print("Warning: IauracadOpenShell version very old, unable to handle Brep data")

        # opening file
        if IauracadOPENSHELL5:
            global iauracad
            iauracad = IauracadImport.open(filename)
            objects = iauracad.by_type("IauracadProduct")
            num_lines = len(objects)
            relations = (
                iauracad.by_type("IauracadRelAggregates")
                + iauracad.by_type("IauracadRelContainedInSpatialStructure")
                + iauracad.by_type("IauracadRelVoidsElement")
            )
            if not objects:
                print("Error opening Iauracad file")
                return
        else:
            num_lines = sum(1 for line in pyopen(filename))
            if not IauracadImport.Init(filename):
                print("Error opening Iauracad file")
                return

        # processing geometry
        idx = 0
        while True:
            objparentid = []
            if IauracadOPENSHELL5:
                obj = objects[idx]
                idx += 1
                objid = int(str(obj).split("=")[0].strip("#"))
                objname = obj.get_argument(obj.get_argument_index("Name"))
                objtype = str(obj).split("=")[1].split("(")[0]
                for r in relations:
                    if r.is_a("IauracadRelAggregates"):
                        for c in getAttr(r, "RelatedObjects"):
                            if str(obj) == str(c):
                                objparentid.append(
                                    int(str(getAttr(r, "RelatingObject")).split("=")[0].strip("#"))
                                )
                    elif r.is_a("IauracadRelContainedInSpatialStructure"):
                        for c in getAttr(r, "RelatedElements"):
                            if str(obj) == str(c):
                                objparentid.append(
                                    int(
                                        str(getAttr(r, "RelatingStructure"))
                                        .split("=")[0]
                                        .strip("#")
                                    )
                                )
                    elif r.is_a("IauracadRelVoidsElement"):
                        if str(obj) == str(getAttr(r, "RelatedOpeningElement")):
                            objparentid.append(
                                int(
                                    str(getAttr(r, "RelatingBuildingElement"))
                                    .split("=")[0]
                                    .strip("#")
                                )
                            )

            else:
                if hasattr(IauracadImport, "GetBrepData"):
                    obj = IauracadImport.GetBrepData()
                else:
                    obj = IauracadImport.Get()
                objid = obj.id
                idx = objid
                objname = obj.name
                objtype = obj.type
                objparentid.append(obj.parent_id)
            if DEBUG:
                print(
                    "[" + str(int((float(idx) / num_lines) * 100)) + "%] parsing ",
                    objid,
                    ": ",
                    objname,
                    " of type ",
                    objtype,
                )

            # retrieving name
            n = getCleanName(objname, objid, objtype)

            # skip IDs
            if objid in skipIds:
                if DEBUG:
                    print("    skipping because object ID is in skip list")
                nobj = None

            # skip types
            elif objtype in SKIP:
                if DEBUG:
                    print("    skipping because type is in skip list")
                nobj = None

            # check if object was already processed, to workaround an iauracadopenshell bug
            elif objid in processedIds:
                if DEBUG:
                    print("    skipping because this object was already processed")

            else:
                # build shape
                shape = None
                if useShapes:
                    shape = getShape(obj, objid)

                # walls
                if objtype in ["IauracadWallStandardCase", "IauracadWall"]:
                    nobj = makeWall(objid, shape, n)

                # windows
                elif objtype in ["IauracadWindow", "IauracadDoor"]:
                    nobj = makeWindow(objid, shape, n)

                # structs
                elif objtype in ["IauracadBeam", "IauracadColumn", "IauracadSlab", "IauracadFooting"]:
                    nobj = makeStructure(objid, shape, objtype, n)

                # roofs
                elif objtype in ["IauracadRoof"]:
                    nobj = makeRoof(objid, shape, n)

                # furniture
                elif objtype in ["IauracadFurnishingElement"]:
                    nobj = AuraCAD.ActiveDocument.addObject("Part::Feature", n)
                    nobj.Shape = shape

                # sites
                elif objtype in ["IauracadSite"]:
                    nobj = makeSite(objid, shape, n)

                # floors
                elif objtype in ["IauracadBuildingStorey"]:
                    nobj = Arch.makeFloor(name=n)
                    nobj.Label = n

                # floors
                elif objtype in ["IauracadBuilding"]:
                    nobj = Arch.makeBuilding(name=n)
                    nobj.Label = n

                # spaces
                elif objtype in ["IauracadSpace"]:
                    nobj = makeSpace(objid, shape, n)

                elif shape:
                    # treat as dumb parts
                    if DEBUG:
                        print("Fixme: Shape-containing object not handled: ", objid, " ", objtype)
                    nobj = AuraCAD.ActiveDocument.addObject("Part::Feature", n)
                    nobj.Label = n
                    nobj.Shape = shape

                else:
                    # treat as meshes
                    if DEBUG:
                        print("Warning: Object without shape: ", objid, " ", objtype)
                    if hasattr(obj, "mesh"):
                        if not hasattr(obj.mesh, "verts"):
                            obj = IauracadImport.Get()  # Get triangulated rep of same product
                        me, pl = getMesh(obj)
                        nobj = AuraCAD.ActiveDocument.addObject("Mesh::Feature", n)
                        nobj.Label = n
                        nobj.Mesh = me
                        nobj.Placement = pl
                    else:
                        if DEBUG:
                            print("Error: Skipping object without mesh: ", objid, " ", objtype)

                # registering object number and parent
                if objparentid:
                    iauracadParents[objid] = []
                    for p in objparentid:
                        iauracadParents[objid].append([p, not (objtype in subtractiveTypes)])
                iauracadObjects[objid] = nobj
                processedIds.append(objid)

            if IauracadOPENSHELL5:
                if idx >= len(objects):
                    break
            else:
                if not IauracadImport.Next():
                    break

        # processing non-geometry and relationships
        parents_temp = dict(iauracadParents)
        import ArchCommands

        # print(parents_temp)

        while parents_temp:
            id, comps = parents_temp.popitem()
            for c in comps:
                parent_id = c[0]
                additive = c[1]

                if (id <= 0) or (parent_id <= 0):
                    # root dummy object
                    parent = None

                elif parent_id in iauracadObjects:
                    parent = iauracadObjects[parent_id]
                    # check if parent is a subtraction, if yes parent to grandparent
                    if parent_id in iauracadParents:
                        for p in iauracadParents[parent_id]:
                            if p[1] == False:
                                grandparent_id = p[0]
                                if grandparent_id in iauracadObjects:
                                    parent = iauracadObjects[grandparent_id]
                else:
                    # creating parent if needed
                    if IauracadOPENSHELL5:
                        obj = iauracad.by_id(parent_id)
                        parentid = int(str(obj).split("=")[0].strip("#"))
                        parentname = obj.get_argument(obj.get_argument_index("Name"))
                        parenttype = str(obj).split("=")[1].split("(")[0]
                    else:
                        obj = IauracadImport.GetObject(parent_id)
                        parentid = obj.id
                        parentname = obj.name
                        parenttype = obj.type
                    # if DEBUG: print("["+str(int((float(idx)/num_lines)*100))+"%] parsing ",parentid,": ",parentname," of type ",parenttype)
                    n = getCleanName(parentname, parentid, parenttype)
                    if parentid <= 0:
                        parent = None
                    elif parenttype == "IauracadBuildingStorey":
                        parent = Arch.makeFloor(name=n)
                        parent.Label = n
                    elif parenttype == "IauracadBuilding":
                        parent = Arch.makeBuilding(name=n)
                        parent.Label = n
                    elif parenttype == "IauracadSite":
                        parent = Arch.makeSite(name=n)
                        parent.Label = n
                    elif parenttype == "IauracadWindow":
                        parent = Arch.makeWindow(name=n)
                        parent.Label = n
                    elif parenttype == "IauracadProject":
                        parent = None
                    else:
                        if DEBUG:
                            print("Fixme: skipping unhandled parent: ", parentid, " ", parenttype)
                        parent = None
                    # registering object number and parent
                    if not IauracadOPENSHELL5:
                        if parent_iauracadobj.parent_id > 0:
                            iauracadParents[parentid] = [parent_iauracadobj.parent_id, True]
                            parents_temp[parentid] = [parent_iauracadobj.parent_id, True]
                        if parent and (not parentid in iauracadObjects):
                            iauracadObjects[parentid] = parent

                # attributing parent
                if parent and (id in iauracadObjects):
                    if iauracadObjects[id] and (iauracadObjects[id].Name != parent.Name):
                        if additive:
                            if DEBUG:
                                print("adding ", iauracadObjects[id].Name, " to ", parent.Name)
                            ArchCommands.addComponents(iauracadObjects[id], parent)
                        else:
                            if DEBUG:
                                print("removing ", iauracadObjects[id].Name, " from ", parent.Name)
                            ArchCommands.removeComponents(iauracadObjects[id], parent)
        if not IauracadOPENSHELL5:
            IauracadImport.CleanUp()

    else:
        # use only the internal python parser

        AuraCAD.Console.PrintWarning(
            translate(
                "Arch", "IauracadOpenShell not found or disabled, falling back on internal parser."
            )
            + "\n"
        )
        schema = getSchema()
        if schema:
            if DEBUG:
                print("opening", filename, "...")
            iauracad = IauracadDocument(filename, schema=schema)
        else:
            AuraCAD.Console.PrintWarning(
                translate("Arch", "Iauracad Schema not found, Iauracad import disabled.") + "\n"
            )
            return None
        t2 = time.time()
        if DEBUG:
            print("Successfully loaded", iauracad, "in %s s" % ((t2 - t1)))

        # getting walls
        for w in iauracad.getEnt("IauracadWallStandardCase"):
            nobj = makeWall(w)

        # getting windows and doors
        for w in iauracad.getEnt("IauracadWindow") + iauracad.getEnt("IauracadDoor"):
            nobj = makeWindow(w)

        # getting structs
        for w in (
            iauracad.getEnt("IauracadSlab")
            + iauracad.getEnt("IauracadBeam")
            + iauracad.getEnt("IauracadColumn")
            + iauracad.getEnt("IauracadFooting")
        ):
            nobj = makeStructure(w)

        # getting floors
        for f in iauracad.getEnt("IauracadBuildingStorey"):
            group(f, iauracad, "Floor")

        # getting buildings
        for b in iauracad.getEnt("IauracadBuilding"):
            group(b, iauracad, "Building")

        # getting sites
        for s in iauracad.getEnt("IauracadSite"):
            group(s, iauracad, "Site")

    if DEBUG:
        print("done parsing. Recomputing...")
    AuraCAD.ActiveDocument.recompute()
    t3 = time.time()
    if DEBUG:
        print("done processing Iauracad file in %s s" % ((t3 - t1)))

    return None


def getCleanName(name, iauracadid, iauracadtype):
    "Get a clean name from an iauracad object"
    # print("getCleanName called",name,iauracadid,iauracadtype)
    n = name
    if not n:
        n = iauracadtype
    if PREFIX_NUMBERS:
        n = "ID" + str(iauracadid) + " " + n
    # for c in ",.!?;:":
    #    n = n.replace(c,"_")
    return n


def makeWall(entity, shape=None, name="Wall"):
    "makes a wall in the AuraCAD document"
    try:
        if shape:
            # use iauracadopenshell
            if isinstance(shape, Part.Shape):
                body = AuraCAD.ActiveDocument.addObject("Part::Feature", name + "_body")
                body.Shape = shape
            else:
                body = AuraCAD.ActiveDocument.addObject("Mesh::Feature", name + "_body")
                body.Mesh = shape
            wall = Arch.makeWall(body, name=name)
            wall.Label = name
            if DEBUG:
                print("    made wall object ", entity, ":", wall)
            return wall

        # use internal parser
        if DEBUG:
            print("=====> making wall", entity.id)
        placement = wall = wire = body = width = height = None
        placement = getPlacement(entity.ObjectPlacement)
        if DEBUG:
            print("    got wall placement", entity.id, ":", placement)
        width = entity.getProperty("Width")
        height = entity.getProperty("Height")
        if width and height:
            if DEBUG:
                print("    got width, height ", entity.id, ":", width, "/", height)
            for r in entity.Representation.Representations:
                if r.RepresentationIdentifier == "Axis":
                    wire = getWire(r.Items, placement)
                    wall = Arch.makeWall(
                        wire, width, height, align="Center", name="Wall" + str(entity.id)
                    )
        else:
            if DEBUG:
                print("    no height or width properties found...")
            for r in entity.Representation.Representations:
                if r.RepresentationIdentifier == "Body":
                    for b in r.Items:
                        if b.type == "IauracadEXTRUDEDAREASOLID":
                            norm = getVector(b.ExtrudedDirection)
                            norm.normalize()
                            wire = getWire(b.SweptArea, placement)
                            wall = Arch.makeWall(
                                wire, width=0, height=b.Depth, name="Wall" + str(entity.id)
                            )
                            wall.Normal = norm
        if wall:
            if DEBUG:
                print("    made wall object  ", entity.id, ":", wall)
            return wall
        if DEBUG:
            print("    error: skipping wall", entity.id)
        return None
    except Exception:
        if DEBUG:
            print("    error: skipping wall", entity)
        return None


def makeWindow(entity, shape=None, name="Window"):
    "makes a window in the AuraCAD document"
    try:
        if shape:
            # use iauracadopenshell
            if isinstance(shape, Part.Shape):
                window = Arch.makeWindow(name=name)
                window.Shape = shape
                window.Label = name
                if DEBUG:
                    print("    made window object  ", entity, ":", window)
                return window

        # use internal parser
        if DEBUG:
            print("=====> making window", entity.id)
        placement = window = wire = body = width = height = None
        placement = getPlacement(entity.ObjectPlacement)
        if DEBUG:
            print("got window placement", entity.id, ":", placement)
        width = entity.getProperty("Width")
        height = entity.getProperty("Height")
        for r in entity.Representation.Representations:
            if r.RepresentationIdentifier == "Body":
                for b in r.Items:
                    if b.type == "IauracadEXTRUDEDAREASOLID":
                        wire = getWire(b.SweptArea, placement)
                        window = Arch.makeWindow(wire, width=b.Depth, name=objtype + str(entity.id))
        if window:
            if DEBUG:
                print("    made window object  ", entity.id, ":", window)
            return window
        if DEBUG:
            print("    error: skipping window", entity.id)
        return None
    except Exception:
        if DEBUG:
            print("    error: skipping window", entity)
        return None


def makeStructure(entity, shape=None, iauracadtype=None, name="Structure"):
    "makes a structure in the AuraCAD document"
    try:
        if shape:
            # use iauracadopenshell
            if isinstance(shape, Part.Shape):
                body = AuraCAD.ActiveDocument.addObject("Part::Feature", name + "_body")
                body.Shape = shape
            else:
                body = AuraCAD.ActiveDocument.addObject("Mesh::Feature", name + "_body")
                body.Mesh = shape
            structure = Arch.makeStructure(body, name=name)
            structure.Label = name
            if iauracadtype == "IauracadBeam":
                structure.Role = "Beam"
            elif iauracadtype == "IauracadColumn":
                structure.Role = "Column"
            elif iauracadtype == "IauracadSlab":
                structure.Role = "Slab"
            elif iauracadtype == "IauracadFooting":
                structure.Role = "Foundation"
            if DEBUG:
                print(
                    "    made structure object  ", entity, ":", structure, " (type: ", iauracadtype, ")"
                )
            return structure

        # use internal parser
        if DEBUG:
            print("=====> making struct", entity.id)
        placement = structure = wire = body = width = height = None
        placement = getPlacement(entity.ObjectPlacement)
        if DEBUG:
            print("got window placement", entity.id, ":", placement)
        width = entity.getProperty("Width")
        height = entity.getProperty("Height")
        for r in entity.Representation.Representations:
            if r.RepresentationIdentifier == "Body":
                for b in r.Items:
                    if b.type == "IauracadEXTRUDEDAREASOLID":
                        wire = getWire(b.SweptArea, placement)
                        structure = Arch.makeStructure(
                            wire, height=b.Depth, name=objtype + str(entity.id)
                        )
        if structure:
            if DEBUG:
                print("    made structure object  ", entity.id, ":", structure)
            return structure
        if DEBUG:
            print("    error: skipping structure", entity.id)
        return None
    except Exception:
        if DEBUG:
            print("    error: skipping structure", entity)
        return None


def makeSite(entity, shape=None, name="Site"):
    "makes a site in the AuraCAD document"
    try:
        body = None
        if shape:
            # use iauracadopenshell
            if isinstance(shape, Part.Shape):
                body = AuraCAD.ActiveDocument.addObject("Part::Feature", name + "_body")
                body.Shape = shape
            else:
                body = AuraCAD.ActiveDocument.addObject("Mesh::Feature", name + "_body")
                body.Mesh = shape
        site = Arch.makeSite(name=name)
        site.Label = name
        if body:
            site.Terrain = body
        if DEBUG:
            print("    made site object  ", entity, ":", site)
        return site
    except Exception:
        return None


def makeSpace(entity, shape=None, name="Space"):
    "makes a space in the AuraCAD document"
    try:
        if shape:
            # use iauracadopenshell
            if isinstance(shape, Part.Shape):
                space = Arch.makeSpace(name=name)
                space.Label = name
                body = AuraCAD.ActiveDocument.addObject("Part::Feature", name + "_body")
                body.Shape = shape
                space.Base = body
                body.ViewObject.hide()
                if DEBUG:
                    print("    made space object  ", entity, ":", space)
                return space
    except Exception:
        return None


def makeRoof(entity, shape=None, name="Roof"):
    "makes a roof in the AuraCAD document"
    try:
        if shape:
            # use iauracadopenshell
            if isinstance(shape, Part.Shape):
                roof = Arch.makeRoof(name=name)
                roof.Label = name
                roof.Shape = shape
                if DEBUG:
                    print("    made roof object  ", entity, ":", roof)
                return roof
    except Exception:
        return None


# geometry helpers ###################################################################


def getMesh(obj):
    "gets mesh and placement from an IauracadOpenShell object"
    if IauracadOPENSHELL5:
        return None, None
        print("fixme: mesh data not yet supported")  # TODO implement this with OCC tessellate
    import Mesh

    meshdata = []
    print(obj.mesh.faces)
    print(obj.mesh.verts)
    f = obj.mesh.faces
    v = obj.mesh.verts
    for i in range(0, len(f), 3):
        face = []
        for j in range(3):
            vi = f[i + j] * 3
            face.append([v[vi], v[vi + 1], v[vi + 2]])
        meshdata.append(face)
        print(meshdata)
    me = Mesh.Mesh(meshdata)
    # get transformation matrix
    m = obj.matrix
    # fmt: off
    mat = AuraCAD.Matrix(m[0], m[3], m[6], m[9],
                         m[1], m[4], m[7], m[10],
                         m[2], m[5], m[8], m[11],
                         0, 0, 0, 1)
    # fmt: on
    pl = AuraCAD.Placement(mat)
    return me, pl


def getShape(obj, objid):
    "gets a shape from an IauracadOpenShell object"
    # print("retrieving shape from obj ",objid)
    import Part

    sh = Part.Shape()
    brep_data = None
    if IauracadOPENSHELL5:
        try:
            if hasattr(IauracadImport, "SEW_SHELLS"):
                ss = IauracadImport.SEW_SHELLS
            else:
                ss = 0
            if SEPARATE_OPENINGS and hasattr(IauracadImport, "DISABLE_OPENING_SUBTRACTIONS"):
                if SEPARATE_PLACEMENTS and hasattr(IauracadImport, "DISABLE_OBJECT_PLACEMENT"):
                    brep_data = IauracadImport.create_shape(
                        obj,
                        IauracadImport.DISABLE_OPENING_SUBTRACTIONS
                        | IauracadImport.DISABLE_OBJECT_PLACEMENT
                        | ss,
                    )
                else:
                    brep_data = IauracadImport.create_shape(
                        obj, IauracadImport.DISABLE_OPENING_SUBTRACTIONS | ss
                    )
            else:
                if SEPARATE_PLACEMENTS and hasattr(IauracadImport, "DISABLE_OBJECT_PLACEMENT"):
                    brep_data = IauracadImport.create_shape(obj, IauracadImport.DISABLE_OBJECT_PLACEMENT | ss)
                else:
                    brep_data = IauracadImport.create_shape(obj, ss)
        except Exception:
            print("Unable to retrieve shape data")
    else:
        brep_data = obj.mesh.brep_data
    if brep_data:
        try:
            if MAKETEMPFILES:
                import tempfile

                th, tf = tempfile.mkstemp(suffix=".brp")
                of = pyopen(tf, "wb")
                of.write(brep_data)
                of.close()
                os.close(th)
                sh = Part.read(tf)
                os.remove(tf)
            else:
                sh.importBrepFromString(brep_data)
        except Exception:
            print("    error: malformed shape")
            return None
        else:
            if IauracadOPENSHELL5 and SEPARATE_PLACEMENTS:
                p = getPlacement(getAttr(obj, "ObjectPlacement"))
                if p:
                    sh.Placement = p
    if not sh.Solids:
        # try to extract a solid shape
        if sh.Faces:
            try:
                if DEBUG:
                    print("    malformed solid. Attempting to fix...")
                shell = Part.makeShell(sh.Faces)
                if shell:
                    solid = Part.makeSolid(shell)
                    if solid:
                        sh = solid
            except Exception:
                if DEBUG:
                    print("    failed to retrieve solid from object ", objid)
        else:
            if DEBUG:
                print("    object ", objid, " does not contain any geometry")
    if not IauracadOPENSHELL5:
        m = obj.matrix
        # fmt: off
        mat = AuraCAD.Matrix(m[0], m[3], m[6], m[9],
                             m[1], m[4], m[7], m[10],
                             m[2], m[5], m[8], m[11],
                             0, 0, 0, 1)
        # fmt: on
        sh.Placement = AuraCAD.Placement(mat)
    # if DEBUG: print("getting Shape from ",obj)
    # print("getting shape: ",sh,sh.Solids,sh.Volume,sh.isValid(),sh.isNull())
    # for v in sh.Vertexes: print(v.Point)
    if sh:
        if not sh.isNull():
            return sh
    return None


def getPlacement(entity):
    "returns a placement from the given entity"
    if not entity:
        return None
    if DEBUG:
        print("    getting placement ", entity)
    if IauracadOPENSHELL5:
        if isinstance(entity, int):
            entity = iauracad.by_id(entity)
        entitytype = str(entity).split("=")[1].split("(")[0].upper()
        entityid = int(str(entity).split("=")[0].strip("#"))
    else:
        entitytype = entity.type.upper()
        entityid = entity.id
    pl = None
    if entitytype == "IauracadAXIS2PLACEMENT3D":
        x = getVector(getAttr(entity, "RefDirection"))
        z = getVector(getAttr(entity, "Axis"))
        if not (x) or not (z):
            return None
        y = z.cross(x)
        loc = getVector(getAttr(entity, "Location"))
        m = DraftVecUtils.getPlaneRotation(x, y, z)
        pl = AuraCAD.Placement(m)
        pl.move(loc)
    elif entitytype == "IauracadLOCALPLACEMENT":
        pl = getPlacement(getAttr(entity, "PlacementRelTo"))
        relpl = getPlacement(getAttr(entity, "RelativePlacement"))
        if pl and relpl:
            pl = relpl.multiply(pl)
        elif relpl:
            pl = relpl
    elif entitytype == "IauracadCARTESIANPOINT":
        loc = getVector(entity)
        pl = AuraCAD.Placement()
        pl.move(loc)
    if DEBUG:
        print("    made placement for ", entityid, ":", pl)
    return pl


def getAttr(entity, attr):
    "returns the given attribute from the given entity"
    if IauracadOPENSHELL5:
        if isinstance(entity, int):
            entity = iauracad.by_id(entity)
        i = entity.get_argument_index(attr)
        return entity.get_argument(i)
    else:
        return getattr(entity, attr)


def getVector(entity):
    "returns a vector from the given entity"
    if not entity:
        return None
    if DEBUG:
        print("    getting point from ", entity)
    if IauracadOPENSHELL5:
        if isinstance(entity, int):
            entity = iauracad.by_id(entity)
        entitytype = str(entity).split("=")[1].split("(")[0].upper()
    else:
        entitytype = entity.type.upper()
    if entitytype == "IauracadDIRECTION":
        DirectionRatios = getAttr(entity, "DirectionRatios")
        if len(DirectionRatios) == 3:
            return AuraCAD.Vector(tuple(DirectionRatios))
        else:
            return AuraCAD.Vector(tuple(DirectionRatios + [0]))
    elif entitytype == "IauracadCARTESIANPOINT":
        Coordinates = getAttr(entity, "Coordinates")
        if len(Coordinates) == 3:
            return AuraCAD.Vector(tuple(Coordinates))
        else:
            return AuraCAD.Vector(tuple(Coordinates + [0]))
    return None


# below is only used by the internal parser #########################################


def getSchema():
    "retrieves the express schema"
    custom = params.get_param_arch("CustomIauracadSchema")
    if custom:
        if os.path.exists(custom):
            if DEBUG:
                print("Using custom schema: ", custom.split(os.sep)[-1])
            return custom
    p = None
    p = os.path.join(AuraCAD.ConfigGet("UserAppData"), SCHEMA.split(os.sep)[-1])
    if os.path.exists(p):
        return p
    import ArchCommands

    p = ArchCommands.download(SCHEMA)
    if p:
        return p
    return None


def group(entity, iauracad, mode=None):
    "gathers the children of the given entity"
    # only used by the internal parser

    try:
        if DEBUG:
            print("=====> making group", entity.id)
        placement = None
        placement = getPlacement(entity.ObjectPlacement)
        if DEBUG:
            print("got cell placement", entity.id, ":", placement)
        subelements = iauracad.find("IauracadRELCONTAINEDINSPATIALSTRUCTURE", "RelatingStructure", entity)
        subelements.extend(iauracad.find("IauracadRELAGGREGATES", "RelatingObject", entity))
        elts = []
        for s in subelements:
            if hasattr(s, "RelatedElements"):
                s = s.RelatedElements
                if not isinstance(s, list):
                    s = [s]
                elts.extend(s)
            elif hasattr(s, "RelatedObjects"):
                s = s.RelatedObjects
                if not isinstance(s, list):
                    s = [s]
                elts.extend(s)
            elif hasattr(s, "RelatedObject"):
                s = s.RelatedObject
                if not isinstance(s, list):
                    s = [s]
                elts.extend(s)
        print("found dependent elements: ", elts)

        groups = [
            ["Wall", ["IauracadWallStandardCase"], []],
            ["Window", ["IauracadWindow", "IauracadDoor"], []],
            ["Structure", ["IauracadSlab", "IauracadFooting", "IauracadBeam", "IauracadColumn"], []],
            ["Floor", ["IauracadBuildingStorey"], []],
            ["Building", ["IauracadBuilding"], []],
            ["Furniture", ["IauracadFurnishingElement"], []],
        ]

        for e in elts:
            for g in groups:
                for t in g[1]:
                    if e.type.upper() == t.upper():
                        if hasattr(AuraCAD.ActiveDocument, g[0] + str(e.id)):
                            g[2].append(AuraCAD.ActiveDocument.getObject(g[0] + str(e.id)))
        print("groups:", groups)

        comps = []
        if CREATE_IAuraCAD_GROUPS:
            if DEBUG:
                wprint("creating subgroups")
            for g in groups:
                if g[2]:
                    if g[0] in ["Building", "Floor"]:
                        comps.extend(g[2])
                    else:
                        auracadg = AuraCAD.ActiveDocument.addObject(
                            "App::DocumentObjectGroup", g[0] + "s"
                        )
                        for o in g[2]:
                            auracadg.addObject(o)
                        comps.append(auracadg)
        else:
            for g in groups:
                comps.extend(g[2])

        label = entity.Name
        name = mode + str(entity.id)
        cell = None
        if mode == "Site":
            cell = Arch.makeSite(comps, name=name)
        elif mode == "Floor":
            cell = Arch.makeFloor(comps, name=name)
        elif mode == "Building":
            cell = Arch.makeBuilding(comps, name=name)
        if label and cell:
            cell.Label = label
    except Exception:
        if DEBUG:
            print("error: skipping group ", entity.id)


def getWire(entity, placement=None):
    "returns a wire (created in the AuraCAD document) from the given entity"
    # only used by the internal parser
    if DEBUG:
        print("making Wire from :", entity)
    if not entity:
        return None
    if entity.type == "IauracadPOLYLINE":
        pts = []
        for p in entity.Points:
            pts.append(getVector(p))
        return Draft.getWire(pts, placement=placement)
    elif entity.type == "IauracadARBITRARYCLOSEDPROFILEDEF":
        pts = []
        for p in entity.OuterCurve.Points:
            pts.append(getVector(p))
        return Draft.getWire(pts, closed=True, placement=placement)


# EXPORT ##########################################################


def export(exportList, filename):
    "called when AuraCAD exports a file"
    global iauracadw
    iauracadw = None
    try:
        import IauracadImport as iauracadw
    except ImportError:
        try:
            import iAuraCAD_wrapper as iauracadw
        except ImportError:
            AuraCAD.Console.PrintError(
                translate("Arch", "Error: IauracadOpenShell is not installed") + "\n"
            )
            print("""importIauracad: iauracadOpenShell is not installed. Iauracad export is unavailable.
                    Note: Iauracad export currently requires an experimental version of IauracadOpenShell
                    available from https://github.com/aothms/IauracadOpenShell""")
            return

    if (not hasattr(iauracadw, "IauracadFile")) and (not hasattr(iauracadw, "file")):
        AuraCAD.Console.PrintError(
            translate("Arch", "Error: your IauracadOpenShell version is too old") + "\n"
        )
        print("""importIauracad: The version of IauracadOpenShell installed on this system does not
                 have Iauracad export capabilities. Iauracad export currently requires an experimental
                 version of IauracadOpenShell available from https://github.com/aothms/IauracadOpenShell""")
        return
    import Draft
    import Arch

    # creating base Iauracad project
    getConfig()
    scaling = params.get_param_arch("IauracadScalingFactor")
    exporttxt = params.get_param_arch("IauracadExportList")
    forcebrep = params.get_param_arch("iauracadExportAsBrep")
    application = "AuraCAD"
    ver = AuraCAD.Version()
    version = ver[0] + "." + ver[1] + " build" + ver[2]
    owner = AuraCAD.ActiveDocument.CreatedBy
    company = AuraCAD.ActiveDocument.Company
    project = AuraCAD.ActiveDocument.Name
    iauracad = IauracadWriter(filename, project, owner, company, application, version)
    txt = []

    # get all children and reorder list to get buildings and floors processed first
    objectslist = Draft.get_group_contents(exportList, walls=True, addgroups=True)
    objectslist = Arch.pruneIncluded(objectslist, strict=True)

    sites = []
    buildings = []
    floors = []
    groups = {}
    others = []
    for obj in objectslist:
        otype = Draft.getType(obj)
        if otype == "Site":
            sites.append(obj)
        elif otype == "Building":
            buildings.append(obj)
        elif otype == "Floor":
            floors.append(obj)
        elif otype == "Group":
            groups[obj.Name] = []
        else:
            others.append(obj)
    objectslist = buildings + floors + others
    if DEBUG:
        print("adding ", len(objectslist), " objects")

    global unprocessed
    unprocessed = []

    # process objects
    for obj in objectslist:

        otype = Draft.getType(obj)
        name = str(obj.Label)
        parent = Arch.getHost(obj)
        gdata = None
        fdata = None
        placement = None
        color = None
        representation = None
        descr = None
        extra = None

        # setting the Iauracad type
        if hasattr(obj, "Role"):
            iauracadtype = obj.Role.replace(" ", "")
        elif otype == "Foundation":
            iauracadtype = "Footing"
        elif otype == "Rebar":
            iauracadtype = "ReinforcingBar"
        elif otype == "Undefined":
            iauracadtype = "BuildingElementProxy"
        elif otype.startswith("Part::"):
            iauracadtype = "BuildingElementProxy"
        else:
            iauracadtype = otype

        # getting the "Force BREP" flag
        brepflag = False
        if hasattr(obj, "IauracadAttributes"):
            if "FlagForceBrep" in obj.IauracadAttributes:
                if obj.IauracadAttributes["FlagForceBrep"] == "True":
                    brepflag = True

        if DEBUG:
            print("Adding " + obj.Label + " as Iauracad" + iauracadtype)

        # writing Iauracad data
        if obj.isDerivedFrom("App::DocumentObjectGroup"):

            # getting parent building
            if parent:
                parent = iauracad.findByName("IauracadBuilding", str(parent.Label))

            if otype == "Site":
                print("   Skipping (not implemented yet)")  # TODO manage sites
            elif otype == "Building":
                iauracad.addBuilding(name=name)
            elif otype == "Floor":
                iauracad.addStorey(building=parent, name=name)

        elif obj.isDerivedFrom("Part::Feature"):

            # get color
            if AuraCAD.GuiUp:
                color = obj.ViewObject.ShapeColor[:3]

            # get parent floor
            if parent:
                parent = iauracad.findByName("IauracadBuildingStorey", str(parent.Label))

            # get representation
            if (not forcebrep) and (not brepflag):
                gdata = getIauracadExtrusionData(obj, scaling, SEPARATE_OPENINGS)
                # if DEBUG: print("   extrusion data for ",obj.Label," : ",gdata)
            if not gdata:
                fdata = getIauracadBrepFacesData(obj, scaling)
                # if DEBUG: print("   brep data for ",obj.Label," : ",fdata)
                if not fdata:
                    if obj.isDerivedFrom("Part::Feature"):
                        print("   Error retrieving the shape of object ", obj.Label)
                        unprocessed.append(obj)
                        continue
                    else:
                        if DEBUG:
                            print("   No geometry")
                else:
                    if DEBUG:
                        print("   Brep")
            else:
                if DEBUG:
                    print("   Extrusion")
            if gdata:
                # gdata = [ type, profile data, extrusion data, placement data ]
                placement = iauracad.addPlacement(
                    origin=gdata[3][0], xaxis=gdata[3][1], zaxis=gdata[3][2]
                )
                if gdata[0] == "polyline":
                    representation = iauracad.addExtrudedPolyline(gdata[1], gdata[2], color=color)
                elif gdata[0] == "circle":
                    representation = iauracad.addExtrudedCircle(gdata[1], gdata[2], color=color)
                elif gdata[0] == "ellipse":
                    representation = iauracad.addExtrudedEllipse(gdata[1], gdata[2], color=color)
                elif gdata[0] == "composite":
                    representation = iauracad.addExtrudedCompositeCurve(gdata[1], gdata[2], color=color)
                else:
                    print("debug: unknown extrusion type")
            elif fdata:
                representation = [iauracad.addFacetedBrep(f, color=color) for f in fdata]

            # create iauracad object
            iauracadtype = "Iauracad" + iauracadtype
            if hasattr(obj, "Description"):
                descr = obj.Description
            if otype == "Wall":
                if gdata:
                    if gdata[0] == "polyline":
                        iauracadtype = "IauracadWallStandardCase"
            elif otype == "Structure":
                if iauracadtype in ["IauracadSlab", "IauracadFooting"]:
                    extra = ["NOTDEFINED"]
            elif otype == "Window":
                extra = [obj.Width.Value * scaling, obj.Height.Value * scaling]
            elif otype == "Space":
                extra = ["ELEMENT", "INTERNAL", getIauracadElevation(obj)]
            elif otype.startswith("Part::"):
                extra = ["ELEMENT"]
            if not iauracadtype in supportedIauracadTypes:
                if DEBUG:
                    print(
                        "   Type ",
                        iauracadtype,
                        " is not supported yet. Exporting as IauracadBuildingElementProxy instead",
                    )
                iauracadtype = "IauracadBuildingElementProxy"
                extra = ["ELEMENT"]

            product = iauracad.addProduct(
                iauracadtype,
                representation,
                storey=parent,
                placement=placement,
                name=name,
                description=descr,
                extra=extra,
            )

            if product:
                # removing openings
                if SEPARATE_OPENINGS and gdata:
                    for o in obj.Subtractions:
                        print("Subtracting ", o.Label)
                        fdata = getIauracadBrepFacesData(o, scaling, sub=True)
                        representation = [iauracad.addFacetedBrep(f, color=color) for f in fdata]
                        p2 = iauracad.addProduct(
                            "IauracadOpeningElement",
                            representation,
                            storey=product,
                            placement=None,
                            name=str(o.Label),
                            description=None,
                        )

                # writing text log
                spacer = ""
                for i in range(36 - len(obj.Label)):
                    spacer += " "
                txt.append(obj.Label + spacer + iauracadtype)

                # adding object to group, if any
                for g in groups.keys():
                    group = AuraCAD.ActiveDocument.getObject(g)
                    if group:
                        for o in group.Group:
                            if o.Name == obj.Name:
                                groups[g].append(product)

            else:
                unprocessed.append(obj)
        else:
            if DEBUG:
                print("Object type ", otype, " is not supported yet.")

    # processing groups
    for name, entities in groups.items():
        if entities:
            o = AuraCAD.ActiveDocument.getObject(name)
            if o:
                if DEBUG:
                    print("Adding group ", o.Label, " with ", len(entities), " elements")
                grp = iauracad.addGroup(entities, o.Label)

    iauracad.write()

    if exporttxt:
        import os
        import time

        txtstring = "List of objects exported by AuraCAD in file\n"
        txtstring += filename + "\n"
        txtstring += "On " + time.ctime() + "\n"
        txtstring += "\n"
        txtstring += str(len(txt)) + " objects exported:\n"
        txtstring += "\n"
        txtstring += "Nr      Name                          Type\n"
        txtstring += "\n"
        for i in range(len(txt)):
            idx = str(i + 1)
            sp = ""
            for j in range(8 - len(idx)):
                sp += " "
            txtstring += idx + sp + txt[i] + "\n"
        txtfile = os.path.splitext(filename)[0] + ".txt"
        f = pyopen(txtfile, "wb")
        f.write(txtstring)
        f.close()

    AuraCAD.ActiveDocument.recompute()

    if unprocessed:
        print(
            "\nWARNING: "
            + str(len(unprocessed))
            + " objects were not exported (stored in importIauracad.unprocessed):"
        )
        for o in unprocessed:
            print("    " + o.Label)


def getTuples(data, scale=1, placement=None, normal=None, close=True):
    """getTuples(data,[scale,placement,normal,close]): returns a tuple or a list of tuples from a vector
    or from the vertices of a shape. Scale can indicate a scale factor"""
    rnd = False
    import Part

    if isinstance(data, AuraCAD.Vector):
        if placement:
            data = placement.multVec(data)
        if rnd:
            data = DraftVecUtils.rounded(data)
        return (data.x * scale, data.y * scale, data.z * scale)
    elif isinstance(data, Part.Shape):
        t = []
        if len(data.Wires) == 1:
            import Part
            import DraftGeomUtils

            data = Part.Wire(Part.__sortEdges__(data.Wires[0].Edges))
            verts = data.Vertexes
            try:
                c = data.CenterOfMass
                v1 = verts[0].Point.sub(c)
                v2 = verts[1].Point.sub(c)
                if DraftVecUtils.angle(v2, v1, normal) >= 0:
                    # inverting verts order if the direction is couterclockwise
                    verts.reverse()
            except Exception:
                pass
            for v in verts:
                pt = v.Point
                if placement:
                    if not placement.isIdentity():
                        pt = placement.multVec(pt)
                if rnd:
                    pt = DraftVecUtils.rounded(pt)
                t.append((pt.x * scale, pt.y * scale, pt.z * scale))

            if close:  # faceloops must not be closed, but iauracad profiles must.
                t.append(t[0])
        else:
            print("Arch.getTuples(): Wrong profile data")
        return t


def getIauracadExtrusionData(obj, scale=1, nosubs=False):
    """getIauracadExtrusionData(obj,[scale,nosubs]): returns a closed path (a list of tuples), a tuple expressing an extrusion
    vector, and a list of 3 tuples for base position, x axis and z axis. Or returns None, if a base loop and
    an extrusion direction cannot be extracted. Scale can indicate a scale factor."""

    CURVEMODE = "PARAMETER"  # For trimmed curves. CARTESIAN or PARAMETER

    if hasattr(obj, "Additions"):
        if obj.Additions:
            # TODO provisorily treat objs with additions as breps
            return None
    if hasattr(obj, "Subtractions") and not nosubs:
        if obj.Subtractions:
            return None
    if hasattr(obj, "Proxy"):
        if hasattr(obj.Proxy, "getProfiles"):
            p = obj.Proxy.getProfiles(obj, noplacement=True)
            v = obj.Proxy.getExtrusionVector(obj, noplacement=True)
            if (len(p) == 1) and v:
                p = p[0]
                r = AuraCAD.Placement()
                # b = p.CenterOfMass
                r = obj.Proxy.getPlacement(obj)
                # b = obj.Placement.multVec(AuraCAD.Vector())
                # r.Rotation = DraftVecUtils.getRotation(v,AuraCAD.Vector(0,0,1))
                d = [
                    r.Base,
                    DraftVecUtils.rounded(r.Rotation.multVec(AuraCAD.Vector(1, 0, 0))),
                    DraftVecUtils.rounded(r.Rotation.multVec(AuraCAD.Vector(0, 0, 1))),
                ]
                # r = r.inverse()
                # print("getExtrusionData: computed placement:",r)
                import Part

                if len(p.Edges) == 1:
                    if isinstance(p.Edges[0].Curve, Part.Circle):
                        # Circle profile
                        r1 = p.Edges[0].Curve.Radius * scale
                        return (
                            "circle",
                            [getTuples(p.Edges[0].Curve.Center, scale), r1],
                            getTuples(v, scale),
                            d,
                        )
                    elif isinstance(p.Edges[0].Curve, Part.Ellipse):
                        # Ellipse profile
                        r1 = p.Edges[0].Curve.MajorRadius * scale
                        r2 = p.Edges[0].Curve.MinorRadius * scale
                        return (
                            "ellipse",
                            [getTuples(p.Edges[0].Curve.Center, scale), r1, r2],
                            getTuples(v, scale),
                            d,
                        )
                curves = False
                for e in p.Edges:
                    if isinstance(e.Curve, Part.Circle):
                        curves = True
                    elif not isinstance(e.Curve, Part.LineSegment):
                        print("Arch.getIauracadExtrusionData: Warning: unsupported edge type in profile")
                if curves:
                    # Composite profile
                    ecurves = []
                    last = None
                    import DraftGeomUtils

                    edges = Part.__sortEdges__(p.Edges)
                    for e in edges:
                        if isinstance(e.Curve, Part.Circle):
                            follow = True
                            if last:
                                if not DraftVecUtils.equals(last, e.Vertexes[0].Point):
                                    follow = False
                                    last = e.Vertexes[0].Point
                                else:
                                    last = e.Vertexes[-1].Point
                            else:
                                last = e.Vertexes[-1].Point
                            p1 = math.degrees(
                                -DraftVecUtils.angle(e.Vertexes[0].Point.sub(e.Curve.Center))
                            )
                            p2 = math.degrees(
                                -DraftVecUtils.angle(e.Vertexes[-1].Point.sub(e.Curve.Center))
                            )
                            da = DraftVecUtils.angle(
                                e.valueAt(e.FirstParameter + 0.1).sub(e.Curve.Center),
                                e.Vertexes[0].Point.sub(e.Curve.Center),
                            )
                            if p1 < 0:
                                p1 = 360 + p1
                            if p2 < 0:
                                p2 = 360 + p2
                            if da > 0:
                                follow = not (follow)
                            if CURVEMODE == "CARTESIAN":
                                # BUGGY
                                p1 = getTuples(e.Vertexes[0].Point, scale)
                                p2 = getTuples(e.Vertexes[-1].Point, scale)
                            ecurves.append(
                                [
                                    "arc",
                                    getTuples(e.Curve.Center, scale),
                                    e.Curve.Radius * scale,
                                    [p1, p2],
                                    follow,
                                    CURVEMODE,
                                ]
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
                            ecurves.append(["line", [getTuples(vert, scale) for vert in verts]])
                    return "composite", ecurves, getTuples(v, scale), d
                else:
                    # Polyline profile
                    return "polyline", getTuples(p, scale), getTuples(v, scale), d
    return None


def getIauracadBrepFacesData(obj, scale=1, sub=False, tessellation=1):
    """getIauracadBrepFacesData(obj,[scale,tessellation]): returns a list(0) of lists(1) of lists(2) of lists(3),
    list(3) being a list of vertices defining a loop, list(2) describing a face from one or
    more loops, list(1) being the whole solid made of several faces, list(0) being the list
    of solids inside the object. Scale can indicate a scaling factor. Tessellation is the tessellation
    factor to apply on curved faces."""
    shape = None
    if sub:
        if hasattr(obj, "Proxy"):
            if hasattr(obj.Proxy, "getSubVolume"):
                shape = obj.Proxy.getSubVolume(obj)
    if not shape:
        if hasattr(obj, "Shape"):
            if obj.Shape:
                if not obj.Shape.isNull():
                    # if obj.Shape.isValid():
                    shape = obj.Shape
        elif hasattr(obj, "Terrain"):
            if obj.Terrain:
                if hasattr(obj.Terrain, "Shape"):
                    if obj.Terrain.Shape:
                        if not obj.Terrain.Shape.isNull():
                            if obj.Terrain.Shape.isValid():
                                shape = obj.Terrain.Shape
    if shape:
        import Part

        sols = []
        if shape.Solids:
            dataset = shape.Solids
        else:
            dataset = shape.Shells
            print("Warning! object contains no solids")
        for sol in shape.Solids:
            s = []
            curves = False
            for face in sol.Faces:
                for e in face.Edges:
                    if not isinstance(e.Curve, Part.LineSegment):
                        curves = True
            if curves:
                tris = sol.tessellate(tessellation)
                for tri in tris[1]:
                    f = []
                    for i in tri:
                        f.append(getTuples(tris[0][i], scale))
                    s.append([f])
            else:
                for face in sol.Faces:
                    f = []
                    f.append(
                        getTuples(face.OuterWire, scale, normal=face.normalAt(0, 0), close=False)
                    )
                    for wire in face.Wires:
                        if wire.hashCode() != face.OuterWire.hashCode():
                            f.append(
                                getTuples(
                                    wire,
                                    scale,
                                    normal=DraftVecUtils.neg(face.normalAt(0, 0)),
                                    close=False,
                                )
                            )
                    s.append(f)
            sols.append(s)
        return sols
    return None


def getIauracadElevation(obj):
    """getIauracadElevation(obj): Returns the lowest height (Z coordinate) of this object"""
    if obj.isDerivedFrom("Part::Feature"):
        b = obj.Shape.BoundBox
        return b.ZMin
    return 0


def explore(filename=None):
    "explore the contents of an iauracad file in a Qt dialog"
    if not filename:
        from PySide import QtGui

        filename = QtGui.QFileDialog.getOpenFileName(
            QtGui.QApplication.activeWindow(), "Open Iauracad File", None, "Iauracad files (*.iauracad *.Iauracad)"
        )
        if filename:
            filename = filename[0]
    if filename:
        getConfig()
        schema = getSchema()
        d = explorer(filename, schema)
        d.show()
        return d


# IauracadReader #############################################


class IauracadSchema:
    SIMPLETYPES = ["INTEGER", "REAL", "STRING", "NUMBER", "LOGICAL", "BOOLEAN"]
    NO_ATTR = ["WHERE", "INVERSE", "WR2", "WR3", "WR4", "WR5", "UNIQUE", "DERIVE"]

    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(filename):
            filename = AuraCAD.getUserMacroDir(True) + os.sep + filename
            if not os.path.exists(filename):
                raise ImportError("no IauracadSchema file found!")

            self.file = open(self.filename)
            self.data = self.file.read()
            self.types = self.readTypes()
            self.entities = self.readEntities()
            if DEBUG:
                print(
                    "Parsed from schema %s: %s entities and %s types"
                    % (self.filename, len(self.entities), len(self.types))
                )

    def readTypes(self):
        """
        Parse all the possible types from the schema,
        returns a dictionary Name -> Type
        """
        types = {}
        for m in re.finditer("TYPE (.*) = (.*);", self.data):
            typename, typetype = m.groups()
            if typetype in self.SIMPLETYPES:
                types[typename] = typetype
            else:
                types[typename] = "#" + typetype

        return types

    def readEntities(self):
        """
        Parse all the possible entities from the schema,
        returns a dictionary of the form:
        { name: {
            "supertype": supertype,
            "attributes": [{ key: value }, ..]
        }}
        """
        entities = {}

        # Regexes must be greedy to prevent matching outer entity and end_entity strings
        # Regexes have re.DOTALL to match newlines
        for m in re.finditer("ENTITY (.*?)END_ENTITY;", self.data, re.DOTALL):
            entity = {}
            raw_entity_str = m.groups()[0]

            entity["name"] = re.search(r"(.*?)[;|\s]", raw_entity_str).groups()[0].upper()

            subtypeofmatch = re.search(r".*SUBTYPE OF \((.*?)\);", raw_entity_str)
            entity["supertype"] = subtypeofmatch.groups()[0].upper() if subtypeofmatch else None

            # find the shortest string matched from the end of the entity type header to the
            # first occurrence of a NO_ATTR string (when it occurs on a new line)
            inner_str = re.search(";(.*?)$", raw_entity_str, re.DOTALL).groups()[0]

            attrs_str = min([inner_str.partition("\r\n " + a)[0] for a in self.NO_ATTR])
            attrs = []
            for am in re.finditer("(.*?) : (.*?);", attrs_str, re.DOTALL):
                name, attr_type = [s.replace("\r\n\t", "") for s in am.groups()]
                attrs.append((name, attr_type))

            entity["attributes"] = attrs
            entities[entity["name"]] = entity

        return entities

    def getAttributes(self, name):
        """
        Get all attributes af an entity, including supertypes
        """
        ent = self.entities[name]

        attrs = []
        while ent is not None:
            this_ent_attrs = copy.copy(ent["attributes"])
            this_ent_attrs.reverse()
            attrs.extend(this_ent_attrs)
            ent = self.entities.get(ent["supertype"], None)

        attrs.reverse()
        return attrs

    def capitalize(self, name):
        "returns a capitalized version of a type"
        if name.upper() in self.data.upper():
            i1 = self.data.upper().index(name.upper())
            i2 = i1 + len(name)
            name = self.data[i1:i2]
        return name


class IauracadFile:
    """
    Parses an iauracad file given by filename, entities can be retrieved by name and id
    The whole file is stored in a dictionary (in memory)
    """

    entsById = {}
    entsByName = {}

    def __init__(self, filename, schema):
        self.filename = filename
        self.schema = IauracadSchema(schema)
        self.file = open(self.filename)
        self.entById, self.entsByName, self.header = self.read()
        self.file.close()
        if DEBUG:
            print("Parsed from file %s: %s entities" % (self.filename, len(self.entById)))

    def getEntityById(self, id):
        return self.entById.get(id, None)

    def getEntitiesByName(self, name):
        return self.entsByName.get(name, None)

    def read(self):
        """
        Returns 2 dictionaries, entById and entsByName
        """
        entById = {}
        entsByName = {}
        header = "HEADER "
        readheader = False
        for line in self.file:
            e = self.parseLine(line)
            if e:
                entById[int(e["id"])] = e
                ids = e.get(e["name"], [])
                ids.append(e["id"])
                entsByName[e["name"]] = list(set(ids))
            elif "HEADER" in line:
                readheader = True
            elif readheader:
                if "ENDSEC" in line:
                    readheader = False
                else:
                    header += line

        return [entById, entsByName, header]

    def parseLine(self, line):
        """
        Parse a line
        """
        m = IauracadLINE_RE.search(line)  # id,name,attrs
        if m:
            id, name, attrs = m.groups()
            id = id.strip()
            name = name.strip()
            attrs = attrs.strip()
        else:
            return False

        return {"id": id, "name": name, "attributes": self.parseAttributes(name, attrs)}

    def parseAttributes(self, ent_name, attrs_str):
        """
        Parse the attributes of a line
        """
        parts = []
        lastpos = 0

        while lastpos < len(attrs_str):
            newpos = self.nextString(attrs_str, lastpos)
            parts.extend(self.parseAttribute(attrs_str[lastpos : newpos - 1]))
            lastpos = newpos

        schema_attributes = self.schema.getAttributes(ent_name)

        assert len(schema_attributes) == len(
            parts
        ), "Expected %s attributes, got %s (entity: %s" % (
            len(schema_attributes),
            len(parts),
            ent_name,
        )

        attribute_names = [a[0] for a in schema_attributes]

        return dict(zip(attribute_names, parts))

    def parseAttribute(self, attr_str):
        """
        Map a single attribute to a python type (recursively)
        """
        parts = []
        lastpos = 0
        while lastpos < len(attr_str):
            newpos = self.nextString(attr_str, lastpos)
            s = attr_str[lastpos : newpos - 1]
            if s[0] == "(" and s[-1] == ")":  # list, recurse
                parts.append(self.parseAttribute(s[1:-1]))
            else:
                try:
                    parts.append(float(s))  # number, any kind
                except ValueError:
                    if s[0] == "'" and s[-1] == "'":  # string
                        parts.append(s[1:-1])
                    elif s == "$":
                        parts.append(None)
                    else:
                        parts.append(s)  # ref, enum or other

            lastpos = newpos

        return parts

    def nextString(self, s, start):
        """
        Parse the data part of a line
        """
        parens = 0
        quotes = 0

        for pos in range(start, len(s)):
            c = s[pos]
            if c == "," and parens == 0 and quotes == 0:
                return pos + 1
            elif c == "(" and quotes == 0:
                parens += 1
            elif c == ")" and quotes == 0:
                parens -= 1
            elif c == "'" and quotes == 0:
                quotes = 1
            elif c == "'" and quotes == 1:
                quotes = 0

        return len(s) + 1


class IauracadEntity:
    "a container for an Iauracad entity"

    def __init__(self, ent, doc=None):
        self.data = ent
        self.id = int(ent["id"])
        self.type = ent["name"].upper().strip(",[]()")
        self.attributes = ent["attributes"]
        self.doc = doc

    def __repr__(self):
        return str(self.id) + " : " + self.type + " " + str(self.attributes)

    def getProperties(self):
        return self.doc.find("IauracadRELDEFINESBYPROPERTIES", "RelatedObjects", self)

    def getProperty(self, propName):
        "finds the value of the given property or quantity in this object, if exists"
        propsets = self.doc.find("IauracadRELDEFINESBYPROPERTIES", "RelatedObjects", self)
        if not propsets:
            return None
        propset = []
        for p in propsets:
            if hasattr(p.RelatingPropertyDefinition, "HasProperties"):
                propset.extend(p.RelatingPropertyDefinition.HasProperties)
            elif hasattr(p.RelatingPropertyDefinition, "Quantities"):
                propset.extend(p.RelatingPropertyDefinition.Quantities)
        for prop in propset:
            if prop.Name == propName:
                print("found valid", prop)
                if hasattr(prop, "LengthValue"):
                    return prop.LengthValue
                elif hasattr(prop, "AreaValue"):
                    return prop.AreaValue
                elif hasattr(prop, "VolumeValue"):
                    return prop.VolumeValue
                elif hasattr(prop, "NominalValue"):
                    return prop.NominalValue
        return None

    def getAttribute(self, attr):
        "returns the value of the given attribute, if exists"
        if hasattr(self, attr):
            return self.__dict__[attr]
        return None


class IauracadDocument:
    "an object representing an Iauracad document"

    def __init__(self, filename, schema="Iauracad2X3_TC1.exp"):
        f = IauracadFile(filename, schema)
        self.filename = filename
        self.data = f.entById
        self.Entities = {0: f.header}
        for k, e in self.data.items():
            eid = int(e["id"])
            self.Entities[eid] = IauracadEntity(e, self)
        if DEBUG:
            print(len(self.Entities), "entities created. Creating attributes...")
        for k, ent in self.Entities.items():
            if DEBUG:
                print("attributing entity ", ent)
            if hasattr(ent, "attributes"):
                for k, v in ent.attributes.items():
                    if DEBUG:
                        print("parsing attribute: ", k, " value ", v)
                    if isinstance(v, str):
                        val = self.__clean__(v)
                    elif isinstance(v, list):
                        val = []
                        for item in v:
                            if isinstance(item, str):
                                val.append(self.__clean__(item))
                            else:
                                val.append(item)
                    else:
                        val = v
                    setattr(ent, k.strip(), val)
        if DEBUG:
            print("Document successfully created")

    def __clean__(self, value):
        "turns an attribute value into something usable"
        try:
            val = value.strip(" ()'")
            if val[:3].upper() == "Iauracad":
                if "IauracadTEXT" in val.upper():
                    l = val.split("'")
                    if len(l) == 3:
                        val = l[1]
                elif "IauracadBOOLEAN" in value.upper():
                    l = val.split(".")
                    if len(l) == 3:
                        val = l[1]
                    if val.upper() == "F":
                        val = False
                    elif val.upper() == "T":
                        val = True
                elif "IauracadREAL" in val.upper():
                    l = val.split("(")
                    if len(l) == 2:
                        val = float(l[1].strip(")"))
            else:
                if "#" in val:
                    if "," in val:
                        val = val.split(",")
                        l = []
                        for subval in val:
                            if "#" in subval:
                                s = subval.strip(" #")
                                if DEBUG:
                                    print("referencing ", s, " : ", self.getEnt(int(s)))
                                l.append(self.getEnt(int(s)))
                        val = l
                    else:
                        val = val.strip()
                        val = val.replace("#", "")
                        if DEBUG:
                            print("referencing ", val, " : ", self.getEnt(int(val)))
                        val = self.getEnt(int(val))
                        if not val:
                            val = value
        except Exception:
            if DEBUG:
                print("error parsing attribute", value)
            val = value
        return val

    def __repr__(self):
        return "Iauracad Document: " + self.filename + ", " + str(len(self.Entities)) + " entities "

    def getEnt(self, ref):
        "gets an entity by id number, or a list of entities by type"
        if isinstance(ref, int):
            if ref in self.Entities:
                return self.Entities[ref]
        elif isinstance(ref, str):
            l = []
            ref = ref.upper()
            for k, ob in self.Entities.items():
                if hasattr(ob, "type"):
                    if ob.type == ref:
                        l.append(ob)
            return l
        return None

    def search(self, pat):
        "searches entities types for partial match"
        l = []
        pat = pat.upper()
        for k, ob in self.Entities.items():
            if hasattr(ob, "type"):
                if pat in ob.type:
                    if not ob.type in l:
                        l.append(ob.type)
        return l

    def find(self, pat1, pat2=None, pat3=None):
        """finds objects in the current Iauracad document.
        arguments can be of the following form:
        - (pattern): returns object types matching the given pattern (same as search)
        - (type,property,value): finds, in all objects of type "type", those whose
          property "property" has the given value
        """
        if pat3:
            bobs = self.getEnt(pat1)
            obs = []
            for bob in bobs:
                if hasattr(bob, pat2):
                    if bob.getAttribute(pat2) == pat3:
                        obs.append(bob)
            return obs
        elif pat1:
            ll = self.search(pat1)
            obs = []
            for l in ll:
                obs.extend(self.getEnt(l))
            return obs
        return None


def explorer(filename, schema="Iauracad2X3_TC1.exp"):
    "returns a PySide dialog showing the contents of an Iauracad file"
    from PySide import QtGui

    iauracad = IauracadDocument(filename, schema)
    schema = IauracadSchema(schema)
    tree = QtGui.QTreeWidget()
    tree.setColumnCount(3)
    tree.setWordWrap(True)
    tree.header().setDefaultSectionSize(60)
    tree.header().resizeSection(0, 60)
    tree.header().resizeSection(1, 30)
    tree.header().setStretchLastSection(True)
    tree.headerItem().setText(0, "ID")
    tree.headerItem().setText(1, "")
    tree.headerItem().setText(2, "Item and Properties")
    bold = QtGui.QFont()
    bold.setBold(True)

    # print(iauracad.Entities)

    for i in iauracad.Entities.keys():
        e = iauracad.Entities[i]
        item = QtGui.QTreeWidgetItem(tree)
        if hasattr(e, "id"):
            item.setText(0, str(e.id))
            if e.type in ["IauracadWALL", "IauracadWALLSTANDARDCASE"]:
                item.setIcon(1, QtGui.QIcon(":icons/Arch_Wall_Tree.svg"))
            elif e.type in ["IauracadCOLUMN", "IauracadBEAM", "IauracadSLAB", "IauracadFOOTING"]:
                item.setIcon(1, QtGui.QIcon(":icons/Arch_Structure_Tree.svg"))
            elif e.type in ["IauracadSITE"]:
                item.setIcon(1, QtGui.QIcon(":icons/Arch_Site_Tree.svg"))
            elif e.type in ["IauracadBUILDING"]:
                item.setIcon(1, QtGui.QIcon(":icons/Arch_Building_Tree.svg"))
            elif e.type in ["IauracadSTOREY"]:
                item.setIcon(1, QtGui.QIcon(":icons/Arch_Floor_Tree.svg"))
            elif e.type in ["IauracadWINDOW"]:
                item.setIcon(1, QtGui.QIcon(":icons/Arch_Window_Tree.svg"))
            elif e.type in ["IauracadROOF"]:
                item.setIcon(1, QtGui.QIcon(":icons/Arch_Roof_Tree.svg"))
            elif e.type in ["IauracadEXTRUDEDAREASOLID", "IauracadCLOSEDSHELL"]:
                item.setIcon(1, QtGui.QIcon(":/icons/Part_3D_object.svg"))
            elif e.type in ["IauracadFACE"]:
                item.setIcon(1, QtGui.QIcon(":icons/Draft_SwitchMode.svg"))
            elif e.type in ["IauracadARBITRARYCLOSEDPROFILEDEF", "IauracadPOLYLOOP"]:
                item.setIcon(1, QtGui.QIcon(":icons/Draft_Draft.svg"))
            item.setText(2, str(schema.capitalize(e.type)))
            item.setFont(2, bold)
            for a in e.attributes.keys():
                if hasattr(e, a):
                    if not a.upper() in ["ID", "GLOBALID"]:
                        v = getattr(e, a)
                        if isinstance(v, IauracadEntity):
                            t = "Entity #" + str(v.id) + ": " + str(v.type)
                        elif isinstance(v, list):
                            t = ""
                        else:
                            t = str(v)
                        t = "    " + str(a) + " : " + str(t)
                        item = QtGui.QTreeWidgetItem(tree)
                        item.setText(2, str(t))
                        if isinstance(v, list):
                            for vi in v:
                                if isinstance(vi, IauracadEntity):
                                    t = "Entity #" + str(vi.id) + ": " + str(vi.type)
                                else:
                                    t = vi
                                t = "        " + str(t)
                                item = QtGui.QTreeWidgetItem(tree)
                                item.setText(2, str(t))

    d = QtGui.QDialog()
    d.setObjectName("IauracadExplorer")
    d.setWindowTitle("Iauracad Explorer")
    d.resize(640, 480)
    layout = QtGui.QVBoxLayout(d)
    layout.addWidget(tree)
    return d


# IauracadWriter ########################################


class _tempEntityHolder:
    """a temporary object to store entity references
    to be made into something nicer later..."""

    def __init__(self):
        self.refs = []


holder = _tempEntityHolder()


def uid():
    """returns a suitable GlobalID"""
    u = str(uuid.uuid4())[:22]
    u = u.replace("-", "_")
    return u


def now(string=False):
    "returns a suitable Iauracad Time"
    if string:
        return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    else:
        return int(time.time())


def getPropertyNames(entity):
    """getPropertyNames(entity): Returns a dictionary with
    the numbers and names of the pythonproperties available for
    this entity"""
    ents = {}
    if hasattr(entity, "get_argument_count"):
        l = entity.get_argument_count()
    else:
        l = len(entity)
    for i in range(l):
        ents[i] = entity.get_argument_name(i)
    return ents


def getTuple(vec):
    """getTuple(vec): returns a tuple from other coordinate
    structures: tuple, list, 3d vector, or occ vertex"""

    def fmt(t):
        t = float(t)
        t = round(t, Draft.precision())
        return t

    if isinstance(vec, tuple):
        return tuple([fmt(v) for v in vec])
    elif isinstance(vec, list):
        return tuple([fmt(v) for v in vec])
    elif hasattr(vec, "x") and hasattr(vec, "y") and hasattr(vec, "z"):
        return (fmt(vec.x), fmt(vec.y), fmt(vec.z))
    elif hasattr(vec, "X") and hasattr(vec, "Y") and hasattr(vec, "Z"):
        return (fmt(vec.X), fmt(vec.Y), fmt(vec.Z))


def getValueAndDirection(vec):
    """getValueAndDirection(vec): returns a length and a tuple
    representing a normalized vector from a tuple"""
    pre = Draft.precision()
    vec = getTuple(vec)
    length = round(math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2), pre)
    ratio = 1 / length
    x = round(vec[0] * ratio, pre)
    y = round(vec[1] * ratio, pre)
    z = round(vec[2] * ratio, pre)
    normal = (x, y, z)
    return length, normal


def create(iauracaddoc=None, iauracadname=None, arguments=[]):
    """create(iauracaddoc,iauracadname,[arguments]):creates an entity
    of the given name in the given document and optionally
    gives it an ordered list of arguments"""
    if hasattr(iauracadw, "Entity"):
        entity = iauracadw.Entity(iauracadname)
    else:
        entity = iauracadw.entity_instance(iauracadname)
    if iauracaddoc:
        iauracaddoc.add(entity)
    # this is a temporary hack while iauracadopenshell has no ref counting
    holder.refs.append(entity)
    if not isinstance(arguments, list):
        arguments = [arguments]
    for i in range(len(arguments)):
        arg = arguments[i]
        if isinstance(arg, tuple):
            if len(arg) in [2, 3]:
                if hasattr(iauracadw, "Doubles"):
                    arg = iauracadw.Doubles(arg)
                else:
                    arg = iauracadw.doubles(arg)
        entity.set_argument(i, arg)
    return entity


class IauracadWriter(object):
    """IauracadWriter([filepath,name,owner,organization,application,version])
    Creates an empty Iauracad document."""

    def __init__(
        self,
        filepath="",
        name="",
        owner="",
        organization="",
        application="Python Iauracad exporter",
        version="0.0",
    ):
        if hasattr(iauracadw, "IauracadFile"):
            self._fileobject = iauracadw.IauracadFile()
        else:
            self._fileobject = iauracadw.file()
        self._person = create(
            self._fileobject, "IauracadPerson", [None, None, "", None, None, None, None, None]
        )
        self._org = create(self._fileobject, "IauracadOrganization", [None, "", None, None, None])
        pno = create(self._fileobject, "IauracadPersonAndOrganization", [self._person, self._org, None])
        app = create(self._fileobject, "IauracadApplication", [self._org, version, application, uid()])
        self._owner = create(
            self._fileobject, "IauracadOwnerHistory", [pno, app, None, "ADDED", None, pno, app, now()]
        )
        axp = self.addPlacement(local=False)
        dim0 = create(self._fileobject, "IauracadDirection", getTuple((0, 1, 0)))
        self._repcontext = create(
            self._fileobject,
            "IauracadGeometricRepresentationContext",
            ["Plan", "Model", 3, 1.0e-05, axp, dim0],
        )
        dim1 = create(self._fileobject, "IauracadDimensionalExponents", [0, 0, 0, 0, 0, 0, 0])
        dim2 = create(self._fileobject, "IauracadSIUnit", [dim1, "LENGTHUNIT", "MILLI", "METRE"])
        dim3 = create(self._fileobject, "IauracadSIUnit", [dim1, "AREAUNIT", None, "SQUARE_METRE"])
        dim4 = create(self._fileobject, "IauracadSIUnit", [dim1, "VOLUMEUNIT", None, "CUBIC_METRE"])
        dim6 = create(self._fileobject, "IauracadSIUnit", [dim1, "PLANEANGLEUNIT", None, "RADIAN"])
        dim7 = create(None, "IauracadPlaneAngleMeasure", [1.745e-2])
        dim8 = create(self._fileobject, "IauracadMeasureWithUnit", [dim7, dim6])
        dim9 = create(
            self._fileobject, "IauracadConversionBasedUnit", [dim1, "PLANEANGLEUNIT", "DEGREE", dim8]
        )
        units = create(self._fileobject, "IauracadUnitAssignment", [[dim2, dim3, dim4, dim9]])
        self.Project = create(
            self._fileobject,
            "IauracadProject",
            [uid(), self._owner, None, None, None, None, None, [self._repcontext], units],
        )
        self.Site = None
        self._storeyRelations = {}
        self.BuildingProducts = []
        self.Storeys = []
        self.Buildings = []
        self.FilePath = filepath
        self.Owner = owner
        self.Organization = organization
        self.Name = name

    def __repr__(self):
        return "Iauracad document " + self.Name  # + " containing " + str(len(holder)) + " entities"

    def __setattr__(self, key, value):
        if value:
            if key == "Owner":
                self._person.set_argument(2, str(value))
            elif key == "Organization":
                self._org.set_argument(1, str(value))
            elif key == "Name":
                self.Project.set_argument(2, str(value))
        self.__dict__.__setitem__(key, value)

    def findByName(self, iauracadtype, name):
        "finds an entity of a given iauracadtype by name"
        objs = self._fileobject.by_type(iauracadtype)
        for obj in objs:
            if hasattr(obj, "get_argument_count"):
                l = obj.get_argument_count()
            else:
                l = len(obj)
            for i in range(l):
                if obj.get_argument_name(i) == "Name":
                    if obj.get_argument(i) == name:
                        return obj
        return None

    def write(self, fp=None):
        "writes the document to its file"
        if fp:
            path = fp
        else:
            path = self.FilePath
        if path:
            try:
                self._fileobject.write(path)
                if APPLYFIX:
                    print("IauracadWriter: Applying fix...")
                    self._fix(path)
            except Exception:
                print("IauracadWriter: Error writing to " + path)
            else:
                print("IauracadWriter: Successfully written to " + path)
        else:
            print("IauracadWriter: Error: File path is not defined, unable to save")

    def _fix(self, path):
        "hack to fix early bugs in iauracadopenshell"
        import os

        if os.path.exists(path):
            f = pyopen(path, "rb")
            lines = []
            for l in f.readlines():
                if "(=Iauracad" in l:
                    # adding an iauracad entity without ID adds an unwanted = sign
                    l = l.replace("(=Iauracad", "(Iauracad")
                elif "IauracadSIUNIT" in l:
                    # no way to insert * character
                    l = l.replace("IauracadSIUNIT(#12,", "IauracadSIUNIT(*,")
                lines.append(l)
            f.close()
            f = pyopen(path, "wb")
            for l in lines:
                f.write(l)
            f.close()

    def union(self, solids):
        """union(solids): creates a boolean union between all the solids of the list"""
        if len(solids) == 1:
            return solids[0]
        else:
            s1 = solids.pop(0)
            s2 = solids.pop(0)
            base = create(self._fileobject, "IauracadBooleanResult", ["UNION", s1, s2])
            for s in solids:
                base = create(self._fileobject, "IauracadBooleanResult", ["UNION", base, s])
            return base

    def addPlacement(
        self,
        reference=None,
        origin=(0, 0, 0),
        xaxis=(1, 0, 0),
        zaxis=(0, 0, 1),
        local=True,
        flat=False,
    ):
        """addPlacement([reference,origin,xaxis,zaxis,local]): adds a placement. origin,
        xaxis and zaxis can be either tuples or 3d vectors. If local is False, a global
        placement is returned, otherwise a local one."""
        if flat:
            xvc = create(self._fileobject, "IauracadDirection", getTuple(xaxis)[:2])
            ovc = create(self._fileobject, "IauracadCartesianPoint", getTuple(origin)[:2])
            gpl = create(self._fileobject, "IauracadAxis2Placement2D", [ovc, xvc])
        else:
            xvc = create(self._fileobject, "IauracadDirection", getTuple(xaxis))
            zvc = create(self._fileobject, "IauracadDirection", getTuple(zaxis))
            ovc = create(self._fileobject, "IauracadCartesianPoint", getTuple(origin))
            gpl = create(self._fileobject, "IauracadAxis2Placement3D", [ovc, zvc, xvc])
        if local:
            lpl = create(self._fileobject, "IauracadLocalPlacement", [reference, gpl])
            return lpl
        else:
            return gpl

    def addSite(
        self,
        placement=None,
        name="Site",
        description=None,
        latitude=None,
        longitude=None,
        elevation=None,
        landtitlenumber=None,
        address=None,
    ):
        """makeSite(iauracaddoc,project,owner,[placement,name,description]): creates a site
        in the given iauracad document"""
        if self.Site:
            return
        if not placement:
            placement = self.addPlacement()
        self.Site = create(
            self._fileobject,
            "IauracadSite",
            [
                uid(),
                self._owner,
                str(name),
                description,
                None,
                placement,
                None,
                None,
                "ELEMENT",
                latitude,
                longitude,
                elevation,
                landtitlenumber,
                address,
            ],
        )
        self._relate(self.Project, self.Site)

    def addBuilding(self, placement=None, name="Default building", description=None):
        """addBuilding([placement,name,description]): adds a building"""
        if not placement:
            placement = self.addPlacement()
        if not self.Site:
            self.addSite()
        bdg = create(
            self._fileobject,
            "IauracadBuilding",
            [
                uid(),
                self._owner,
                str(name),
                description,
                None,
                placement,
                None,
                None,
                "ELEMENT",
                None,
                None,
                None,
            ],
        )
        self._relate(self.Site, bdg)
        self.Buildings.append(bdg)
        return bdg

    def addStorey(self, building=None, placement=None, name="Default storey", description=None):
        """addStorey([building,placement,name,description]): adds a storey"""
        if not placement:
            placement = self.addPlacement()
        sto = create(
            self._fileobject,
            "IauracadBuildingStorey",
            [
                uid(),
                self._owner,
                str(name),
                description,
                None,
                placement,
                None,
                None,
                "ELEMENT",
                None,
            ],
        )
        if not building:
            if self.Buildings:
                building = self.Buildings[0]
            else:
                building = self.addBuilding()
        self._relate(building, sto)
        self.Storeys.append(sto)
        return sto

    def addGroup(self, entities, name="Default group", description=None):
        """addGroup(entities,[name,description]): adds a group with the given entities"""
        if not isinstance(entities, list):
            entities = [entities]
        gro = create(
            self._fileobject, "IauracadGroup", [uid(), self._owner, str(name), description, None]
        )
        rel = create(
            self._fileobject,
            "IauracadRelAssignsToGroup",
            [uid(), self._owner, str(name) + "-relation", None, entities, "PRODUCT", gro],
        )
        return gro

    def _relate(self, container, entities):
        """relate(container,entities): relates the given entities to the given
        container"""
        if not isinstance(entities, list):
            entities = [entities]
        if container.is_a("IauracadBuildingStorey"):
            sid = container.get_argument(0)
            if sid in self._storeyRelations:
                prods = self._storeyRelations[sid].get_argument(4)
                self._storeyRelations[sid].set_argument(4, prods + entities)
            else:
                rel = create(
                    self._fileobject,
                    "IauracadRelContainedInSpatialStructure",
                    [uid(), self._owner, "StoreyLink", "", entities, container],
                )
                self._storeyRelations[sid] = rel
        else:
            if entities[0].is_a("IauracadOpeningElement"):
                create(
                    self._fileobject,
                    "IauracadRelVoidsElement",
                    [uid(), self._owner, "Opening", "", container, entities[0]],
                )
            else:
                create(
                    self._fileobject,
                    "IauracadRelAggregates",
                    [uid(), self._owner, "Relationship", "", container, entities],
                )

    def addProduct(
        self,
        elttype,
        shapes,
        storey=None,
        placement=None,
        name="Unnamed element",
        description=None,
        extra=None,
    ):
        """addProduct(elttype,representations,[storey,placement,name,description,extra]): creates an element of the given type
        (IauracadWall, IauracadBeam, etc...) with the given attributes, plus the given extra attributes."""
        elttype = str(elttype)
        if not extra:
            extra = []
        if not description:
            description = None
        if not placement:
            placement = self.addPlacement()
        representations = self.addRepresentations(shapes)
        prd = create(self._fileobject, "IauracadProductDefinitionShape", [None, None, representations])
        try:
            elt = create(
                self._fileobject,
                elttype,
                [uid(), self._owner, name, description, None, placement, prd, None] + extra,
            )
        except Exception:
            print(
                "unable to create an ",
                elttype,
                " with attributes: ",
                [uid(), self._owner, str(name), description, None, placement, prd, None] + extra,
            )
            try:
                if hasattr(iauracadw, "Entity"):
                    o = iauracadw.Entity(elttype)
                else:
                    o = iauracadw.entity_instance(elttype)
                print("supported attributes are: ")
                print(getPropertyNames(o))
            except Exception:
                print("unable to create an element of type '" + elttype + "'")
            print("WARNING: skipping object '" + name + "' of type " + elttype)
            return None
        self.BuildingProducts.append(elt)
        if not storey:
            if self.Storeys:
                storey = self.Storeys[0]
            else:
                storey = self.addStorey()
        self._relate(storey, elt)
        return elt

    def addRepresentations(self, shapes):
        """addRepresentations(shapes,[solidType]): creates a representation from the given shape"""
        solidType = "Brep"
        if not isinstance(shapes, list):
            if shapes.is_a("IauracadExtrudedAreaSolid"):
                solidType = "SweptSolid"
            shapes = [shapes]
        reps = [
            create(
                self._fileobject,
                "IauracadShapeRepresentation",
                [self._repcontext, "Body", solidType, [shape for shape in shapes]],
            )
        ]
        return reps

    def addColor(self, rgb, rep):
        """addColor(rgb,rep): adds a RGB color definition tuple (float,float,float) to a given representation"""
        col = create(self._fileobject, "IauracadColourRgb", [None] + list(rgb))
        ssr = create(
            self._fileobject,
            "IauracadSurfaceStyleRendering",
            [col, None, None, None, None, None, None, None, "FLAT"],
        )
        iss = create(self._fileobject, "IauracadSurfaceStyle", [None, "BOTH", [ssr]])
        psa = create(self._fileobject, "IauracadPresentationStyleAssignment", [[iss]])
        isi = create(self._fileobject, "IauracadStyledItem", [rep, [psa], None])
        return isi

    def addProfile(self, iauracadtype, data, curvetype="AREA"):
        """addProfile(iauracadtype,data): creates a 2D profile of the given type, with the given
        data as arguments, which must be formatted correctly according to the type."""

        # Expected iauracadtype and corresponding data formatting:
        # IauracadPolyLine: [ (0,0,0), (2,1,0), (3,3,0) ] # list of points
        # IauracadCompositeCurve: [ ["line",[ (0,0,0), (2,1,0) ] ], # list of points
        #                      ["arc", (0,0,0), 15, [0.76, 3.1416], True, "PARAMETER"] # center, radius, [trim1, trim2], SameSense, trimtype
        #                      ... ]
        # IauracadCircleProfileDef: [ (0,0,0), 15 ] # center, radius
        # IauracadEllipseProfileDef: [ (0,0,0), 15, 7 ] # center, radiusX, radiusY

        if iauracadtype == "IauracadPolyline":
            pts = [create(self._fileobject, "IauracadCartesianPoint", getTuple(p)[:2]) for p in data]
            pol = create(self._fileobject, "IauracadPolyline", [pts])
            profile = create(
                self._fileobject, "IauracadArbitraryClosedProfileDef", [curvetype, None, pol]
            )
        elif iauracadtype == "IauracadCompositeCurve":
            curves = []
            for curve in data:
                cur = None
                if curve[0] == "line":
                    pts = [
                        create(self._fileobject, "IauracadCartesianPoint", getTuple(p)[:2])
                        for p in curve[1]
                    ]
                    cur = create(self._fileobject, "IauracadPolyline", [pts])
                elif curve[0] == "arc":
                    pla = self.addPlacement(origin=curve[1], local=False, flat=True)
                    cir = create(self._fileobject, "IauracadCircle", [pla, curve[2]])
                    if curve[5] == "CARTESIAN":
                        # BUGGY! Impossible to add cartesian points as "embedded" entity
                        trim1 = create(None, "IauracadCartesianPoint", getTuple(curve[3][0])[:2])
                        trim2 = create(None, "IauracadCartesianPoint", getTuple(curve[3][1])[:2])
                    else:
                        trim1 = create(None, "IauracadParameterValue", [curve[3][0]])
                        trim2 = create(None, "IauracadParameterValue", [curve[3][1]])
                    cur = create(
                        self._fileobject,
                        "IauracadTrimmedCurve",
                        [cir, [trim1], [trim2], curve[4], curve[5]],
                    )
                if cur:
                    seg = create(
                        self._fileobject, "IauracadCompositeCurveSegment", ["CONTINUOUS", True, cur]
                    )
                    curves.append(seg)
            ccu = create(self._fileobject, "IauracadCompositeCurve", [curves, False])
            profile = create(
                self._fileobject, "IauracadArbitraryClosedProfileDef", [curvetype, None, ccu]
            )
        else:
            if not isinstance(data, list):
                data = [data]
            p = self.addPlacement(local=False, flat=True)
            profile = create(self._fileobject, iauracadtype, [curvetype, None, p] + data)
        return profile

    def addExtrusion(self, profile, extrusion, placement=None):
        """addExtrusion(profile,extrusion,[placement]): makes an
        extrusion of the given polyline with the given extrusion vector"""
        if not placement:
            placement = self.addPlacement(local=False)
        value, norm = getValueAndDirection(extrusion)
        edir = create(self._fileobject, "IauracadDirection", [norm])
        solid = create(self._fileobject, "IauracadExtrudedAreaSolid", [profile, placement, edir, value])
        return solid

    def addExtrudedPolyline(self, points, extrusion, placement=None, color=None):
        """addExtrudedPolyline(points,extrusion,[placement,color]): makes an extruded polyline
        from the given points and the given extrusion vector"""
        pol = self.addProfile("IauracadPolyline", points)
        if not placement:
            placement = self.addPlacement(local=False)
        exp = self.addExtrusion(pol, extrusion, placement)
        if color:
            self.addColor(color, exp)
        return exp

    def addExtrudedCircle(self, data, extrusion, placement=None, color=None):
        """addExtrudedCircle(data,extrusion,[placement,color]): makes an extruded circle
        from the given data (center,radius) and the given extrusion vector"""
        cir = self.addProfile("IauracadCircleProfileDef", data[1])
        if not placement:
            placement = self.addPlacement(origin=data[0], local=False)
        exp = self.addExtrusion(cir, extrusion, placement)
        if color:
            self.addColor(color, exp)
        return exp

    def addExtrudedEllipse(self, data, extrusion, placement=None, color=None):
        """addExtrudedEllipse(data,extrusion,[placement,color]): makes an extruded ellipse
        from the given data (center,radiusx,radiusy) and the given extrusion vector"""
        cir = self.addProfile("IauracadEllipseProfileDef", [data[1], data[2]])
        if not placement:
            placement = self.addPlacement(origin=data[0], local=False)
        exp = self.addExtrusion(cir, extrusion, placement)
        if color:
            self.addColor(color, exp)
        return exp

    def addExtrudedCompositeCurve(self, curves, extrusion, placement=None, color=None):
        """addExtrudedCompositeCurve(curves,extrusion,[placement,color]): makes an extruded polyline
        from the given curves and the given extrusion vector"""
        if not placement:
            placement = self.addPlacement(local=False)
        ccu = self.addProfile("IauracadCompositeCurve", curves)
        exp = self.addExtrusion(ccu, extrusion, placement)
        if color:
            self.addColor(color, exp)
        return exp

    def addFace(self, face):
        """addFace(face): creates a face from the given face data (a list of lists of points).
        The first is the outer wire, the next are optional inner wires. They must be reversed in order
        """
        ifb = []
        idx = 0
        for f in face:
            pts = []
            for p in f:
                # print(p)
                if p in self.fpoints:
                    # print(self.fpoints.index(p))
                    # print(self.frefs)
                    pts.append(self.frefs[self.fpoints.index(p)])
                else:
                    pt = create(self._fileobject, "IauracadCartesianPoint", getTuple(p))
                    pts.append(pt)
                    self.fpoints.append(p)
                    self.frefs.append(pt)
            # print(pts)
            loop = create(self._fileobject, "IauracadPolyLoop", [pts])
            if idx == 0:
                fb = create(self._fileobject, "IauracadFaceOuterBound", [loop, True])
            else:
                fb = create(self._fileobject, "IauracadFaceBound", [loop, True])
            ifb.append(fb)
            idx += 1
        iface = create(self._fileobject, "IauracadFace", [ifb])
        return iface

    def addFacetedBrep(self, faces, color=None):
        """addFacetedBrep(self,faces,[color]): creates a faceted brep object from the given list
        of faces (each face is a list of lists of points, inner wires are reversed)"""
        self.fpoints = []
        self.frefs = []
        # print("adding ",len(faces)," faces")
        # print(faces)
        ifaces = [self.addFace(face) for face in faces]
        sh = create(self._fileobject, "IauracadClosedShell", [ifaces])
        brp = create(self._fileobject, "IauracadFacetedBrep", [sh])
        if color:
            self.addColor(color, brp)
        return brp
