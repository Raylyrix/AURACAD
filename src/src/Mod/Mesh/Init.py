# SPDX-License-Identifier: LGPL-2.1-or-later

# AuraCAD init script of the Mesh module
# (c) 2004 Werner Mayer LGPL

import AuraCAD

translate = AuraCAD.Qt.translate

# Append the open handler
AuraCAD.addImportType("STL Mesh (*.stl *.STL *.ast *.AST)", "Mesh")
AuraCAD.addImportType("Binary Mesh (*.bms *.BMS)", "Mesh")
AuraCAD.addImportType("Alias Mesh (*.obj *.OBJ)", "Mesh")
AuraCAD.addImportType("Object File Format Mesh (*.off *.OFF)", "Mesh")
AuraCAD.addImportType("Stanford Triangle Mesh (*.ply *.PLY)", "Mesh")
AuraCAD.addImportType("Simple Model Format (*.smf *.SMF)", "Mesh")
AuraCAD.addImportType("3D Manufacturing Format (*.3mf *.3MF)", "Mesh")

AuraCAD.addTranslatableExportType(translate("FileFormat", "STL Mesh"), ["stl", "ast"], "Mesh")
AuraCAD.addTranslatableExportType(translate("FileFormat", "Binary Mesh"), ["bms"], "Mesh")

#: Translation note: "Alias" in this case is a product/format name and should not be translated
AuraCAD.addTranslatableExportType(translate("FileFormat", "Alias Mesh"), ["obj"], "Mesh")

#: Translation note: "Object File Format" is the official name and should not be translated
AuraCAD.addTranslatableExportType(
    translate("FileFormat", "Object File Format Mesh"), ["off"], "Mesh"
)

AuraCAD.addExportType("Stanford Triangle Mesh (*.ply)", "Mesh")
AuraCAD.addExportType("Additive Manufacturing Format (*.amf)", "Mesh")
AuraCAD.addExportType("Simple Model Format (*.smf)", "Mesh")
AuraCAD.addExportType("3D Manufacturing Format (*.3mf)", "Mesh")

AuraCAD.__unit_test__ += ["MeshTestsApp"]
