# SPDX-License-Identifier: LGPL-2.1-or-later

add_library(AuraCADApp SHARED)

if(WIN32)
    add_definitions(-DauracadApp)
    add_definitions(-DBOOST_DYN_LINK)
endif(WIN32)

if(BUILD_TRACY_FRAME_PROFILER)
    add_definitions(-DBUILD_TRACY_FRAME_PROFILER)
endif()

if(CMAKE_BUILD_TYPE)
    add_definitions(-DCMAKE_BUILD_TYPE="${CMAKE_BUILD_TYPE}")
endif(CMAKE_BUILD_TYPE)

if(AuraCAD_RELEASE_SEH)
    add_definitions(-DHAVE_SEH)
endif(AuraCAD_RELEASE_SEH)

# This causes some problems with the resource files to be found, especially with the StartPage
IF(RESOURCEDIR)
    add_definitions(-DRESOURCEDIR="${RESOURCEDIR}")
ENDIF(RESOURCEDIR)

IF(LIBRARYDIR)
    add_definitions(-DLIBRARYDIR="${LIBRARYDIR}")
ENDIF(LIBRARYDIR)

IF(DOCDIR)
    add_definitions(-DDOCDIR="${DOCDIR}")
ENDIF(DOCDIR)

# -----------------------------------------------------------------------------

#write relevant cmake variables to a file for later access with python. Exported are all variables
#starting with BUILD. As the variable only exists if the user set it to ON a dict is useless, we
#use a python list for export.
set(_vars "const char CMakeVariables[] =\"cmake = [")
set(_delim "")
get_cmake_property(_variableNames VARIABLES)
foreach (_variableName ${_variableNames})
    if (${_variableName})
        STRING(REGEX MATCH "^[_]?[^_]*" _prefix "${_variableName}_")
        if(${_prefix} STREQUAL "BUILD")
            STRING(REPLACE "\\" "\\\\" _name ${_variableName})
            set(_vars "${_vars}${_delim}\\n\"\n\"\\\"${_name}\\\"")
            set(_delim ",")
        endif()
    endif ()
endforeach()
set(_vars "${_vars}]\\n\" \n;")
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/CMakeScript.hh "${_vars}" )

AuraCAD_copy_file_if_different(
    "${CMAKE_CURRENT_BINARY_DIR}/CMakeScript.hh"
    "${CMAKE_CURRENT_BINARY_DIR}/CMakeScript.h"
)

# -----------------------------------------------------------------------------

target_include_directories(
    AuraCADApp
    PRIVATE
    ${CMAKE_BINARY_DIR}
    ${CMAKE_BINARY_DIR}/src
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_CURRENT_BINARY_DIR}
)

target_include_directories(
    AuraCADApp
    SYSTEM
    PUBLIC
    ${QtCore_INCLUDE_DIRS}
    ${QtXml_INCLUDE_DIRS}
)

set(AuraCADApp_LIBS
    AuraCADBase
    ${Boost_LIBRARIES}
    fmt::fmt
)

if(BUILD_TRACY_FRAME_PROFILER)
    list(APPEND AuraCADApp_LIBS TracyClient)
endif()

list(APPEND AuraCADApp_LIBS
        ${QtCore_LIBRARIES}
        ${QtXml_LIBRARIES}
)

generate_from_py(ApplicationDirectories)
generate_from_py(Document)
generate_from_py(DocumentObject)
generate_from_py(Extension)
generate_from_py(ExtensionContainer)
generate_from_py(DocumentObjectExtension)
generate_from_py(GroupExtension)
generate_from_py(LinkBaseExtension)
generate_from_py(DocumentObjectGroup)
generate_from_py(GeoFeature)
generate_from_py(GeoFeatureGroupExtension)
generate_from_py(SuppressibleExtension)
generate_from_py(Metadata)
generate_from_py(OriginGroupExtension)
generate_from_py(Part)
generate_from_py(StringHasher)
generate_from_py(StringID)

generate_from_py(ComplexGeoData)
generate_from_py(PropertyContainer)
generate_from_py(Material)
generate_from_py(MeasureManager)

generate_embed_from_py(AuraCADInit InitScript.h)
generate_embed_from_py(AuraCADTest TestScript.h)

