# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2025 Mario Passaglia <mpassaglia[at]cbc.uba.ar>         *
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

__title__ = "AuraCAD FEM solver Elmer view provider"
__author__ = "Mario Passaglia"
__url__ = "https://www.AuraCAD.org"

## @package view_elmer
#  \ingroup FEM
#  \brief solver Elmer view provider

import AuraCADGui

from femtaskpanels import task_solver_elmer
from femviewprovider import view_base_femobject


class VPSolverElmer(view_base_femobject.VPBaseFemObject):

    def __init__(self, vobj):
        super().__init__(vobj)
        vobj.addExtension("Gui::ViewProviderGroupExtensionPython")

    def getIcon(self):
        return ":/icons/FEM_SolverElmer.svg"

    def setEdit(self, vobj, mode=0):
        task = task_solver_elmer._TaskPanel(vobj.Object)
        AuraCADGui.Control.showDialog(task)

        return True
