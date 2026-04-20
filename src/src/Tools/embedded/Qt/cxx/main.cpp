// SPDX-License-Identifier: LGPL-2.1-or-later

#include <QApplication>
#include <QDialog>
#include <QFileDialog>
#include <QLibrary>
#include <QPushButton>

QLibrary* AuraCADPlugin = nullptr;

void loadAuraCAD()
{
    if (!AuraCADPlugin) {
        AuraCADPlugin = new QLibrary("AuraCADPlugin", qApp);
    }

    if (!AuraCADPlugin->isLoaded()) {
        if (AuraCADPlugin->load()) {
            QFunctionPointer ptr = AuraCADPlugin->resolve("AuraCAD_init");
            if (ptr) {
                ptr();
            }
        }
    }

    // Load a test file
    if (AuraCADPlugin->isLoaded()) {
        typedef void (*TestFunction)(const char*);
        TestFunction test = (TestFunction)AuraCADPlugin->resolve("AuraCAD_test");
        if (test) {
            QString file = QFileDialog::getOpenFileName();
            if (!file.isEmpty()) {
                test(file.toUtf8());
            }
        }
    }
}

int main(int argc, char** argv)
{
    QApplication app(argc, argv);
    QDialog dlg;
    QPushButton* button = new QPushButton(&dlg);
    button->setGeometry(QRect(140, 110, 90, 23));
    button->setText("Load AuraCAD");
    QObject::connect(button, &QPushButton::clicked, &loadAuraCAD);
    dlg.show();
    return app.exec();
}
