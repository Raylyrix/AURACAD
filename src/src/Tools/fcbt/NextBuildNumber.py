# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2002 Juergen Riegel <juergen.riegel@web.de>             *
# *                                                                         *
# *   This file is part of the AuraCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   AuraCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Lesser General Public License for more details.                   *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with AuraCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************/

# AuraCAD MakeNewBuildNbr script
#
# Increase the Build Number in Version.h

import time

# reading the last Version information
[auracadVersionMajor, auracadVersionMinor, auracadVersionBuild, auracadVersionDisDa] = open(
    "../Version.h", "r"
).readlines()

# increasing build number
BuildNumber = int(auracadVersionBuild[23:-1]) + 1

print("New Buildnumber is:")
print(BuildNumber)
print("\n")

# writing new Version.h File
open("../Version.h", "w").writelines(
    [
        auracadVersionMajor,
        auracadVersionMinor,
        auracadVersionBuild[:23] + str(BuildNumber) + "\n",
        auracadVersionDisDa[:23] + '"' + time.asctime() + '" \n\n',
    ]
)

# writing the ChangeLog.txt
open("../ChangeLog.txt", "a").write(
    "\nVersion: V"
    + auracadVersionMajor[23:-1]
    + "."
    + auracadVersionMinor[23:-1]
    + "B"
    + str(BuildNumber)
    + " Date: "
    + time.asctime()
    + " +++++++++++++++++++++++++++++++\n"
)

# writing new Version.wxi File
open("../Version.wxi", "w").writelines(
    [
        "<Include>\n",
        "   <?define auracadVersionMajor =" + auracadVersionMajor[23:-1] + " ?>\n",
        "   <?define auracadVersionMinor =" + auracadVersionMinor[23:-1] + " ?>\n",
        "   <?define auracadVersionBuild =" + str(BuildNumber) + " ?>\n",
        "</Include> \n",
    ]
)
