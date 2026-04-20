# SPDX-License-Identifier: LGPL-2.1-or-later

add_subdirectory(App)

if(BUILD_GUI)
    add_subdirectory(Gui)
endif(BUILD_GUI)

SET(MaterialScripts_Files
    Init.py
    InitGui.py
    importauracadMat.py
    MaterialEditor.py
    TestMaterialsApp.py
    TestMaterialsGui.py
    Templatematerial.yml
)

# SOURCE_GROUP("MaterialScripts" FILES ${MaterialScripts_Files})
SET(MaterialTools_Files
    materialtools/__init__.py
    materialtools/cardutils.py
    materialtools/MaterialModels.py
)

# collect all the material cards:
SET(MaterialLib_Files
    Resources/Materials/Standard/Default.auracadMat
    Resources/Materials/Standard/Aggregate/Concrete-EN-C35_45.auracadMat
    Resources/Materials/Standard/Aggregate/Concrete-Generic.auracadMat
    Resources/Materials/Standard/Aggregate/Reinforcement-FIB-B500.auracadMat
    Resources/Materials/Standard/Carbon/Graphite.auracadMat
    Resources/Materials/Standard/Glass/Glass-E-GlassFibre.auracadMat
    Resources/Materials/Standard/Glass/Glass-Generic.auracadMat
    Resources/Materials/Standard/Glass/Glass-S2-GlassFibre.auracadMat
    Resources/Materials/Standard/Metal/Alloys/Invar-Generic.auracadMat
    Resources/Materials/Standard/Metal/Aluminum/AlMg3F24.auracadMat
    Resources/Materials/Standard/Metal/Aluminum/AlMgSi1F31.auracadMat
    Resources/Materials/Standard/Metal/Aluminum/Aluminum-6061-T6.auracadMat
    Resources/Materials/Standard/Metal/Aluminum/Aluminum-7075-T6.auracadMat
    Resources/Materials/Standard/Metal/Aluminum/Aluminum-Generic.auracadMat
    Resources/Materials/Standard/Metal/Aluminum/AlZn4-5Mg1F35.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-102.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-122a.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-122b.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-150.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-220.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-230.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-443.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-464.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-510.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-614.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-647.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-655.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-706.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-715.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-955.auracadMat
    Resources/Materials/Standard/Metal/Copper/Copper-Generic.auracadMat
    Resources/Materials/Standard/Metal/Iron/Iron-Generic.auracadMat
    Resources/Materials/Standard/Metal/Steel/CalculiX-Steel.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-15CrNi6.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-17CrNiMo6.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-1C22.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-1C35.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-1C45.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-1C60.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-20NiCrMo2.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-28Mn6.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-2C10.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-30CrNiMo8.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-34CrNiMo6.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-36CrNiMo4.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-36NiCrMo16.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-3C15.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-3C22.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-3C35.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-3V45.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-C10.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-C15.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-C22E.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-C25E.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-C30E.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-C40E.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-C50E.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-C55E.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-C60E.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-E295-GC.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-E295.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-E335-GC.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-E335.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-E360-GC.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-E360.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJL-100.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJL-150.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJL-200.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJL-250.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJL-300.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJL-350.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJMB-350-10.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJMB-550-4.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJMB-650-2.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJMW-350-4.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJMW-360-12.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJMW-400-5.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJMW-450-7.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJS-400-15.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJS-500-7.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJS-600-3.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJS-700-2.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-EN-GJS-800-1.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-G16Mn5.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-G200.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-G20Mn5.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-G230.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-G260.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-G300.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-G30Mn5.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-Generic.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S185.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S235JO.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S235JR.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S235JRG1.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S260NC.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S275JO.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S275JR.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S275N.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S335JO.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S335JR.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S335N.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S340MC.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S355J2G3.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S380MC.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S420MC.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S420N.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S460MC.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S460N.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S500MC.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S550MC.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-S690MC.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-St-37-2K.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-St-E-255.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-St-E-315.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-St-E-380.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-St-E-460.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-St-E-500.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-X2CrNiMoN17-13-3.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-X2CrNiN24-4.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-X39CrMo17-1.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-X3CrNiMo13-14.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-X5CrNi18-10.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-X5CrNiMo17-12-2.auracadMat
    Resources/Materials/Standard/Metal/Steel/Steel-X6CrNiTi18-10.auracadMat
    Resources/Materials/Standard/Metal/Titanium/Ti-6Al-4V.auracadMat
    Resources/Materials/Standard/Thermoplast/ABS-Generic.auracadMat
    Resources/Materials/Standard/Thermoplast/Acrylic-Glass-Generic.auracadMat
    Resources/Materials/Standard/Thermoplast/PA6-Generic.auracadMat
    Resources/Materials/Standard/Thermoplast/PEEK-Generic.auracadMat
    Resources/Materials/Standard/Thermoplast/PET-Generic.auracadMat
    Resources/Materials/Standard/Thermoplast/PLA-Generic.auracadMat
    Resources/Materials/Standard/Thermoplast/PMMA-Generic.auracadMat
    Resources/Materials/Standard/Thermoplast/POM-Homopolymer-Generic.auracadMat
    Resources/Materials/Standard/Thermoplast/POM-Copolymer-Generic.auracadMat
    Resources/Materials/Standard/Thermoplast/PP-Generic.auracadMat
    Resources/Materials/Standard/Thermoplast/PTFE-Generic.auracadMat
    Resources/Materials/Standard/Thermoplast/PVC-Generic.auracadMat
    Resources/Materials/Standard/Thermoplast/PC-Molded.auracadMat
    Resources/Materials/Standard/Wood/Wood-Generic.auracadMat
)

