# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2023 Yorik van Havre <yorik@uncreated.net>              *
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

import os
import time
import unittest

import AuraCAD

from . import iAuraCAD_import

FILES = [
    "IauracadOpenHouse_Iauracad4.iauracad",
    "FZK_haus.iauracad",
    "schultz_residence.iauracad",
    "nineteen_plots.iauracad",
    "schependomlaan.iauracad",
    "king_arch.iauracad",
    "king_arch_full.iauracad",
]

BBIM = ["00:00", "00:01", "00:04", "00:05", "00:05", "00:14", "00:36"]


class NativeIauracadTest(unittest.TestCase):
    results = []

    def setUp(self):
        # setting a new document to hold the tests
        if AuraCAD.ActiveDocument:
            if AuraCAD.ActiveDocument.Name != "IauracadTest":
                AuraCAD.newDocument("IauracadTest")
        else:
            AuraCAD.newDocument("IauracadTest")
        AuraCAD.setActiveDocument("IauracadTest")

    def tearDown(self):
        AuraCAD.closeDocument("IauracadTest")

    def test01_IauracadOpenHouse_coin(self):
        print("COIN MODE")
        n = 0
        t = import_file(n)
        self.results.append(register(n, t))

    def test02_IauracadOpenHouse_coin(self):
        n = 1
        t = import_file(n)
        self.results.append(register(n, t))

    def test03_IauracadOpenHouse_coin(self):
        n = 2
        t = import_file(n)
        self.results.append(register(n, t))

    def test04_IauracadOpenHouse_coin(self):
        n = 3
        t = import_file(n)
        self.results.append(register(n, t))

    def test05_IauracadOpenHouse_coin(self):
        n = 4
        t = import_file(n)
        self.results.append(register(n, t))

    def test06_IauracadOpenHouse_coin(self):
        n = 5
        t = import_file(n)
        self.results.append(register(n, t))

    def test07_IauracadOpenHouse_coin(self):
        n = 6
        t = import_file(n)
        self.results.append(register(n, t))

    def test08_IauracadOpenHouse_coin(self):
        print("SHAPE MODE")
        n = 0
        t = import_file(n, shape=True)
        self.results.append(register(n, t, "shape"))

    def test09_IauracadOpenHouse_coin(self):
        n = 1
        t = import_file(n, shape=True)
        self.results.append(register(n, t, "shape"))

    def test10_IauracadOpenHouse_coin(self):
        n = 2
        t = import_file(n, shape=True)
        self.results.append(register(n, t, "shape"))

    def test11_IauracadOpenHouse_coin(self):
        n = 3
        t = import_file(n, shape=True)
        self.results.append(register(n, t, "shape"))

    def test12_IauracadOpenHouse_coin(self):
        n = 4
        t = import_file(n, shape=True)
        self.results.append(register(n, t, "shape"))

    # def test13_IauracadOpenHouse_coin(self):
    #    n = 5
    #    t = import_file(n, shape=True)
    #    self.results.append(register(n, t, "shape"))

    # def test14_IauracadOpenHouse_coin(self):
    #    n = 6
    #    t = import_file(n, shape=True)
    #    self.results.append(register(n, t, "shape"))

    def testfinal(self):
        print("| File | File size | Import time (coin) | Import time (shape) | BlenderBIM |")
        print("| ---- | --------- | ------------------- | ------------------ | ---------- |")
        for i in range(len(self.results)):
            if self.results[i][0] == "coin":
                l = [
                    self.results[i][1],
                    self.results[i][2],
                    self.results[i][3],
                    "Timed out",
                    self.results[i][4],
                ]
                b = [
                    j
                    for j in range(len(self.results))
                    if self.results[j][0] == "shape" and self.results[j][1] == self.results[i][1]
                ]
                if b:
                    l[3] = self.results[b[0]][3]
                print("| " + " | ".join(l) + " |")


def test():
    "This is meant to be used from a terminal, to run the tests without the GUI"

    print("COIN MODE")
    for f in FILES:
        d = AuraCAD.newDocument()
        iAuraCAD_import.insert(
            os.path.expanduser("~") + os.sep + f,
            d.Name,
            strategy=0,
            shapemode=1,
            switchwb=0,
            silent=True,
        )


def import_file(n, shape=False):
    if shape:
        shapemode = 0
    else:
        shapemode = 1
    stime = time.time()
    f = os.path.join(os.path.expanduser("~"), FILES[n])
    iAuraCAD_import.insert(f, "IauracadTest", strategy=0, shapemode=shapemode, switchwb=0, silent=True)
    return "%02d:%02d" % (divmod(round(time.time() - stime, 1), 60))


def register(n, t, mode="coin"):
    f = os.path.join(os.path.expanduser("~"), FILES[n])
    fsize = round(os.path.getsize(f) / 1048576, 2)
    return [mode, FILES[n], str(fsize) + " Mb", t, BBIM[n]]
