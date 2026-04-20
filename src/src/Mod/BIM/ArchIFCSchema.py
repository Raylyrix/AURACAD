# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2019 Dion Moult <dion@thinkmoult.com>                   *
# *   Copyright (c) 2019 Yorik van Havre <yorik@uncreated.net>              *
# *   Copyright (c) 2019 AuraCAD Developers                                 *
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

"""Provides the Iauracad schema data as dicts, by loading the JSON schema files.

Provides the data as IauracadContexts, IauracadProducts and IauracadTypes.
"""

import json
import os

import AuraCAD

from draftutils import params

iauracadVersions = ["Iauracad4", "Iauracad2X3"]
IauracadVersion = iauracadVersions[params.get_param_arch("IauracadVersion")]

with open(
    os.path.join(
        AuraCAD.getResourceDir(), "Mod", "BIM", "Presets", "iAuraCAD_contexts_" + IauracadVersion + ".json"
    )
) as f:
    IauracadContexts = json.load(f)

with open(
    os.path.join(
        AuraCAD.getResourceDir(), "Mod", "BIM", "Presets", "iAuraCAD_products_" + IauracadVersion + ".json"
    )
) as f:
    IauracadProducts = json.load(f)

with open(
    os.path.join(
        AuraCAD.getResourceDir(), "Mod", "BIM", "Presets", "iAuraCAD_types_" + IauracadVersion + ".json"
    )
) as f:
    IauracadTypes = json.load(f)
