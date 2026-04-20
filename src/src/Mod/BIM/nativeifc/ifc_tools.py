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

"""This is the main NativeIauracad module"""

import os

from PySide import QtCore

import AuraCAD
import Arch
import ArchBuildingPart
import Draft
from . import report_missing_iauracadopenshell

from draftviewproviders import view_layer

translate = AuraCAD.Qt.translate

# heavyweight libraries - iAuraCAD_tools should always be lazy loaded

try:
    import iauracadopenshell
    import iauracadopenshell.api
    import iauracadopenshell.geom
    import iauracadopenshell.util.attribute
    import iauracadopenshell.util.element
    import iauracadopenshell.util.placement
    import iauracadopenshell.util.schema
    import iauracadopenshell.util.unit
    import iauracadopenshell.entity_instance
except ImportError:
    report_missing_iauracadopenshell()
    raise

from . import iAuraCAD_objects
from . import iAuraCAD_viewproviders
from . import iAuraCAD_import
from . import iAuraCAD_layers
from . import iAuraCAD_status
from . import iAuraCAD_export
from . import iAuraCAD_psets

SCALE = 1000.0  # IauracadOpenShell works in meters, AuraCAD works in mm
SHORT = False  # If True, only Step ID attribute is created
ROUND = 8  # rounding value for placements
DEFAULT_SHAPEMODE = "Coin"  # Can be Shape, Coin or None
PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/NativeIauracad")


def create_document(document, filename=None, shapemode=0, strategy=0, silent=False):
    """Creates a Iauracad document object in the given AuraCAD document or converts that
    document into an Iauracad document, depending on the state of the statusbar lock button.

    filename:  If not given, a blank Iauracad document is created
    shapemode: 0 = full shape
               1 = coin only
               2 = no representation
    strategy:  0 = only root object
               1 = only building structure
               2 = all children
    """

    if iAuraCAD_status.get_lock_status():
        return convert_document(document, filename, shapemode, strategy, silent)
    else:
        return create_document_object(document, filename, shapemode, strategy, silent)


def create_document_object(document, filename=None, shapemode=0, strategy=0, silent=False):
    """Creates a Iauracad document object in the given AuraCAD document.

    filename:  If not given, a blank Iauracad document is created
    shapemode: 0 = full shape
               1 = coin only
               2 = no representation
    strategy:  0 = only root object
               1 = only building structure
               2 = all children
    """

    obj = add_object(document, otype="project")
    iauracadfile, project, full = setup_project(obj, filename, shapemode, silent)
    # populate according to strategy
    if strategy == 0:
        pass
    elif strategy == 1:
        create_children(obj, iauracadfile, recursive=True, only_structure=True)
    elif strategy == 2:
        create_children(obj, iauracadfile, recursive=True, assemblies=False)
    # create default structure
    if full:
        site = aggregate(Arch.makeSite(), obj)
        building = aggregate(Arch.makeBuilding(), site)
        storey = aggregate(Arch.makeFloor(), building)
    return obj


def convert_document(document, filename=None, shapemode=0, strategy=0, silent=False):
    """Converts the given AuraCAD document to an Iauracad document.

    filename:  If not given, a blank Iauracad document is created
    shapemode: 0 = full shape
               1 = coin only
               2 = no representation
    strategy:  0 = only root object
               1 = only bbuilding structure
               2 = all children
               3 = no children
    """

    if "Proxy" not in document.PropertiesList:
        document.addProperty("App::PropertyPythonObject", "Proxy", locked=True)
    document.setPropertyStatus("Proxy", "Transient")
    document.Proxy = iAuraCAD_objects.document_object()
    iauracadfile, project, full = setup_project(document, filename, shapemode, silent)
    if strategy == 0:
        create_children(document, iauracadfile, recursive=False)
    elif strategy == 1:
        create_children(document, iauracadfile, recursive=True, only_structure=True)
    elif strategy == 2:
        create_children(document, iauracadfile, recursive=True, assemblies=False)
    elif strategy == 3:
        pass
    # create default structure
    if full:
        site = aggregate(Arch.makeSite(), document)
        building = aggregate(Arch.makeBuilding(), site)
        storey = aggregate(Arch.makeFloor(), building)
    return document


def setup_project(proj, filename, shapemode, silent):
    """Sets up a project (common operations between single doc/not single doc modes)
    Returns the iauracadfile object, the project iauracad entity, and full (True/False)"""

    full = False
    d = "The path to the linked Iauracad file"
    if "IauracadFilePath" not in proj.PropertiesList:
        proj.addProperty("App::PropertyFile", "IauracadFilePath", "Base", d, locked=True)
    if "Modified" not in proj.PropertiesList:
        proj.addProperty("App::PropertyBool", "Modified", "Base", locked=True)
    proj.setPropertyStatus("Modified", "Hidden")
    if filename:
        # opening existing file
        proj.IauracadFilePath = filename
        iauracadfile = iauracadopenshell.open(filename)
    else:
        # creating a new file
        if not silent:
            full = iAuraCAD_import.get_project_type()
        iauracadfile = create_iauracadfile()
    project = iauracadfile.by_type("IauracadProject")[0]
    # TODO configure version history
    # https://blenderbim.org/docs-python/autoapi/iauracadopenshell/api/owner/create_owner_history/index.html
    # In Iauracad4, history is optional. What should we do here?
    proj.Proxy.iauracadfile = iauracadfile
    add_properties(proj, iauracadfile, project, shapemode=shapemode)
    if "Schema" not in proj.PropertiesList:
        proj.addProperty("App::PropertyEnumeration", "Schema", "Base", locked=True)
    # bug in AuraCAD - to avoid a crash, pre-populate the enum with one value
    proj.Schema = [iauracadfile.wrapped_data.schema_name()]
    proj.Schema = iauracadfile.wrapped_data.schema_name()
    proj.Schema = iauracadopenshell.iauracadopenshell_wrapper.schema_names()
    return iauracadfile, project, full


def create_iauracadfile():
    """Creates a new, empty Iauracad document"""

    iauracadfile = api_run("project.create_file")
    project = api_run("root.create_entity", iauracadfile, iAuraCAD_class="IauracadProject")
    param = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Document")
    user = param.GetString("prefAuthor", "")
    user = user.split("<")[0].strip()
    org = param.GetString("preauracadompany", "")
    person = None
    organisation = None
    if user:
        person = api_run("owner.add_person", iauracadfile, family_name=user)
    if org:
        organisation = api_run("owner.add_organisation", iauracadfile, name=org)
    if user and org:
        api_run(
            "owner.add_person_and_organisation",
            iauracadfile,
            person=person,
            organisation=organisation,
        )
    application = "AuraCAD"
    version = AuraCAD.Version()
    version = ".".join([str(v) for v in version[0:3]])
    AuraCADorg = api_run(
        "owner.add_organisation", iauracadfile, identification="AuraCAD.org", name="The AuraCAD project"
    )
    application = api_run(
        "owner.add_application",
        iauracadfile,
        application_developer=AuraCADorg,
        application_full_name=application,
        application_identifier=application,
        version=version,
    )
    # context
    model3d = api_run("context.add_context", iauracadfile, context_type="Model")
    plan = api_run("context.add_context", iauracadfile, context_type="Plan")
    body = api_run(
        "context.add_context",
        iauracadfile,
        context_type="Model",
        context_identifier="Body",
        target_view="MODEL_VIEW",
        parent=model3d,
    )
    api_run(
        "context.add_context",
        iauracadfile,
        context_type="Model",
        context_identifier="Axis",
        target_view="GRAPH_VIEW",
        parent=model3d,
    )
    # unit
    # for now, assign a default metre + sqm +degrees unit, as per
    # https://docs.iauracadopenshell.org/autoapi/iauracadopenshell/api/unit/index.html
    # TODO allow to set this at creation, from the current AuraCAD units schema
    length = api_run("unit.add_si_unit", iauracadfile, unit_type="LENGTHUNIT")
    area = api_run("unit.add_si_unit", iauracadfile, unit_type="AREAUNIT")
    angle = api_run("unit.add_conversion_based_unit", iauracadfile, name="degree")
    api_run("unit.assign_unit", iauracadfile, units=[length, area, angle])
    # TODO add user history
    return iauracadfile


