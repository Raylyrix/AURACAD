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

__title__ = "AuraCAD FEM mesh distance ViewProvider for the document object"
__author__ = "Stefan TrÃ¶ger"
__url__ = "https://www.AuraCAD.org"

## @package view_mesh_distance
#  \ingroup FEM
#  \brief view provider for mesh distance object

from femtaskpanels import task_mesh_distance
from . import view_base_femmeshelement


class VPMeshDistance(view_base_femmeshelement.VPBaseFemMeshElement):
    """
    A View Provider for the FemMeshDistance object
    """

    def setEdit(self, vobj, mode=0):
        return super().setEdit(vobj, mode, task_mesh_distance._TaskPanel)
