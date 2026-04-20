include(GNUInstallDirs)

if(NOT DEFINED APPDATA_RELEASE_DATE)
    if(EXISTS "${CMAKE_SOURCE_DIR}/.git")
        execute_process(COMMAND git log -1 --pretty=%cd --date=short
            OUTPUT_VARIABLE APPDATA_RELEASE_DATE
            WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
            OUTPUT_STRIP_TRAILING_WHITESPACE)
    else()
        string(TIMESTAMP APPDATA_RELEASE_DATE "%Y-%m-%d")
    endif()
endif()

configure_file(
    org.AuraCAD.AuraCAD.metainfo.xml.in
    ${CMAKE_BINARY_DIR}/org.AuraCAD.AuraCAD.metainfo.xml
)
install(
    FILES ${CMAKE_BINARY_DIR}/org.AuraCAD.AuraCAD.metainfo.xml
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/metainfo
)

install(
    FILES org.AuraCAD.AuraCAD.desktop
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/applications
)

install(
    FILES org.AuraCAD.AuraCAD.xml
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/mime/packages
)

configure_file(
    AuraCAD.thumbnailer.in
    ${CMAKE_BINARY_DIR}/AuraCAD.thumbnailer
)
install(
    FILES ${CMAKE_BINARY_DIR}/AuraCAD.thumbnailer
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/thumbnailers
)

configure_file(
    ${CMAKE_SOURCE_DIR}/src/Tools/AuraCAD-thumbnailer.in
    ${CMAKE_BINARY_DIR}/AuraCAD-thumbnailer
)
install(
    PROGRAMS ${CMAKE_BINARY_DIR}/AuraCAD-thumbnailer
    TYPE BIN
)