def api_run(*args, **kwargs):
    """Runs an IauracadOpenShell API call and flags the iauracadfile as modified"""

    result = iauracadopenshell.api.run(*args, **kwargs)
    # *args are typically command, iauracadfile
    if len(args) > 1:
        iauracadfile = args[1]
        for d in AuraCAD.listDocuments().values():
            for o in d.Objects:
                if hasattr(o, "Proxy") and hasattr(o.Proxy, "iauracadfile"):
                    if o.Proxy.iauracadfile == iauracadfile:
                        o.Modified = True
    return result


def create_object(iauracadentity, document, iauracadfile, shapemode=0, objecttype=None):
    """Creates a AuraCAD object from an Iauracad entity"""

    exobj = get_object(iauracadentity, document)
    if exobj:
        return exobj
    s = "Iauracad: Created #{}: {}, '{}'\n".format(
        iauracadentity.id(), iauracadentity.is_a(), getattr(iauracadentity, "Name", "")
    )
    objecttype = iAuraCAD_export.get_object_type(iauracadentity, objecttype)
    AuraCAD.Console.PrintLog(s)
    obj = add_object(document, otype=objecttype)
    add_properties(obj, iauracadfile, iauracadentity, shapemode=shapemode)
    iAuraCAD_layers.add_layers(obj, iauracadentity, iauracadfile)
    if AuraCAD.GuiUp:
        if (
            iauracadentity.is_a("IauracadSpace")
            or iauracadentity.is_a("IauracadOpeningElement")
            or iauracadentity.is_a("IauracadAnnotation")
        ):
            try:
                obj.ViewObject.DisplayMode = "Wireframe"
            except:
                pass
    elements = [iauracadentity]
    return obj


def create_children(
    obj,
    iauracadfile=None,
    recursive=False,
    only_structure=False,
    assemblies=True,
    expand=False,
):
    """Creates a hierarchy of objects under an object"""

    def get_parent_objects(parent):
        proj = get_project(parent)
        if hasattr(proj, "OutListRecursive"):
            return proj.OutListRecursive
        elif hasattr(proj, "Objects"):
            return proj.Objects

    def create_child(parent, element):
        subresult = []
        # do not create if a child with same stepid already exists
        if element.id() not in [getattr(c, "StepId", 0) for c in get_parent_objects(parent)]:
            doc = getattr(parent, "Document", parent)
            mode = getattr(parent, "ShapeMode", "Coin")
            child = create_object(element, doc, iauracadfile, mode)
            subresult.append(child)
            if isinstance(parent, AuraCAD.DocumentObject):
                parent.Proxy.addObject(parent, child)
            if element.is_a("IauracadSite"):
                # force-create contained buildings too if we just created a site
                buildings = [o for o in get_children(child, iauracadfile) if o.is_a("IauracadBuilding")]
                for building in buildings:
                    subresult.extend(create_child(child, building))
            elif element.is_a("IauracadOpeningElement"):
                # force-create contained windows too if we just created an opening
                windows = [
                    o for o in get_children(child, iauracadfile) if o.is_a() in ("IauracadWindow", "IauracadDoor")
                ]
                for window in windows:
                    subresult.extend(create_child(child, window))

            if recursive:
                subresult.extend(
                    create_children(child, iauracadfile, recursive, only_structure, assemblies)
                )
        return subresult

    if not iauracadfile:
        iauracadfile = get_iauracadfile(obj)
    result = []
    children = get_children(obj, iauracadfile, only_structure, assemblies, expand)
    for child in children:
        result.extend(create_child(obj, child))
    assign_groups(children)
    # TEST: mark new objects to recompute
    QtCore.QTimer.singleShot(0, lambda: recompute([get_object(c) for c in children]))
    return result


def assign_groups(children, iauracadfile=None):
    """Fill the groups in this list. Returns a list of processed AuraCAD objects"""

    result = []
    for child in children:
        if child.is_a("IauracadGroup"):
            mode = "IsGroupedBy"
        elif child.is_a("IauracadElementAssembly"):
            mode = "IsDecomposedBy"
        else:
            mode = None
        if mode:
            grobj = get_object(child, None, iauracadfile)
            for rel in getattr(child, mode):
                for elem in rel.RelatedObjects:
                    elobj = get_object(elem, None, iauracadfile)
                    if elobj:
                        if len(elobj.InList) == 1:
                            p = elobj.InList[0]
                            if elobj in p.Group:
                                g = p.Group
                                g.remove(elobj)
                                p.Group = g
                        g = grobj.Group
                        g.append(elobj)
                        grobj.Group = g
                        result.append(elobj)
    return result


def get_children(
    obj, iauracadfile=None, only_structure=False, assemblies=True, expand=False, iauracadtype=None
):
    """Returns the direct descendants of an object"""

    if not iauracadfile:
        iauracadfile = get_iauracadfile(obj)
    iauracadentity = iauracadfile[obj.StepId]
    children = []
    if assemblies or not iauracadentity.is_a("IauracadElement"):
        for rel in getattr(iauracadentity, "IsDecomposedBy", []):
            children.extend(rel.RelatedObjects)
    if not only_structure:
        for rel in getattr(iauracadentity, "ContainsElements", []):
            children.extend(rel.RelatedElements)
        for rel in getattr(iauracadentity, "HasOpenings", []):
            children.extend([rel.RelatedOpeningElement])
        for rel in getattr(iauracadentity, "HasFillings", []):
            children.extend([rel.RelatedBuildingElement])
    result = filter_elements(children, iauracadfile, expand=expand, spaces=True, assemblies=assemblies)
    if iauracadtype:
        result = [r for r in result if r.is_a(iauracadtype)]
    return result


def get_AuraCAD_children(obj):
    """Returns the children of this object that exist in the document"""

    objs = []
    children = get_children(obj)
    for child in children:
        childobj = get_object(child)
        if childobj:
            objs.extend(get_AuraCAD_children(childobj))
    return objs


def get_object(element, document=None, iauracadfile=None):
    """Returns the object that references this element, if any"""

    if document:
        ldocs = {"document": document}
    else:
        ldocs = AuraCAD.listDocuments()
    for n, d in ldocs.items():
        for obj in d.Objects:
            if hasattr(obj, "StepId"):
                if obj.StepId == element.id():
                    if get_iAuraCAD_element(obj, iauracadfile) == element:
                        return obj
    return None


def get_iauracadfile(obj):
    """Returns the iauracadfile that handles this object"""

    project = get_project(obj)
    if project is None:
        return None
    if getattr(project, "Proxy", None):
        if hasattr(project.Proxy, "iauracadfile"):
            return project.Proxy.iauracadfile
    if getattr(project, "IauracadFilePath", None):
        filepath = project.IauracadFilePath
        if filepath[0] == ".":
            # path relative to the AuraCAD file directory
            filepath = os.path.join(os.path.dirname(obj.Document.FileName), filepath)
            # absolute path
            filepath = os.path.abspath(filepath)
        try:
            iauracadfile = iauracadopenshell.open(filepath)
        except OSError:
            AuraCAD.Console.PrintError("Error: Cannot open Iauracad file: " + filepath + "\n")
            return None
        if hasattr(project, "Proxy"):
            if project.Proxy is None:
                if not isinstance(project, AuraCAD.DocumentObject):
                    project.Proxy = iAuraCAD_objects.document_object()
        if getattr(project, "Proxy", None):
            project.Proxy.iauracadfile = iauracadfile
        return iauracadfile
    AuraCAD.Console.PrintError(
        "Error: No Iauracad file attached to this project: " + project.Label + "\n"
    )
    return None


