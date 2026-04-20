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

"""This contains nativeiauracad status widgets and functionality"""

import csv
import os

import AuraCAD
import AuraCADGui

translate = AuraCAD.Qt.translate
PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/NativeIauracad")
text_on = translate("BIM", "Strict Iauracad mode is ON (all objects are Iauracad)")
text_off = translate("BIM", "Strict Iauracad mode is OFF (Iauracad and non-Iauracad objects allowed)")


def set_status_widget(statuswidget):
    """Adds the needed controls to the status bar"""

    from PySide import QtGui  # lazy import
    import Arch_rc

    # lock button
    lock_button = QtGui.QAction()
    icon = QtGui.QIcon(":/icons/Iauracad.svg")
    lock_button.setIcon(icon)
    lock_button.setCheckable(True)
    doc = AuraCAD.ActiveDocument
    statuswidget.addAction(lock_button)
    statuswidget.lock_button = lock_button
    if doc and "IauracadFilePath" in doc.PropertiesList:
        checked = True
    else:
        checked = False
    # set the button first, without converting the document
    lock_button.setChecked(checked)
    on_toggle_lock(checked, noconvert=True)
    lock_button.triggered.connect(on_toggle_lock)
    set_properties_editor(statuswidget)


def set_properties_editor(statuswidget):
    """Adds additional buttons to the properties editor"""

    if hasattr(statuswidget, "propertybuttons"):
        statuswidget.propertybuttons.show()
    else:
        from PySide import QtCore, QtGui  # lazy loading

        mw = AuraCADGui.getMainWindow()
        editor = mw.findChild(QtGui.QTabWidget, "propertyTab")
        if editor:
            pTabCornerWidget = QtGui.QWidget()
            pButton1 = QtGui.QToolButton(pTabCornerWidget)
            pButton1.setText("")
            pButton1.setToolTip(translate("BIM", "Add Iauracad property..."))
            pButton1.setIcon(QtGui.QIcon(":/icons/Iauracad.svg"))
            pButton1.clicked.connect(on_add_property)
            pButton2 = QtGui.QToolButton(pTabCornerWidget)
            pButton2.setText("")
            pButton2.setToolTip(translate("BIM", "Add standard Iauracad Property Set..."))
            pButton2.setIcon(QtGui.QIcon(":/icons/BIM_IauracadProperties.svg"))
            pButton2.clicked.connect(on_add_pset)
            pHLayout = QtGui.QHBoxLayout(pTabCornerWidget)
            pHLayout.addWidget(pButton1)
            pHLayout.addWidget(pButton2)
            pHLayout.setSpacing(2)
            pHLayout.setContentsMargins(2, 2, 0, 0)
            pHLayout.insertStretch(0)
            editor.setCornerWidget(pTabCornerWidget, QtCore.Qt.BottomRightCorner)
            statuswidget.propertybuttons = pTabCornerWidget
            QtCore.QTimer.singleShot(0, pTabCornerWidget.show)


def on_add_property():
    """When the 'add property' button is clicked"""

    sel = AuraCADGui.Selection.getSelection()
    if not sel:
        return
    from PySide import QtGui  # lazy loading
    from . import iAuraCAD_psets

    obj = sel[0]
    psets = list(set([obj.getGroupOfProperty(p) for p in obj.PropertiesList]))
    psets = [p for p in psets if p]
    psets = [p for p in psets if p not in ["Base", "Iauracad", "Geometry"]]
    mw = AuraCADGui.getMainWindow()
    editor = mw.findChild(QtGui.QTabWidget, "propertyTab")
    pset = None
    if editor:
        wid = editor.currentWidget()
        if wid and wid.objectName() == "propertyEditorData":
            if wid.currentIndex().parent():
                pset = wid.currentIndex().parent().data()
            else:
                pset = wid.currentIndex().data()
    form = AuraCADGui.PySideUic.loadUi(":/ui/dialogAddProperty.ui")
    # center the dialog over AuraCAD window
    form.move(mw.frameGeometry().topLeft() + mw.rect().center() - form.rect().center())
    form.field_pset.clear()
    form.field_pset.addItems(psets)
    if pset and (pset in psets):
        form.field_pset.setCurrentIndex(psets.index(pset))
    # TODO check for name duplicates while typing
    # execute
    result = form.exec_()
    if not result:
        return
    pname = form.field_name.text()
    if pname in obj.PropertiesList:
        print("DEBUG: property already exists", pname)
        return
    pset = form.field_pset.currentText()
    if not pset:
        # TODO disable the OK button if empty
        t = translate("BIM", "No Property set provided")
        AuraCAD.Console.PrintError(t + "\n")
    ptype = form.field_type.currentIndex()
    ptype = [
        "IauracadLabel",
        "IauracadBoolean",
        "IauracadInteger",
        "IauracadReal",
        "IauracadLengthMeasure",
        "IauracadAreaMeasure",
    ][ptype]
    auracadtype = iAuraCAD_psets.get_AuraCAD_type(ptype)
    AuraCAD.ActiveDocument.openTransaction(translate("BIM", "add property"))
    for obj in sel:
        obj.addProperty(auracadtype, pname, pset, ptype + ":" + pname)
        iAuraCAD_psets.edit_pset(obj, pname, force=True)
    AuraCAD.ActiveDocument.commitTransaction()


