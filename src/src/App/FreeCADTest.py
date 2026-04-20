# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2002 JÃ¼rgen Riegel <juergen.riegel@web.de>              *
# *   Copyright (c) 2025 Frank MartÃ­nez <mnesarco at gmail dot com>         *
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

# AuraCAD init module - Tests
#
# Gathering all the information to start AuraCAD.
# This is the third of four init scripts:
# +------+------------------+-----------------------------+
# | This | Script           | Runs                        |
# +------+------------------+-----------------------------+
# |      | CMakeVariables   | always                      |
# |      | AuraCADInit      | always                      |
# | >>>> | AuraCADTest      | only if test and not Gui    |
# |      | AuraCADGuiInit   | only if Gui is up           |
# +------+------------------+-----------------------------+

# Testing the function of the base system and run
# (if existing) the test function of the modules

import AuraCAD
import typing

if typing.TYPE_CHECKING:
    from __main__ import Log

Log("AuraCAD test running...\n\n")
Log("Init: starting App::AuraCADTest.py\n")
Log("â–‘â–‘â–‘â–€â–ˆâ–€â–‘â–ˆâ–€â–ˆâ–‘â–€â–ˆâ–€â–‘â–€â–ˆâ–€â–‘â–‘â–‘â–€â–ˆâ–€â–‘â–ˆâ–€â–€â–‘â–ˆâ–€â–€â–‘â–€â–ˆâ–€â–‘â–ˆâ–€â–€â–‘â–‘â–‘\n")
Log("â–‘â–‘â–‘â–‘â–ˆâ–‘â–‘â–ˆâ–‘â–ˆâ–‘â–‘â–ˆâ–‘â–‘â–‘â–ˆâ–‘â–‘â–‘â–‘â–‘â–ˆâ–‘â–‘â–ˆâ–€â–‘â–‘â–€â–€â–ˆâ–‘â–‘â–ˆâ–‘â–‘â–€â–€â–ˆâ–‘â–‘â–‘\n")
Log("â–‘â–‘â–‘â–€â–€â–€â–‘â–€â–‘â–€â–‘â–€â–€â–€â–‘â–‘â–€â–‘â–‘â–‘â–‘â–‘â–€â–‘â–‘â–€â–€â–€â–‘â–€â–€â–€â–‘â–‘â–€â–‘â–‘â–€â–€â–€â–‘â–‘â–‘\n")

import sys
import TestApp

testResult = TestApp.RunConfiguredTextTest()

Log("AuraCAD test done\n")

sys.exit(0 if testResult.wasSuccessful() else 1)