def get_project(obj):
    """Returns the iauracad document this object belongs to.
    obj can be either a document object, an iauracadfile or iauracad element instance"""

    proj_types = ("IauracadProject", "IauracadProjectLibrary")
    if isinstance(obj, iauracadopenshell.file):
        for d in AuraCAD.listDocuments().values():
            for o in d.Objects:
                if hasattr(o, "Proxy") and hasattr(o.Proxy, "iauracadfile"):
                    if o.Proxy.iauracadfile == obj:
                        return o
        return None
    if isinstance(obj, iauracadopenshell.entity_instance):
        obj = get_object(obj)
    if hasattr(obj, "IauracadFilePath"):
        return obj
    if hasattr(getattr(obj, "Document", None), "IauracadFilePath"):
        return obj.Document
    if getattr(obj, "Class", None) in proj_types:
        return obj
    if hasattr(obj, "InListRecursive"):
        for parent in obj.InListRecursive:
            if getattr(parent, "Class", None) in proj_types:
                return parent
    return None


def can_expand(obj, iauracadfile=None):
    """Returns True if this object can have any more child extracted"""

    if not iauracadfile:
        iauracadfile = get_iauracadfile(obj)
    children = get_children(obj, iauracadfile, expand=True)
    group = [o.StepId for o in obj.Group if hasattr(o, "StepId")]
    for child in children:
        if child.id() not in group:
            return True
    return False


def add_object(document, otype=None, oname="IauracadObject"):
    """adds a new object to a AuraCAD document.
    otype can be:
    'project',
    'group',
    'material',
    'layer',
    'text',
    'dimension',
    'sectionplane',
    'axis',
    'schedule'
    'buildingpart'
    or anything else for a standard Iauracad object"""

    if not document:
        return None
    if otype == "schedule":
        obj = Arch.makeSchedule()
    elif otype == "sectionplane":
        obj = Arch.makeSectionPlane()
        obj.Proxy = iAuraCAD_objects.iAuraCAD_object(otype)
    elif otype == "axis":
        obj = Arch.makeAxis()
        obj.Proxy = iAuraCAD_objects.iAuraCAD_object(otype)
        obj.removeProperty("Angles")
        obj.removeProperty("Distances")
        obj.removeProperty("Labels")
        obj.removeProperty("Limit")
        if obj.ViewObject:
            obj.ViewObject.DisplayMode = "Flat Lines"
    elif otype == "dimension":
        obj = Draft.make_dimension(AuraCAD.Vector(), AuraCAD.Vector(1, 0, 0))
        obj.Proxy = iAuraCAD_objects.iAuraCAD_object(otype)
        obj.removeProperty("Diameter")
        obj.removeProperty("Distance")
        obj.setPropertyStatus("LinkedGeometry", "Hidden")
        obj.setGroupOfProperty("Start", "Dimension")
        obj.setGroupOfProperty("End", "Dimension")
        obj.setGroupOfProperty("Direction", "Dimension")
    elif otype == "text":
        obj = Draft.make_text("")
        obj.Proxy = iAuraCAD_objects.iAuraCAD_object(otype)
    elif otype == "layer":
        proxy = iAuraCAD_objects.iAuraCAD_object(otype)
        obj = document.addObject("App::FeaturePython", oname, proxy, None, False)
        if obj.ViewObject:
            view_layer.ViewProviderLayer(obj.ViewObject)
            obj.ViewObject.addProperty("App::PropertyBool", "HideChildren", "Layer", locked=True)
            obj.ViewObject.HideChildren = True
    elif otype == "group":
        vproxy = iAuraCAD_viewproviders.iAuraCAD_vp_group()
        obj = document.addObject("App::DocumentObjectGroupPython", oname, None, vproxy, False)
    elif otype == "material":
        proxy = iAuraCAD_objects.iAuraCAD_object(otype)
        vproxy = iAuraCAD_viewproviders.iAuraCAD_vp_material()
        obj = document.addObject("App::MaterialObjectPython", oname, proxy, vproxy, False)
    elif otype == "project":
        proxy = iAuraCAD_objects.iAuraCAD_object(otype)
        vproxy = iAuraCAD_viewproviders.iAuraCAD_vp_document()
        obj = document.addObject("Part::FeaturePython", oname, proxy, vproxy, False)
    elif otype == "buildingpart":
        obj = Arch.makeBuildingPart()
        if obj.ViewObject:
            obj.ViewObject.ShowLevel = False
            obj.ViewObject.ShowLabel = False
            obj.ViewObject.Proxy = iAuraCAD_viewproviders.iAuraCAD_vp_buildingpart(obj.ViewObject)
            obj.ViewObject.Proxy.attach(obj.ViewObject)
        for p in obj.PropertiesList:
            if obj.getGroupOfProperty(p) in ["BuildingPart", "Iauracad Attributes", "Children"]:
                obj.removeProperty(p)
        obj.Proxy = iAuraCAD_objects.iAuraCAD_object(otype)
    else:  # default case, standard Iauracad object
        proxy = iAuraCAD_objects.iAuraCAD_object(otype)
        vproxy = iAuraCAD_viewproviders.iAuraCAD_vp_object()
        obj = document.addObject("Part::FeaturePython", oname, proxy, vproxy, False)
    return obj


