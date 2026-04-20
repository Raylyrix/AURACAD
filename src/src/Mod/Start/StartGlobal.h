// SPDX-License-Identifier: LGPL-2.1-or-later
/****************************************************************************
 *                                                                          *
 *   Copyright (c) 2024 The AuraCAD Project Association AISBL               *
 *                                                                          *
 *   This file is part of AuraCAD.                                          *
 *                                                                          *
 *   AuraCAD is free software: you can redistribute it and/or modify it     *
 *   under the terms of the GNU Lesser General Public License as            *
 *   published by the Free Software Foundation, either version 2.1 of the   *
 *   License, or (at your option) any later version.                        *
 *                                                                          *
 *   AuraCAD is distributed in the hope that it will be useful, but         *
 *   WITHOUT ANY WARRANTY; without even the implied warranty of             *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU       *
 *   Lesser General Public License for more details.                        *
 *                                                                          *
 *   You should have received a copy of the GNU Lesser General Public       *
 *   License along with AuraCAD. If not, see                                *
 *   <https://www.gnu.org/licenses/>.                                       *
 *                                                                          *
 ***************************************************************************/

#include <auracadGlobal.h>

#pragma once


// Start
#ifndef StartExport
# ifdef Start_EXPORTS
#  define StartExport AuraCAD_DECL_EXPORT
# else
#  define StartExport AuraCAD_DECL_IMPORT
# endif
#endif

// StartGui
#ifndef StartGuiExport
# ifdef StartGui_EXPORTS
#  define StartGuiExport AuraCAD_DECL_EXPORT
# else
#  define StartGuiExport AuraCAD_DECL_IMPORT
# endif
#endif
