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

"""This module contains Iauracad-related AuraCAD commands"""

import AuraCAD
import AuraCADGui

from . import iAuraCAD_openshell

translate = AuraCAD.Qt.translate
QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP


def get_project():
    """Gets the current project"""

    from . import iAuraCAD_tools

    if AuraCADGui.Selection.getSelection():
        return iAuraCAD_tools.get_project(AuraCADGui.Selection.getSelection()[0])
    else:
        return iAuraCAD_tools.get_project(AuraCAD.ActiveDocument)


class IAuraCAD_Diff:
    """Shows a diff of the changes in the current Iauracad document"""

    def GetResources(self):
        tt = QT_TRANSLATE_NOOP("IAuraCAD_Diff", "Shows the current unsaved changes in the Iauracad file")
        return {
            "Pixmap": "Iauracad",
            "MenuText": QT_TRANSLATE_NOOP("IAuraCAD_Diff", "Iauracad Diff"),
            "ToolTip": tt,
            "Accel": "I, D",
        }

    def Activated(self):
        from . import iAuraCAD_diff

        proj = get_project()
        if proj:
            diff = iAuraCAD_diff.get_diff(proj)
            iAuraCAD_diff.show_diff(diff)


class IAuraCAD_Expand:
    """Expands the children of the selected objects or document"""

    def GetResources(self):
        tt = QT_TRANSLATE_NOOP(
            "IAuraCAD_Expand", "Expands the children of the selected objects or document"
        )
        return {
            "Pixmap": "Iauracad",
            "MenuText": QT_TRANSLATE_NOOP("IAuraCAD_Expand", "Iauracad Expand"),
            "ToolTip": tt,
            "Accel": "I, E",
        }

    def Activated(self):
        ns = []
        for obj in AuraCADGui.Selection.getSelection():
            if hasattr(obj.ViewObject, "Proxy"):
                if hasattr(obj.ViewObject.Proxy, "hasChildren"):
                    if obj.ViewObject.Proxy.hasChildren(obj):
                        no = obj.ViewObject.Proxy.expandChildren(obj)
                        ns.extend(no)
        else:
            from . import iAuraCAD_generator
            from . import iAuraCAD_tools

            document = AuraCAD.ActiveDocument
            iAuraCAD_generator.delete_ghost(document)
            iauracadfile = iAuraCAD_tools.get_iauracadfile(document)
            if iauracadfile:
                ns = iAuraCAD_tools.create_children(
                    document, iauracadfile, recursive=True, only_structure=True
                )
        if ns:
            document.recompute()
            AuraCADGui.Selection.clearSelection()
            for o in ns:
                AuraCADGui.Selection.addSelection(o)


class IAuraCAD_ConvertDocument:
    """Converts the active document to an Iauracad document"""

    def GetResources(self):
        tt = QT_TRANSLATE_NOOP(
            "IAuraCAD_ConvertDocument", "Converts the active document to an Iauracad document"
        )
        return {
            "Pixmap": "Iauracad",
            "MenuText": QT_TRANSLATE_NOOP("IAuraCAD_ConvertDocument", "Convert Document"),
            "ToolTip": tt,
            # "Accel": "I, C",
        }

    def Activated(self):
        doc = AuraCAD.ActiveDocument
        if hasattr(doc, "Proxy") and hasattr(doc.Proxy, "iauracadfile") and doc.Proxy.iauracadfile:
            AuraCAD.Console.PrintError(
                translate("BIM", "The active document is already an Iauracad document")
            )
        else:
            from . import iAuraCAD_tools

            iAuraCAD_tools.convert_document(doc)