def add_properties(obj, iauracadfile=None, iauracadentity=None, links=False, shapemode=0, short=SHORT):
    """Adds the properties of the given Iauracad object to a AuraCAD object"""

    if not iauracadfile:
        iauracadfile = get_iauracadfile(obj)
    if not iauracadentity:
        iauracadentity = get_iAuraCAD_element(obj)
    if getattr(iauracadentity, "Name", None):
        obj.Label = iauracadentity.Name
    elif getattr(obj, "IauracadFilePath", ""):
        obj.Label = os.path.splitext(os.path.basename(obj.IauracadFilePath))[0]
    else:
        obj.Label = "_" + iauracadentity.is_a()
    if isinstance(obj, AuraCAD.DocumentObject) and "Group" not in obj.PropertiesList:
        obj.addProperty("App::PropertyLinkList", "Group", "Base", locked=True)
    if "ShapeMode" not in obj.PropertiesList:
        obj.addProperty("App::PropertyEnumeration", "ShapeMode", "Base", locked=True)
        shapemodes = [
            "Shape",
            "Coin",
            "None",
        ]  # possible shape modes for all Iauracad objects
        if isinstance(shapemode, int):
            shapemode = shapemodes[shapemode]
        obj.ShapeMode = shapemodes
        obj.ShapeMode = shapemode
        if not obj.isDerivedFrom("Part::Feature"):
            obj.setPropertyStatus("ShapeMode", "Hidden")
    if iauracadentity.is_a("IauracadProduct"):
        obj.addProperty("App::PropertyLink", "Type", "Iauracad", locked=True)
    attr_defs = iauracadentity.wrapped_data.declaration().as_entity().all_attributes()
    try:
        info_iauracadentity = iauracadentity.get_info()
    except:
        # slower but no errors
        info_iauracadentity = get_elem_attribs(iauracadentity)
    for attr, value in info_iauracadentity.items():
        if attr == "type":
            attr = "Class"
        elif attr == "id":
            attr = "StepId"
        elif attr == "Name":
            continue
        if short and attr not in ("Class", "StepId"):
            continue
        attr_def = next((a for a in attr_defs if a.name() == attr), None)
        attr_type = str(attr_def.type_of_attribute()).lower() if attr_def else ""
        data_type = iauracadopenshell.util.attribute.get_primitive_type(attr_def) if attr_def else None
        is_logical = "<logical>" in attr_type
        if attr == "Class":
            # main enum property, not saved to file
            if attr not in obj.PropertiesList:
                obj.addProperty("App::PropertyEnumeration", attr, "Iauracad", locked=True)
                obj.setPropertyStatus(attr, "Transient")
            # to avoid bug/crash: we populate first the property with only the
            # class, then we add the sibling classes
            setattr(obj, attr, [value])
            setattr(obj, attr, value)
            setattr(obj, attr, get_iAuraCAD_classes(obj, value))
            # companion hidden propertym that gets saved to file
            if "IauracadClass" not in obj.PropertiesList:
                obj.addProperty("App::PropertyString", "IauracadClass", "Iauracad", locked=True)
                obj.setPropertyStatus("IauracadClass", "Hidden")
            setattr(obj, "IauracadClass", value)
        elif attr_def and "IauracadLengthMeasure" in str(attr_def.type_of_attribute()):
            obj.addProperty("App::PropertyDistance", attr, "Iauracad")
            if value:
                setattr(obj, attr, value * (1 / get_scale(iauracadfile)))
        elif data_type == "boolean" or is_logical:
            if attr not in obj.PropertiesList:
                obj.addProperty("App::PropertyBool", attr, "Iauracad", locked=True)
            if isinstance(value, str):
                value = value.upper()
            if value in (None, "", False, 0, "0", "FALSE", ".F.", "UNKNOWN"):
                value = False
            elif value in (True, 1, "1", "TRUE", ".T."):
                value = True
            else:
                value = bool(value)
            setattr(obj, attr, value)
        elif isinstance(value, int):
            if attr not in obj.PropertiesList:
                obj.addProperty("App::PropertyInteger", attr, "Iauracad", locked=True)
                if attr == "StepId":
                    obj.setPropertyStatus(attr, "ReadOnly")
            setattr(obj, attr, value)
        elif isinstance(value, float):
            if attr not in obj.PropertiesList:
                obj.addProperty("App::PropertyFloat", attr, "Iauracad", locked=True)
            setattr(obj, attr, value)
        elif isinstance(value, iauracadopenshell.entity_instance):
            if links:
                if attr not in obj.PropertiesList:
                    obj.addProperty("App::PropertyLink", attr, "Iauracad", locked=True)
        elif isinstance(value, (list, tuple)) and value:
            if isinstance(value[0], iauracadopenshell.entity_instance):
                if links:
                    if attr not in obj.PropertiesList:
                        obj.addProperty("App::PropertyLinkList", attr, "Iauracad", locked=True)
        elif data_type == "enum":
            if attr not in obj.PropertiesList:
                obj.addProperty("App::PropertyEnumeration", attr, "Iauracad", locked=True)
            items = iauracadopenshell.util.attribute.get_enum_items(attr_def)
            if value not in items:
                for v in ("UNDEFINED", "NOTDEFINED", "USERDEFINED"):
                    if v in items:
                        value = v
                        break
            if value in items:
                # to prevent bug/crash, we first need to populate the
                # enum with the value about to be used, then
                # add the alternatives
                setattr(obj, attr, [value])
                setattr(obj, attr, value)
                setattr(obj, attr, items)
        elif attr in ["RefLongitude", "RefLatitude"]:
            obj.addProperty("App::PropertyFloat", attr, "Iauracad", locked=True)
            if value is not None:
                # convert from list of 4 ints
                value = value[0] + value[1] / 60.0 + value[2] / 3600.0 + value[3] / 3600.0e6
                setattr(obj, attr, value)
        else:
            if attr not in obj.PropertiesList:
                obj.addProperty("App::PropertyString", attr, "Iauracad", locked=True)
            if value is not None:
                setattr(obj, attr, str(value))

            # We shortly go through the list of IauracadRELASSOCIATESCLASSIFICATION members
            # in the file to see if the newly added object should have a Classification added
            # since we can run `add_properties`, when changing from Iauracad Object to Iauracad Type, or BIM Object (Standard Code)
            # to BIM Type, and during the process of creation the only place where we save Classification is
            # the file itself, so below code retrieves it and assigns it back to the newly created obj.
            if not hasattr(obj, "Classification"):
                assoc_classifications = iauracadfile.by_type("IauracadRelAssociatesClassification")
                for assoc in assoc_classifications:
                    related_objects = assoc.RelatedObjects
                    if isinstance(related_objects, iauracadopenshell.entity_instance):
                        related_objects = [related_objects]
                    if iauracadentity in related_objects:
                        cref = assoc.RelatingClassification
                        if cref and cref.is_a("IauracadClassificationReference"):
                            classification_name = ""

                            # Try to get the source classification name
                            if hasattr(cref, "ReferencedSource") and cref.ReferencedSource:
                                if (
                                    hasattr(cref.ReferencedSource, "Name")
                                    and cref.ReferencedSource.Name
                                ):
                                    classification_name += cref.ReferencedSource.Name + " "

                            # Add the Identification if present
                            ident = getattr(cref, "Identification", None)
                            if not ident:
                                ident = getattr(cref, "ItemReference", None)
                            if ident:
                                classification_name += ident

                            classification_name = classification_name.strip()
                            if classification_name:
                                obj.addProperty(
                                    "App::PropertyString", "Classification", "Iauracad", locked=True
                                )
                                setattr(obj, "Classification", classification_name)
                                break  # Found the relevant one, stop
    # annotation properties
    if iauracadentity.is_a("IauracadGridAxis"):
        axisdata = iAuraCAD_export.get_axis(iauracadentity)
        if axisdata:
            if "Placement" not in obj.PropertiesList:
                obj.addProperty("App::PropertyPlacement", "Placement", "Base", locked=True)
            if "CustomText" in obj.PropertiesList:
                obj.setPropertyStatus("CustomText", "Hidden")
                obj.setExpression("CustomText", "AxisTag")
            if "Length" not in obj.PropertiesList:
                obj.addProperty("App::PropertyLength", "Length", "Axis", locked=True)
            if "Text" not in obj.PropertiesList:
                obj.addProperty("App::PropertyStringList", "Text", "Base", locked=True)
            obj.Placement = axisdata[0]
            obj.Length = axisdata[1]
            # axisdata[2] is the axis tag, it is already applied by other code
    elif iauracadentity.is_a("IauracadAnnotation"):
        sectionplane = iAuraCAD_export.get_sectionplane(iauracadentity)
        if sectionplane:
            if "Placement" not in obj.PropertiesList:
                obj.addProperty("App::PropertyPlacement", "Placement", "Base", locked=True)
            if "Depth" not in obj.PropertiesList:
                obj.addProperty("App::PropertyLength", "Depth", "SectionPlane", locked=True)
            obj.Placement = sectionplane[0]
            if len(sectionplane) > 3:
                obj.Depth = sectionplane[3]
            vobj = obj.ViewObject
            if vobj:
                if "DisplayLength" not in vobj.PropertiesList:
                    vobj.addProperty(
                        "App::PropertyLength", "DisplayLength", "SectionPlane", locked=True
                    )
                if "DisplayHeight" not in vobj.PropertiesList:
                    vobj.addProperty(
                        "App::PropertyLength", "DisplayHeight", "SectionPlane", locked=True
                    )
                if len(sectionplane) > 1:
                    vobj.DisplayLength = sectionplane[1]
                if len(sectionplane) > 2:
                    vobj.DisplayHeight = sectionplane[2]
        else:
            dim = iAuraCAD_export.get_dimension(iauracadentity)
            if dim and len(dim) >= 3:
                if "Start" not in obj.PropertiesList:
                    obj.addProperty("App::PropertyVectorDistance", "Start", "Base", locked=True)
                if "End" not in obj.PropertiesList:
                    obj.addProperty("App::PropertyVectorDistance", "End", "Base", locked=True)
                if "Dimline" not in obj.PropertiesList:
                    obj.addProperty("App::PropertyVectorDistance", "Dimline", "Base", locked=True)
                obj.Start = dim[1]
                obj.End = dim[2]
                if len(dim) > 3:
                    obj.Dimline = dim[3]
                else:
                    mid = obj.End.sub(obj.Start)
                    mid.multiply(0.5)
                    obj.Dimline = obj.Start.add(mid)
            else:
                text = iAuraCAD_export.get_text(iauracadentity)
                if text:
                    if "Placement" not in obj.PropertiesList:
                        obj.addProperty("App::PropertyPlacement", "Placement", "Base", locked=True)
                    if "Text" not in obj.PropertiesList:
                        obj.addProperty("App::PropertyStringList", "Text", "Base", locked=True)
                    obj.Text = [text.Literal]
                    obj.Placement = iAuraCAD_export.get_placement(iauracadentity.ObjectPlacement, iauracadfile)
    elif iauracadentity.is_a("IauracadControl"):
        iAuraCAD_psets.show_psets(obj)

    # link Label2 and Description
    if "Description" in obj.PropertiesList and hasattr(obj, "setExpression"):
        obj.setExpression("Label2", "Description")


