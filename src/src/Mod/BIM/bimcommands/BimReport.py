# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Copyright (c) 2025 The AuraCAD Project

import AuraCAD
import AuraCADGui


class BIM_Report:
    """The command to create a new BIM Report object."""

    def GetResources(self):
        return {
            "Pixmap": "BIM_Report",
            "MenuText": "BIM Report",
            "ToolTip": "Create a new BIM Report to query model data with SQL",
        }

    def Activated(self):
        AuraCADGui.addModule("Arch")
        AuraCADGui.doCommand("Arch.makeReport()")

    def IsActive(self):
        return AuraCAD.ActiveDocument is not None


AuraCADGui.addCommand("BIM_Report", BIM_Report())
