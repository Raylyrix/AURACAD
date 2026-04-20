# SPDX-License-Identifier: LGPL-2.1-or-later

add_executable(PartDesign_tests_run
        BackwardCompatibility.cpp
        DatumPlane.cpp
        ShapeBinder.cpp
        Pad.cpp
)

set(PartDesignTestData_Files
        TestModels/ModelFromV021.auracadStd
        TestModels/TwoLengthsPadWithExpression.auracadStd
        TestModels/TwoLengthsPadCyclicExpr.auracadStd
        TestModels/TwoLengthsPadCrossObjectRef.auracadStd
)

ADD_CUSTOM_TARGET(PartDesignTestData ALL
        SOURCES ${PartDesignTestData_Files}
)

AuraCAD_target_copy_resource(PartDesignTestData
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_BINARY_DIR}/tests
        ${PartDesignTestData_Files}
)
