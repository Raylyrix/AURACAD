# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2017 Yorik van Havre <yorik@uncreated.net>              *
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

"""The BIM TD View command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate


class BIM_TDView:
    def GetResources(self):
        return {
            "Pixmap": "BIM_InsertView",
            "MenuText": QT_TRANSLATE_NOOP("BIM_TDView", "New View"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_TDView",
                "Inserts a drawing view on a page.\n"
                "To choose where to insert the view when multiple pages are available,\n"
                "select both the view and the page before executing the command.",
            ),
            "Accel": "V, I",
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        import Draft

        sections = []
        page = None
        drafts = []
        for obj in AuraCADGui.Selection.getSelection():
            t = Draft.getType(obj)
            if t == "SectionPlane":
                sections.append(obj)
            elif t == "TechDraw::DrawPage":
                page = obj
            else:
                drafts.append(obj)
        if not page:
            pages = AuraCAD.ActiveDocument.findObjects(Type="TechDraw::DrawPage")
            if pages:
                page = pages[0]
        if (not page) or ((not sections) and (not drafts)):
            AuraCAD.Console.PrintError(
                translate(
                    "BIM",
                    "No section view, Draft object, or page found or selected in the document",
                )
                + "\n"
            )
            return
        AuraCAD.ActiveDocument.openTransaction("Create view")
        for section in sections:
            view = AuraCAD.ActiveDocument.addObject("TechDraw::DrawViewArch", "BIMView")
            view.Label = section.Label
            view.Source = section
            page.addView(view)
            if page.Scale:
                view.Scale = page.Scale
        for draft in drafts:
            view = AuraCAD.ActiveDocument.addObject("TechDraw::DrawViewDraft", "DraftView")
            view.Label = draft.Label
            view.Source = draft
            page.addView(view)
            if page.Scale:
                view.Scale = page.Scale
            if "ShapeMode" in draft.PropertiesList:
                draft.ShapeMode = "Shape"
            for child in draft.OutListRecursive:
                if "ShapeMode" in child.PropertiesList:
                    child.ShapeMode = "Shape"
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()


AuraCADGui.addCommand("BIM_TDView", BIM_TDView())