SET(FluidMaterial_Files
    Resources/Materials/Fluid/None.auracadMat
    Resources/Materials/Fluid/Air.auracadMat
    Resources/Materials/Fluid/Argon.auracadMat
    "Resources/Materials/Fluid/Carbon Dioxide.auracadMat"
    Resources/Materials/Fluid/Nitrogen.auracadMat
    Resources/Materials/Fluid/Water.auracadMat
)

SET(AppearanceLib_Files
    Resources/Materials/Appearance/Aluminum.auracadMat
    Resources/Materials/Appearance/Brass.auracadMat
    Resources/Materials/Appearance/Bronze.auracadMat
    Resources/Materials/Appearance/Chrome.auracadMat
    Resources/Materials/Appearance/Copper.auracadMat
    Resources/Materials/Appearance/Default.auracadMat
    Resources/Materials/Appearance/Emerald.auracadMat
    Resources/Materials/Appearance/Gold.auracadMat
    Resources/Materials/Appearance/Jade.auracadMat
    Resources/Materials/Appearance/Metalized.auracadMat
    "Resources/Materials/Appearance/Neon GNC.auracadMat"
    "Resources/Materials/Appearance/Neon PHC.auracadMat"
    Resources/Materials/Appearance/Obsidian.auracadMat
    Resources/Materials/Appearance/Pewter.auracadMat
    Resources/Materials/Appearance/Plaster.auracadMat
    Resources/Materials/Appearance/Plastic.auracadMat
    Resources/Materials/Appearance/Ruby.auracadMat
    Resources/Materials/Appearance/Satin.auracadMat
    "Resources/Materials/Appearance/Shiny Plastic.auracadMat"
    Resources/Materials/Appearance/Silver.auracadMat
    Resources/Materials/Appearance/Steel.auracadMat
    Resources/Materials/Appearance/Stone.auracadMat
    Resources/Materials/Appearance/Wood.auracadMat
)

SET(PatternLib_Files
    Resources/Materials/Patterns/PAT/Diagonal4.auracadMat
    Resources/Materials/Patterns/PAT/Diagonal5.auracadMat
    Resources/Materials/Patterns/PAT/Diamond.auracadMat
    Resources/Materials/Patterns/PAT/Diamond2.auracadMat
    Resources/Materials/Patterns/PAT/Diamond4.auracadMat
    Resources/Materials/Patterns/PAT/Horizontal5.auracadMat
    Resources/Materials/Patterns/PAT/Square.auracadMat
    Resources/Materials/Patterns/PAT/Vertical5.auracadMat
    "Resources/Materials/Patterns/Pattern Files/aluminum.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/brick01.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/concrete.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/cross.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/cuprous.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/diagonal1.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/diagonal2.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/earth.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/general_steel.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/glass.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/hatch45L.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/hatch45R.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/hbone.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/line.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/plastic.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/plus.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/simple.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/solid.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/square.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/steel.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/titanium.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/wood.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/woodgrain.auracadMat"
    "Resources/Materials/Patterns/Pattern Files/zinc.auracadMat"
)

