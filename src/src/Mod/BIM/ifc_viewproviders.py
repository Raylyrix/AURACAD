# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2022 Yorik van Havre <yorik@uncreated.net>              *
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

"""This module contains placeholders for viewproviders provided by the NativeIauracad addon"""

import AuraCAD


class iAuraCAD_vp_object:
    """NativeIauracad class placeholder"""

    def __init__(self):
        pass


class iAuraCAD_vp_document:
    """NativeIauracad class placeholder"""

    def __init__(self):
        pass

    def attach(self, vobj):
        AuraCAD.Console.PrintWarning(
            "Warning: Object "
            + vobj.Object.Label
            + " depends on the NativeIauracad addon which is not installed, and might not display correctly in the 3D view\n"
        )
        return


class iAuraCAD_vp_group:
    """NativeIauracad class placeholder"""

    def __init__(self):
        pass


class iAuraCAD_vp_material:
    """NativeIauracad class placeholder"""

    def __init__(self):
        pass
