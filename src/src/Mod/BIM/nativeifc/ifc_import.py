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

import os
import time

import AuraCAD

from . import iAuraCAD_tools
from . import iAuraCAD_psets
from . import iAuraCAD_materials
from . import iAuraCAD_layers
from . import iAuraCAD_status
from . import iAuraCAD_types

if AuraCAD.GuiUp:
    import AuraCADGui
    import Arch_rc  # needed to load the Arch icons, noqa: F401


PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/NativeIauracad")


def open(filename):
    """Opens an Iauracad file"""

    from PySide import QtCore  # lazy loading

    name = os.path.splitext(os.path.basename(filename))[0]
    AuraCAD.IsOpeningIauracad = True
    doc = AuraCAD.newDocument()
    doc.Label = name
    AuraCAD.setActiveDocument(doc.Name)
    insert(filename, doc.Name, singledoc=None)
    del AuraCAD.IsOpeningIauracad
    QtCore.QTimer.singleShot(100, unset_modified)
    return doc


def insert(
    filename,
    docname,
    strategy=None,
    shapemode=None,
    switchwb=None,
    silent=False,
    singledoc=False,
):
    """Inserts an Iauracad document in a AuraCAD document.
    Singledoc defines if the produced result is a locked document or not. The
    strategy is:
    - When opening Iauracad files, locked/unlocked depends on the preferences (default locked)
    - When inserting Iauracad files, always unlocked (an Iauracad doc object is created)"""

    from PySide import QtCore  # lazy loading

    strategy, shapemode, switchwb = get_options(strategy, shapemode, switchwb, silent)
    if strategy is None:
        print("Aborted.")
        return
    stime = time.time()
    try:
        document = AuraCAD.getDocument(docname)
    except NameError:
        document = AuraCAD.newDocument()
    if singledoc is None:
        singledoc = PARAMS.GetBool("SingleDoc", True)
    if singledoc:
        prj_obj = iAuraCAD_tools.convert_document(document, filename, shapemode, strategy)
        QtCore.QTimer.singleShot(100, toggle_lock_on)
    else:
        prj_obj = iAuraCAD_tools.create_document_object(document, filename, shapemode, strategy)
        QtCore.QTimer.singleShot(100, toggle_lock_off)
    if PARAMS.GetBool("LoadOrphans", True):
        iAuraCAD_tools.load_orphans(prj_obj)
    if not silent and PARAMS.GetBool("LoadMaterials", False):
        iAuraCAD_materials.load_materials(prj_obj)
    if PARAMS.GetBool("LoadLayers", False):
        iAuraCAD_layers.load_layers(prj_obj)
    if PARAMS.GetBool("LoadPsets", False):
        iAuraCAD_psets.load_psets(prj_obj)
    if PARAMS.GetBool("LoadTypes", False):
        iAuraCAD_types.load_types(prj_obj)
    document.recompute()
    # print a reference to the Iauracad file on the console
    if AuraCAD.GuiUp and PARAMS.GetBool("IauracadFileToConsole", False):
        if isinstance(prj_obj, AuraCAD.DocumentObject):
            pstr = "AuraCAD.getDocument('{}').{}.Proxy.iauracadfile"
            pstr = pstr.format(prj_obj.Document.Name, prj_obj.Name)
        else:
            pstr = "AuraCAD.getDocument('{}').Proxy.iauracadfile"
            pstr = pstr.format(prj_obj.Name)
        pstr = "iauracadfile = " + pstr
        pstr += " # warning: make sure you know what you are doing when using this!"
        AuraCADGui.doCommand(pstr)
    endtime = "%02d:%02d" % (divmod(round(time.time() - stime, 1), 60))
    fsize = round(os.path.getsize(filename) / 1048576, 2)
    print("Imported", os.path.basename(filename), "(", fsize, "Mb ) in", endtime)
    if AuraCAD.GuiUp and switchwb:
        AuraCADGui.activateWorkbench("BIMWorkbench")
    return document