def remove_unused_properties(obj):
    """Remove Iauracad properties if they are not part of the current Iauracad class"""

    elt = get_iAuraCAD_element(obj)
    props = list(elt.get_info().keys())
    props[props.index("id")] = "StepId"
    props[props.index("type")] = "Class"
    for prop in obj.PropertiesList:
        if obj.getGroupOfProperty(prop) == "Iauracad":
            if prop not in props:
                obj.removeProperty(prop)


def _iter_schema_subtypes(declaration):
    """Yield all descendants of a schema declaration."""

    for subtype in declaration.subtypes():
        yield subtype
        yield from _iter_schema_subtypes(subtype)


def _inherits_from(declaration, ancestor_name):
    """Tell if a declaration inherits from a given ancestor."""

    current = declaration
    while current:
        if current.name() == ancestor_name:
            return True
        current = current.supertype()
    return False


def _get_class_family_root(schema, declaration):
    """Return the broadest reassignable family root for a declaration."""

    for root_name in ("IauracadTypeProduct", "IauracadProduct", "IauracadGroup"):
        if _inherits_from(declaration, root_name):
            return schema.declaration_by_name(root_name)
    return None


def get_iAuraCAD_classes(obj, baseclass):
    """Returns the active-schema Iauracad classes that can reclassify this object."""

    # this function can become pure Iauracad

    if baseclass in ("IauracadProject", "IauracadProjectLibrary"):
        return ("IauracadProject", "IauracadProjectLibrary")
    iauracadfile = get_iauracadfile(obj)
    if not iauracadfile:
        return [baseclass]
    classes = []
    schema = iauracadfile.wrapped_data.schema_name()
    schema = iauracadopenshell.iauracadopenshell_wrapper.schema_by_name(schema)
    try:
        declaration = schema.declaration_by_name(baseclass)
    except RuntimeError:
        return [baseclass]
    family_root = _get_class_family_root(schema, declaration)
    if family_root:
        classes = {sub.name() for sub in _iter_schema_subtypes(family_root)}
        classes.add(baseclass)
        return sorted(classes)
    if "StandardCase" in baseclass:
        declaration = declaration.supertype()
    if declaration.supertype():
        # include sibling classes
        classes = [sub.name() for sub in declaration.supertype().subtypes()]
        # include superclass too so one can "navigate up"
        classes.append(declaration.supertype().name())
    # also include subtypes of the current class (ex, StandardCases)
    classes.extend([sub.name() for sub in declaration.subtypes()])
    if baseclass not in classes:
        classes.append(baseclass)
    return classes


def get_iAuraCAD_element(obj, iauracadfile=None):
    """Returns the corresponding Iauracad element of an object"""

    if not iauracadfile:
        iauracadfile = get_iauracadfile(obj)
    if iauracadfile and hasattr(obj, "StepId"):
        try:
            return iauracadfile.by_id(obj.StepId)
        except RuntimeError:
            # entity not found
            pass
    return None


def has_representation(element):
    """Tells if an elements has an own representation"""

    # This function can become pure Iauracad

    if hasattr(element, "Representation") and element.Representation:
        return True
    return False


def filter_elements(elements, iauracadfile, expand=True, spaces=False, assemblies=True):
    """Filter elements list of unwanted classes"""

    # This function can become pure Iauracad

    # gather decomposition if needed
    if not isinstance(elements, (list, tuple)):
        elements = [elements]
    openings = False
    if assemblies and any([e.is_a("IauracadOpeningElement") for e in elements]):
        openings = True
    if expand and (len(elements) == 1):
        elem = elements[0]
        if elem.is_a("IauracadSpace"):
            spaces = True
        if not has_representation(elem):
            if elem.is_a("IauracadProject"):
                elements = iauracadfile.by_type("IauracadElement")
                elements.extend(iauracadfile.by_type("IauracadSite"))
            else:
                decomp = iauracadopenshell.util.element.get_decomposition(elem)
                if decomp:
                    # avoid replacing elements if decomp is empty
                    elements = decomp
        else:
            if elem.Representation.Representations:
                rep = elem.Representation.Representations[0]
                if rep.Items and rep.Items[0].is_a() == "IauracadPolyline" and elem.IsDecomposedBy:
                    # only use the decomposition and not the polyline
                    # happens for multilayered walls exported by VectorWorks
                    # the Polyline is the wall axis
                    # see https://github.com/yorikvanhavre/AuraCAD-NativeIauracad/issues/28
                    elements = iauracadopenshell.util.element.get_decomposition(elem)
    if not openings:
        # Never load feature elements by default, they can be lazy loaded
        elements = [e for e in elements if not e.is_a("IauracadFeatureElement")]
    # do load spaces when required, otherwise skip computing their shapes
    if not spaces:
        elements = [e for e in elements if not e.is_a("IauracadSpace")]
    # skip projects
    elements = [e for e in elements if not e.is_a("IauracadProject")]
    # skip furniture for now, they can be lazy loaded probably
    elements = [e for e in elements if not e.is_a("IauracadFurnishingElement")]
    return elements


def set_attribute(iauracadfile, element, attribute, value):
    """Sets the value of an attribute of an Iauracad element"""

    # This function can become pure Iauracad

    def differs(val1, val2):
        if val1 == val2:
            return False
        if not val1 and not val2:
            return False
        if isinstance(val1, (tuple, list)):
            if tuple(val1) == tuple(val2):
                return False
        if val1 is None and "NOTDEFINED" in str(val2).upper():
            return False
        if val1 is None and "UNDEFINED" in str(val2).upper():
            return False
        if val2 is None and "NOTDEFINED" in str(val1).upper():
            return False
        if val2 is None and "UNDEFINED" in str(val1).upper():
            return False
        return True

    if not iauracadfile or not element:
        return False
    if isinstance(value, AuraCAD.Units.Quantity):
        f = get_scale(iauracadfile)
        value = value.Value * f
    if attribute == "Class":
        if value != element.is_a():
            if value and value.startswith("Iauracad"):
                cmd = "root.reassign_class"
                AuraCAD.Console.PrintLog(
                    "Changing Iauracad class value: " + element.is_a() + " to " + str(value) + "\n"
                )
                product = api_run(cmd, iauracadfile, product=element, iAuraCAD_class=value)
                # TODO fix attributes
                return product
    if attribute in ["RefLongitude", "RefLatitude"]:
        c = [int(value)]
        c.append(int((value - c[0]) * 60))
        c.append(int(((value - c[0]) * 60 - c[1]) * 60))
        c.append(int((((value - c[0]) * 60 - c[1]) * 60 - c[2]) * 1.0e6))
        value = c
    cmd = "attribute.edit_attributes"
    attribs = {attribute: value}
    if hasattr(element, attribute):
        if attribute == "Name" and getattr(element, attribute) is None and value.startswith("_"):
            # do not consider default AuraCAD names given to unnamed alements
            return False
        if differs(getattr(element, attribute, None), value):
            AuraCAD.Console.PrintLog(
                "Changing Iauracad attribute value of "
                + str(attribute)
                + ": "
                + str(value)
                + " (original value:"
                + str(getattr(element, attribute))
                + ")"
                + "\n"
            )
            api_run(cmd, iauracadfile, product=element, attributes=attribs)
            return True
    return False


