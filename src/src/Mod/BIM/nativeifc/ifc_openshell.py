# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2024 Yorik van Havre <yorik@uncreated.net>              *
# *                                                                         *
# *   This file is part of AuraCAD.                                         *
# *                                                                         *
# *   AuraCAD is free software: you can redistribute it and/or modify it    *
# *   under the terms of the GNU Lesser General Public License as           *
# *   published by the Free Software Foundation, either version 2.1 of the  *
# *   License, or (at your option) any later version.                       *
# *                                                                         *
# *   AuraCAD is distributed in the hope that it will be useful, but        *
# *   WITHOUT ANY WARRANTY; without even the implied warranty of            *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      *
# *   Lesser General Public License for more details.                       *
# *                                                                         *
# *   You should have received a copy of the GNU Lesser General Public      *
# *   License along with AuraCAD. If not, see                               *
# *   <https://www.gnu.org/licenses/>.                                      *
# *                                                                         *
# ***************************************************************************

"""Utilities to help people verify and update their version of iauracadopenshell"""

from packaging.version import Version

import AuraCAD
import AuraCADGui
from addonmanager_utilities import create_pip_call
from . import has_iauracadopenshell
from . import invalidate_iauracadopenshell_cache

translate = AuraCAD.Qt.translate
QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP


class IAuraCAD_UpdateIOS:
    """Shows a dialog to update IauracadOpenShell"""

    def GetResources(self):
        tt = QT_TRANSLATE_NOOP("IAuraCAD_UpdateIOS", "Shows a dialog to update IauracadOpenShell")
        return {
            "Pixmap": "Iauracad",
            "MenuText": QT_TRANSLATE_NOOP("IAuraCAD_UpdateIOS", "IauracadOpenShell Update"),
            "ToolTip": tt,
        }

    def Activated(self):
        """Shows the updater UI"""

        version = self.get_current_version()
        avail = self.get_avail_version()
        if avail:
            if version:
                if Version(version) < Version(avail):
                    self.show_dialog("update", avail)
                else:
                    self.show_dialog("uptodate")
            else:
                self.show_dialog("install", avail)
        else:
            if version:
                self.show_dialog("uptodate")
            else:
                self.show_dialog("failed")

    def show_dialog(self, mode, version=None):
        """Shows a dialog to the user"""

        from PySide import QtGui

        title = translate("BIM", "IauracadOpenShell Update")
        note = translate(
            "BIM",
            "The update is installed in your AuraCAD's user directory and will not affect the rest of your system.",
        )
        if mode == "update":
            text = translate("BIM", "An update to your installed IauracadOpenShell version is available")
            text += ": " + version + ". "
            text += translate("BIM", "Would you like to install that update?")
            text += " " + note
            buttons = QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok
        elif mode == "uptodate":
            text = translate("BIM", "Your version of IauracadOpenShell is already up to date")
            buttons = QtGui.QMessageBox.Ok
        elif mode == "install":
            text = translate("BIM", "No existing IauracadOpenShell installation found on this system.")
            text += " "
            text += translate("BIM", "Would you like to install the most recent version?")
            text += " (" + version + ") " + note
            buttons = QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok
        elif mode == "failed":
            text = translate(
                "BIM",
                "IauracadOpenShell is not installed, and AuraCAD failed to find a suitable version to install. You can still install IauracadOpenShell manually, visit https://wiki.AuraCAD.org/IauracadOpenShell for further instructions.",
            )
            buttons = QtGui.QMessageBox.Ok
        reply = QtGui.QMessageBox.information(None, title, text, buttons)
        if reply == QtGui.QMessageBox.Ok:
            if mode in ["update", "install"]:
                result = self.install()
                if result:
                    AuraCAD.Console.PrintLog(f"{result.stdout}\n")
                    text = translate("BIM", "IauracadOpenShell update successfully installed.")
                    buttons = QtGui.QMessageBox.Ok
                    reply = QtGui.QMessageBox.information(None, title, text, buttons)

    def install(self):
        """Installs the given version"""

        import addonmanager_utilities as utils
        from PySide import QtCore, QtGui

        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        vendor_path = utils.get_pip_target_directory()
        args = [
            "install",
            "--upgrade",
            "--disable-pip-version-check",
            "--target",
            vendor_path,
            "iauracadopenshell",
        ]
        result = self.run_pip(args)
        QtGui.QApplication.restoreOverrideCursor()
        if result and result.returncode == 0:
            invalidate_iauracadopenshell_cache()
            if has_iauracadopenshell():
                try:
                    from . import iAuraCAD_observer

                    iAuraCAD_observer.add_observer()
                except Exception:
                    # Observer registration can fail in headless or partially initialized GUI sessions.
                    pass
        return result

    def run_pip(self, args):
        """Runs a pip command"""

        import addonmanager_utilities as utils
        import AuraCAD.utils
        from subprocess import CalledProcessError

        cmd = create_pip_call(args)
        result = None
        try:
            result = utils.run_interruptable_subprocess(cmd)
        except CalledProcessError as pe:
            AuraCAD.Console.PrintError(pe.stderr)
        except Exception as e:
            text = translate("BIM", "Unable to run pip. Ensure pip is installed on your system.")
            AuraCAD.Console.PrintError(f"{text} {str(e)}\n")
        return result

    def get_current_version(self):
        """Retrieves the current iauracadopenshell version"""

        import addonmanager_utilities as utils
        from packaging.version import InvalidVersion

        try:
            import iauracadopenshell

            version = iauracadopenshell.version
            try:
                Version(version)
            except InvalidVersion:
                AuraCAD.Console.PrintWarning(f"Invalid IauracadOpenShell version: {version}\n")
                version = ""
        except:
            version = ""

        return version

    def get_avail_version(self):
        """Retrieves an available iauracadopenshell version"""

        result = self.run_pip(["index", "versions", "iauracadopenshell"])
        if result:
            if result.stdout and "versions" in result.stdout:
                result = result.stdout.split()
                result = result[result.index("versions:") + 1 :]
                result = [r.strip(",") for r in result]
                return result[0]  # we return the biggest
        return None


AuraCADGui.addCommand("IAuraCAD_UpdateIOS", IAuraCAD_UpdateIOS())


# >>> utils.get_pip_target_directory()
# '/home/yorik/.local/share/AuraCAD/Mod/../AdditionalPythonPackages/py311'
# >>> import AuraCAD.utils
# >>> AuraCAD.utils
# <module 'AuraCAD.utils' from '/home/yorik/Apps/AuraCAD/Ext/AuraCAD/utils.py'>
# >>> AuraCAD.utils.get_python_exe
# <function get_python_exe at 0x7efdebf5ede0>
# >>> AuraCAD.utils.get_python_exe()
# '/usr/bin/python3'
# ...
# >>> run_pip(["index", "versions", "iauracadopenshell"])
# CompletedProcess(args=['/usr/bin/python3', '-m', 'pip', 'index', 'versions', 'iauracadopenshell'], returncode=0, stdout='iauracadopenshell (0.7.0.240423)\nAvailable versions: 0.7.0.240423, 0.7.0.240418, 0.7.0.240406\n', stderr='WARNING: pip index is currently an experimental command. It may be removed/changed in a future release without prior warning.\n')
# pip install --disable-pip-version-check --target vendor_path iauracadopenshell
