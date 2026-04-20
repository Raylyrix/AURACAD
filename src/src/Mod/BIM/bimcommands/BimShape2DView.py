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

"""The BIM ShapeView command"""

import AuraCAD
import AuraCADGui

from draftguitools import gui_shape2dview

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate


class BIM_Shape2DView(gui_shape2dview.Shape2DView):

    def GetResources(self):
        d = super().GetResources()
        d["Pixmap"] = "Arch_BuildingPart_Tree"
        d["MenuText"] = QT_TRANSLATE_NOOP("BIM_Shape2DView", "Section View")
        d["Accel"] = "V, V"
        return d

    def proceed(self):
        """Proceed with the command if one object was selected."""
        self.proceed_BimShape2DView()  # Common
        if self.commitlist_BimShape2DView:
            commitlist = self.commitlist_BimShape2DView
            commitlist.append("AuraCAD.ActiveDocument.recompute()")
            self.commit(translate("draft", "Create 2D view"), self.commitlist_BimShape2DView)
        self.finish()

    def proceed_BimShape2DView(self):  # Common
        """Proceed with the command if one object was selected."""
        # difference from Draft: it sets InPlace to False
        import DraftVecUtils

        if self.call is not None:
            self.end_callbacks(self.call)
        faces = []
        objs = []
        view = AuraCADGui.ActiveDocument.ActiveView
        vec = view.getViewDirection().negative()
        sel = AuraCADGui.Selection.getSelectionEx()
        for s in sel:
            objs.append(s.Object)
            for e in s.SubElementNames:
                if "Face" in e:
                    faces.append(int(e[4:]) - 1)
        # print(objs, faces)
        self.objs_BimShape2DView = objs
        commitlist = []
        AuraCADGui.addModule("Draft")
        if len(objs) == 1 and faces:
            _cmd = "Draft.make_shape2dview"
            _cmd += "("
            _cmd += "AuraCAD.ActiveDocument." + objs[0].Name + ", "
            _cmd += DraftVecUtils.toString(vec) + ", "
            _cmd += "facenumbers=" + str(faces)
            _cmd += ")"
            # commitlist.append("sv = " + _cmd)
            # commitlist.append("sv.InPlace = False")
            commitlist.append("sv0 = " + _cmd)
            commitlist.append("sv0.InPlace = False")
        else:
            n = 0
            for o in objs:
                _cmd = "Draft.make_shape2dview"
                _cmd += "("
                _cmd += "AuraCAD.ActiveDocument." + o.Name + ", "
                _cmd += DraftVecUtils.toString(vec)
                _cmd += ")"
                commitlist.append("sv" + str(n) + " = " + _cmd)
                commitlist.append("sv" + str(n) + ".InPlace = False")
                n += 1
        if commitlist:
            # commitlist.append("AuraCAD.ActiveDocument.recompute()")
            self.commitlist_BimShape2DView = commitlist
        else:
            self.commitlist_BimShape2DView = None

        #    self.commit(translate("draft", "Create 2D view"),
        #                commitlist)
        # self.finish()


class BIM_Shape2DCut(BIM_Shape2DView):

    def GetResources(self):
        d = super().GetResources()
        d["Pixmap"] = "Arch_View_Cut"
        d["MenuText"] = QT_TRANSLATE_NOOP("BIM_Shape2DView", "Section Cut")
        d["Accel"] = "V, C"
        return d

    def proceed(self):
        # super().proceed()
        #'sv' is not passed from BIM_Shape2DView() to BIM_Shape2DCut()
        # AuraCADGui.doCommand("sv.ProjectionMode = \"Cutfaces\"")

        """Proceed with the command if one object was selected."""
        self.proceed_BimShape2DView()  # Common
        if self.commitlist_BimShape2DView:
            commitlist = self.commitlist_BimShape2DView

            # BIM_Shape2DCut specific
            # commitlist.append("sv.ProjectionMode = \"Cutfaces\"")
            objs = self.objs_BimShape2DView
            n = 0
            for o in objs:
                commitlist.append("sv" + str(n) + '.ProjectionMode = "Cutfaces"')
                n += 1
            commitlist.append("AuraCAD.ActiveDocument.recompute()")
            self.commit(translate("draft", "Create 2D Cut"), commitlist)
        self.finish()


AuraCADGui.addCommand("BIM_Shape2DView", BIM_Shape2DView())
AuraCADGui.addCommand("BIM_Shape2DCut", BIM_Shape2DCut())