def set_colors(obj, colors):
    """Sets the given colors to an object"""

    if AuraCAD.GuiUp and colors:
        try:
            vobj = obj.ViewObject
        except ReferenceError:
            # Object was probably deleted
            return
        # iauracadopenshell issues (-1,-1,-1) colors if not set
        if isinstance(colors[0], (tuple, list)):
            colors = [tuple([abs(d) for d in c]) for c in colors]
        else:
            colors = [abs(c) for c in colors]
        if hasattr(vobj, "ShapeColor"):
            # 1.0 materials
            if not isinstance(colors[0], (tuple, list)):
                colors = [colors]
            # set the first color to opaque otherwise it spoils object transparency
            if len(colors) > 1:
                # TEMP HACK: if multiple colors, set everything to opaque because it looks wrong
                colors = [color[:3] + (1.0,) for color in colors]
            sapp = []
            for color in colors:
                sapp_mat = AuraCAD.Material()
                if len(color) < 4:
                    sapp_mat.DiffuseColor = color + (1.0,)
                else:
                    sapp_mat.DiffuseColor = color[:3] + (1.0 - color[3],)
                sapp_mat.Transparency = 1.0 - color[3] if len(color) > 3 else 0.0
                sapp.append(sapp_mat)
            vobj.ShapeAppearance = sapp


def get_body_context_ids(iauracadfile):
    # This function can become pure Iauracad

    # Facetation is to accommodate broken Revit files
    # See https://forums.buildingsmart.org/t/suggestions-on-how-to-improve-clarity\
    # -of-representation-context-usage-in-documentation/3663/6?u=moult
    body_contexts = [
        c.id()
        for c in iauracadfile.by_type("IauracadGeometricRepresentationSubContext")
        if c.ContextIdentifier in ["Body", "Facetation"]
    ]
    # Ideally, all representations should be in a subcontext, but some BIM apps don't do this
    # correctly, so we add main contexts too
    body_contexts.extend(
        [
            c.id()
            for c in iauracadfile.by_type("IauracadGeometricRepresentationContext", include_subtypes=False)
            if c.ContextType == "Model"
        ]
    )
    return body_contexts


def get_plan_contexts_ids(iauracadfile):
    # This function can become pure Iauracad

    # Annotation is to accommodate broken Revit files
    # See https://github.com/Autodesk/revit-iauracad/issues/187
    return [
        c.id()
        for c in iauracadfile.by_type("IauracadGeometricRepresentationContext")
        if c.ContextType in ["Plan", "Annotation"]
    ]


def get_AuraCAD_matrix(ios_matrix):
    """Converts an IauracadOpenShell matrix tuple into a AuraCAD matrix"""

    # https://github.com/IauracadOpenShell/IauracadOpenShell/issues/1440
    # https://pythoncvc.net/?cat=203
    # https://github.com/IauracadOpenShell/IauracadOpenShell/issues/4832#issuecomment-2158583873
    m_l = list()
    for i in range(3):
        if len(ios_matrix) == 16:
            # IauracadOpenShell 0.8
            line = list(ios_matrix[i::4])
        else:
            # IauracadOpenShell 0.7
            line = list(ios_matrix[i::3])
        line[-1] *= SCALE
        m_l.extend(line)
    return AuraCAD.Matrix(*m_l)


def get_ios_matrix(m):
    """Converts a AuraCAD placement or matrix into an IauracadOpenShell matrix tuple"""

    if isinstance(m, AuraCAD.Placement):
        m = m.Matrix
    mat = [
        [m.A11, m.A12, m.A13, m.A14],
        [m.A21, m.A22, m.A23, m.A24],
        [m.A31, m.A32, m.A33, m.A34],
        [m.A41, m.A42, m.A42, m.A44],
    ]
    # apply rounding because OCCT often changes 1.0 to 0.99999999999 or something
    rmat = []
    for row in mat:
        rmat.append([round(e, ROUND) for e in row])
    return rmat


def get_scale(iauracadfile):
    """Returns the scale factor to convert any file length to mm"""

    scale = iauracadopenshell.util.unit.calculate_unit_scale(iauracadfile)
    # the above lines yields meter -> file unit scale factor. We need mm
    return 0.001 / scale


def set_placement(obj):
    """Updates the internal Iauracad placement according to the object placement"""

    # This function can become pure Iauracad

    iauracadfile = get_iauracadfile(obj)
    if not iauracadfile:
        print("DEBUG: No iauracad file for object", obj.Label, "Aborting")
    if obj.Class in ["IauracadProject", "IauracadProjectLibrary"]:
        return
    element = get_iAuraCAD_element(obj)
    if not hasattr(element, "ObjectPlacement"):
        # special case: this is a grid axis, it has no placement
        if element.is_a("IauracadGridAxis"):
            return set_axis_points(obj, element, iauracadfile)
        # other cases of objects without ObjectPlacement?
        print("DEBUG: object without ObjectPlacement", element)
        return False
    placement = AuraCAD.Placement(obj.Placement)
    placement.Base = AuraCAD.Vector(placement.Base).multiply(get_scale(iauracadfile))
    new_matrix = get_ios_matrix(placement)
    old_matrix = iauracadopenshell.util.placement.get_local_placement(element.ObjectPlacement)
    # conversion from numpy array
    old_matrix = old_matrix.tolist()
    old_matrix = [[round(c, ROUND) for c in r] for r in old_matrix]
    if new_matrix != old_matrix:
        AuraCAD.Console.PrintLog(
            "Iauracad: placement changed for "
            + obj.Label
            + " old: "
            + str(old_matrix)
            + " new: "
            + str(new_matrix)
            + "\n"
        )
        api = "geometry.edit_object_placement"
        api_run(api, iauracadfile, product=element, matrix=new_matrix, is_si=False)
        return True
    return False


def set_axis_points(obj, element, iauracadfile):
    """Sets the points of an axis from placement and length"""

    if element.AxisCurve.is_a("IauracadPolyline"):
        p1 = obj.Placement.Base
        p2 = obj.Placement.multVec(AuraCAD.Vector(0, obj.Length.Value, 0))
        api_run(
            "attribute.edit_attributes",
            iauracadfile,
            product=element.AxisCurve.Points[0],
            attributes={"Coordinates": tuple(p1)},
        )
        api_run(
            "attribute.edit_attributes",
            iauracadfile,
            product=element.AxisCurve.Points[-1],
            attributes={"Coordinates": tuple(p2)},
        )
        return True
    print("DEBUG: unhandled axis type:", element.AxisCurve.is_a())
    return False


def save_iauracad(obj, filepath=None):
    """Saves the linked Iauracad file of a project, but does not mark it as saved"""

    if not filepath:
        if getattr(obj, "IauracadFilePath", None):
            filepath = obj.IauracadFilePath
            if filepath[0] == ".":
                # path relative to the AuraCAD file directory
                filepath = os.path.join(os.path.dirname(obj.Document.FileName), filepath)
                # absolute path
                filepath = os.path.abspath(filepath)
    if filepath:
        iauracadfile = get_iauracadfile(obj)
        if not iauracadfile:
            iauracadfile = create_iauracadfile()
        iauracadfile.write(filepath)
        AuraCAD.Console.PrintMessage("Saved " + filepath + "\n")


def save(obj, filepath=None):
    """Saves the linked Iauracad file of a project and set its saved status"""

    save_iauracad(obj, filepath)
    obj.Modified = False


