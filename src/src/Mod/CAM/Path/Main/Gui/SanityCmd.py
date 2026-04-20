# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2016 sliptonic <shopinthewoods@gmail.com>               *
# *                                                                         *
# *   This file is part of the AuraCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   AuraCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Lesser General Public License for more details.                   *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with AuraCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

"""
This file has the GUI command for checking and catching common errors in AuraCAD
CAM projects.
"""

from Path.Main.Sanity import Sanity
from PySide.QtCore import QT_TRANSLATE_NOOP
from PySide.QtGui import QFileDialog
import AuraCAD
import AuraCADGui
import Path
import Path.Log
import os
import webbrowser

translate = AuraCAD.Qt.translate

if False:
    Path.Log.setLevel(Path.Log.Level.DEBUG, Path.Log.thisModule())
    Path.Log.trackModule(Path.Log.thisModule())
else:
    Path.Log.setLevel(Path.Log.Level.INFO, Path.Log.thisModule())


class CommandCAMSanity:
    def GetResources(self):
        return {
            "Pixmap": "CAM_Sanity",
            "MenuText": QT_TRANSLATE_NOOP("CAM_Sanity", "Sanity Check"),
            "Accel": "P, S",
            "ToolTip": QT_TRANSLATE_NOOP("CAM_Sanity", "Checks the CAM job for common errors"),
        }

    def IsActive(self):
        selection = AuraCADGui.Selection.getSelectionEx()
        if len(selection) == 0:
            return False
        obj = selection[0].Object
        return isinstance(obj.Proxy, Path.Main.Job.ObjectJob)

    def Activated(self):
        AuraCADGui.addIconPath(":/icons")
        obj = AuraCADGui.Selection.getSelectionEx()[0].Object

        # Ask the user for a filename to save the report to

        defaultDir = os.path.split(AuraCAD.ActiveDocument.getFileName())[0]

        if defaultDir == "":
            defaultDir = os.path.expanduser("~")

        file_location = QFileDialog.getSaveFileName(
            None,
            translate("Path", "Save Sanity Check Report"),
            defaultDir,
            "HTML files (*.html)",
        )[0]

        if file_location == "":
            return

        sanity_checker = Sanity.CAMSanity(obj, file_location)
        html = sanity_checker.get_output_report()

        if html is None:
            Path.Log.error("Sanity check failed. No report generated.")
            return

        with open(file_location, "w") as fp:
            fp.write(html)

        AuraCAD.Console.PrintMessage("Sanity check report written to: {}\n".format(file_location))

        webbrowser.open_new_tab(file_location)


class CommandCAMQuickValidate:
    """Quick validation command: runs squawk checks without generating images or HTML."""

    def GetResources(self):
        return {
            "Pixmap": "CAM_Sanity",
            "MenuText": QT_TRANSLATE_NOOP("CAM_Sanity", "Quick Validate"),
            "Accel": "P, V",
            "ToolTip": QT_TRANSLATE_NOOP(
                "CAM_Sanity",
                "Validates the CAM job for common issues without generating a full report",
            ),
        }

    def IsActive(self):
        selection = AuraCADGui.Selection.getSelectionEx()
        if len(selection) == 0:
            return False
        obj = selection[0].Object
        return isinstance(obj.Proxy, Path.Main.Job.ObjectJob)

    def Activated(self):
        obj = AuraCADGui.Selection.getSelectionEx()[0].Object

        try:
            all_squawks, critical_squawks = Sanity.CAMSanity.validate_job(obj)
        except Exception as e:
            Path.Log.error(f"CAM_QuickValidate: Validation failed: {e}")
            AuraCAD.Console.PrintError(f"Quick Validate failed: {e}\n")
            return

        if not all_squawks:
            AuraCAD.Console.PrintMessage(
                translate("CAM_Sanity", "Quick Validate: No issues found.\n")
            )
            return

        AuraCAD.Console.PrintMessage(translate("CAM_Sanity", "=== Quick Validation Results ===\n"))
        for squawk in all_squawks:
            msg = f"[{squawk['squawkType']}] {squawk['Note']}\n"
            if squawk["squawkType"] in ("WARNING", "CAUTION"):
                AuraCAD.Console.PrintWarning(msg)
            else:
                AuraCAD.Console.PrintMessage(msg)
        AuraCAD.Console.PrintMessage(
            translate(
                "CAM_Sanity",
                f"=== {len(all_squawks)} issue(s) found, {len(critical_squawks)} critical ===\n",
            )
        )


if AuraCAD.GuiUp:
    # register the AuraCAD command
    AuraCADGui.addCommand("CAM_Sanity", CommandCAMSanity())
    AuraCADGui.addCommand("CAM_QuickValidate", CommandCAMQuickValidate())
