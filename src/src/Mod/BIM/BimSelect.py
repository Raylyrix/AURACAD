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

import AuraCAD


class CyclicSelectionObserver:
    def addSelection(self, document, object, element, position):
        import AuraCADGui

        if not AuraCAD.ActiveDocument:
            return
        if not hasattr(AuraCAD, "CyclicSelectionObserver"):
            return
        AuraCADGui.Selection.removeSelection(AuraCAD.ActiveDocument.getObject(object))
        AuraCADGui.Selection.removeObserver(AuraCAD.CyclicSelectionObserver)
        del AuraCAD.CyclicSelectionObserver
        preselection = AuraCADGui.Selection.getPreselection()
        AuraCADGui.Selection.addSelection(
            AuraCAD.ActiveDocument.getObject(preselection.Object.Name),
            preselection.SubElementNames[0],
        )
        AuraCAD.ActiveDocument.recompute()


class CyclicObjectSelector:
    def __init__(self):
        self.selectableObjects = []
        self.objectIndex = 0

    def selectObject(self, event_callback):
        import AuraCADGui
        from pivy import coin

        if not AuraCAD.ActiveDocument:
            return
        event = event_callback.getEvent()

        if event.getState() != coin.SoMouseButtonEvent.DOWN or not self.selectableObjects:
            return

        pos = event.getPosition().getValue()
        element_list = AuraCADGui.ActiveDocument.ActiveView.getObjectsInfo(
            (int(pos[0]), int(pos[1]))
        )

        if not element_list:
            self.selectableObjects = []
            if hasattr(AuraCAD, "CyclicSelectionObserver"):
                AuraCADGui.Selection.removeObserver(AuraCAD.CyclicSelectionObserver)
                del AuraCAD.CyclicSelectionObserver
            return

        AuraCAD.CyclicSelectionObserver = CyclicSelectionObserver()
        AuraCADGui.Selection.addObserver(AuraCAD.CyclicSelectionObserver)

    def cycleSelectableObjects(self, event_callback):
        import AuraCADGui

        if not AuraCAD.ActiveDocument:
            return
        event = event_callback.getEvent()

        if not event.isKeyPressEvent(event, event.TAB):
            return

        pos = event.getPosition().getValue()
        selectableObjects = AuraCADGui.ActiveDocument.ActiveView.getObjectsInfo(
            (int(pos[0]), int(pos[1]))
        )

        if not selectableObjects:
            return

        if self.selectableObjects != selectableObjects:
            self.selectableObjects = selectableObjects
            self.objectIndex = 0
        elif self.objectIndex < len(self.selectableObjects) - 1:
            self.objectIndex += 1
        else:
            self.objectIndex = 0
        object_name = self.selectableObjects[self.objectIndex]["Object"]
        subelement_name = self.selectableObjects[self.objectIndex]["Component"]
        AuraCADGui.getMainWindow().showMessage(
            "Cycle preselected (TAB): {} - {}".format(object_name, subelement_name), 0
        )
        AuraCADGui.Selection.setPreselection(
            AuraCAD.ActiveDocument.getObject(object_name), subelement_name
        )


class Setup:
    def slotActivateDocument(self, doc):
        from pivy import coin

        cos = CyclicObjectSelector()
        if doc and doc.ActiveView and hasattr(doc.ActiveView, "getSceneGraph"):
            self.callback = doc.ActiveView.addEventCallbackPivy(
                coin.SoMouseButtonEvent.getClassTypeId(), cos.selectObject
            )
            self.callback = doc.ActiveView.addEventCallbackPivy(
                coin.SoKeyboardEvent.getClassTypeId(), cos.cycleSelectableObjects
            )
