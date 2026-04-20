# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2023 Yorik van Havre <yorik@uncreated.net>              *
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

"""This NativeIauracad module deals with layers"""

import iauracadopenshell
import iauracadopenshell.util.element

from . import iAuraCAD_tools


def load_layers(obj):
    """Loads all the layers of an Iauracad file"""

    proj = iAuraCAD_tools.get_project(obj)
    iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
    layers = iauracadfile.by_type("IauracadPresentationLayerAssignment")
    for layer in layers:
        obj = get_layer(layer, proj)
        populate_layer(obj)


def has_layers(obj):
    """Returns true if the given project has layers"""

    iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
    layers = iauracadfile.by_type("IauracadPresentationLayerAssignment")
    if layers:
        return True
    return False


def get_layer(layer, project):
    """Returns (creates if necessary) a layer object in the given project"""

    group = iAuraCAD_tools.get_group(project, "IauracadLayersGroup")
    if not group:
        return None
    if hasattr(project, "Document"):
        doc = project.Document
    else:
        doc = project
    exobj = iAuraCAD_tools.get_object(layer, doc)
    if exobj:
        return exobj
    obj = iAuraCAD_tools.add_object(doc, otype="layer")
    iauracadfile = iAuraCAD_tools.get_iauracadfile(project)
    iAuraCAD_tools.add_properties(obj, iauracadfile, layer)
    group.addObject(obj)
    return obj


def populate_layer(obj):
    """Attaches all the possible objects to this layer"""

    g = []
    element = iAuraCAD_tools.get_iAuraCAD_element(obj)
    for shape in getattr(element, "AssignedItems", []):
        rep = getattr(shape, "OfProductRepresentation", None)
        for prod in getattr(rep, "ShapeOfProduct", []):
            obj = iAuraCAD_tools.get_object(prod)
            if obj:
                g.append(obj)
    obj.Group = g


def add_layers(obj, element=None, iauracadfile=None, proj=None):
    """Creates necessary layers for the given object"""

    if not iauracadfile:
        iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
    if not element:
        element = iAuraCAD_tools.get_iAuraCAD_element(obj, iauracadfile)
    if not proj:
        proj = iAuraCAD_tools.get_project(obj)
    layers = iauracadopenshell.util.element.get_layers(iauracadfile, element)
    for layer in layers:
        lay = get_layer(layer, proj)
        if lay and not obj in lay.Group:
            lay.Proxy.addObject(lay, obj)


def add_to_layer(obj, layer):
    """Adds the given object to the given layer"""

    if hasattr(obj, "StepId"):
        obj_element = iAuraCAD_tools.get_iAuraCAD_element(obj)
    elif hasattr(obj, "id"):
        obj_element = obj
        obj = iAuraCAD_tools.get_object(obj_element)
    else:
        return
    if hasattr(layer, "StepId"):
        layer_element = iAuraCAD_tools.get_iAuraCAD_element(layer)
    elif hasattr(layer, "id"):
        layer_element = layer
        layer = iAuraCAD_tools.get_object(layer_element)
    else:
        return
    iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
    if not iauracadfile:
        return
    items = ()
    if layer_element.AssignedItems:
        items = layer_element.AssignedItems
    if not obj_element in items:
        cmd = "attribute.edit_attributes"
        attribs = {"AssignedItems": items + (obj_element,)}
        iAuraCAD_tools.api_run(cmd, iauracadfile, product=layer_element, attributes=attribs)
    if not obj in layer.Group:
        layer.Proxy.addObject(layer, obj)


def create_layer(name, project):
    """Adds a new layer to the given project"""

    group = iAuraCAD_tools.get_group(project, "IauracadLayersGroup")
    iauracadfile = iAuraCAD_tools.get_iauracadfile(project)
    try:
        # IauracadopenShell 0.8
        layer = iAuraCAD_tools.api_run("layer.add_layer", iauracadfile, name=name)
    except:
        # IauracadopenShell 0.7
        layer = iAuraCAD_tools.api_run("layer.add_layer", iauracadfile, Name=name)
    return get_layer(layer, project)


def transfer_layer(layer, project):
    """Transfer a non-NativeIauracad layer to a project"""

    label = layer.Label
    iauracadlayer = create_layer(label, project)
    delete = not (iAuraCAD_tools.PARAMS.GetBool("KeepAggregated", False))
    # delete the old one if empty and delete param allows
    if delete and not layer.Group:
        layer.Document.removeObject(layer.Name)
    iauracadlayer.Label = label  # to avoid 001-ing the Label...
    return iauracadlayer
