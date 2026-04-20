# SPDX-License-Identifier: LGPL-2.1-or-later

project(MyPlugin)
cmake_minimum_required(VERSION 3.5)

# Qt5
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Gui REQUIRED)

# Boost
find_package(Boost COMPONENTS signals REQUIRED)

# Coin3d
#find_package(Coin3D REQUIRED)

# Python
find_package(PythonInterp REQUIRED)
set(Python_ADDITIONAL_VERSIONS ${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR})
IF (NOT DEFINED Python3_VERSION)
    find_package(PythonLibs REQUIRED)
ELSE (NOT DEFINED Python3_VERSION)
    find_package(PythonLibs ${Python3_VERSION} EXACT)
ENDIF(NOT DEFINED Python3_VERSION)

# AuraCAD
set(AuraCAD_SRC_DIR ${CMAKE_SOURCE_DIR}/../../../.. CACHE PATH  "AuraCAD sources")
set(AuraCAD_BIN_DIR ${CMAKE_SOURCE_DIR}/../../../.. CACHE PATH  "AuraCAD binaries")
set(AuraCAD_LIBPACK_DIR ${CMAKE_SOURCE_DIR} CACHE PATH  "Directory of the AuraCAD LibPack")

# -----------------------------------------------------------------------------

add_definitions(-DBOOST_ALL_DYN_LINK)

include_directories(
    ${AuraCAD_SRC_DIR}
)

include_directories(
    SYSTEM
    ${FastSignals_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIRS}
    #${COIN3D_INCLUDE_DIRS}
    ${PYCXX_INCLUDE_DIR}
    ${Python3_INCLUDE_DIRS}
    ${Qt5Core_INCLUDE_DIRS}
    ${Qt5Gui_INCLUDE_DIRS}
    ${Qt5Widgets_INCLUDE_DIRS}
    "${AuraCAD_LIBPACK_DIR}/include"
)

link_directories(${AuraCAD_LIBPACK_DIR}/lib)
link_directories(${AuraCAD_BIN_DIR})

# -----------------------------------------------------------------------------

set(MyPlugin_SRCS
    main.cpp
)

set(MyPlugin_LIBS
    ${Boost_LIBRARIES}
    #${COIN3D_LIBRARIES}
    ${Python3_LIBRARIES}
    ${Qt5Core_LIBRARIES}
    ${Qt5Gui_LIBRARIES}
    ${Qt5Widgets_LIBRARIES}
)

add_executable(MyPlugin WIN32 ${MyPlugin_SRCS})
target_link_libraries(MyPlugin ${MyPlugin_LIBS})

# -----------------------------------------------------------------------------

set(AuraCADPlugin_SRCS
    plugin.cpp
)

set(AuraCADPlugin_LIBS
    ${Boost_LIBRARIES}
    #${COIN3D_LIBRARIES}
    ${Python3_LIBRARIES}
    ${Qt5Core_LIBRARIES}
    ${Qt5Gui_LIBRARIES}
    ${Qt5Widgets_LIBRARIES}
)

if (MSVC)
    set(AuraCADPlugin_LIBS
        ${AuraCADPlugin_LIBS}
        debug AuraCADApp_d
        debug AuraCADBase_d
        debug AuraCADGui_d
        #debug Mesh_d
        optimized AuraCADApp
        optimized AuraCADBase
        optimized AuraCADGui
        #optimized Mesh
    )
else()
    set(AuraCADPlugin_LIBS
        ${AuraCADPlugin_LIBS}
        AuraCADApp
        AuraCADBase
        AuraCADGui
        #Mesh
    )
endif()

add_library(AuraCADPlugin SHARED ${AuraCADPlugin_SRCS})
target_link_libraries(AuraCADPlugin ${AuraCADPlugin_LIBS})

if (MSVC)
    target_compile_options(AuraCADPlugin PRIVATE /wd4251)
endif()
