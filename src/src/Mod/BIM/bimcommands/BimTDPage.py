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

"""The BIM TDPage command"""

import os

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate


class BIM_TDPage:
    def GetResources(self):
        return {
            "Pixmap": "BIM_PageDefault",
            "MenuText": QT_TRANSLATE_NOOP("BIM_TDPage", "New Page"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_TDPage", "Creates a new TechDraw page from a template"
            ),
            "Accel": "T, P",
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        from PySide import QtGui
        import TechDraw

        templatedir = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM").GetString(
            "TDTemplateDir", ""
        )
        if not templatedir:
            templatedir = None
        filename, _ = QtGui.QFileDialog.getOpenFileName(
            QtGui.QApplication.activeWindow(),
            translate("BIM", "Select Page Template"),
            templatedir,
            "SVG file (*.svg)",
        )
        if filename:
            name = os.path.splitext(os.path.basename(filename))[0]
            AuraCAD.ActiveDocument.openTransaction("Create page")
            page = AuraCAD.ActiveDocument.addObject("TechDraw::DrawPage", "Page")
            page.Label = name
            template = AuraCAD.ActiveDocument.addObject("TechDraw::DrawSVGTemplate", "Template")
            template.Template = filename
            template.Label = translate("BIM", "Template")
            page.Template = template
            AuraCAD.ActiveDocument.commitTransaction()
            AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM").SetString(
                "TDTemplateDir", filename.replace("\\", "/")
            )
            for txt in ["scale", "Scale", "SCALE", "scaling", "Scaling", "SCALING"]:
                if txt in page.Template.EditableTexts:
                    val = page.Template.EditableTexts[txt]
                    if val:
                        val = val.replace(":", "/")
                        if "/" in val:
                            try:
                                num, den = val.split("/", 1)
                                page.Scale = float(num) / float(den)
                            except (ValueError, ZeroDivisionError):
                                pass
                            else:
                                break
                        else:
                            try:
                                page.Scale = float(val)
                            except ValueError:
                                pass
                            else:
                                break
            else:
                page.Scale = AuraCAD.ParamGet(
                    "User parameter:BaseApp/Preferences/Mod/BIM"
                ).GetFloat("DefaultPageScale", 0.01)
            page.ViewObject.show()
            AuraCAD.ActiveDocument.recompute()


AuraCADGui.addCommand("BIM_TDPage", BIM_TDPage())