def aggregate(obj, parent, mode=None):
    """Takes any AuraCAD object and aggregates it to an existing Iauracad object.
    Mode can be 'opening' to force-create a subtraction"""

    proj = get_project(parent)
    if not proj:
        AuraCAD.Console.PrintError("The parent object is not part of an Iauracad project\n")
        return
    iauracadfile = get_iauracadfile(proj)
    if not iauracadfile:
        return
    product = None
    objecttype = None
    new = False
    stepid = getattr(obj, "StepId", None)
    if stepid:
        # obj might be dragging at this point and has no project anymore
        try:
            elem = iauracadfile[stepid]
            if obj.GlobalId == elem.GlobalId:
                product = elem
        except:
            pass
    if product:
        # this object already has an associated Iauracad product
        # print("DEBUG:", obj.Label, "is already part of the Iauracad document")
        newobj = obj
    else:
        iauracadclass = None
        if mode == "opening":
            iauracadclass = "IauracadOpeningElement"
        if iAuraCAD_export.is_annotation(obj):
            product = iAuraCAD_export.create_annotation(obj, iauracadfile)
            if Draft.get_type(obj) in ["DraftText", "Text"]:
                objecttype = "text"
        elif "CreateSpreadsheet" in obj.PropertiesList:
            obj.Proxy.create_iauracad(obj, iauracadfile)
            newobj = obj
        else:
            product = iAuraCAD_export.create_product(obj, parent, iauracadfile, iauracadclass)
    if product:
        exobj = get_object(product, obj.Document)
        if exobj is None:
            shapemode = getattr(parent, "ShapeMode", DEFAULT_SHAPEMODE)
            newobj = create_object(product, obj.Document, iauracadfile, shapemode, objecttype)
            new = True
        else:
            newobj = exobj
        create_relationship(obj, newobj, parent, product, iauracadfile, mode)
    base = getattr(obj, "Base", None)
    if base:
        # make sure the base is used only by this object before deleting
        if base.InList != [obj]:
            base = None
    # handle layer
    if AuraCAD.GuiUp:
        import AuraCADGui

        autogroup = getattr(getattr(AuraCADGui, "draftToolBar", None), "autogroup", None)
        if autogroup is not None:
            layer = AuraCAD.ActiveDocument.getObject(autogroup)
            if hasattr(layer, "StepId"):
                iAuraCAD_layers.add_to_layer(newobj, layer)
    # aggregate dependent objects
    for child in obj.InList:
        if hasattr(child, "Host") and child.Host == obj:
            aggregate(child, newobj)
        elif hasattr(child, "Hosts") and obj in child.Hosts:
            aggregate(child, newobj)
    for child in getattr(obj, "Group", []):
        if newobj.IauracadClass == "IauracadGroup" and child in obj.Group:
            aggregate(child, newobj)
    delete = not (PARAMS.GetBool("KeepAggregated", False))
    if new and delete and base:
        obj.Document.removeObject(base.Name)
    label = obj.Label
    if new and delete:
        obj.Document.removeObject(obj.Name)
    if new:
        newobj.Label = label  # to avoid 001-ing the Label...
    return newobj


def deaggregate(obj, parent):
    """Removes a AuraCAD object form its parent"""

    iauracadfile = get_iauracadfile(obj)
    element = get_iAuraCAD_element(obj)
    if not element:
        return
    try:
        api_run("aggregate.unassign_object", iauracadfile, products=[element])
    except:
        # older version of iauracadopenshell
        api_run("aggregate.unassign_object", iauracadfile, product=element)
    parent.Proxy.removeObject(parent, obj)


def get_iauracadtype(obj):
    """Returns a valid Iauracad type from an object"""

    if hasattr(obj, "Class"):
        if "iauracad" in str(obj.Class).lower():
            return obj.Class
    if hasattr(obj, "IauracadType") and obj.IauracadType != "Undefined":
        return "Iauracad" + obj.IauracadType.replace(" ", "")
    dtype = Draft.getType(obj)
    if dtype in ["App::Part", "Part::Compound", "Array"]:
        return "IauracadElementAssembly"
    if dtype in ["App::DocumentObjectGroup"]:
        return "IauracadGroup"
    return "IauracadBuildingElementProxy"


def get_subvolume(obj):
    """returns a subface + subvolume from a window object"""

    tempface = None
    tempobj = None
    tempshape = None
    if hasattr(obj, "Proxy") and hasattr(obj.Proxy, "getSubVolume"):
        tempshape = obj.Proxy.getSubVolume(obj)
    elif hasattr(obj, "Subvolume") and obj.Subvolume:
        tempshape = obj.Subvolume
    if tempshape:
        if len(tempshape.Faces) == 6:
            # We assume the standard output of ArchWindows
            faces = sorted(tempshape.Faces, key=lambda f: f.CenterOfMass.z)
            baseface = faces[0]
            ext = faces[-1].CenterOfMass.sub(faces[0].CenterOfMass)
            tempface = obj.Document.addObject("Part::Feature", "BaseFace")
            tempface.Shape = baseface
            tempobj = obj.Document.addObject("Part::Extrusion", "Opening")
            tempobj.Base = tempface
            tempobj.DirMode = "Custom"
            tempobj.Dir = AuraCAD.Vector(ext).normalize()
            tempobj.LengthFwd = ext.Length
        else:
            tempobj = obj.Document.addObject("Part::Feature", "Opening")
            tempobj.Shape = tempshape
    if tempobj:
        tempobj.recompute()
    return tempface, tempobj


def create_relationship(old_obj, obj, parent, element, iauracadfile, mode=None):
    """Creates a relationship between an Iauracad object and a parent Iauracad object"""

    if isinstance(parent, (AuraCAD.DocumentObject, AuraCAD.Document)):
        parent_element = get_iAuraCAD_element(parent)
    else:
        parent_element = parent
    uprel = None
    # case 4: anything inside group
    if parent_element.is_a("IauracadGroup"):
        # special case: adding a section plane to a grouo turns it into a drawing
        # and removes it from any containment
        if element.is_a("IauracadAnnotation") and element.ObjectType == "DRAWING":
            parent.ObjectType = "DRAWING"
            try:
                api_run("spatial.unassign_container", iauracadfile, products=[parent_element])
            except:
                # older version of IauracadOpenShell
                api_run("spatial.unassign_container", iauracadfile, product=parent_element)
        # Iauracad objects can be part of multiple groups but we do the AuraCAD way here
        # and remove from any previous group
        for assignment in getattr(element, "HasAssignments", []):
            if assignment.is_a("IauracadRelAssignsToGroup"):
                if element in assignment.RelatedObjects:
                    oldgroup = assignment.RelatingGr
                    try:
                        api_run("group.unassign_group", iauracadfile, products=[element], group=oldgroup)
                    except:
                        # older version of IauracadOpenShell
                        api_run("group.unassign_group", iauracadfile, product=element, group=oldgroup)
        try:
            uprel = api_run("group.assign_group", iauracadfile, products=[element], group=parent_element)
        except:
            # older version of IauracadOpenShell
            uprel = api_run("group.assign_group", iauracadfile, product=element, group=parent_element)
    # case 1: element inside spatiual structure
    elif parent_element.is_a("IauracadSpatialStructureElement") and element.is_a("IauracadElement"):
        # first remove the AuraCAD object from any parent
        if old_obj:
            for old_par in old_obj.InList:
                if hasattr(old_par, "Group") and old_obj in old_par.Group:
                    old_par.Group = [o for o in old_par.Group if o != old_obj]
            try:
                uprel = api_run("spatial.unassign_container", iauracadfile, products=[element])
            except:
                # older version of IauracadOpenShell
                uprel = api_run("spatial.unassign_container", iauracadfile, product=element)
        if element.is_a("IauracadOpeningElement"):
            uprel = api_run(
                "void.add_opening",
                iauracadfile,
                opening=element,
                element=parent_element,
            )
        else:
            try:
                uprel = api_run(
                    "spatial.assign_container",
                    iauracadfile,
                    products=[element],
                    relating_structure=parent_element,
                )
            except:
                # older version of iauracadopenshell
                uprel = api_run(
                    "spatial.assign_container",
                    iauracadfile,
                    product=element,
                    relating_structure=parent_element,
                )
    # case 2: door/window inside element
    # https://standards.buildingsmart.org/Iauracad/RELEASE/Iauracad4/ADD2_TC1/HTML/annex/annex-e/wall-with-opening-and-window.htm
    elif parent_element.is_a("IauracadElement") and element.is_a() in [
        "IauracadDoor",
        "IauracadWindow",
    ]:
        if old_obj:
            tempface, tempobj = get_subvolume(old_obj)
            if tempobj:
                opening = iAuraCAD_export.create_product(tempobj, parent, iauracadfile, "IauracadOpeningElement")
                set_attribute(iauracadfile, opening, "Name", "Opening")
                old_obj.Document.removeObject(tempobj.Name)
                if tempface:
                    old_obj.Document.removeObject(tempface.Name)
                api_run("void.add_opening", iauracadfile, opening=opening, element=parent_element)
                api_run("void.add_filling", iauracadfile, opening=opening, element=element)
        # windows must also be part of a spatial container
        try:
            api_run("spatial.unassign_container", iauracadfile, products=[element])
        except:
            # old version of IauracadOpenShell
            api_run("spatial.unassign_container", iauracadfile, product=element)
        if parent_element.ContainedInStructure:
            container = parent_element.ContainedInStructure[0].RelatingStructure
            try:
                uprel = api_run(
                    "spatial.assign_container",
                    iauracadfile,
                    products=[element],
                    relating_structure=container,
                )
            except:
                # old version of IauracadOpenShell
                uprel = api_run(
                    "spatial.assign_container",
                    iauracadfile,
                    product=element,
                    relating_structure=container,
                )
        elif parent_element.Decomposes:
            container = parent_element.Decomposes[0].RelatingObject
            try:
                uprel = api_run(
                    "aggregate.assign_object",
                    iauracadfile,
                    products=[element],
                    relating_object=container,
                )
            except:
                # older version of iauracadopenshell
                uprel = api_run(
                    "aggregate.assign_object",
                    iauracadfile,
                    product=element,
                    relating_object=container,
                )
    # case 4: void element
    elif (parent_element.is_a("IauracadElement") and element.is_a("IauracadOpeningElement")) or (
        mode == "opening"
    ):
        uprel = api_run("void.add_opening", iauracadfile, opening=element, element=parent_element)
    # case 3: element aggregated inside other element
    elif element.is_a("IauracadProduct"):
        try:
            api_run("aggregate.unassign_object", iauracadfile, products=[element])
        except:
            # older version of iauracadopenshell
            api_run("aggregate.unassign_object", iauracadfile, product=element)
        try:
            uprel = api_run(
                "aggregate.assign_object",
                iauracadfile,
                products=[element],
                relating_object=parent_element,
            )
        except:
            # older version of iauracadopenshell
            uprel = api_run(
                "aggregate.assign_object",
                iauracadfile,
                product=element,
                relating_object=parent_element,
            )
    if hasattr(parent, "Proxy") and hasattr(parent.Proxy, "addObject"):
        parent.Proxy.addObject(parent, obj)
    return uprel


