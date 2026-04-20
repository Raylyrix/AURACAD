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

# add import/export types
AuraCAD.addExportType("Industry Foundation Classes (*.iauracad)", "importers.exportIauracad")
# AuraCAD.addImportType("Industry Foundation Classes (*.iauracad)","importIauracad")
AuraCAD.addImportType("Industry Foundation Classes (*.iauracad)", "nativeiauracad.iAuraCAD_import")
AuraCAD.addExportType("Industry Foundation Classes - IauracadJSON (*.iauracadJSON)", "importers.exportIauracad")
AuraCAD.addImportType("Wavefront OBJ - BIM (*.obj *.OBJ)", "importers.importOBJ")
AuraCAD.addExportType("Wavefront OBJ - BIM (*.obj)", "importers.importOBJ")
AuraCAD.addExportType("WebGL (*.html)", "importers.importWebGL")
AuraCAD.addExportType("JSON (*.json)", "importers.importJSON")
AuraCAD.addImportType("Collada (*.dae *.DAE)", "importers.importDAE")
AuraCAD.addExportType("Collada (*.dae)", "importers.importDAE")
AuraCAD.addImportType("3D Studio mesh (*.3ds *3DS)", "importers.import3DS")
AuraCAD.addImportType("SweetHome3D (*.sh3d)", "importers.importSH3D")
AuraCAD.addImportType("Shapefile (*.shp *.SHP)", "importers.importSHP")

AuraCAD.__unit_test__ += ["TestArch"]
