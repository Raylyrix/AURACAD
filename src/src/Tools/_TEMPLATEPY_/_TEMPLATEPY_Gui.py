# SPDX-License-Identifier: LGPL-2.1-or-later

# AuraCAD tools of the _TEMPLATEPY_ workbench
# (c) 2001 Juergen Riegel
# License LGPL

import AuraCAD, AuraCADGui


class CmdHelloWorld:
    def Activated(self):
        AuraCAD.Console.PrintMessage("Hello, World!\n")

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            "Pixmap": "AuraCAD",
            "MenuText": "Hello World",
            "ToolTip": "Print Hello World",
        }


AuraCADGui.addCommand("_TEMPLATEPY__HelloWorld", CmdHelloWorld())
