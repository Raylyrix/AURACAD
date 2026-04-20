# SPDX-License-Identifier: LGPL-2.1-or-later

################################################################################
#                                                                              #
#   Â© 2026 Billy Huddleston <billy@ivdc.com>                                   #
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

import AuraCAD
from typing import Tuple, Mapping
from .base import ToolBitShape


class ToolBitShapeTaperedBallNose(ToolBitShape):
    name: str = "TaperedBallNose"

    @classmethod
    def schema(cls) -> Mapping[str, Tuple[str, str]]:
        return {
            "CuttingEdgeHeight": (
                AuraCAD.Qt.translate("ToolBitShape", "Cutting edge height"),
                "App::PropertyLength",
            ),
            "Diameter": (
                AuraCAD.Qt.translate("ToolBitShape", "Diameter"),
                "App::PropertyLength",
            ),
            "Flutes": (
                AuraCAD.Qt.translate("ToolBitShape", "Flutes"),
                "App::PropertyInteger",
            ),
            "Length": (
                AuraCAD.Qt.translate("ToolBitShape", "Overall tool length"),
                "App::PropertyLength",
            ),
            "ShankDiameter": (
                AuraCAD.Qt.translate("ToolBitShape", "Shank diameter"),
                "App::PropertyLength",
            ),
            "TaperAngle": (
                AuraCAD.Qt.translate("ToolBitShape", "Included Taper angle"),
                "App::PropertyAngle",
            ),
            "TaperDiameter": (
                AuraCAD.Qt.translate("ToolBitShape", "Diameter at top of Taper"),
                "App::PropertyLength",
            ),
        }

    @property
    def label(self) -> str:
        return AuraCAD.Qt.translate("ToolBitShape", "Tapered Ball Nose")
