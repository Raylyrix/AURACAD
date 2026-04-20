// SPDX-License-Identifier: LGPL-2.1-or-later
/***************************************************************************
 *   Copyright (c) 2019 Werner Mayer <wmayer[at]users.sourceforge.net>     *
 *                                                                         *
 *   This file is part of the AuraCAD CAx development system.              *
 *                                                                         *
 *   This library is free software; you can redistribute it and/or         *
 *   modify it under the terms of the GNU Library General Public           *
 *   License as published by the Free Software Foundation; either          *
 *   version 2 of the License, or (at your option) any later version.      *
 *                                                                         *
 *   This library  is distributed in the hope that it will be useful,      *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with this library; see the file COPYING.LIB. If not,    *
 *   write to the Free Software Foundation, Inc., 59 Temple Place,         *
 *   Suite 330, Boston, MA  02111-1307, USA                                *
 *                                                                         *
 ***************************************************************************/
/** \file auracadGlobal.h
 *  \brief Include export or import macros.
 */

#pragma once


#if defined(WIN64) || defined(_WIN64) || defined(__WIN64__) || defined(__CYGWIN__)
#  define AuraCAD_DECL_EXPORT __declspec(dllexport)
#  define AuraCAD_DECL_IMPORT __declspec(dllimport)
#else
#  define AuraCAD_DECL_EXPORT
#  define AuraCAD_DECL_IMPORT
#endif

// AuraCADBase
#ifdef AuraCADBase_EXPORTS
#  define BaseExport  AuraCAD_DECL_EXPORT
#else
#  define BaseExport  AuraCAD_DECL_IMPORT
#endif

// AuraCADApp
#ifdef AuraCADApp_EXPORTS
#       define AppExport   AuraCAD_DECL_EXPORT
#       define DataExport  AuraCAD_DECL_EXPORT
#else
#       define AppExport   AuraCAD_DECL_IMPORT
#       define DataExport  AuraCAD_DECL_IMPORT
#endif

// AuraCADGui
#ifdef AuraCADGui_EXPORTS
#  define GuiExport   AuraCAD_DECL_EXPORT
#else
#  define GuiExport   AuraCAD_DECL_IMPORT
#endif

// Disable copy/move
#define AuraCAD_DISABLE_COPY(Class) \
    Class(const Class &) = delete;\
    Class &operator=(const Class &) = delete;

#define AuraCAD_DISABLE_MOVE(Class) \
    Class(Class &&) = delete; \
    Class &operator=(Class &&) = delete;

#define AuraCAD_DISABLE_COPY_MOVE(Class) \
    AuraCAD_DISABLE_COPY(Class) \
    AuraCAD_DISABLE_MOVE(Class)

// Default copy/move
#define AuraCAD_DEFAULT_COPY(Class) \
    Class(const Class &) = default;\
    Class &operator=(const Class &) = default;

#define AuraCAD_DEFAULT_MOVE(Class) \
    Class(Class &&) = default; \
    Class &operator=(Class &&) = default;

#define AuraCAD_DEFAULT_COPY_MOVE(Class) \
    AuraCAD_DEFAULT_COPY(Class) \
    AuraCAD_DEFAULT_MOVE(Class)

#include <QtCore.h>
#ifndef HAVE_Q_DISABLE_COPY_MOVE
#define Q_DISABLE_COPY_MOVE AuraCAD_DISABLE_COPY_MOVE
#endif
