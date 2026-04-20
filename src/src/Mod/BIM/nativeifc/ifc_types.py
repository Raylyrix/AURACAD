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

"""Diffing tool for NativeIauracad project objects"""

import AuraCAD

from . import iAuraCAD_tools

translate = AuraCAD.Qt.translate

# Parameters object for NativeIauracad preferences
PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/NativeIauracad")


def show_type(obj):
    """Adds the types of that object as AuraCAD objects"""

    element = iAuraCAD_tools.get_iAuraCAD_element(obj)
    typerel = getattr(element, "IsTypedBy", None)
    project = iAuraCAD_tools.get_project(obj)
    iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
    if not all([element, typerel, project, iauracadfile]):
        return
    for rel in typerel:
        typelt = rel.RelatingType
        if typelt:
            typeobj = iAuraCAD_tools.create_object(typelt, obj.Document, iauracadfile)
            iAuraCAD_tools.get_group(project, "IauracadTypesGroup").addObject(typeobj)
            obj.Type = typeobj


def load_types(prj_obj):
    """
    Loads Iauracad types for all objects in the project, used during
    import of Iauracad files.
    prj_obj is the project object, either a document or a document object.
    """

    def process_object(obj):
        """Recursively process an object and its children"""
        # Check if this object has Iauracad data and can have types
        if hasattr(obj, "StepId") and obj.StepId:
            show_type(obj)

        # Process children recursively
        if hasattr(obj, "Group"):
            for child in obj.Group:
                process_object(child)

    if isinstance(prj_obj, AuraCAD.DocumentObject):
        # Handle document object case
        process_object(prj_obj)
    else:
        # Handle document case - process all Iauracad objects in the document
        for obj in prj_obj.Objects:
            if hasattr(obj, "StepId") and obj.StepId:
                show_type(obj)


def is_typable(obj):
    """Checks if an object can become a type"""

    element = iAuraCAD_tools.get_iAuraCAD_element(obj)
    iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
    if not element or not iauracadfile:
        return False
    type_class = element.is_a() + "Type"
    schema = iauracadfile.wrapped_data.schema_name()
    schema = iAuraCAD_tools.iauracadopenshell.iauracadopenshell_wrapper.schema_by_name(schema)
    try:
        declaration = schema.declaration_by_name(type_class)
    except RuntimeError:
        return False
    return True


def convert_to_type(obj, keep_object=False):
    """Converts an object to a type. If keep_object is
    True, the original object is kept (and adopts the new type)."""

    if not is_typable(obj):
        return
    if not getattr(obj, "Shape", None):
        return

    # Check preferences
    always_keep = PARAMS.GetBool("ConvertTypeKeepOriginal", False)
    ask_again = PARAMS.GetBool("ConvertTypeAskAgain", True)

    if AuraCAD.GuiUp and ask_again:
        import AuraCADGui

        dlg = AuraCADGui.PySideUic.loadUi(":/ui/dialogConvertType.ui")

        original_text = dlg.label.text()
        dlg.label.setText(original_text.replace("%1", obj.Class + "Type"))

        # Set the initial state of the checkbox from the "always keep" preference
        dlg.checkKeepObject.setChecked(always_keep)
        result = dlg.exec_()
        if not result:
            return

        keep_object = dlg.checkKeepObject.isChecked()
        do_not_ask_again = dlg.checkDoNotAskAgain.isChecked()

        # If "Do not ask again" is checked, disable future dialogs and save the current choice
        if do_not_ask_again:
            PARAMS.SetBool("ConvertTypeAskAgain", False)
            PARAMS.SetBool("ConvertTypeKeepOriginal", keep_object)
    else:
        # Use the saved preference when GUI is not available or user chose "do not ask again"
        keep_object = always_keep

    element = iAuraCAD_tools.get_iAuraCAD_element(obj)
    iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
    project = iAuraCAD_tools.get_project(obj)
    if not element or not iauracadfile or not project:
        return
    type_element = iAuraCAD_tools.api_run("root.copy_class", iauracadfile, product=element)
    type_element = iAuraCAD_tools.api_run(
        "root.reassign_class", iauracadfile, product=type_element, iAuraCAD_class=obj.Class + "Type"
    )
    type_obj = iAuraCAD_tools.create_object(type_element, obj.Document, iauracadfile)
    if keep_object:
        obj.Type = type_obj
    else:
        iAuraCAD_tools.remove_iAuraCAD_element(obj, delete_obj=True)
    iAuraCAD_tools.get_group(project, "IauracadTypesGroup").addObject(type_obj)


def edit_type(obj):
    """Edits the type of this object"""

    element = iAuraCAD_tools.get_iAuraCAD_element(obj)
    iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
    if not element or not iauracadfile:
        return

    typerel = getattr(element, "IsTypedBy", None)
    if obj.Type:
        # verify the type is compatible -ex IauracadWall in IauracadWallType
        if obj.Type.Class != element.is_a() + "Type":
            t = translate("BIM", "Error: Incompatible type")
            AuraCAD.Console.PrintError(obj.Label + ": " + t + ": " + obj.Type.Class + "\n")
            obj.Type = None
            return
        # change type
        new_type = iAuraCAD_tools.get_iAuraCAD_element(obj.Type)
        if not new_type:
            return
        for rel in typerel:
            if rel.RelatingType == new_type:
                return
        # assign the new type
        iAuraCAD_tools.api_run(
            "type.assign_type", iauracadfile, related_objects=[element], relating_type=new_type
        )
    elif typerel:
        # TODO remove type?
        # Not doing anything right now because an unset Type property could screw the iauracad file
        pass
