// SPDX-License-Identifier: LGPL-2.1-or-later

/***************************************************************************
 *   Copyright (c) 2023 David Carter <dcarter@david.carter.ca>             *
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

#include <auracadGlobal.h>

#pragma once

// Material
#ifndef MaterialsExport
#ifdef Materials_EXPORTS
#define MaterialsExport AuraCAD_DECL_EXPORT
#else
#define MaterialsExport AuraCAD_DECL_IMPORT
#endif
#endif

// MatGui
#ifndef MatGuiExport
#ifdef MatGui_EXPORTS
#define MatGuiExport AuraCAD_DECL_EXPORT
#else
#define MatGuiExport AuraCAD_DECL_IMPORT
#endif
#endif