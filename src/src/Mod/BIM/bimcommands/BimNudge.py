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

"""BIM nudge commands"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate


class BIM_Nudge:
    # base class for the different nudge commands

    def getNudgeValue(self, mode):
        "mode can be dist, up, down, left, right. dist returns a float in mm, other modes return a 3D vector"

        from PySide import QtGui
        import WorkingPlane

        mw = AuraCADGui.getMainWindow()
        if mw:
            st = mw.statusBar()
            statuswidget = st.findChild(QtGui.QToolBar, "BIMStatusWidget")
            if statuswidget:
                nudgeValue = statuswidget.nudge.text().replace("&", "")
                dist = 0
                if "auto" in nudgeValue.lower():
                    unit = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt(
                        "UserSchema", 0
                    )
                    if unit in [2, 3, 5, 7]:
                        scale = [1.5875, 3.175, 6.35, 25.4, 152.4, 304.8]
                    else:
                        scale = [1, 5, 10, 50, 100, 500]
                    viewsize = (
                        AuraCADGui.ActiveDocument.ActiveView.getCameraNode()
                        .getViewVolume()
                        .getWidth()
                    )
                    if viewsize < 250:
                        dist = scale[0]
                    elif viewsize < 750:
                        dist = scale[1]
                    elif viewsize < 4500:
                        dist = scale[2]
                    elif viewsize < 8000:
                        dist = scale[3]
                    elif viewsize < 25000:
                        dist = scale[4]
                    else:
                        dist = scale[5]
                    # u = AuraCAD.Units.Quantity(dist,AuraCAD.Units.Length).UserString
                    statuswidget.nudge.setText(translate("BIM", "Auto"))
                else:
                    try:
                        dist = AuraCAD.Units.Quantity(nudgeValue)
                    except ValueError:
                        try:
                            dist = float(nudgeValue)
                        except ValueError:
                            return None
                    else:
                        dist = dist.Value
                if not dist:
                    return None
                if mode == "dist":
                    return dist
                wp = WorkingPlane.get_working_plane()
                if mode == "up":
                    return AuraCAD.Vector(wp.v).multiply(dist)
                if mode == "down":
                    return AuraCAD.Vector(wp.v).negative().multiply(dist)
                if mode == "right":
                    return AuraCAD.Vector(wp.u).multiply(dist)
                if mode == "left":
                    return AuraCAD.Vector(wp.u).negative().multiply(dist)
        return None

    def toStr(self, objs):
        "builds a string which is a list of objects"

        return "[" + ",".join(["AuraCAD.ActiveDocument." + obj.Name for obj in objs]) + "]"

    def getCenter(self, objs):
        "returns the center point of a group of objects"

        bb = None
        for obj in objs:
            if hasattr(obj, "Shape") and hasattr(obj.Shape, "BoundBox"):
                if not bb:
                    bb = obj.Shape.BoundBox
                else:
                    bb.add(obj.Shape.BoundBox)
        if bb:
            return bb.Center
        else:
            return None


class BIM_Nudge_Switch(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Switch", "Nudge Switch"),
            "Accel": "Alt+/",
        }

    def Activated(self):
        from PySide import QtGui

        mw = AuraCADGui.getMainWindow()
        if mw:
            st = mw.statusBar()
            statuswidget = st.findChild(QtGui.QToolBar, "BIMStatusWidget")
            if statuswidget:
                nudgeValue = statuswidget.nudge.text()
                nudge = self.getNudgeValue("dist")
                if nudge:
                    u = AuraCAD.Units.Quantity(nudge, AuraCAD.Units.Length).UserString
                    if "auto" in nudgeValue.lower():
                        statuswidget.nudge.setText(u)
                    else:
                        statuswidget.nudge.setText(translate("BIM", "Auto"))


class BIM_Nudge_Up(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Up", "Nudge Up"),
            "Accel": "Alt+Up",
        }

    def Activated(self):
        sel = AuraCADGui.Selection.getSelection()
        if sel:
            nudge = self.getNudgeValue("up")
            if nudge:
                AuraCADGui.addModule("Draft")
                AuraCADGui.doCommand(
                    "Draft.move(" + self.toStr(sel) + ",AuraCAD." + str(nudge) + ")"
                )
                AuraCADGui.doCommand("AuraCAD.ActiveDocument.recompute()")


class BIM_Nudge_Down(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Down", "Nudge Down"),
            "Accel": "Alt+Down",
        }

    def Activated(self):
        sel = AuraCADGui.Selection.getSelection()
        if sel:
            nudge = self.getNudgeValue("down")
            if nudge:
                AuraCADGui.addModule("Draft")
                AuraCADGui.doCommand(
                    "Draft.move(" + self.toStr(sel) + ",AuraCAD." + str(nudge) + ")"
                )
                AuraCADGui.doCommand("AuraCAD.ActiveDocument.recompute()")


class BIM_Nudge_Left(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Left", "Nudge Left"),
            "Accel": "Alt+Left",
        }

    def Activated(self):
        sel = AuraCADGui.Selection.getSelection()
        if sel:
            nudge = self.getNudgeValue("left")
            if nudge:
                AuraCADGui.addModule("Draft")
                AuraCADGui.doCommand(
                    "Draft.move(" + self.toStr(sel) + ",AuraCAD." + str(nudge) + ")"
                )
                AuraCADGui.doCommand("AuraCAD.ActiveDocument.recompute()")


class BIM_Nudge_Right(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Right", "Nudge Right"),
            "Accel": "Alt+Right",
        }

    def Activated(self):
        sel = AuraCADGui.Selection.getSelection()
        if sel:
            nudge = self.getNudgeValue("right")
            if nudge:
                AuraCADGui.addModule("Draft")
                AuraCADGui.doCommand(
                    "Draft.move(" + self.toStr(sel) + ",AuraCAD." + str(nudge) + ")"
                )
                AuraCADGui.doCommand("AuraCAD.ActiveDocument.recompute()")


class BIM_Nudge_Extend(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Extend", "Nudge Extend"),
            "Accel": "Alt+PgUp",
        }

    def Activated(self):
        sel = AuraCADGui.Selection.getSelection()
        if sel:
            nudge = self.getNudgeValue("dist")
            if nudge:
                for obj in sel:
                    if hasattr(obj, "Height"):
                        AuraCADGui.doCommand(
                            "AuraCAD.ActiveDocument."
                            + obj.Name
                            + ".Height="
                            + str(obj.Height.Value + nudge)
                        )
                        AuraCADGui.doCommand("AuraCAD.ActiveDocument.recompute()")


class BIM_Nudge_Shrink(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Shrink", "Nudge Shrink"),
            "Accel": "Alt+PgDown",
        }

    def Activated(self):
        sel = AuraCADGui.Selection.getSelection()
        if sel:
            nudge = self.getNudgeValue("dist")
            if nudge:
                for obj in sel:
                    if hasattr(obj, "Height"):
                        AuraCADGui.doCommand(
                            "AuraCAD.ActiveDocument."
                            + obj.Name
                            + ".Height="
                            + str(obj.Height.Value - nudge)
                        )
                        AuraCADGui.doCommand("AuraCAD.ActiveDocument.recompute()")


class BIM_Nudge_RotateLeft(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_RotateLeft", "Nudge Rotate Left"),
            "Accel": "Alt+,",
        }

    def Activated(self):

        import WorkingPlane

        sel = AuraCADGui.Selection.getSelection()
        if sel:
            center = self.getCenter(sel)
            if center:
                AuraCADGui.addModule("Draft")
                AuraCADGui.doCommand(
                    "Draft.rotate("
                    + self.toStr(sel)
                    + ",45,AuraCAD."
                    + str(center)
                    + ",AuraCAD."
                    + str(WorkingPlane.get_working_plane().axis)
                    + ")"
                )
                AuraCADGui.doCommand("AuraCAD.ActiveDocument.recompute()")


class BIM_Nudge_RotateRight(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_RotateRight", "Nudge Rotate Right"),
            "Accel": "Alt+.",
        }

    def Activated(self):

        import WorkingPlane

        sel = AuraCADGui.Selection.getSelection()
        if sel:
            center = self.getCenter(sel)
            if center:
                AuraCADGui.addModule("Draft")
                AuraCADGui.doCommand(
                    "Draft.rotate("
                    + self.toStr(sel)
                    + ",-45,AuraCAD."
                    + str(center)
                    + ",AuraCAD."
                    + str(WorkingPlane.get_working_plane().axis)
                    + ")"
                )
                AuraCADGui.doCommand("AuraCAD.ActiveDocument.recompute()")


AuraCADGui.addCommand("BIM_Nudge_Switch", BIM_Nudge_Switch())
AuraCADGui.addCommand("BIM_Nudge_Up", BIM_Nudge_Up())
AuraCADGui.addCommand("BIM_Nudge_Down", BIM_Nudge_Down())
AuraCADGui.addCommand("BIM_Nudge_Left", BIM_Nudge_Left())
AuraCADGui.addCommand("BIM_Nudge_Right", BIM_Nudge_Right())
AuraCADGui.addCommand("BIM_Nudge_Extend", BIM_Nudge_Extend())
AuraCADGui.addCommand("BIM_Nudge_Shrink", BIM_Nudge_Shrink())
AuraCADGui.addCommand("BIM_Nudge_RotateLeft", BIM_Nudge_RotateLeft())
AuraCADGui.addCommand("BIM_Nudge_RotateRight", BIM_Nudge_RotateRight())
