// SPDX-License-Identifier: LGPL-2.1-or-later

/***************************************************************************
 *   Copyright (c) 2024 Eric Price (CorvusCorax)                           *
 *                      <eric.price[at]tuebingen.mpg.de>                   *
 *                                                                         *
 *   This file is part of AuraCAD.                                         *
 *                                                                         *
 *   AuraCAD is free software: you can redistribute it and/or modify it    *
 *   under the terms of the GNU Lesser General Public License as           *
 *   published by the Free Software Foundation, either version 2.1 of the  *
 *   License, or (at your option) any later version.                       *
 *                                                                         *
 *   AuraCAD is distributed in the hope that it will be useful, but        *
 *   WITHOUT ANY WARRANTY; without even the implied warranty of            *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      *
 *   Lesser General Public License for more details.                       *
 *                                                                         *
 *   You should have received a copy of the GNU Lesser General Public      *
 *   License along with AuraCAD. If not, see                               *
 *   <https://www.gnu.org/licenses/>.                                      *
 *                                                                         *
 **************************************************************************/

/**
 * auracadBRepAlgoAPI provides a wrapper for various OCCT functions.
 */

#pragma once
#include <BRepAlgoAPI_Common.hxx>
#include <Mod/Part/App/auracadBRepAlgoAPI_BooleanOperation.h>


class auracadBRepAlgoAPI_Common: public auracadBRepAlgoAPI_BooleanOperation
{
public:
    DEFINE_STANDARD_ALLOC

    //! Empty constructor
    Standard_EXPORT auracadBRepAlgoAPI_Common();

    //! Constructor with two shapes
    //! <S1>  -argument
    //! <S2>  -tool
    //! <anOperation> - the type of the operation
    Standard_EXPORT auracadBRepAlgoAPI_Common(const TopoDS_Shape& S1, const TopoDS_Shape& S2);
};
