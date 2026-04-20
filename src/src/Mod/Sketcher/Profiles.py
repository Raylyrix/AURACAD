# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2014 Juergen Riegel <AuraCAD@juergen-riegel.net>        *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import AuraCAD

if AuraCAD.GuiUp:
    import AuraCADGui
    from PySide import QtCore


__title__ = "Sketcher profile lib handling"
__author__ = "Juergen Riegel"
__url__ = "https://www.AuraCAD.org"


def isProfileActive():
    return not AuraCAD.ActiveDocument is None


def getSketch():
    edit = AuraCADGui.ActiveDocument.getInEdit()
    if edit and edit.isDerivedFrom("SketcherGui::ViewProviderSketch"):
        return edit.Object
    return None


class _CommandProfileHexagon1:
    "The basis hexagon profile command definition"

    def GetResources(self):
        return {
            "Pixmap": "Sketcher_CreateHexagon",
            "MenuText": QtCore.QT_TRANSLATE_NOOP(
                "Sketcher_ProfilesHexagon1", "Creates a hexagonal profile"
            ),
            "Accel": "",
            "CmdType": "ForEdit",
            "ToolTip": QtCore.QT_TRANSLATE_NOOP(
                "Sketcher_ProfilesHexagon1", "Creates a hexagonal profile in the sketch"
            ),
        }

    def Activated(self):
        AuraCAD.ActiveDocument.openTransaction("Create hexagon profile")
        AuraCADGui.addModule("ProfileLib.Hexagon")
        sketch = getSketch()
        if not sketch is None:
            AuraCADGui.doCommand("ProfileLib.Hexagon.makeHexagonSimple('%s')" % (sketch.Name))
        else:
            AuraCADGui.doCommand("ProfileLib.Hexagon.makeHexagonSimple()")
        AuraCAD.ActiveDocument.recompute()

    def IsActive(self):
        return isProfileActive()


AuraCADGui.addCommand("Sketcher_ProfilesHexagon1", _CommandProfileHexagon1())
