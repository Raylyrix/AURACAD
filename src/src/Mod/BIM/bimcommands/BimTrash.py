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

"""The BIM Trash command"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate


class BIM_Trash:

    def GetResources(self):
        return {
            "Pixmap": "BIM_Trash",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Trash", "Move to Trash"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_Trash", "Moves the selected objects to the trash folder"
            ),
            "Accel": "Shift+Del",
        }

    def Activated(self):
        if AuraCADGui.Selection.getSelection():
            trash = AuraCAD.ActiveDocument.getObject("Trash")
            if not trash or not trash.isDerivedFrom("App::DocumentObjectGroup"):
                trash = AuraCAD.ActiveDocument.addObject("App::DocumentObjectGroup", "Trash")
                trash.Label = translate("BIM", "Trash")
            for obj in AuraCADGui.Selection.getSelection():
                trash.addObject(obj)
                # check for parents still there
                for par in obj.InList:
                    if (par != trash) and hasattr(par, "Group"):
                        if obj in par.Group:
                            if hasattr(par, "removeObject"):
                                par.removeObject(obj)
                            else:
                                g = par.Group
                                g.remove(obj)
                                par.Group = g
                obj.ViewObject.hide()

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v


AuraCADGui.addCommand("BIM_Trash", BIM_Trash())


class BIM_EmptyTrash:
    def GetResources(self):
        return {
            "Pixmap": "BIM_Trash",
            "MenuText": QT_TRANSLATE_NOOP("BIM_EmptyTrash", "Empty Trash"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_EmptyTrash",
                "Deletes from the trash bin all objects that are not used by any other",
            ),
        }

    def Activated(self):
        trash = AuraCAD.ActiveDocument.getObject("Trash")
        if trash and trash.isDerivedFrom("App::DocumentObjectGroup"):
            deletelist = []
            for obj in trash.Group:
                if (len(obj.InList) == 1) and (obj.InList[0] == trash):
                    deletelist.append(obj.Name)
                    deletelist.extend(self.getDeletableChildren(obj))
            if deletelist:
                AuraCAD.ActiveDocument.openTransaction("Empty Trash")
                for name in deletelist:
                    AuraCAD.ActiveDocument.removeObject(name)
                AuraCAD.ActiveDocument.commitTransaction()

    def getDeletableChildren(self, obj):
        deletelist = []
        for child in obj.OutList:
            if (len(child.InList) == 1) and (child.InList[0] == obj):
                deletelist.append(child.Name)
                deletelist.extend(self.getDeletableChildren(child))
        return deletelist
