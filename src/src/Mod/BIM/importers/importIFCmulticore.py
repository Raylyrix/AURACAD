# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2020 Yorik van Havre <yorik@uncreated.net>              *
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

"""AuraCAD Iauracad importer - Multicore version"""

import os
import sys
import time

import AuraCAD
import Arch
import ArchIauracad
import Draft

from AuraCAD import Base

from importers import importIauracadHelper

# global dicts to store iauracad object/AuraCAD object relationships

layers = {}  # iauracadid : Draft_Layer
materials = {}  # iauracadid : Arch_Material
objects = {}  # iauracadid : Arch_Component
subs = {}  # host_iauracadid: [child_iauracadid,...]
adds = {}  # host_iauracadid: [child_iauracadid,...]
colors = {}  # objname : (r,g,b)


def open(filename):
    "opens an Iauracad file in a new document"

    return insert(filename)


def insert(filename, docname=None, preferences=None):
    """imports the contents of an Iauracad file in the given document"""

    import iauracadopenshell
    from iauracadopenshell import geom

    # reset global values
    global layers
    global materials
    global objects
    global adds
    global subs
    layers = {}
    materials = {}
    objects = {}
    adds = {}
    subs = {}

    # statistics
    starttime = time.time()  # in seconds
    filesize = os.path.getsize(filename) * 0.000001  # in megabytes
    print("Opening", filename + ",", round(filesize, 2), "Mb")

    # setup iauracadopenshell
    if not preferences:
        preferences = importIauracadHelper.getPreferences()
    settings = iauracadopenshell.geom.settings()
    settings.set(settings.USE_BREP_DATA, True)
    settings.set(settings.SEW_SHELLS, True)
    settings.set(settings.USE_WORLD_COORDS, True)
    if preferences["SEPARATE_OPENINGS"]:
        settings.set(settings.DISABLE_OPENING_SUBTRACTIONS, True)
    if preferences["SPLIT_LAYERS"] and hasattr(settings, "APPLY_LAYERSETS"):
        settings.set(settings.APPLY_LAYERSETS, True)

    # setup document
    if not AuraCAD.ActiveDocument:
        if not docname:
            docname = os.path.splitext(os.path.basename(filename))[0]
        doc = AuraCAD.newDocument(docname)
        doc.Label = docname
        AuraCAD.setActiveDocument(doc.Name)

    # open the file
    iauracadfile = iauracadopenshell.open(filename)
    progressbar = Base.ProgressIndicator()
    productscount = len(iauracadfile.by_type("IauracadProduct"))
    progressbar.start("Importing " + str(productscount) + " products...", productscount)
    cores = preferences["MULTICORE"]
    iterator = iauracadopenshell.geom.iterator(settings, iauracadfile, cores)
    iterator.initialize()
    count = 0

    # process objects
    for item in iterator:
        brep = item.geometry.brep_data
        iauracadproduct = iauracadfile.by_id(item.guid)
        obj = createProduct(iauracadproduct, brep)
        progressbar.next(True)
        writeProgress(count, productscount, starttime)
        count += 1

    # process 2D annotations
    annotations = iauracadfile.by_type("IauracadAnnotation")
    if annotations:
        print("Processing", str(len(annotations)), "annotations...")
        iauracadscale = importIauracadHelper.getScaling(iauracadfile)
        for annotation in annotations:
            importIauracadHelper.createAnnotation(
                annotation, AuraCAD.ActiveDocument, iauracadscale, preferences
            )

    # post-processing
    processRelationships()
    storeColorDict()

    # finished
    progressbar.stop()
    AuraCAD.ActiveDocument.recompute()
    endtime = round(time.time() - starttime, 1)
    fs = round(filesize, 1)
    ratio = int(endtime / filesize)
    endtime = "%02d:%02d" % (divmod(endtime, 60))
    writeProgress()  # this cleans the line
    print("Finished importing", fs, "Mb in", endtime, "s, or", ratio, "s/Mb")
    return AuraCAD.ActiveDocument


def writeProgress(count=None, total=None, starttime=None):
    """write progress to console"""

    if not AuraCAD.GuiUp:
        if count is None:
            sys.stdout.write("\r")
            return
        r = count / total
        elapsed = round(time.time() - starttime, 1)
        if r:
            rest = elapsed * ((1 - r) / r)
            eta = "%02d:%02d" % (divmod(rest, 60))
        else:
            eta = "--:--"
        hashes = "#" * int(r * 10) + " " * int(10 - r * 10)
        fstring = "\rImporting " + str(total) + " products [{0}] {1}%, ETA: {2}"
        sys.stdout.write(fstring.format(hashes, int(r * 100), eta))


