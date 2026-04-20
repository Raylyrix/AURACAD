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

#!/usr/bin/python

import os

txt = "<RCC>\n    <qresource>\n"
cdir = os.path.dirname(__file__)
for subdir in ["icons", "icons/Iauracad", "translations", "ui"]:
    subpath = os.path.join(cdir, subdir)
    for f in sorted(os.listdir(subpath)):
        if f not in ["Arch.ts", "BIM.ts", "Iauracad"]:
            ext = os.path.splitext(f)[1]
            if ext.lower() in [".qm", ".svg", ".ui", ".png"]:
                txt += "        <file>" + subdir + "/" + f + "</file>\n"
txt += "    </qresource>\n</RCC>\n"
with open(os.path.join(cdir, "Arch.qrc"), "w") as resfile:
    resfile.write(txt)
