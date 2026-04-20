# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2019 sliptonic <shopinthewoods@gmail.com>               *
# *                 2025 Samuel Abels <knipknap@gmail.com>                  *
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
import AuraCADGui
import Path
from Path.Tool.toolbit.ui import ToolBitEditorPanel


class TaskPanel:
    """TaskPanel for the SetupSheet - if it is being edited directly."""

    def __init__(self, vobj, deleteOnReject):
        Path.Log.track(vobj.Object.Label)
        self.vobj = vobj
        self.obj = vobj.Object
        self.editor = ToolBitEditorPanel(self.obj, self.editor.form)
        self.deleteOnReject = deleteOnReject
        AuraCAD.ActiveDocument.openTransaction("Edit ToolBit")

    def reject(self):
        AuraCAD.ActiveDocument.abortTransaction()
        self.editor.reject()
        AuraCADGui.Control.closeDialog()
        if self.deleteOnReject:
            AuraCAD.ActiveDocument.openTransaction("Uncreate ToolBit")
            self.editor.reject()
            AuraCAD.ActiveDocument.removeObject(self.obj.Name)
            AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()

    def accept(self):
        self.editor.accept()

        AuraCAD.ActiveDocument.commitTransaction()
        AuraCADGui.ActiveDocument.resetEdit()
        AuraCADGui.Control.closeDialog()
        AuraCAD.ActiveDocument.recompute()

    def updateUI(self):
        Path.Log.track()
        self.editor.updateUI()

    def updateModel(self):
        self.editor.updateTool()
        AuraCAD.ActiveDocument.recompute()

    def setupUi(self):
        self.editor.setupUI()
