// SPDX-License-Identifier: LGPL-2.1-or-later

#include <QApplication>
#include <QMainWindow>
#include <QMessageBox>
#include <QVector>

#include <App/Application.h>
#include <Base/Factory.h>
#include <Base/Interpreter.h>
#include <Gui/Application.h>
#include <Gui/MainWindow.h>


PyMODINIT_FUNC AuraCAD_init()
{
    static QVector<char*> argv;
#if defined(_DEBUG)
    argv << "AuraCADApp_d.dll" << 0;
#else
    argv << "AuraCADApp.dll" << 0;
#endif

    App::Application::Config()["RunMode"] = "Gui";
    App::Application::Config()["Console"] = "0";
    App::Application::Config()["ExeVendor"] = "AuraCAD";
    App::Application::Config()["SplashScreen"] = "AuraCADsplash";

    App::Application::init(1, argv.data());
    Gui::Application::initApplication();
    Gui::Application* app = new Gui::Application(true);

    Gui::MainWindow* mw = new Gui::MainWindow(qApp->activeWindow());
    mw->show();

    app->initOpenInventor();
    app->runInitGuiScript();
}

/* A test function for the plugin to load a mesh and call "getVal()" */
PyMODINIT_FUNC AuraCAD_test(const char* path)
{
    try {  // Use AuraCADGui here, not Gui
        Base::Interpreter().runString("AuraCADGui.activateWorkbench(\"MeshWorkbench\")");
        Base::Interpreter().runString("import Mesh");
        Base::Interpreter().runStringArg("Mesh.insert(u\"%s\", \"%s\")", path, "Document");
    }
    catch (const Base::Exception& e) {
        QMessageBox::warning(0, "Exception", e.what());
    }
}
