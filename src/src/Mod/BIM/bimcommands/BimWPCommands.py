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

"""The BIM SetWPFront command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP


class BIM_SetWPFront:

    def GetResources(self):
        return {
            "Pixmap": "view-front.svg",
            "MenuText": QT_TRANSLATE_NOOP("BIM_SetWPFront", "Working Plane Front"),
            "ToolTip": QT_TRANSLATE_NOOP("BIM_SetWPFront", "Sets the working plane to Front"),
            "Accel": "W,P,1",
        }

    def Activated(self):
        AuraCADGui.addModule("WorkingPlane")
        AuraCADGui.doCommand("WorkingPlane.get_working_plane(update=False).set_to_front()")


class BIM_SetWPSide:

    def GetResources(self):
        return {
            "Pixmap": "view-right.svg",
            "MenuText": QT_TRANSLATE_NOOP("BIM_SetWPSide", "Working Plane Side"),
            "ToolTip": QT_TRANSLATE_NOOP("BIM_SetWPSide", "Sets the working plane to Side"),
            "Accel": "W,P,3",
        }

    def Activated(self):
        AuraCADGui.addModule("WorkingPlane")
        AuraCADGui.doCommand("WorkingPlane.get_working_plane(update=False).set_to_side()")


class BIM_SetWPTop:

    def GetResources(self):
        return {
            "Pixmap": "view-top.svg",
            "MenuText": QT_TRANSLATE_NOOP("BIM_SetWPTop", "Working Plane Top"),
            "ToolTip": QT_TRANSLATE_NOOP("BIM_SetWPTop", "Sets the working plane to Top"),
            "Accel": "W,P,2",
        }

    def Activated(self):
        AuraCADGui.addModule("WorkingPlane")
        AuraCADGui.doCommand("WorkingPlane.get_working_plane(update=False).set_to_top()")


class BIM_WPView:

    def GetResources(self):
        return {
            "Pixmap": "BIM_WPView",
            "MenuText": QT_TRANSLATE_NOOP("BIM_WPView", "Working Plane View"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_WPView",
                "Aligns the view to the current item in BIM Views Manager or to the current working plane",
            ),
            "Accel": "9",
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        from bimcommands import BimViews
        import WorkingPlane

        vm = BimViews.findWidget()
        if vm:
            sel = vm.tree.selectedItems()
            if sel:
                # Aligning to current widget item
                BimViews.show(sel[0])
                return
            if hasattr(vm, "lastSelected"):
                # Aligning to stored widget item
                BimViews.show(vm.lastSelected)
                return
        # Aligning to current working plane
        WorkingPlane.get_working_plane().align_view()


AuraCADGui.addCommand("BIM_WPView", BIM_WPView())
AuraCADGui.addCommand("BIM_SetWPTop", BIM_SetWPTop())
AuraCADGui.addCommand("BIM_SetWPSide", BIM_SetWPSide())
AuraCADGui.addCommand("BIM_SetWPFront", BIM_SetWPFront())
