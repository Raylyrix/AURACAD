
SET(Examples_Files
    Schenkel.stp
    draft_test_objects.auracadStd
    EngineBlock.auracadStd
    PartDesignExample.auracadStd
    BIMExample.auracadStd
    FEMExample.auracadStd
    AssemblyExample.auracadStd
    ArchDetail.auracadStd
    auracadPAT.pat
    osifont.license
    osifont-lgpl3fe.ttf
)

ADD_CUSTOM_TARGET(Example_data ALL
    SOURCES ${Examples_Files}
)

# 0001097: CMake stops with error "Circular ... <- ... dependency dropped."
if(NOT "${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    AuraCAD_copy_sources(Example_data "${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_DATADIR}/examples" ${Examples_Files})
endif()

if (WIN32 AND AuraCAD_LIBPACK_USE)
    # pivy
    foreach (it ${AuraCAD_LIBPACK_PIVY_COIN})
        get_filename_component(libfile ${it} NAME)
        set(out "${CMAKE_BINARY_DIR}/lib/pivy/${libfile}")
        add_custom_command(
            DEPENDS   ${it}
            OUTPUT    ${out}
            COMMAND   ${CMAKE_COMMAND}
            ARGS      -E copy_if_different ${it} ${out}
            MAIN_DEPENDENCY ${it}
            COMMENT   "Copy file to ${out}"
    )
    endforeach (it)
    SOURCE_GROUP("pivy" FILES ${AuraCAD_LIBPACK_PIVY_COIN})

    # shiboken
    foreach (it ${AuraCAD_LIBPACK_SHIBOKEN})
        get_filename_component(libfile ${it} NAME)
        set(out "${CMAKE_BINARY_DIR}/lib/${libfile}")
        add_custom_command(
            DEPENDS   ${it}
            OUTPUT    ${out}
            COMMAND   ${CMAKE_COMMAND}
            ARGS      -E copy_if_different ${it} ${out}
            MAIN_DEPENDENCY ${it}
            COMMENT   "Copy file to ${out}"
    )
    endforeach (it)
    SOURCE_GROUP("Shiboken" FILES ${AuraCAD_LIBPACK_SHIBOKEN})

    # PySide
    foreach (it ${AuraCAD_LIBPACK_PYSIDE})
        get_filename_component(libfile ${it} NAME)
        set(out "${CMAKE_BINARY_DIR}/lib/PySide/${libfile}")
        add_custom_command(
            DEPENDS   ${it}
            OUTPUT    ${out}
            COMMAND   ${CMAKE_COMMAND}
            ARGS      -E copy_if_different ${it} ${out}
            MAIN_DEPENDENCY ${it}
            COMMENT   "Copy file to ${out}"
    )
    endforeach (it)
    SOURCE_GROUP("PySide" FILES ${AuraCAD_LIBPACK_PYSIDE})

    # PySide tools
    foreach (it ${AuraCAD_LIBPACK_PYSIDEUIC})
        get_filename_component(libpath ${it} PATH)
        set(src "${AuraCAD_LIBPACK_PYSIDEUIC_REL}/${it}")
        if("${libpath}" STREQUAL "pysideuic")
            set(AuraCAD_LIBPACK_PYSIDEUIC_TOP ${AuraCAD_LIBPACK_PYSIDEUIC_TOP} ${src})
        elseif("${libpath}" STREQUAL "pysideuic/Compiler")
            set(AuraCAD_LIBPACK_PYSIDEUIC_CMP ${AuraCAD_LIBPACK_PYSIDEUIC_CMP} ${src})
        elseif("${libpath}" STREQUAL "pysideuic/port_v2")
            set(AuraCAD_LIBPACK_PYSIDEUIC_PV2 ${AuraCAD_LIBPACK_PYSIDEUIC_PV2} ${src})
        elseif("${libpath}" STREQUAL "pysideuic/port_v3")
            set(AuraCAD_LIBPACK_PYSIDEUIC_PV3 ${AuraCAD_LIBPACK_PYSIDEUIC_PV3} ${src})
        elseif("${libpath}" STREQUAL "pysideuic/widget-plugins")
            set(AuraCAD_LIBPACK_PYSIDEUIC_WPL ${AuraCAD_LIBPACK_PYSIDEUIC_WPL} ${src})
        else()
            set(AuraCAD_LIBPACK_PYSIDEUIC_OTH ${AuraCAD_LIBPACK_PYSIDEUIC_OTH} ${src})
        endif()
        set(AuraCAD_LIBPACK_PYSIDEUIC_ABS ${AuraCAD_LIBPACK_PYSIDEUIC_ABS} ${src})
        set(out "${CMAKE_BINARY_DIR}/lib/${it}")
        add_custom_command(
            DEPENDS   ${src}
            OUTPUT    ${out}
            COMMAND   ${CMAKE_COMMAND}
            ARGS      -E copy_if_different ${src} ${out}
            MAIN_DEPENDENCY ${src}
            COMMENT   "Copy file to ${out}"
    )
    endforeach (it)
    SOURCE_GROUP("PySide tools" FILES ${AuraCAD_LIBPACK_PYSIDEUIC_OTH})
    SOURCE_GROUP("PySide tools\\pysideuic" FILES ${AuraCAD_LIBPACK_PYSIDEUIC_TOP})
    SOURCE_GROUP("PySide tools\\pysideuic\\Compiler" FILES ${AuraCAD_LIBPACK_PYSIDEUIC_CMP})
    SOURCE_GROUP("PySide tools\\pysideuic\\port_v2" FILES ${AuraCAD_LIBPACK_PYSIDEUIC_PV2})
    SOURCE_GROUP("PySide tools\\pysideuic\\port_v3" FILES ${AuraCAD_LIBPACK_PYSIDEUIC_PV3})
    SOURCE_GROUP("PySide tools\\pysideuic\\widget-plugins" FILES ${AuraCAD_LIBPACK_PYSIDEUIC_WPL})

    # Python extension modules
    foreach (it ${AuraCAD_LIBPACK_PYTHON})
        get_filename_component(libfile ${it} NAME)
        set(out "${CMAKE_BINARY_DIR}/lib/${libfile}")
        add_custom_command(
            DEPENDS   ${it}
            OUTPUT    ${out}
            COMMAND   ${CMAKE_COMMAND}
            ARGS      -E copy_if_different ${it} ${out}
            MAIN_DEPENDENCY ${it}
            COMMENT   "Copy file to ${out}"
    )
    endforeach (it)
    SOURCE_GROUP("Python" FILES ${AuraCAD_LIBPACK_PYTHON})

    set(AuraCAD_LIBPACK_FILES
        ${AuraCAD_LIBPACK_PIVY_COIN}
        ${AuraCAD_LIBPACK_SHIBOKEN}
        ${AuraCAD_LIBPACK_PYSIDE}
        ${AuraCAD_LIBPACK_PYSIDEUIC_ABS}
        ${AuraCAD_LIBPACK_PYTHON}
    )
    add_custom_target(LibPack_Files ALL SOURCES ${AuraCAD_LIBPACK_FILES})

endif(WIN32 AND AuraCAD_LIBPACK_USE)

INSTALL(
    FILES
        ${Examples_Files}
    DESTINATION
        ${CMAKE_INSTALL_DATADIR}/examples
)
