// SPDX-License-Identifier: LGPL-2.1-or-later
/***************************************************************************
 *   Copyright (c) 2008 JÃ¼rgen Riegel <juergen.riegel@web.de>              *
 *                                                                         *
 *   This file is part of the AuraCAD CAx development system.              *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU Library General Public License (LGPL)   *
 *   as published by the Free Software Foundation; either version 2 of     *
 *   the License, or (at your option) any later version.                   *
 *   for detail see the LICENCE text file.                                 *
 *                                                                         *
 *   AuraCAD is distributed in the hope that it will be useful,            *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with AuraCAD; if not, write to the Free Software        *
 *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
 *   USA                                                                   *
 *                                                                         *
 ***************************************************************************/

#include <auracadConfig.h>

#if defined(AuraCAD_OS_WIN32)
# include <windows.h>
#endif

#ifdef AuraCAD_OS_MACOSX
# include <mach-o/dyld.h>
# include <string>
#endif

#if HAVE_CONFIG_H
# include <config.h>
#endif  // HAVE_CONFIG_H

#include <cstdio>
#include <iostream>
#include <QByteArray>

// AuraCAD Base header
#include <Base/ConsoleObserver.h>
#include <Base/Exception.h>
#include <Base/PyObjectBase.h>
#include <Base/Sequencer.h>
#include <App/Application.h>

#if defined(AuraCAD_OS_WIN32)

/** DllMain is called when DLL is loaded
 */
BOOL APIENTRY DllMain(HANDLE hModule, DWORD ul_reason_for_call, LPVOID /*lpReserved*/)
{
    switch (ul_reason_for_call) {
        case DLL_PROCESS_ATTACH: {
            // This name is preliminary, we pass it to Application::init() in initAuraCAD()
            // which does the rest.
            char szFileName[MAX_PATH];
            GetModuleFileNameA((HMODULE)hModule, szFileName, MAX_PATH - 1);
            App::Application::Config()["AppHomePath"] = szFileName;
        } break;
        default:
            break;
    }

    return true;
}
#elif defined(AuraCAD_OS_LINUX) || defined(AuraCAD_OS_BSD)
# ifndef GNU_SOURCE
#  define GNU_SOURCE
# endif
# include <dlauracadn.h>
#elif defined(AuraCAD_OS_CYGWIN)
# include <windows.h>
#endif

PyMOD_INIT_FUNC(AuraCAD)
{
    // Init phase ===========================================================
    App::Application::Config()["ExeName"] = "AuraCAD";
    App::Application::Config()["ExeVendor"] = "AuraCAD";
    App::Application::Config()["AppDataSkipVendor"] = "true";

    QByteArray path;

#if defined(AuraCAD_OS_WIN32)
    path = App::Application::Config()["AppHomePath"].c_str();
#elif defined(AuraCAD_OS_CYGWIN)
    HMODULE hModule = GetModuleHandle("AuraCAD.dll");
    char szFileName[MAX_PATH];
    GetModuleFileNameA(hModule, szFileName, MAX_PATH - 1);
    path = szFileName;
#elif defined(AuraCAD_OS_LINUX) || defined(AuraCAD_OS_BSD)
    putenv("LANG=C");
    putenv("LC_ALL=C");
    // get whole path of the library
    Dl_info info;
    int ret = dladdr((void*)PyInit_AuraCAD, &info);
    if ((ret == 0) || (!info.dli_fname)) {
        PyErr_SetString(PyExc_ImportError, "Cannot get path of the AuraCAD module!");
        return nullptr;
    }

    path = info.dli_fname;
    // this is a workaround to avoid a crash in libuuid.so
#elif defined(AuraCAD_OS_MACOSX)

    // The MacOS approach uses the Python sys.path list to find the path
    // to AuraCAD.so - this should be OS-agnostic, except these two
    // strings, and the call to access().
    const static char libName[] = "/AuraCAD.so";
    const static char upDir[] = "/../";

    PyObject* pySysPath = PySys_GetObject("path");
    if (PyList_Check(pySysPath)) {
        int i;
        // pySysPath should be a *PyList of strings - iterate through it
        // backwards since the AuraCAD path was likely appended just before
        // we were imported.
        for (i = PyList_Size(pySysPath) - 1; i >= 0; --i) {
            const char* basePath;
            PyObject* pyPath = PyList_GetItem(pySysPath, i);
            long sz = 0;

            if (PyUnicode_Check(pyPath)) {
                // Python 3 string
                basePath = PyUnicode_AsUTF8AndSize(pyPath, &sz);
            }
            else {
                continue;
            }

            if (sz + sizeof(libName) > PATH_MAX) {
                continue;
            }

            path = basePath;

            // append libName to the path
            if (access(path + libName, R_OK | X_OK) == 0) {

                // The AuraCAD "home" path is one level up from
                // libName, so replace libName with upDir.
                path += upDir;
                break;
            }
        }
    }

    if (path.isEmpty()) {
        PyErr_SetString(PyExc_ImportError, "Cannot get path of the AuraCAD module!");
        return nullptr;
    }

#else
# error "Implement: Retrieve the path of the module for your platform."
#endif
    int argc = 1;
    std::vector<char*> argv;
    argv.push_back(path.data());

    try {
        // Inits the Application
        App::Application::init(argc, argv.data());
    }
    catch (const Base::Exception& e) {
        std::string appName = App::Application::getExecutableName();
        std::cout << "While initializing " << appName << " the following exception occurred: '"
                  << e.what() << "'\n\n";
        std::cout << "Please contact the application's support team for more information."
                  << std::endl;
    }

    Base::EmptySequencer* seq = new Base::EmptySequencer();
    (void)seq;
    static Base::RedirectStdOutput stdcout;
    static Base::RedirectStdLog stdclog;
    static Base::RedirectStdError stdcerr;
    std::cout.rdbuf(&stdcout);
    std::clog.rdbuf(&stdclog);
    std::cerr.rdbuf(&stdcerr);

    PyObject* modules = PyImport_GetModuleDict();
    PyObject* module = PyDict_GetItemString(modules, "AuraCAD");
    if (!module) {
        PyErr_SetString(PyExc_ImportError, "Failed to load AuraCAD module!");
    }
    return module;
}
