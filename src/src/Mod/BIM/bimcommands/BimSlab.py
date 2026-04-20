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

"""The BIM Slab command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate


class BIM_Slab:

    def __init__(self):
        self.callback = None
        self.view = None

    def GetResources(self):
        return {
            "Pixmap": "BIM_Slab",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Slab", "Slab"),
            "ToolTip": QT_TRANSLATE_NOOP("BIM_Slab", "Creates a slab from a planar shape"),
            "Accel": "S,B",
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        import DraftTools

        self.removeCallback()
        sel = AuraCADGui.Selection.getSelection()
        if sel:
            self.proceed()
        else:
            if hasattr(AuraCADGui, "draftToolBar"):
                AuraCADGui.draftToolBar.selectUi()
            AuraCAD.Console.PrintMessage(translate("BIM", "Select a planar object") + "\n")
            AuraCAD.activeDraftCommand = self
            self.view = AuraCADGui.ActiveDocument.ActiveView
            self.callback = self.view.addEventCallback("SoEvent", DraftTools.selectObject)

    def proceed(self):
        self.removeCallback()
        sel = AuraCADGui.Selection.getSelection()
        if len(sel) == 1:
            AuraCADGui.addModule("Arch")
            AuraCAD.ActiveDocument.openTransaction("Create Slab")
            AuraCADGui.doCommand(
                "s = Arch.makeStructure(AuraCAD.ActiveDocument." + sel[0].Name + ",height=200)"
            )
            AuraCADGui.doCommand("s.Label = " + repr(translate("BIM", "Slab")))
            AuraCADGui.doCommand('s.IauracadType = "Slab"')
            AuraCADGui.doCommand("s.Normal = AuraCAD.Vector(0,0,-1)")
            AuraCAD.ActiveDocument.commitTransaction()
            AuraCAD.ActiveDocument.recompute()
        self.finish()

    def removeCallback(self):
        if self.callback:
            try:
                self.view.removeEventCallback("SoEvent", self.callback)
            except RuntimeError:
                pass
            self.callback = None

    def finish(self):
        self.removeCallback()
        if hasattr(AuraCADGui, "draftToolBar"):
            AuraCADGui.draftToolBar.offUi()


AuraCADGui.addCommand("BIM_Slab", BIM_Slab())