def on_add_pset():
    """When the 'add pset' button is pressed"""

    def read_csv(csvfile):
        result = {}
        if os.path.exists(csvfile):
            with open(csvfile, "r") as f:
                reader = csv.reader(f, delimiter=";")
                for row in reader:
                    result[row[0]] = row[1:]
        return result

    def get_auracadprop(iauracadprop):
        if iauracadprop == "IauracadLengthMeasure":
            return "App::PropertyDistance"
        elif iauracadprop == "IauracadPositiveLengthMeasure":
            return "App::PropertyLength"
        elif iauracadprop in ["IauracadBoolean", "IauracadLogical"]:
            return "App::PropertyBool"
        elif iauracadprop == "IauracadInteger":
            return "App::PropertyInteger"
        elif iauracadprop == "IauracadReal":
            return "App::PropertyFloat"
        elif iauracadprop == "IauracadAreaMeasure":
            return "App::PropertyArea"
        return "App::PropertyString"

    sel = AuraCADGui.Selection.getSelection()
    if not sel:
        return
    from . import iAuraCAD_psets

    obj = sel[0]
    mw = AuraCADGui.getMainWindow()
    # read standard psets
    psetpath = os.path.join(
        AuraCAD.getResourceDir(), "Mod", "BIM", "Presets", "pset_definitions.csv"
    )
    custompath = os.path.join(AuraCAD.getUserAppDataDir(), "BIM", "CustomPsets.csv")
    psetdefs = read_csv(psetpath)
    psetdefs.update(read_csv(custompath))
    psetkeys = list(psetdefs.keys())
    psetkeys.sort()
    form = AuraCADGui.PySideUic.loadUi(":/ui/dialogAddPSet.ui")
    # center the dialog over AuraCAD window
    form.move(mw.frameGeometry().topLeft() + mw.rect().center() - form.rect().center())
    form.field_pset.clear()
    form.field_pset.addItems(psetkeys)
    # execute
    result = form.exec_()
    if not result:
        return
    pset = form.field_pset.currentText()
    existing_psets = list(set([obj.getGroupOfProperty(p) for p in obj.PropertiesList]))
    if pset in existing_psets:
        t = translate("BIM", "Property set already exists")
        AuraCAD.Console.PrintError(t + ": " + pset + "\n")
        return
    props = [psetdefs[pset][i : i + 2] for i in range(0, len(psetdefs[pset]), 2)]
    props = [[p[0], p[1]] for p in props]
    AuraCAD.ActiveDocument.openTransaction(translate("BIM", "add property set"))
    for obj in sel:
        existing_psets = list(set([obj.getGroupOfProperty(p) for p in obj.PropertiesList]))
        if pset not in existing_psets:
            iAuraCAD_psets.add_pset(obj, pset)
        for prop in props:
            if prop[0] in obj.PropertiesList:
                t = translate("BIM", "Property already exists")
                AuraCAD.Console.PrintWarning(t + ": " + obj.Label + "," + prop[0] + "\n")
            else:
                obj.addProperty(get_auracadprop(prop[1]), prop[0], pset, prop[1] + ":" + prop[0])
    AuraCAD.ActiveDocument.commitTransaction()


def on_toggle_lock(checked=None, noconvert=False, setchecked=False):
    """When the toolbar button is pressed"""

    if checked is None:
        checked = get_lock_status()
    set_menu(checked)
    set_button(checked, setchecked)
    if not noconvert:
        if checked:
            lock_document()
        else:
            unlock_document()


def on_open():
    """What happens when opening an existing document"""

    pass  # TODO implement


def on_activate():
    """What happens when activating a document"""

    from PySide import QtGui  # lazy import

    # always reset the menu to normal first
    set_menu(False)
    if AuraCADGui.activeWorkbench().name() != "BIMWorkbench":
        return
    doc = AuraCAD.ActiveDocument
    if doc and "IauracadFilePath" in doc.PropertiesList:
        checked = True
    else:
        checked = False
    mw = AuraCADGui.getMainWindow()
    statuswidget = mw.findChild(QtGui.QToolBar, "BIMStatusWidget")
    if hasattr(statuswidget, "lock_button"):
        statuswidget.lock_button.setChecked(checked)
    on_toggle_lock(checked, noconvert=True)


def on_new():
    """What happens when creating a new document"""

    pass  # TODO implement