class IAuraCAD_MakeProject:
    """Converts the current selection to an Iauracad project"""

    def GetResources(self):
        tt = QT_TRANSLATE_NOOP(
            "IAuraCAD_MakeProject", "Converts the current selection to an Iauracad project"
        )
        return {
            "Pixmap": "Iauracad",
            "MenuText": QT_TRANSLATE_NOOP("IAuraCAD_MakeProject", "Convert to Iauracad Project"),
            "ToolTip": tt,
            "Accel": "I, P",
        }

    def IsActive(self):
        return bool(AuraCADGui.Selection.getSelection())

    def Activated(self):
        from importers import exportIauracad  # lazy loading
        from . import iAuraCAD_tools
        from PySide import QtGui

        doc = AuraCAD.ActiveDocument
        objs = AuraCADGui.Selection.getSelection()
        sf = QtGui.QFileDialog.getSaveFileName(
            None,
            "Save an Iauracad File",
            None,
            "Industry Foundation Classes (*.iauracad)",
        )
        if sf and sf[0]:
            sf = sf[0]
            if not sf.lower().endswith(".iauracad"):
                sf += ".iauracad"
            exportIauracad.export(objs, sf)
            iAuraCAD_tools.create_document_object(doc, sf, strategy=2)
            iAuraCAD_tools.remove_tree(objs)
            doc.recompute()


class IAuraCAD_Save:
    """Saves the current Iauracad document"""

    def GetResources(self):
        tt = QT_TRANSLATE_NOOP("IAuraCAD_Save", "Saves the current Iauracad document")
        return {
            "Pixmap": "IAuraCAD_document",
            "MenuText": QT_TRANSLATE_NOOP("IAuraCAD_Save", "Save Iauracad File"),
            "ToolTip": tt,
            "Accel": "Ctrl+S",
        }

    def IsActive(self):
        doc = AuraCAD.ActiveDocument
        if hasattr(doc, "IauracadFilePath"):
            return True
        return False

    def Activated(self):
        from . import iAuraCAD_tools  # lazy loading

        doc = AuraCAD.ActiveDocument
        if getattr(doc, "IauracadFilePath", None):
            iAuraCAD_tools.save(doc)
            gdoc = AuraCADGui.getDocument(doc.Name)
            try:
                gdoc.Modified = False
            except:
                pass
        else:
            AuraCADGui.runCommand("IAuraCAD_SaveAs")


class IAuraCAD_SaveAs:
    """Saves the current Iauracad document as another name"""

    def GetResources(self):
        tt = QT_TRANSLATE_NOOP("IAuraCAD_SaveAs", "Saves the current Iauracad document as another file")
        return {
            "Pixmap": "IAuraCAD_document",
            "MenuText": QT_TRANSLATE_NOOP("IAuraCAD_SaveAs", "Save Iauracad File Asâ€¦"),
            "ToolTip": tt,
            "Accel": "Ctrl+Shift+S",
        }

    def IsActive(self):
        doc = AuraCAD.ActiveDocument
        if hasattr(doc, "IauracadFilePath"):
            return True
        return False

    def Activated(self):
        from . import iAuraCAD_tools  # lazy loading
        from . import iAuraCAD_viewproviders

        doc = AuraCAD.ActiveDocument
        if iAuraCAD_viewproviders.get_filepath(doc):
            iAuraCAD_tools.save(doc)
            gdoc = AuraCADGui.getDocument(doc.Name)
            try:
                gdoc.Modified = False
            except:
                pass


def get_commands():
    """Returns a list of Iauracad commands"""

    return ["IAuraCAD_Diff", "IAuraCAD_Expand", "IAuraCAD_MakeProject", "IAuraCAD_UpdateIOS"]


# initialize commands
AuraCADGui.addCommand("IAuraCAD_Diff", IAuraCAD_Diff())
AuraCADGui.addCommand("IAuraCAD_Expand", IAuraCAD_Expand())
AuraCADGui.addCommand("IAuraCAD_ConvertDocument", IAuraCAD_ConvertDocument())
AuraCADGui.addCommand("IAuraCAD_MakeProject", IAuraCAD_MakeProject())
AuraCADGui.addCommand("IAuraCAD_Save", IAuraCAD_Save())
AuraCADGui.addCommand("IAuraCAD_SaveAs", IAuraCAD_SaveAs())