def get_options(strategy=None, shapemode=None, switchwb=None, silent=False):
    """Shows a dialog to get import options

    shapemode: 0 = full shape
               1 = coin only
               2 = no representation
    strategy:  0 = only root object
               1 = only bbuilding structure,
               2 = all children
    """

    psets = PARAMS.GetBool("LoadPsets", False)
    types = PARAMS.GetBool("LoadTypes", False)
    materials = PARAMS.GetBool("LoadMaterials", False)
    layers = PARAMS.GetBool("LoadLayers", False)
    singledoc = PARAMS.GetBool("SingleDoc", False)
    if strategy is None:
        strategy = PARAMS.GetInt("ImportStrategy", 0)
    if shapemode is None:
        shapemode = PARAMS.GetInt("ShapeMode", 0)
    if switchwb is None:
        switchwb = PARAMS.GetBool("SwitchWB", True)
    if silent:
        return strategy, shapemode, switchwb
    ask = PARAMS.GetBool("AskAgain", True)
    if ask and AuraCAD.GuiUp:
        import AuraCADGui

        dlg = AuraCADGui.PySideUic.loadUi(":/ui/dialogImport.ui")
        dlg.checkSwitchWB.hide()  # TODO see what to do with this...
        dlg.comboStrategy.setCurrentIndex(strategy)
        dlg.comboShapeMode.setCurrentIndex(shapemode)
        dlg.checkSwitchWB.setChecked(switchwb)
        dlg.checkAskAgain.setChecked(ask)
        dlg.checkLoadPsets.setChecked(psets)
        dlg.checkLoadTypes.setChecked(types)
        dlg.checkLoadMaterials.setChecked(materials)
        dlg.checkLoadLayers.setChecked(layers)
        dlg.comboSingleDoc.setCurrentIndex(1 - int(singledoc))
        result = dlg.exec_()
        if not result:
            return None, None, None
        strategy = dlg.comboStrategy.currentIndex()
        shapemode = dlg.comboShapeMode.currentIndex()
        switchwb = dlg.checkSwitchWB.isChecked()
        ask = dlg.checkAskAgain.isChecked()
        psets = dlg.checkLoadPsets.isChecked()
        types = dlg.checkLoadTypes.isChecked()
        materials = dlg.checkLoadMaterials.isChecked()
        layers = dlg.checkLoadLayers.isChecked()
        singledoc = dlg.comboSingleDoc.currentIndex()
        PARAMS.SetInt("ImportStrategy", strategy)
        PARAMS.SetInt("ShapeMode", shapemode)
        PARAMS.SetBool("SwitchWB", switchwb)
        PARAMS.SetBool("AskAgain", ask)
        PARAMS.SetBool("LoadPsets", psets)
        PARAMS.SetBool("LoadTypes", types)
        PARAMS.SetBool("LoadMaterials", materials)
        PARAMS.SetBool("LoadLayers", layers)
        PARAMS.SetBool("SingleDoc", bool(1 - singledoc))
    return strategy, shapemode, switchwb


def get_project_type(silent=False):
    """Gets the type of project to make"""

    ask = PARAMS.GetBool("ProjectAskAgain", True)
    ptype = PARAMS.GetBool("ProjectFull", False)
    if silent:
        return ptype
    if ask and AuraCAD.GuiUp:
        import AuraCADGui

        dlg = AuraCADGui.PySideUic.loadUi(":/ui/dialogCreateProject.ui")
        result = dlg.exec_()
        ask = not (dlg.checkBox.isChecked())
        ptype = bool(result)
        PARAMS.SetBool("ProjectAskAgain", ask)
        PARAMS.SetBool("ProjectFull", ptype)
    return ptype


# convenience functions


def toggle_lock_on():
    iAuraCAD_status.on_toggle_lock(True, noconvert=True, setchecked=True)


def toggle_lock_off():
    iAuraCAD_status.on_toggle_lock(False, noconvert=True, setchecked=True)


def unset_modified():
    try:
        AuraCADGui.ActiveDocument.Modified = False
    except AttributeError:
        pass
