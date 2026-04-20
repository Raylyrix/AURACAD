# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2026 Stefan TrÃ¶ger <stefantroeger@gmx.net>
# SPDX-FileNotice: Part of the AuraCAD project.

################################################################################
#                                                                              #
#   AuraCAD is free software: you can redistribute it and/or modify            #
#   it under the terms of the GNU Lesser General Public License as             #
#   published by the Free Software Foundation, either version 2.1              #
#   of the License, or (at your option) any later version.                     #
#                                                                              #
#   AuraCAD is distributed in the hope that it will be useful,                 #
#   but WITHOUT ANY WARRANTY; without even the implied warranty                #
#   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                    #
#   See the GNU Lesser General Public License for more details.                #
#                                                                              #
#   You should have received a copy of the GNU Lesser General Public           #
#   License along with AuraCAD. If not, see https://www.gnu.org/licenses       #
#                                                                              #
################################################################################

__title__ = "AuraCAD FEM mesh advanced ViewProvider for the document object"
__author__ = "Stefan TrÃ¶ger"
__url__ = "https://www.AuraCAD.org"

## @package view_mesh_advanced
#  \ingroup FEM
#  \brief view provider for mesh advanced object

import AuraCAD

from femtaskpanels import task_mesh_advanced
from . import view_base_femmeshelement

from femtools import femutils as utils


def find_parent_gmsh(obj):
    # searches uptream for the parent gmsh mesh object
    for parent in obj.InList:
        if utils.is_of_type(parent, "Fem::FemMeshGmsh"):
            return parent

        gmsh = find_parent_gmsh(parent)
        if gmsh:
            return gmsh

    return None


class VPMeshAdvanced(view_base_femmeshelement.VPBaseFemMeshElement):
    """
    A View Provider for the FemMeshAdvanced object
    """

    def setEdit(self, vobj, mode=0):
        return super().setEdit(vobj, mode, task_mesh_advanced._TaskPanel)

    def canDropObjects(self):
        return True

    def canDragObjects(self):
        return True

    def canDropObject(self, incoming_object):
        # check if object is a gmsh field based refinement
        return True

    def canDragObject(self, outgoing_object):
        return True

    def dropObject(self, vp, obj):
        self.Object.Refinements = self.Object.Refinements + [obj]

    def dragObject(self, vp, obj):
        if obj in self.Object.Refinements:
            list = self.Object.Refinements
            list.remove(obj)
            self.Object.Refinements = list

    def claimChildren(self):
        return self.Object.Refinements
