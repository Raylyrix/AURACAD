# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2025 Furgo                                              *
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

import AuraCAD as App
import Arch
import Draft
from bimtests import TestArchBase


class TestArchGrid(TestArchBase.TestArchBase):

    def test_makeGrid(self):
        """Test the makeGrid function."""
        operation = "Testing makeGrid..."
        self.printTestMessage(operation)

        # Call makeGrid with only the name parameter
        grid = Arch.makeGrid(name="TestGrid")
        self.assertIsNotNone(grid, "makeGrid failed to create a grid object.")
        self.assertEqual(grid.Label, "TestGrid", "Grid label is incorrect.")