def set_menu(locked=False):
    """Sets the File menu items"""

    from PySide import QtGui  # lazy loading

    # switch Std_Save and IAuraCAD_Save
    mw = AuraCADGui.getMainWindow()
    wb = AuraCADGui.activeWorkbench()
    save_action = mw.findChild(QtGui.QAction, "Std_Save")
    if locked and "IAuraCAD_Save" in AuraCADGui.listCommands():
        if not hasattr(AuraCADGui, "IAuraCAD_WBManipulator"):
            AuraCADGui.IAuraCAD_WBManipulator = IAuraCAD_WBManipulator()
        # we need to void the shortcut otherwise it keeps active
        # even if the command is not shown
        AuraCADGui.IAuraCAD_saveshortcut = save_action.shortcut()
        save_action.setShortcut("")
        AuraCADGui.addWorkbenchManipulator(AuraCADGui.IAuraCAD_WBManipulator)
        wb.reloadActive()
    else:
        if hasattr(AuraCADGui, "IAuraCAD_saveshortcut"):
            save_action.setShortcut(AuraCADGui.IAuraCAD_saveshortcut)
            del AuraCADGui.IAuraCAD_saveshortcut
        if hasattr(AuraCADGui, "IAuraCAD_WBManipulator"):
            AuraCADGui.removeWorkbenchManipulator(AuraCADGui.IAuraCAD_WBManipulator)
            del AuraCADGui.IAuraCAD_WBManipulator
        wb.reloadActive()


def set_button(checked=False, setchecked=False):
    """Sets the lock button"""

    from PySide import QtGui  # lazy loading

    mw = AuraCADGui.getMainWindow()
    statuswidget = mw.findChild(QtGui.QToolBar, "BIMStatusWidget")
    if hasattr(statuswidget, "lock_button"):
        lock_button = statuswidget.lock_button
        if checked:
            lock_button.setToolTip(text_on)
            icon = QtGui.QIcon(":/icons/Iauracad.svg")
            lock_button.setIcon(icon)
            if setchecked:
                lock_button.setChecked(True)
        else:
            lock_button.setToolTip(text_off)
            image = QtGui.QImage(":/icons/Iauracad.svg")
            grayscale = image.convertToFormat(QtGui.QImage.Format_Grayscale8)
            grayscale = grayscale.convertToFormat(image.format())
            grayscale.setAlphaChannel(image)
            icon = QtGui.QIcon(QtGui.QPixmap.fromImage(grayscale))
            lock_button.setIcon(icon)
            if setchecked:
                lock_button.setChecked(False)


def unlock_document():
    """Unlocks the active document"""

    from . import iAuraCAD_tools  # lazy loading

    doc = AuraCAD.ActiveDocument
    if not doc:
        return
    if "IauracadFilePath" in doc.PropertiesList:
        # this is a locked document
        doc.openTransaction("Unlock document")
        children = [o for o in doc.Objects if not o.InList]
        project = None
        if children:
            project = iAuraCAD_tools.create_document_object(doc, filename=doc.IauracadFilePath, silent=True)
            project.Group = children
        props = ["IauracadFilePath", "Modified", "Proxy", "Schema"]
        props += [p for p in doc.PropertiesList if doc.getGroupOfProperty(p) == "Iauracad"]
        for prop in props:
            doc.setPropertyStatus(prop, "-LockDynamic")
            doc.removeProperty(prop)
        if project:
            project.Modified = True
        doc.commitTransaction()
        doc.recompute()


