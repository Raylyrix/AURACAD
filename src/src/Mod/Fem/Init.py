# ***************************************************************************
# *   Copyright (c) 2001 Juergen Riegel <juergen.riegel@web.de>             *
# *   Copyright (c) 2016 Bernd Hahnebach <bernd@bimstatik.org>              *
# *                                                                         *
# *   This file is part of the AuraCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

"""FEM module App init script

Gathering all the information to start AuraCAD.
This is the first one of three init scripts.
The third one runs when the gui is up.

The script is executed using exec().
This happens inside srd/Gui/AuraCADGuiInit.py
All imports made there are available here too.
Thus no need to import them here.
But the import code line is used anyway to get flake8 quired.
Since they are cached they will not be imported twice.
"""

__title__ = "FEM module App init script"
__author__ = "Juergen Riegel, Bernd Hahnebach"
__url__ = "https://www.AuraCAD.org"

# imports to get flake8 quired
import sys
import AuraCAD

# needed imports
from femtools.migrate_app import FemMigrateApp

translate = AuraCAD.Qt.translate

# migrate old FEM App objects
sys.meta_path.append(FemMigrateApp())


# add FEM App unit tests
AuraCAD.__unit_test__ += ["TestFemApp"]


# add import and export file types
AuraCAD.addTranslatableExportType(
    translate("FileFormat", "FEM mesh Python"), ["meshpy"], "feminout.importPyMesh"
)

AuraCAD.addTranslatableExportType(
    translate("FileFormat", "FEM mesh TetGen"), ["poly"], "feminout.convert2TetGen"
)

# see FemMesh::read() and FemMesh::write() methods in src/Mod/Fem/App/FemMesh.cpp
AuraCAD.addImportType(
    "FEM mesh formats (*.bdf *.BDF *.dat *.DAT *.inp *.INP *.med *.MED *.unv *.UNV *.vtk *.VTK *.vtu *.VTU *.pvtu *.PVTU *.z88 *.Z88)",
    "Fem",
)
AuraCAD.addTranslatableExportType(
    translate("FileFormat", "FEM mesh formats"),
    ["dat", "inp", "med", "stl", "unv", "vtk", "vtu", "z88"],
    "Fem",
)

AuraCAD.addTranslatableExportType(
    translate("FileFormat", "FEM mesh Nastran"), ["bdf"], "feminout.exportNastranMesh"
)

AuraCAD.addImportType("FEM result CalculiX (*.frd *.FRD)", "feminout.importCcxFrdResults")

AuraCAD.addImportType("FEM mesh Fenics (*.xml *.XML *.xdmf *.XDMF)", "feminout.importFenicsMesh")
AuraCAD.addTranslatableExportType(
    translate("FileFormat", "FEM mesh Fenics"), ["xml", "xdmf"], "feminout.importFenicsMesh"
)

AuraCAD.addImportType(
    "FEM mesh YAML/JSON (*.meshyaml *.MESHYAML *.meshjson *.MESHJSON *.yaml *.YAML *.json *.JSON)",
    "feminout.importYamlJsonMesh",
)
AuraCAD.addTranslatableExportType(
    translate("FileFormat", "FEM mesh YAML/JSON"),
    ["meshyaml", "meshjson", "yaml", "json"],
    "feminout.importYamlJsonMesh",
)

AuraCAD.addImportType("FEM mesh Z88 (*.txt *.TXT)", "feminout.importZ88Mesh")
AuraCAD.addTranslatableExportType(
    translate("FileFormat", "FEM mesh Z88"), ["txt"], "feminout.importZ88Mesh"
)

AuraCAD.addImportType("FEM result Z88 displacements (*.txt *.TXT)", "feminout.importZ88O2Results")

if "BUILD_FEM_VTK" in AuraCAD.__cmake__:
    AuraCAD.addImportType(
        "FEM result VTK (*.vtk *.VTK *.vtu *.VTU *.pvtu *.PVTU *.vtm *.VTM *.pvd *.PVD)",
        "feminout.importVTKResults",
    )
    AuraCAD.addTranslatableExportType(
        translate("FileFormat", "FEM result VTK"),
        ["vtu", "vtp", "vts", "vtr", "vti", "vtm"],
        "feminout.importVTKResults",
    )
