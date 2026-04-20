# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2023 Mario Passaglia <mpassaglia[at]cbc.uba.ar>         *
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
# **************************************************************************/

import AuraCAD
import unittest


class TestStringHasher(unittest.TestCase):
    def setUp(self):
        self.strHash = AuraCAD.StringHasher()
        self.strID = self.strHash.getID("A")

    def testInit(self):
        with self.assertRaises(TypeError):
            AuraCAD.StringHasher(0)

    def testGetID(self):
        with self.assertRaises(ValueError):
            self.strHash.getID(0)

    def testStringHasherIsSame(self):
        with self.assertRaises(TypeError):
            self.strHash.isSame(0)

    def testStringIDIsSame(self):
        with self.assertRaises(TypeError):
            self.strID.isSame(0)
