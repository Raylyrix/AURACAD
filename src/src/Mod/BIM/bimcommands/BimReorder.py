# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2021 Yorik van Havre <yorik@uncreated.net>              *
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


"""This module contains AuraCAD commands for the BIM workbench"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate


class BIM_Reorder:
    def GetResources(self):
        return {
            "Pixmap": "BIM_Reorder",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Reorder", "Reorder Children"),
            # 'Accel': "R, D",
            "ToolTip": QT_TRANSLATE_NOOP("BIM_Reorder", "Reorders children of the selected object"),
        }

    def Activated(self):
        if len(AuraCADGui.Selection.getSelection()) == 1:
            obj = AuraCADGui.Selection.getSelection()[0]
            if hasattr(obj, "Group"):
                if obj.getTypeIdOfProperty("Group") == "App::PropertyLinkList":
                    AuraCADGui.Control.showDialog(BIM_Reorder_TaskPanel(obj))
                    return
        AuraCAD.Console.PrintError(
            translate("BIM", "You must choose a group object before using this command") + "\n"
        )


class BIM_Reorder_TaskPanel:

    def __init__(self, obj):
        from PySide import QtGui

        self.obj = obj
        self.form = AuraCADGui.PySideUic.loadUi(":/ui/dialogReorder.ui")
        self.form.setWindowIcon(QtGui.QIcon(":/icons/BIM_Reorder.svg"))
        self.form.pushButton.clicked.connect(self.form.listWidget.sortItems)
        for child in self.obj.Group:
            i = QtGui.QListWidgetItem(child.Label)
            i.setIcon(child.ViewObject.Icon)
            i.setToolTip(child.Name)
            self.form.listWidget.addItem(i)

    def accept(self):
        names = [
            self.form.listWidget.item(i).toolTip() for i in range(self.form.listWidget.count())
        ]
        group = [AuraCAD.ActiveDocument.getObject(n) for n in names]
        AuraCAD.ActiveDocument.openTransaction("Reorder children")
        self.obj.Group = group
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCADGui.doCommand("AuraCAD.ActiveDocument.recompute()")
        return self.reject()

    def reject(self):
        AuraCADGui.Control.closeDialog()
        AuraCAD.ActiveDocument.recompute()
        return True


AuraCADGui.addCommand("BIM_Reorder", BIM_Reorder())
