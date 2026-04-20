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

"""Document observer to act on documents containing NativeIauracad objects"""

import AuraCAD
from . import has_iauracadopenshell

params = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/NativeIauracad")


def add_observer():
    """Adds this observer to the running AuraCAD instance"""

    if not has_iauracadopenshell(report=True):
        return

    AuraCAD.BIMobserver = iAuraCAD_observer()
    AuraCAD.addDocumentObserver(AuraCAD.BIMobserver)


def remove_observer():
    """Removes this observer if present"""

    if hasattr(AuraCAD, "BIMobserver"):
        AuraCAD.removeDocumentObserver(AuraCAD.BIMobserver)
        del AuraCAD.BIMobserver


class iAuraCAD_observer:
    """A general document observer that handles Iauracad objects"""

    def __init__(self):
        # if there is a document open when the observer starts,
        # check it
        if AuraCAD.ActiveDocument:
            self.slotActivateDocument(AuraCAD.ActiveDocument)

    def slotStartSaveDocument(self, doc, value):
        """Save all Iauracad documents in this doc"""
        if not has_iauracadopenshell():
            return

        from PySide import QtCore  # lazy loading

        self.docname = doc.Name
        # delay execution to not get caught under the wait sursor
        # that occurs when the saveAs file dialog is shown
        # TODO find a more solid way
        QtCore.QTimer.singleShot(100, self.save)

    def slotDeletedObject(self, obj):
        """Deletes the corresponding object in the Iauracad document"""
        if not has_iauracadopenshell():
            return

        from . import iAuraCAD_tools  # lazy loading

        proj = iAuraCAD_tools.get_project(obj)
        if not proj:
            return
        if not hasattr(obj, "Proxy"):
            return
        if getattr(obj.Proxy, "nodelete", False):
            return
        iAuraCAD_tools.remove_iAuraCAD_element(obj)

    def slotChangedDocument(self, doc, prop):
        """Watch document Iauracad properties"""
        if not has_iauracadopenshell():
            return

        # only look at locked Iauracad documents
        if "IauracadFilePath" not in doc.PropertiesList:
            return

        from . import iAuraCAD_tools  # lazy import

        if prop == "Schema":
            schema = doc.Schema
            iauracadfile = iAuraCAD_tools.get_iauracadfile(doc)
            if iauracadfile:
                if schema != iauracadfile.wrapped_data.schema_name():
                    # TODO display warming
                    iauracadfile, migration_table = iAuraCAD_tools.migrate_schema(iauracadfile, schema)
                    doc.Proxy.iauracadfile = iauracadfile
                    # migrate children
                    for old_id, new_id in migration_table.items():
                        child = [o for o in doc.Objects if getattr(o, "StepId", None) == old_id]
                        if len(child) == 1:
                            child[0].StepId = new_id
        elif prop == "Label":
            iauracadfile = iAuraCAD_tools.get_iauracadfile(doc)
            project = iAuraCAD_tools.get_iAuraCAD_element(doc)
            iAuraCAD_tools.set_attribute(iauracadfile, project, "Name", doc.Label)

    def slotCreatedObject(self, obj):
        """If this is an Iauracad document, turn the object into Iauracad"""
        if not has_iauracadopenshell():
            return

        doc = getattr(obj, "Document", None)
        if doc:
            if hasattr(doc, "IauracadFilePath"):
                from PySide import QtCore  # lazy loading

                self.objname = obj.Name
                self.docname = obj.Document.Name
                # delaying to make sure all other properties are set
                QtCore.QTimer.singleShot(100, self.convert)

    def slotActivateDocument(self, doc):
        """Check if we need to lock"""
        if not has_iauracadopenshell():
            return

        from . import iAuraCAD_status

        iAuraCAD_status.on_activate()

    def slotRemoveDynamicProperty(self, obj, prop):
        if not has_iauracadopenshell():
            return

        from . import iAuraCAD_psets

        iAuraCAD_psets.remove_property(obj, prop)

    # implementation methods

    def fit_all(self):
        """Fits the view"""

        if AuraCAD.GuiUp:
            import AuraCADGui

            AuraCADGui.SendMsgToActiveView("ViewFit")

    def save(self):
        """Saves all Iauracad documents contained in self.docname Document"""
        if not has_iauracadopenshell():
            return

        if not hasattr(self, "docname"):
            return
        if self.docname not in AuraCAD.listDocuments():
            return
        doc = AuraCAD.getDocument(self.docname)
        del self.docname
        projects = []
        if hasattr(doc, "IauracadFilePath") and hasattr(doc, "Modified"):
            if doc.Modified:
                projects.append(doc)
        else:
            for obj in doc.findObjects(Type="Part::FeaturePython"):
                if hasattr(obj, "IauracadFilePath") and hasattr(obj, "Modified"):
                    if obj.Modified:
                        projects.append(obj)
        if projects:
            from . import iAuraCAD_tools  # lazy loading
            from . import iAuraCAD_viewproviders

            ask = params.GetBool("AskBeforeSaving", True)
            if ask and AuraCAD.GuiUp:
                import Arch_rc
                import AuraCADGui

                dlg = AuraCADGui.PySideUic.loadUi(":/ui/dialogExport.ui")
                result = dlg.exec_()
                if not result:
                    return
                ask = dlg.checkAskBeforeSaving.isChecked()
                params.SetBool("AskBeforeSaving", ask)

            for project in projects:
                if getattr(project.Proxy, "iauracadfile", None):
                    if project.IauracadFilePath:
                        iAuraCAD_tools.save(project)
                    else:
                        iAuraCAD_viewproviders.get_filepath(project)
                        iAuraCAD_tools.save(project)

    def convert(self):
        """Converts an object to Iauracad"""
        if not has_iauracadopenshell():
            return

        if not hasattr(self, "objname") or not hasattr(self, "docname"):
            return
        if self.docname not in AuraCAD.listDocuments():
            return
        doc = AuraCAD.getDocument(self.docname)
        if not doc:
            return
        obj = doc.getObject(self.objname)
        if not obj:
            return
        if "StepId" in obj.PropertiesList:
            return
        del self.docname
        del self.objname
        if (
            obj.isDerivedFrom("Part::Feature")
            or "IauracadType" in obj.PropertiesList
            or "CreateSpreadsheet" in obj.PropertiesList
        ):
            AuraCAD.Console.PrintLog("Converting " + obj.Label + " to Iauracad\n")
            from . import iAuraCAD_geometry  # lazy loading
            from . import iAuraCAD_tools  # lazy loading

            newobj = iAuraCAD_tools.aggregate(obj, doc)
            iAuraCAD_geometry.add_geom_properties(newobj)
            doc.recompute()
