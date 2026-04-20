# SPDX-License-Identifier: LGPL-2.1-or-later

configure_file(AuraCAD.rc.cmake ${CMAKE_CURRENT_BINARY_DIR}/AuraCAD.rc)
configure_file(AuraCADCmd.rc.cmake ${CMAKE_CURRENT_BINARY_DIR}/AuraCADCmd.rc)
file(COPY icon.ico DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

######################## AuraCADMain ########################
if(BUILD_GUI)

    SET(AuraCAD_SRCS
        ${CMAKE_CURRENT_BINARY_DIR}/AuraCAD.rc
        icon.ico
        MainGui.cpp
    )

    SET(AuraCAD_LIBS
        AuraCADGui
    )

    if(NOT BUILD_DYNAMIC_LINK_PYTHON)
        # executables have to be linked against python libraries,
        # because extension modules are not.
        list(APPEND AuraCAD_LIBS
            ${Python3_LIBRARIES}
        )
    endif(NOT BUILD_DYNAMIC_LINK_PYTHON)

    add_executable(AuraCADMain WIN32 ${AuraCAD_SRCS})
    target_link_libraries(AuraCADMain ${AuraCAD_LIBS})
    if(BUILD_TEST)
        add_dependencies(AuraCADMain TestSources)
        add_dependencies(AuraCADMain TestGuiSources)
    endif()
    if (AuraCAD_WARN_ERROR)
        target_compile_warn_error(AuraCADMain)
    endif()

    SET_BIN_DIR(AuraCADMain AuraCAD)

    if(WIN32)
        INSTALL(TARGETS AuraCADMain
            RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        )
    elseif(APPLE AND NOT BUILD_WITH_CONDA)
        INSTALL(TARGETS AuraCADMain
        RUNTIME DESTINATION MacOS
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        )
    else()
        INSTALL(TARGETS AuraCADMain
            RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        )
    endif()
endif(BUILD_GUI)
######################## AuraCADMainCmd ########################

SET(AuraCADMainCmd_SRCS
    ${CMAKE_CURRENT_BINARY_DIR}/AuraCADCmd.rc
    icon.ico
    MainCmd.cpp
)

add_executable(AuraCADMainCmd ${AuraCADMainCmd_SRCS})
if(BUILD_TEST)
    add_dependencies(AuraCADMainCmd TestSources)
endif()

SET(AuraCADMainCmd_LIBS
    AuraCADApp
    ${QtCore_LIBRARIES}
    ${QtXml_LIBRARIES}
)

if(NOT BUILD_DYNAMIC_LINK_PYTHON)
    # executables have to be linked against python libraries,
    # because extension modules are not.
    list(APPEND AuraCADMainCmd_LIBS
        ${Python3_LIBRARIES}
    )
endif(NOT BUILD_DYNAMIC_LINK_PYTHON)

target_link_libraries(AuraCADMainCmd
    ${AuraCADMainCmd_LIBS}
)
if (AuraCAD_WARN_ERROR)
    target_compile_warn_error(AuraCADMainCmd)
endif()

SET_BIN_DIR(AuraCADMainCmd AuraCADCmd)

if(WIN32)
    INSTALL(TARGETS AuraCADMainCmd
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
elseif(APPLE AND NOT BUILD_WITH_CONDA)
    INSTALL(TARGETS AuraCADMainCmd
        RUNTIME DESTINATION MacOS
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
else()
    INSTALL(TARGETS AuraCADMainCmd
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
endif()

######################## AuraCADMainPy ########################

SET(AuraCADMainPy_SRCS
    MainPy.cpp
)

add_library(AuraCADMainPy SHARED ${AuraCADMainPy_SRCS})

target_link_libraries(AuraCADMainPy AuraCADApp)
if (AuraCAD_WARN_ERROR)
    target_compile_warn_error(AuraCADMainPy)
endif()

SET_BIN_DIR(AuraCADMainPy AuraCAD)
SET_PYTHON_PREFIX_SUFFIX(AuraCADMainPy)

if(WIN32)
    INSTALL(TARGETS AuraCADMainPy
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
else(WIN32)
    INSTALL(TARGETS AuraCADMainPy
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
endif(WIN32)

######################## AuraCADGuiPy ########################
if(BUILD_GUI)

    SET(AuraCADGuiPy_SRCS
        AuraCADGuiPy.cpp
    )

    add_library(AuraCADGuiPy SHARED ${AuraCADGuiPy_SRCS})

    target_link_libraries(AuraCADGuiPy AuraCADGui)
    if (AuraCAD_WARN_ERROR)
        target_compile_warn_error(AuraCADGuiPy)
    endif()

    SET_BIN_DIR(AuraCADGuiPy AuraCADGui)
    SET_PYTHON_PREFIX_SUFFIX(AuraCADGuiPy)
    if(WIN32)
        # Name clash with target "AuraCADGui"
        # Must be called "AuraCADGuiPy_d" and "AuraCADGuiPy" to work so override default
        set_target_properties(AuraCADGuiPy PROPERTIES PDB_NAME_DEBUG "AuraCADGuiPy_d")
        set_target_properties(AuraCADGuiPy PROPERTIES PDB_NAME_RELEASE "AuraCADGuiPy")
    endif(WIN32)

    if(WIN32)
        INSTALL(TARGETS AuraCADGuiPy
            RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        )
    else(WIN32)
        INSTALL(TARGETS AuraCADGuiPy
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        )
    endif(WIN32)
endif(BUILD_GUI)
