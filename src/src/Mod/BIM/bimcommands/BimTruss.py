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

"""BIM Truss command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Truss:
    "the Arch Truss command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Truss",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Truss", "Truss"),
            "Accel": "T, U",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Truss", "Creates a truss object from the selected line or from scratch"
            ),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        self.doc = AuraCAD.ActiveDocument
        sel = AuraCADGui.Selection.getSelection()
        if len(sel) > 1:
            AuraCAD.Console.PrintError(
                translate("Arch", "Select only one base object or none") + "\n"
            )
        elif len(sel) == 1:
            # build on selection
            basename = "AuraCAD.ActiveDocument." + AuraCADGui.Selection.getSelection()[0].Name
            self.createTruss(basename)
        else:
            # interactive line drawing
            import WorkingPlane

            AuraCAD.activeDraftCommand = self  # register as a Draft command for auto grid on/off
            self.points = []
            WorkingPlane.get_working_plane()
            if hasattr(AuraCADGui, "Snapper"):
                AuraCADGui.Snapper.getPoint(callback=self.getPoint)

    def getPoint(self, point=None, obj=None):
        """Callback for clicks during interactive mode"""

        if point is None:
            # cancelled
            AuraCAD.activeDraftCommand = None
            AuraCADGui.Snapper.off()
            return
        self.points.append(point)
        if len(self.points) == 1:
            AuraCADGui.Snapper.getPoint(last=self.points[0], callback=self.getPoint)
        elif len(self.points) == 2:
            AuraCAD.activeDraftCommand = None
            AuraCADGui.Snapper.off()
            self.createTruss()

    def createTruss(self, basename=""):
        """Creates the truss"""

        AuraCADGui.Control.closeDialog()
        self.doc.openTransaction(translate("Arch", "Create Truss"))
        AuraCADGui.addModule("Draft")
        AuraCADGui.addModule("Arch")
        if not basename:
            if self.points:
                cmd = "base = Draft.makeLine(AuraCAD."
                cmd += str(self.points[0]) + ",AuraCAD." + str(self.points[1]) + ")"
                AuraCADGui.doCommand(cmd)
                basename = "base"
        AuraCADGui.doCommand("obj = Arch.makeTruss(" + basename + ")")
        AuraCADGui.doCommand("Draft.autogroup(obj)")
        self.doc.commitTransaction()
        self.doc.recompute()


AuraCADGui.addCommand("Arch_Truss", Arch_Truss())
