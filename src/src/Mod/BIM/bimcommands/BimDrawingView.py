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

"""The BIM DrawingView command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class BIM_DrawingView:
    """The command definition for the Drawing View command"""

    def GetResources(self):

        return {
            "Pixmap": "BIM_ArchView",
            "MenuText": QT_TRANSLATE_NOOP("BIM_DrawingView", "2D Drawing"),
            "Accel": "V, D",
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_DrawingView", "Creates a drawing container to contain elements of a 2D view"
            ),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        import Draft

        AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create 2D View"))
        AuraCADGui.addModule("Arch")
        AuraCADGui.addModule("Draft")
        AuraCADGui.addModule("WorkingPlane")
        AuraCADGui.doCommand("obj = Arch.make2DDrawing()")
        AuraCADGui.doCommand("Draft.autogroup(obj)")
        s = AuraCADGui.Selection.getSelection()
        if len(s) == 1:
            s = s[0]
            if Draft.getType(s) == "SectionPlane":
                AuraCADGui.doCommand(
                    "vobj = Draft.make_shape2dview(AuraCAD.ActiveDocument." + s.Name + ")"
                )
                AuraCADGui.doCommand("vobj.Label = " + repr(translate("BIM", "Viewed lines")))
                AuraCADGui.doCommand("vobj.InPlace = False")
                AuraCADGui.doCommand("obj.addObject(vobj)")
                AuraCADGui.doCommand(
                    "cobj = Draft.make_shape2dview(AuraCAD.ActiveDocument." + s.Name + ")"
                )
                AuraCADGui.doCommand("cobj.Label = " + repr(translate("BIM", "Cut lines")))
                AuraCADGui.doCommand("cobj.InPlace = False")
                AuraCADGui.doCommand('cobj.ProjectionMode = "Cutfaces"')
                AuraCADGui.doCommand("obj.addObject(cobj)")
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()


AuraCADGui.addCommand("BIM_DrawingView", BIM_DrawingView())