SET(AuraCADApp_Pyi_SRCS
    ApplicationDirectories.pyi
    Extension.pyi
    ExtensionContainer.pyi
    DocumentObjectExtension.pyi
    GroupExtension.pyi
    LinkBaseExtension.pyi
    Metadata.pyi
    DocumentObjectGroup.pyi
    DocumentObject.pyi
    GeoFeature.pyi
    GeoFeatureGroupExtension.pyi
    OriginGroupExtension.pyi
    SuppressibleExtension.pyi
    Part.pyi
    Document.pyi
    PropertyContainer.pyi
    ComplexGeoData.pyi
    Material.pyi
    MeasureManager.pyi
    StringHasher.pyi
    StringID.pyi
)
SOURCE_GROUP("Pyi" FILES ${AuraCADApp_Pyi_SRCS})

# The document stuff
SET(Document_CPP_SRCS
    Annotation.cpp
    BackupPolicy.cpp
    Document.cpp
    RecoverySnapshot.cpp
    DocumentObject.cpp
    Extension.cpp
    ExtensionPyImp.cpp
    DocumentObjectExtension.cpp
    DocumentObjectExtensionPyImp.cpp
    ExtensionContainer.cpp
    ExtensionContainerPyImp.cpp
    Graphviz.cpp
    GroupExtension.cpp
    GroupExtensionPyImp.cpp
    DocumentObjectFileIncluded.cpp
    DocumentObjectGroup.cpp
    DocumentObjectGroupPyImp.cpp
    GeoFeaturePyImp.cpp
    DocumentObjectPyImp.cpp
    DocumentObserver.cpp
    DocumentObserverPython.cpp
    DocumentPyImp.cpp
    Expression.cpp
    ExpressionTokenizer.cpp
    FeaturePython.cpp
    FeatureTest.cpp
    GeoFeature.cpp
    GeoFeatureGroupExtensionPyImp.cpp
    GeoFeatureGroupExtension.cpp
    ImagePlane.cpp
    OriginGroupExtensionPyImp.cpp
    OriginGroupExtension.cpp
    SuppressibleExtensionPyImp.cpp
    SuppressibleExtension.cpp
    PartPyImp.cpp
    Part.cpp
    Origin.cpp
    Path.cpp
    InventorObject.cpp
    Placement.cpp
    ProjectFile.cpp
    Datums.cpp
    Range.cpp
    Transactions.cpp
    TransactionalObject.cpp
    VRMLObject.cpp
    MaterialObject.cpp
    MergeDocuments.cpp
    TextDocument.cpp
    Link.cpp
    LinkBaseExtensionPyImp.cpp
    VarSet.cpp
    License.h
)

SET(Document_HPP_SRCS
    Annotation.h
    BackupPolicy.h
    Document.h
    RecoverySnapshot.h
    DocumentObject.h
    Extension.h
    ExtensionContainer.h
    GroupExtension.h
    DocumentObjectExtension.h
    DocumentObjectFileIncluded.h
    DocumentObjectGroup.h
    DocumentObserver.h
    DocumentObserverPython.h
    Expression.h
    ExpressionParser.h
    ExpressionTokenizer.h
    ExpressionVisitors.h
    FeatureCustom.h
    FeaturePython.h
    FeaturePythonPyImp.h
    FeaturePythonPyImp.inl
    FeatureTest.h
    GeoFeature.h
    GeoFeatureGroupExtension.h
    ImagePlane.h
    OriginGroupExtension.h
    SuppressibleExtension.h
    Part.h
    Origin.h
    Path.h
    InventorObject.h
    Placement.h
    ProjectFile.h
    Datums.h
    Range.h
    Transactions.h
    TransactionalObject.h
    VRMLObject.h
    MaterialObject.h
    MergeDocuments.h
    TextDocument.h
    VarSet.h
    Link.h
)
SET(Document_SRCS
    ${Document_CPP_SRCS}
    ${Document_HPP_SRCS}
)
SOURCE_GROUP("Document" FILES ${Document_SRCS})

# The property stuff
SET(Properties_CPP_SRCS
    DynamicProperty.cpp
    ObjectIdentifier.cpp
    Property.cpp
    PropertyContainer.cpp
    PropertyContainerPyImp.cpp
    PropertyFile.cpp
    PropertyGeo.cpp
    PropertyLinks.cpp
    PropertyPythonObject.cpp
    PropertyStandard.cpp
    PropertyUnits.cpp
    PropertyExpressionEngine.cpp
)
SET(Properties_HPP_SRCS
    DynamicProperty.h
    ObjectIdentifier.h
    Property.h
    PropertyContainer.h
    PropertyFile.h
    PropertyGeo.h
    PropertyLinks.h
    PropertyPythonObject.h
    PropertyStandard.h
    PropertyUnits.h
    PropertyExpressionEngine.h
    PropertyOverrides.h
)
SET(Properties_SRCS
    ${Properties_CPP_SRCS}
    ${Properties_HPP_SRCS}
)
SOURCE_GROUP("Properties" FILES ${Properties_SRCS})