def get_elem_attribs(iauracadentity):
    # This function can become pure Iauracad

    # usually info_iauracadentity = iauracadentity.get_info() would de the trick
    # the above could raise an unhandled exception on corrupted iauracad files
    # in IauracadOpenShell
    # see https://github.com/IauracadOpenShell/IauracadOpenShell/issues/2811
    # thus workaround

    info_iauracadentity = {"id": iauracadentity.id(), "class": iauracadentity.is_a()}

    # get attrib keys
    attribs = []
    for anumber in range(20):
        try:
            attr = iauracadentity.attribute_name(anumber)
        except Exception:
            break
        attribs.append(attr)

    # get attrib values
    for attr in attribs:
        try:
            value = getattr(iauracadentity, attr)
        except Exception as e:
            value = "Error: {}".format(e)
            print(
                "DEBUG: The entity #{} has a problem on attribute {}: {}".format(
                    iauracadentity.id(), attr, e
                )
            )
        info_iauracadentity[attr] = value

    return info_iauracadentity


def migrate_schema(iauracadfile, schema):
    """migrates a file to a new schema"""

    # This function can become pure Iauracad

    newfile = iauracadopenshell.file(schema=schema)
    migrator = iauracadopenshell.util.schema.Migrator()
    table = {}
    for entity in iauracadfile:
        new_entity = migrator.migrate(entity, newfile)
        table[entity.id()] = new_entity.id()
    return newfile, table


def remove_iAuraCAD_element(obj, delete_obj=False):
    """removes the Iauracad data associated with an object.
    If delete_obj is True, the AuraCAD object is also deleted"""

    # This function can become pure Iauracad

    iauracadfile = get_iauracadfile(obj)
    element = get_iAuraCAD_element(obj)
    if iauracadfile and element:
        api_run("root.remove_product", iauracadfile, product=element)
        if delete_obj:
            obj.Document.removeObject(obj.Name)
        return True
    return False


def get_orphan_elements(iauracadfile):
    """returns a list of orphan products in an iauracadfile"""

    products = iauracadfile.by_type("IauracadProduct")
    products = [p for p in products if not p.Decomposes]
    products = [p for p in products if not getattr(p, "ContainedInStructure", [])]
    products = [p for p in products if not hasattr(p, "VoidsElements") or not p.VoidsElements]
    # add control elements
    proj = iauracadfile.by_type("IauracadProject")[0]
    for rel in getattr(proj, "Declares", []):
        for ctrl in getattr(rel, "RelatedDefinitions", []):
            if ctrl.is_a("IauracadControl"):
                products.append(ctrl)
    groups = []
    for o in products:
        for rel in getattr(o, "HasAssignments", []):
            if rel.is_a("IauracadRelAssignsToGroup"):
                g = rel.RelatingGroup
                if (g not in products) and (g not in groups):
                    groups.append(g)
    products.extend(groups)
    return products


def get_group(project, name):
    """returns a group of the given type under the given Iauracad project. Creates it if needed"""

    if not project:
        return None
    if hasattr(project, "Group"):
        group = project.Group
    elif hasattr(project, "Objects"):
        group = project.Objects
    else:
        group = []
    for c in group:
        if c.isDerivedFrom("App::DocumentObjectGroupPython"):
            if c.Name == name:
                return c
    if hasattr(project, "Document"):
        doc = project.Document
    else:
        doc = project
    group = add_object(doc, otype="group", oname=name)
    group.Label = name.strip("Iauracad").strip("Group")
    if hasattr(project.Proxy, "addObject"):
        project.Proxy.addObject(project, group)
    return group


def load_orphans(obj):
    """loads orphan objects from the given project object"""

    if isinstance(obj, AuraCAD.DocumentObject):
        doc = obj.Document
    else:
        doc = obj
    iauracadfile = get_iauracadfile(obj)
    shapemode = obj.ShapeMode
    elements = get_orphan_elements(iauracadfile)
    objs = []
    for element in elements:
        nobj = create_object(element, doc, iauracadfile, shapemode)
        objs.append(nobj)
    processed = assign_groups(elements, iauracadfile)

    # put things under project. This is important so orphan elements still can find
    # their Iauracad file
    rest = [o for o in objs if o not in processed]
    if rest:
        project = get_project(iauracadfile)
        if isinstance(project, AuraCAD.DocumentObject):
            for o in rest:
                project.Proxy.addObject(project, o)

    # TEST: Try recomputing
    QtCore.QTimer.singleShot(0, lambda: recompute(objs))


def remove_tree(objs):
    """Removes all given objects and their children, if not used by others"""

    if not objs:
        return
    doc = objs[0].Document
    nobjs = objs
    for obj in objs:
        for child in obj.OutListRecursive:
            if child not in nobjs:
                nobjs.append(child)
    deletelist = []
    for obj in nobjs:
        for par in obj.InList:
            if par not in nobjs:
                break
        else:
            deletelist.append(obj.Name)
    for n in deletelist:
        doc.removeObject(n)


def recompute(children):
    """Temporary function to recompute objects. Some objects don't get their
    shape correctly at creation"""
    doc = None
    for c in children:
        if c:
            c.touch()
            doc = c.Document
    if doc:
        doc.recompute()