SET(MachiningLib_Files
    Resources/Materials/Machining/AluminumCastAlloy.auracadMat
    Resources/Materials/Machining/AluminumWroughtAlloy.auracadMat
    Resources/Materials/Machining/AusteniticStainlessSteel.auracadMat
    Resources/Materials/Machining/BalsaWood.auracadMat
    Resources/Materials/Machining/GrayCastIron.auracadMat
    Resources/Materials/Machining/HardWood.auracadMat
    Resources/Materials/Machining/LowAlloySteel.auracadMat
    Resources/Materials/Machining/MalleableCastIron.auracadMat
    Resources/Materials/Machining/MildSteel.auracadMat
    Resources/Materials/Machining/MDF.auracadMat
    Resources/Materials/Machining/ParticleBoard.auracadMat
    Resources/Materials/Machining/SoftWood.auracadMat
    Resources/Materials/Machining/ToolSteel.auracadMat
)

SET(MaterialTestLib_Files
    "Resources/Materials/Test/Test Material.auracadMat"
)

SET(MaterialModel_Files
    Resources/Models/Architectural/Architectural.yml
    Resources/Models/Architectural/ArchitecturalRendering.yml
    Resources/Models/Costs/Costs.yml
    Resources/Models/Electromagnetic/Electromagnetic.yml
    Resources/Models/Fluid/Fluid.yml
    Resources/Models/Legacy/Father.yml
    Resources/Models/Legacy/MaterialStandard.yml
    Resources/Models/Machining/Machinability.yml
    Resources/Models/Mechanical/ArrudaBoyce.yml
    Resources/Models/Mechanical/Density.yml
    Resources/Models/Mechanical/Hardness.yml
    Resources/Models/Mechanical/IsotropicLinearElastic.yml
    Resources/Models/Mechanical/IsotropicLinearElasticArrays.yml
    Resources/Models/Mechanical/LinearElastic.yml
    Resources/Models/Mechanical/LinearElasticArrays.yml
    Resources/Models/Mechanical/MooneyRivlin.yml
    Resources/Models/Mechanical/NeoHooke.yml
    Resources/Models/Mechanical/OgdenN1.yml
    Resources/Models/Mechanical/OgdenN2.yml
    Resources/Models/Mechanical/OgdenN3.yml
    Resources/Models/Mechanical/OgdenYld2004p18.yml
    Resources/Models/Mechanical/OrthotropicLinearElastic.yml
    Resources/Models/Mechanical/PolynomialN1.yml
    Resources/Models/Mechanical/PolynomialN2.yml
    Resources/Models/Mechanical/PolynomialN3.yml
    Resources/Models/Mechanical/ReducedPolynomialN1.yml
    Resources/Models/Mechanical/ReducedPolynomialN2.yml
    Resources/Models/Mechanical/ReducedPolynomialN3.yml
    Resources/Models/Mechanical/Toughness.yml
    Resources/Models/Mechanical/ToughnessArrays.yml
    Resources/Models/Mechanical/Yeoh.yml
    Resources/Models/Patterns/PAT.yml
    "Resources/Models/Patterns/Pattern File.yml"
    "Resources/Models/Render Workbench/RenderAppleseed.yml"
    "Resources/Models/Render Workbench/RenderCarpaint.yml"
    "Resources/Models/Render Workbench/RenderCycles.yml"
    "Resources/Models/Render Workbench/RenderDiffuse.yml"
    "Resources/Models/Render Workbench/RenderDisney.yml"
    "Resources/Models/Render Workbench/RenderEmission.yml"
    "Resources/Models/Render Workbench/RenderGlass.yml"
    "Resources/Models/Render Workbench/RenderLuxcore.yml"
    "Resources/Models/Render Workbench/RenderLuxrender.yml"
    "Resources/Models/Render Workbench/RenderMixed.yml"
    "Resources/Models/Render Workbench/RenderOspray.yml"
    "Resources/Models/Render Workbench/RenderPbrt.yml"
    "Resources/Models/Render Workbench/RenderPovray.yml"
    "Resources/Models/Render Workbench/RenderSubstancePBR.yml"
    "Resources/Models/Render Workbench/RenderTexture.yml"
    "Resources/Models/Render Workbench/RenderWB.yml"
    Resources/Models/Rendering/AdvancedRendering.yml
    Resources/Models/Rendering/BasicRendering.yml
    Resources/Models/Rendering/TextureRendering.yml
    Resources/Models/Rendering/VectorRendering.yml
    "Resources/Models/Test/Test Model.yml"
    Resources/Models/Thermal/Thermal.yml
)