SET(AuraCADApp_CPP_SRCS
    ${Document_CPP_SRCS}
    ${Properties_CPP_SRCS}
    Application.cpp
    ApplicationDirectories.cpp
    ApplicationDirectoriesPyImp.cpp
    ApplicationPy.cpp
    AutoTransaction.cpp
    Branding.cpp
    CleanupProcess.cpp
    ColorModel.cpp
    ComplexGeoData.cpp
    ComplexGeoDataPyImp.cpp
    ConsoleQtBridge.cpp
    TranslationQtBridge.cpp
    ElementMap.cpp
    Enumeration.cpp
    IndexedName.cpp
    MappedElement.cpp
    MappedName.cpp
    Material.cpp
    MaterialPyImp.cpp
    MeasureManager.cpp
    MeasureManagerPyImp.cpp
    Metadata.cpp
    MetadataPyImp.cpp
    ElementNamingUtils.cpp
    ProgramInformation.cpp
    SafeMode.cpp
    Services.cpp
    StringHasher.cpp
    StringHasherPyImp.cpp
    StringIDPyImp.cpp
)

SET(AuraCADApp_HPP_SRCS
    ${Document_HPP_SRCS}
    ${Properties_HPP_SRCS}
    Application.h
    ApplicationDirectories.h
    AutoTransaction.h
    Branding.h
    CleanupProcess.h
    ColorModel.h
    ComplexGeoData.h
    ElementMap.h
    Enumeration.h
    IndexedName.h
    MappedName.h
    MappedElement.h
    Material.h
    MeasureManager.h
    Metadata.h
    ElementNamingUtils.h
    ProgramInformation.h
    Services.h
    StringHasher.h
    MainThreadSignal.h
)

# auto-generate resource file with all available translations
set (AuraCADApp_TR_QRC ${CMAKE_CURRENT_BINARY_DIR}/Resources/App_translation.qrc)
qt_find_and_add_translation(QM_SRCS "Resources/translations/*_*.ts"
    ${CMAKE_CURRENT_BINARY_DIR}/Resources/translations)
qt_find_and_add_translation(QM_SRCS "${CMAKE_SOURCE_DIR}/src/Base/Resources/translations/*_*.ts"
    ${CMAKE_CURRENT_BINARY_DIR}/Resources/translations)
qt_create_resource_file(${AuraCADApp_TR_QRC} ${QM_SRCS})
qt_add_resources(AuraCADApp_QRC_SRCS ${AuraCADApp_TR_QRC})

SET(AuraCADApp_SRCS
    ${AuraCADApp_QRC_SRCS}
    ${AuraCADApp_CPP_SRCS}
    ${AuraCADApp_HPP_SRCS}
    ${AuraCADApp_Pyi_SRCS}
    AuraCADInit.py
    AuraCADTest.py
    PreCompiled.h
)

if(AuraCAD_USE_PCH)
    target_precompile_headers(AuraCADApp PRIVATE
        $<$<COMPILE_LANGUAGE:CXX>:"${CMAKE_CURRENT_LIST_DIR}/PreCompiled.h">
    )
endif(AuraCAD_USE_PCH)

target_sources(AuraCADApp PRIVATE ${AuraCADApp_SRCS})
target_link_libraries(AuraCADApp ${AuraCADApp_LIBS})

if (MSVC)
    target_compile_definitions(AuraCADApp PRIVATE WIN32_LEAN_AND_MEAN)
    target_compile_options(AuraCADApp PRIVATE /wd4251 /wd4273 /wd4275)
endif()

if (AuraCAD_WARN_ERROR)
    target_compile_warn_error(AuraCADApp)
endif()

add_dependencies(AuraCADApp AuraCAD_version)

SET_BIN_DIR(AuraCADApp AuraCADApp)

if(WIN32)
    INSTALL(TARGETS AuraCADApp
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
else(WIN32)
    INSTALL(TARGETS AuraCADApp
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
endif(WIN32)
