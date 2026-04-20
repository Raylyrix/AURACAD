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

"""The BIM DimensionAligned command"""

import AuraCAD
import AuraCADGui

from draftguitools import gui_dimensions

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP


class BIM_DimensionAligned(gui_dimensions.Dimension):

    def __init__(self):
        super().__init__()

    def GetResources(self):
        return {
            "Pixmap": "BIM_DimensionAligned",
            "MenuText": QT_TRANSLATE_NOOP("BIM_DimensionAligned", "Aligned Dimension"),
            "ToolTip": QT_TRANSLATE_NOOP("BIM_DimensionAligned", "Creates an aligned dimension"),
            "Accel": "D, I",
        }


class BIM_DimensionHorizontal(gui_dimensions.Dimension):

    def __init__(self):
        super().__init__()

    def GetResources(self):
        return {
            "Pixmap": "BIM_DimensionHorizontal.svg",
            "MenuText": QT_TRANSLATE_NOOP("BIM_DimensionHorizontal", "Horizontal Dimension"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_DimensionHorizontal", "Creates an horizontal dimension"
            ),
            "Accel": "D, H",
        }

    def Activated(self):
        import WorkingPlane

        self.dir = WorkingPlane.get_working_plane().u
        super().Activated(dir_vec=self.dir)


class BIM_DimensionVertical(gui_dimensions.Dimension):

    def __init__(self):
        super().__init__()

    def GetResources(self):
        return {
            "Pixmap": "BIM_DimensionVertical",
            "MenuText": QT_TRANSLATE_NOOP("BIM_DimensionVertical", "Vertical Dimension"),
            "ToolTip": QT_TRANSLATE_NOOP("BIM_DimensionVertical", "Creates a vertical dimension"),
            "Accel": "D, V",
        }

    def Activated(self):
        import WorkingPlane

        self.dir = WorkingPlane.get_working_plane().v
        super().Activated(dir_vec=self.dir)


AuraCADGui.addCommand("BIM_DimensionVertical", BIM_DimensionVertical())
AuraCADGui.addCommand("BIM_DimensionHorizontal", BIM_DimensionHorizontal())
AuraCADGui.addCommand("BIM_DimensionAligned", BIM_DimensionAligned())