set(MaterialTest_Files
    materialtests/__init__.py
    materialtests/TestModels.py
    materialtests/TestMaterials.py
    materialtests/TestMaterialCreation.py
    materialtests/TestMaterialDocument.py
    materialtests/TestMaterialFilter.py
)

ADD_CUSTOM_TARGET(MaterialTest ALL
    SOURCES ${MaterialTest_Files}
)

AuraCAD_target_copy_resource(MaterialTest
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/Mod/Material
    ${MaterialTest_Files})

set(MaterialPythonTestData_Files
    materialtests/Materials/TestAcrylicLegacy.auracadMat
    materialtests/Materials/TestAluminumAppearance.auracadMat
    materialtests/Materials/TestAluminumMixed.auracadMat
    materialtests/Materials/TestAluminumPhysical.auracadMat
    materialtests/Materials/TestBrassAppearance.auracadMat
)

ADD_CUSTOM_TARGET(MaterialPythonTestData ALL
    SOURCES ${MaterialPythonTestData_Files}
)

AuraCAD_target_copy_resource(MaterialPythonTestData
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/Mod/Material
    ${MaterialPythonTestData_Files})

ADD_CUSTOM_TARGET(MaterialScripts ALL
    SOURCES ${MaterialScripts_Files} ${Material_QRC_SRCS}
)

AuraCAD_target_copy_resource(MaterialScripts
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/Mod/Material
    ${MaterialScripts_Files})

INSTALL(FILES ${MaterialScripts_Files} DESTINATION Mod/Material)

ADD_CUSTOM_TARGET(MaterialToolsLib ALL
    SOURCES ${MaterialTools_Files}
)

AuraCAD_target_copy_resource(MaterialToolsLib
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/Mod/Material
    ${MaterialTools_Files})

INSTALL(FILES ${MaterialTools_Files} DESTINATION Mod/Material/materialtools)

ADD_CUSTOM_TARGET(MaterialLib ALL
    SOURCES ${MaterialLib_Files}
)
ADD_CUSTOM_TARGET(FluidMaterialLib ALL
    SOURCES ${FluidMaterial_Files}
)
ADD_CUSTOM_TARGET(AppearanceLib ALL
    SOURCES ${AppearanceLib_Files}
)
ADD_CUSTOM_TARGET(PatternLib ALL
    SOURCES ${PatternLib_Files}
)
ADD_CUSTOM_TARGET(MaterialTestLib ALL
    SOURCES ${MaterialTestLib_Files}
)
ADD_CUSTOM_TARGET(MachiningLib ALL
    SOURCES ${MachiningLib_Files}
)
ADD_CUSTOM_TARGET(MaterialModelLib ALL
    SOURCES ${MaterialModel_Files}
)

# When a target copies files to different output directories then apparently it always builds the project
# which is very annoying. So, the trick is to split this into two targets to avoid this behaviour.
AuraCAD_target_copy_resource(MaterialLib
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_DATADIR}/Mod/Material/
    ${MaterialLib_Files})
AuraCAD_target_copy_resource(FluidMaterialLib
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_DATADIR}/Mod/Material/
    ${FluidMaterial_Files})
AuraCAD_target_copy_resource(AppearanceLib
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_DATADIR}/Mod/Material/
    ${AppearanceLib_Files})
AuraCAD_target_copy_resource(PatternLib
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_DATADIR}/Mod/Material/
    ${PatternLib_Files})
AuraCAD_target_copy_resource(MachiningLib
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_DATADIR}/Mod/Material/
    ${MachiningLib_Files})
AuraCAD_target_copy_resource(MaterialTestLib
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_DATADIR}/Mod/Material/
    ${MaterialTestLib_Files})
AuraCAD_target_copy_resource(MaterialModelLib
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_DATADIR}/Mod/Material/
    ${MaterialModel_Files})

INSTALL(
    FILES ${MaterialTest_Files}
    DESTINATION Mod/Material/materialtests
)

INSTALL(
    FILES ${MaterialPythonTestData_Files}
    DESTINATION Mod/Material/materialtests/Materials
)

foreach(file ${MaterialLib_Files} ${FluidMaterial_Files} ${AppearanceLib_Files} ${PatternLib_Files} ${MachiningLib_Files} ${MaterialTestLib_Files} ${MaterialModel_Files})
    get_filename_component(filepath ${file} DIRECTORY)
    INSTALL(
        FILES ${file}
        DESTINATION ${CMAKE_INSTALL_DATADIR}/Mod/Material/${filepath}
    )
endforeach()
