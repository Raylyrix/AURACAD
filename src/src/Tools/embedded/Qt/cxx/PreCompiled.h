// SPDX-License-Identifier: LGPL-2.1-or-later

#pragma once

#ifdef AuraCAD_OS_WIN32
// cmake generates this define
# if defined(AuraCADPlugin_EXPORTS)
#  define AuraCAD_PLUGIN_EXPORT __declspec(dllexport)
# else
#  define AuraCAD_PLUGIN_EXPORT __declspec(dllimport)
# endif
# define MeshExport __declspec(dllimport)
#else  // for Linux
# define AuraCAD_PLUGIN_EXPORT
# define MeshExport
#endif
