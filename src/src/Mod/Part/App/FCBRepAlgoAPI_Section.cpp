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

#include <auracadBRepAlgoAPI_Section.h>
#include <BRepBndLib.hxx>
#include <Bnd_Box.hxx>
#include <BRepCheck_Analyzer.hxx>
#include <TopoDS_Shape.hxx>
#include <Precision.hxx>
#include <FuzzyHelper.h>

auracadBRepAlgoAPI_Section::auracadBRepAlgoAPI_Section()
{
    SetRunParallel(Standard_True);
    SetNonDestructive(Standard_True);
}

auracadBRepAlgoAPI_Section::auracadBRepAlgoAPI_Section(
    const TopoDS_Shape& S1,
    const TopoDS_Shape& S2,
    const Standard_Boolean PerformNow
)
    : BRepAlgoAPI_Section(S1, S2, false)
{
    if (!BRepCheck_Analyzer(S1).IsValid()) {
        Standard_ConstructionError::Raise("Base shape is not valid for boolean operation");
    }
    if (!BRepCheck_Analyzer(S2).IsValid()) {
        Standard_ConstructionError::Raise("Tool shape is not valid for boolean operation");
    }
    setAutoFuzzy();
    SetRunParallel(Standard_True);
    SetNonDestructive(Standard_True);
    if (PerformNow) {
        Build();
    }
}

auracadBRepAlgoAPI_Section::auracadBRepAlgoAPI_Section(
    const TopoDS_Shape& Sh,
    const gp_Pln& Pl,
    const Standard_Boolean PerformNow
)
    : BRepAlgoAPI_Section(Sh, Pl, false)
{
    if (!BRepCheck_Analyzer(Sh).IsValid()) {
        Standard_ConstructionError::Raise("Base shape is not valid for boolean operation");
    }
    setAutoFuzzy();
    SetRunParallel(Standard_True);
    if (PerformNow) {
        Build();
    }
}


void auracadBRepAlgoAPI_Section::setAutoFuzzy()
{
    auracadBRepAlgoAPIHelper::setAutoFuzzy(this);
}