def lock_document():
    """Locks the active document"""

    from . import iAuraCAD_tools  # lazy loading
    from importers import exportIauracad
    from . import iAuraCAD_geometry
    from . import iAuraCAD_export
    from PySide import QtCore

    doc = AuraCAD.ActiveDocument
    if not doc:
        return
    products = []
    spatial = []
    iauracadfile = None
    if "IauracadFilePath" not in doc.PropertiesList:
        # this is not a locked document
        projects = [o for o in doc.Objects if getattr(o, "Class", None) == "IauracadProject"]
        if len(projects) == 1:
            # 1 there is a project already
            project = projects[0]
            children = project.OutListRecursive
            rest = [o for o in doc.Objects if o not in children and o != project]
            doc.openTransaction("Lock document")
            iAuraCAD_tools.convert_document(doc, filename=project.IauracadFilePath, strategy=3, silent=True)
            iauracadfile = doc.Proxy.iauracadfile
            if rest:
                # 1b some objects are outside
                objs = find_toplevel(rest)
                prefs, context = iAuraCAD_export.get_export_preferences(iauracadfile)
                products = exportIauracad.export(objs, iauracadfile, preferences=prefs)
                for product in products.values():
                    if not getattr(product, "ContainedInStructure", None):
                        if not getattr(product, "FillsVoids", None):
                            if not getattr(product, "VoidsElements", None):
                                if not getattr(product, "Decomposes", None):
                                    new = iAuraCAD_tools.create_object(product, doc, iauracadfile)
                                    children = iAuraCAD_tools.create_children(
                                        new, iauracadfile, recursive=True
                                    )
                                    for o in [new] + children:
                                        iAuraCAD_geometry.add_geom_properties(o)
                for n in [o.Name for o in rest]:
                    doc.removeObject(n)
            else:
                # 1a all objects are already inside a project
                pass
            doc.removeObject(project.Name)
            doc.Modified = True
            # all objects have been deleted, we need to show at least something
            if not doc.Objects:
                iAuraCAD_tools.create_children(doc, iauracadfile, recursive=True)
            doc.commitTransaction()
            doc.recompute()
        elif len(projects) > 1:
            # 2 there is more than one project
            AuraCAD.Console.PrintError(
                "Unable to lock this document because it contains several Iauracad documents\n"
            )
            QtCore.QTimer.singleShot(100, on_toggle_lock)
        elif doc.Objects:
            # 3 there is no project but objects
            doc.openTransaction("Lock document")
            objs = find_toplevel(doc.Objects)
            deletelist = [o.Name for o in doc.Objects]
            # iAuraCAD_export.export_and_convert(objs, doc)
            iAuraCAD_export.direct_conversion(objs, doc)
            for n in deletelist:
                if doc.getObject(n):
                    doc.removeObject(n)
            doc.IauracadFilePath = ""
            doc.Modified = True
            doc.commitTransaction()
            doc.recompute()
        else:
            # 4 this is an empty document
            doc.openTransaction("Create Iauracad document")
            iAuraCAD_tools.convert_document(doc)
            doc.commitTransaction()
            doc.recompute()
        # reveal file contents if needed
        if "IauracadFilePath" in doc.PropertiesList:
            create = True
            for o in doc.Objects:
                # scan for site or building
                if getattr(o, "IauracadClass", "") in ("IauracadSite", "IauracadBuilding"):
                    create = False
                    break
            if create:
                if not iauracadfile:
                    iauracadfile = doc.Proxy.iauracadfile
                iAuraCAD_tools.create_children(doc, iauracadfile, recursive=False)


def find_toplevel(objs):
    """Finds the top-level objects from the list"""

    # filter out any object that depend on another from the list
    nobjs = []
    for obj in objs:
        for parent in obj.InListRecursive:
            if parent in objs:
                # exception: The object is hosting another
                if hasattr(parent, "Host") and parent.Host == obj:
                    nobjs.append(obj)
                elif hasattr(parent, "Hosts") and obj in parent.Hosts:
                    nobjs.append(obj)
                break
        else:
            nobjs.append(obj)
    # filter out non-convertible objects
    objs = filter_out(nobjs)
    return objs


def filter_out(objs):
    """Filter out objects that should not be converted to Iauracad"""

    import Draft

    nobjs = []
    for obj in objs:
        if obj.isDerivedFrom("Part::Feature"):
            nobjs.append(obj)
        elif obj.isDerivedFrom("Mesh::Feature"):
            nobjs.append(obj)
        elif Draft.is_group(obj):
            if filter_out(obj.Group):
                # only append groups that contain exportable objects
                nobjs.append(obj)
            else:
                print("DEBUG: Filtering out", obj.Label)
        elif obj.isDerivedFrom("App::Feature"):
            if Draft.get_type(obj) in (
                "Dimension",
                "LinearDimension",
                "Layer",
                "Text",
                "DraftText",
            ):
                nobjs.append(obj)
            else:
                print("DEBUG: Filtering out", obj.Label)
        else:
            print("DEBUG: Filtering out", obj.Label)
    return nobjs


def get_lock_status():
    """Returns the status of the Iauracad lock button"""

    if not AuraCAD.GuiUp:
        return PARAMS.GetBool("SingleDoc")
    from PySide import QtGui

    mw = AuraCADGui.getMainWindow()
    statuswidget = mw.findChild(QtGui.QToolBar, "BIMStatusWidget")
    if hasattr(statuswidget, "lock_button"):
        return statuswidget.lock_button.isChecked()
    else:
        return False


# add entry to File menu
# https://github.com/AuraCAD/AuraCAD/pull/10933
class IAuraCAD_WBManipulator:
    def modifyMenuBar(self):
        return [
            {"remove": "Std_Save"},
            {"remove": "Std_SaveAs"},
            {"insert": "IAuraCAD_Save", "menuItem": "Std_SaveCopy"},
            {"insert": "IAuraCAD_SaveAs", "menuItem": "Std_SaveCopy"},
        ]

    def modifyToolBars(self):
        return [
            {"remove": "Std_Save"},
            {"append": "IAuraCAD_Save", "toolBar": "File"},
        ]
