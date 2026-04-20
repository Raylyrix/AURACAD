# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2017 Yorik van Havre <yorik@uncreated.net>              *
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

"""This module contains AuraCAD commands for the BIM workbench"""

import os

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate


# Status bar buttons


def setStatusIcons(show=True):
    "shows or hides the BIM icons in the status bar"

    import AuraCADGui
    from PySide import QtCore, QtGui

    nudgeLabelsI = [
        translate("BIM", "Customâ€¦"),
        '1/16"',
        '1/8"',
        '1/4"',
        '1"',
        '6"',
        "1'",
        translate("BIM", "Auto"),
    ]
    nudgeLabelsM = [
        translate("BIM", "Customâ€¦"),
        "1 mm",
        "5 mm",
        "1 cm",
        "5 cm",
        "10 cm",
        "50 cm",
        translate("BIM", "Auto"),
    ]

    def toggleBimViews(state):
        AuraCADGui.runCommand("BIM_Views")

    def toggleBackground(state):
        AuraCADGui.runCommand("BIM_Background")

    def setNudge(action):
        utext = action.text().replace("&", "")
        if utext == nudgeLabelsM[0]:
            # load dialog
            form = AuraCADGui.PySideUic.loadUi(":/ui/dialogNudgeValue.ui")
            # center the dialog over AuraCAD window
            mw = AuraCADGui.getMainWindow()
            form.move(mw.frameGeometry().topLeft() + mw.rect().center() - form.rect().center())
            result = form.exec_()
            if not result:
                return
            utext = form.inputField.text()
        action.parent().parent().parent().setText(utext)

    # main code

    mw = AuraCADGui.getMainWindow()
    if mw:
        st = mw.statusBar()
        statuswidget = st.findChild(QtGui.QToolBar, "BIMStatusWidget")
        if show:
            if statuswidget:
                statuswidget.show()
                if hasattr(statuswidget, "propertybuttons"):
                    statuswidget.propertybuttons.show()
            else:
                statuswidget = AuraCADGui.UiLoader().createWidget("Gui::ToolBar")
                statuswidget.setObjectName("BIMStatusWidget")
                text = translate(
                    "BIMStatusWidget",
                    "BIM Status Widget",
                    "A context menu action used to show or hide this toolbar widget",
                )
                statuswidget.setWindowTitle(text)
                s = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/General").GetInt(
                    "ToolbarIconSize", 24
                )
                statuswidget.setIconSize(QtCore.QSize(s, s))
                st.insertPermanentWidget(2, statuswidget)

                # bim views widget toggle button
                from bimcommands import BimViews

                bimviewsbutton = QtGui.QAction()
                bimviewsbutton.setIcon(QtGui.QIcon(":/icons/BIM_Views.svg"))

                bimviewsbutton.setText("")
                bimviewsbutton.setToolTip(
                    translate("BIM", "Toggles the BIM Views Manager on/off (Ctrl+9)")
                )
                bimviewsbutton.setCheckable(True)
                if BimViews.findWidget():
                    bimviewsbutton.setChecked(True)
                statuswidget.bimviewsbutton = bimviewsbutton
                bimviewsbutton.triggered.connect(toggleBimViews)
                statuswidget.addAction(bimviewsbutton)

                # background toggle button
                bgbutton = QtGui.QAction()
                # bwidth = bgbutton.fontMetrics().boundingRect("AAAA").width()
                # bgbutton.setMaximumWidth(bwidth)
                bgbutton.setIcon(QtGui.QIcon(":/icons/BIM_Background.svg"))
                bgbutton.setText("")
                bgbutton.setToolTip(
                    translate("BIM", "Toggles the 3D View background between simple and gradient")
                )
                statuswidget.bgbutton = bgbutton
                bgbutton.triggered.connect(toggleBackground)
                statuswidget.addAction(bgbutton)

                # iauracad widgets
                try:
                    from nativeiauracad import iAuraCAD_status
                except:
                    pass
                else:
                    iAuraCAD_status.set_status_widget(statuswidget)

                # nudge button
                nudge = QtGui.QPushButton(nudgeLabelsM[-1])
                nudge.setIcon(QtGui.QIcon(":/icons/BIM_Nudge.svg"))
                nudge.setFlat(True)
                nudge.setToolTip(
                    translate(
                        "BIM",
                        "The value of the nudge movement (rotation is always 45Â°)."
                        "Alt+arrows to move\nAlt+, to rotate left"
                        "Alt+. to rotate right\nAlt+PgUp to extend extrusion"
                        "Alt+PgDown to shrink extrusion"
                        "Alt+/ to switch between auto and manual mode",
                    )
                )
                statuswidget.addWidget(nudge)
                statuswidget.nudge = nudge
                menu = QtGui.QMenu(nudge)
                gnudge = QtGui.QActionGroup(menu)
                for u in nudgeLabelsM:
                    a = QtGui.QAction(gnudge)
                    a.setText(u)
                    menu.addAction(a)
                nudge.setMenu(menu)
                gnudge.triggered.connect(setNudge)
                statuswidget.nudgeLabelsI = nudgeLabelsI
                statuswidget.nudgeLabelsM = nudgeLabelsM
                statuswidget.show()

        else:
            if statuswidget is None:
                # when switching workbenches, the toolbar sometimes "jumps"
                # out of the status bar to any other dock area...
                statuswidget = mw.findChild(QtGui.QToolBar, "BIMStatusWidget")
            if statuswidget:
                statuswidget.hide()
                statuswidget.toggleViewAction().setVisible(False)
                if hasattr(statuswidget, "propertybuttons"):
                    statuswidget.propertybuttons.hide()