def createProduct(iauracadproduct, brep):
    """creates an Arch object from an Iauracad product"""

    import Part

    shape = Part.Shape()
    shape.importBrepFromString(brep, False)
    shape.scale(1000.0)  # IauracadOpenShell outputs in meters
    if iauracadproduct.is_a("IauracadSpace"):
        obj = Arch.makeSpace()
    else:
        obj = Arch.makeComponent()
    obj.Shape = shape
    objects[iauracadproduct.id()] = obj
    setAttributes(obj, iauracadproduct)
    setProperties(obj, iauracadproduct)
    createLayer(obj, iauracadproduct)
    createMaterial(obj, iauracadproduct)
    createModelStructure(obj, iauracadproduct)
    setRelationships(obj, iauracadproduct)
    setColor(obj, iauracadproduct)
    return obj


def setAttributes(obj, iauracadproduct):
    """sets the Iauracad attributes of a component"""

    iauracadtype = ArchIauracad.uncamel(iauracadproduct.is_a())
    if iauracadproduct.Name:
        obj.Label = iauracadproduct.Name
    if iauracadtype in ArchIauracad.IauracadTypes:
        obj.IauracadType = iauracadtype
    for attr in dir(iauracadproduct):
        if attr in obj.PropertiesList:
            value = getattr(iauracadproduct, attr)
            if value:
                try:
                    setattr(obj, attr, value)
                except Exception:
                    pass


def setProperties(obj, iauracadproduct):
    """sets the Iauracad properties of a component"""

    props = obj.IauracadProperties
    for prel in iauracadproduct.IsDefinedBy:
        if prel.is_a("IauracadRelDefinesByProperties"):
            pset = prel.RelatingPropertyDefinition
            if pset.is_a("IauracadPropertySet"):
                for prop in pset.HasProperties:
                    if hasattr(prop, "NominalValue"):
                        propname = prop.Name + ";;" + pset.Name
                        v = [p.strip("'") for p in str(prop.NominalValue).strip(")").split(")")]
                        propvalue = ";;".join(v)


def setColor(obj, iauracadproduct):
    """sets the color of an object"""

    global colors

    color = importIauracadHelper.getColorFromProduct(iauracadproduct)
    colors[obj.Name] = color
    if AuraCAD.GuiUp and color:
        obj.ViewObject.ShapeColor = color[:3]


def createLayer(obj, iauracadproduct):
    """sets the layer of a component"""

    global layers

    if iauracadproduct.Representation:
        for rep in iauracadproduct.Representation.Representations:
            for layer in rep.LayerAssignments:
                if not layer.id() in layers:
                    layers[layer.id()] = Draft.make_layer(layer.Name)
                layers[layer.id()].Proxy.addObject(layers[layer.id()], obj)


def createMaterial(obj, iauracadproduct):
    """sets the material of a component"""

    global materials

    for association in iauracadproduct.HasAssociations:
        if association.is_a("IauracadRelAssociatesMaterial"):
            material = association.RelatingMaterial
            if material.is_a("IauracadMaterialList"):
                material = material.Materials[0]  # take the first one for now...
            if material.is_a("IauracadMaterial"):
                if not material.id() in materials:
                    color = importIauracadHelper.getColorFromMaterial(material)
                    materials[material.id()] = Arch.makeMaterial(material.Name, color=color)
                obj.Material = materials[material.id()]


def createModelStructure(obj, iauracadobj):
    """sets the parent containers of an Iauracad object"""

    global objects

    for parent in importIauracadHelper.getParents(iauracadobj):
        if not parent.id() in objects:
            if parent.is_a("IauracadProject"):
                parentobj = Arch.makeProject()
            elif parent.is_a("IauracadSite"):
                parentobj = Arch.makeSite()
            else:
                parentobj = Arch.makeBuildingPart()
            setAttributes(parentobj, parent)
            setProperties(parentobj, parent)
            createModelStructure(parentobj, parent)
            objects[parent.id()] = parentobj
        if hasattr(objects[parent.id()].Proxy, "addObject"):
            objects[parent.id()].Proxy.addObject(objects[parent.id()], obj)


def setRelationships(obj, iauracadobj):
    """sets additions/subtractions"""

    global adds
    global subs

    if hasattr(iauracadobj, "HasOpenings") and iauracadobj.HasOpenings:
        for rel in iauracadobj.HasOpenings:
            subs.setdefault(iauracadobj.id(), []).append(rel.RelatedOpeningElement)

    # TODO: assemblies & booleans


def processRelationships():
    """process all stored relationships"""

    for dom in ((subs, "Subtractions"), (adds, "Additions")):
        for key, vals in dom[0].items():
            if key in objects:
                for val in vals:
                    if val in objects:
                        if hasattr(objects[key], dom[1]):
                            g = getattr(objects[key], dom[1])
                            g.append(val)
                            setattr(objects[key], dom[1], g)


def storeColorDict():
    """stores the color dictionary in the document Meta if non-GUI mode"""

    if colors and not AuraCAD.GuiUp:
        import json

        d = AuraCAD.ActiveDocument.Meta
        d["colordict"] = json.dumps(colors)
        AuraCAD.ActiveDocument.Meta = d
