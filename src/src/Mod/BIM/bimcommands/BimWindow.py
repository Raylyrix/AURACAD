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

"""BIM window command"""

import os

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")
ALLOWEDHOSTS = ["Wall", "Structure", "Roof"]


class Arch_Window:
    "the Arch Window command definition"

    def __init__(self):

        self.doormode = False

    def GetResources(self):

        return {
            "Pixmap": "Arch_Window",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Window", "Window"),
            "Accel": "W, N",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Window",
                "Creates a window object from a selected object (wire, rectangle or sketch)",
            ),
        }

    def IsActive(self):

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        from draftutils import params
        import Draft
        import WorkingPlane
        import draftguitools.gui_trackers as DraftTrackers

        self.doc = AuraCAD.ActiveDocument
        self.sel = AuraCADGui.Selection.getSelection()
        self.W1 = params.get_param_arch("WindowW1")  # thickness of the fixed frame
        if self.doormode:
            self.Width = params.get_param_arch("DoorWidth")
            self.Height = params.get_param_arch("DoorHeight")
        else:
            self.Width = params.get_param_arch("WindowWidth")
            self.Height = params.get_param_arch("WindowHeight")
        self.RemoveExternal = params.get_param_arch("archRemoveExternal")
        self.Preset = 0
        self.LibraryPreset = 0
        self.SillHeight = 0
        self.Include = True
        self.baseFace = None
        self.wparams = ["Width", "Height", "H1", "H2", "H3", "W1", "W2", "O1", "O2"]
        self.wp = None

        # autobuild mode
        if AuraCADGui.Selection.getSelectionEx():
            AuraCADGui.draftToolBar.offUi()
            obj = self.sel[0]
            if hasattr(obj, "Shape"):
                if obj.Shape.Wires and (not obj.Shape.Solids) and (not obj.Shape.Shells):
                    AuraCADGui.Control.closeDialog()
                    host = None
                    if hasattr(obj, "AttachmentSupport"):
                        if obj.AttachmentSupport:
                            if isinstance(obj.AttachmentSupport, tuple):
                                host = obj.AttachmentSupport[0]
                            elif isinstance(obj.AttachmentSupport, list):
                                host = obj.AttachmentSupport[0][0]
                            else:
                                host = obj.AttachmentSupport
                            obj.AttachmentSupport = None  # remove
                    elif Draft.isClone(obj, "Window"):
                        if obj.Objects[0].Inlist:
                            host = obj.Objects[0].Inlist[0]

                    self.doc.openTransaction(translate("Arch", "Create Window"))
                    AuraCADGui.addModule("Arch")
                    AuraCADGui.doCommand(
                        "win = Arch.makeWindow(AuraCAD.ActiveDocument." + obj.Name + ")"
                    )
                    if host and self.Include:
                        AuraCADGui.doCommand(
                            "win.Hosts = [AuraCAD.ActiveDocument." + host.Name + "]"
                        )
                        siblings = host.Proxy.getSiblings(host)
                        sibs = [host]
                        for sibling in siblings:
                            if not sibling in sibs:
                                sibs.append(sibling)
                                AuraCADGui.doCommand(
                                    "win.Hosts = win.Hosts+[AuraCAD.ActiveDocument."
                                    + sibling.Name
                                    + "]"
                                )
                    self.doc.commitTransaction()
                    self.doc.recompute()
                    return

                # Try to detect an object to use as a window type - TODO we must make this safer

                elif obj.Shape.Solids and (Draft.getType(obj) not in ["Wall", "Structure", "Roof"]):
                    # we consider the selected object as a type
                    self.doc.openTransaction(translate("Arch", "Create Window"))
                    AuraCADGui.addModule("Arch")
                    AuraCADGui.doCommand("Arch.makeWindow(AuraCAD.ActiveDocument." + obj.Name + ")")
                    self.doc.commitTransaction()
                    self.doc.recompute()
                    return

        # interactive mode

        AuraCAD.activeDraftCommand = self  # register as a Draft command for auto grid on/off
        self.wp = WorkingPlane.get_working_plane()
        self.tracker = DraftTrackers.boxTracker()
        self.tracker.length(self.Width)
        self.tracker.width(self.W1)
        self.tracker.height(self.Height)
        self.tracker.on()
        AuraCAD.Console.PrintMessage(
            translate("Arch", "Choose a face on an existing object or select a preset") + "\n"
        )
        AuraCADGui.Snapper.getPoint(
            callback=self.getPoint, movecallback=self.update, extradlg=self.taskbox()
        )
        # AuraCADGui.Snapper.setSelectMode(True)

    def has_width_and_height_constraint(self, sketch):
        width_found = False
        height_found = False

        for constr in sketch.Constraints:
            if constr.Name == "Width":
                width_found = True
            elif constr.Name == "Height":
                height_found = True
            elif width_found and height_found:
                break

        return width_found and height_found

    def getPoint(self, point=None, obj=None):
        "this function is called by the snapper when it has a 3D point"

        import Draft
        from draftutils import gui_utils
        from draftutils.messages import _wrn
        from ArchWindowPresets import WindowPresets

        SketchArch = False

        AuraCAD.activeDraftCommand = None
        AuraCADGui.Snapper.off()
        self.tracker.off()
        if point is None:
            return
        # if something was selected, override the underlying object
        if self.sel:
            obj = self.sel[0]
        point = point.add(AuraCAD.Vector(0, 0, self.SillHeight))
        self.doc.openTransaction(translate("Arch", "Create Window"))

        AuraCADGui.doCommand("import AuraCAD, Arch, DraftGeomUtils, WorkingPlane")
        AuraCADGui.doCommand("wp = WorkingPlane.get_working_plane()")

        if self.baseFace is not None:
            AuraCADGui.doCommand(
                "face = AuraCAD.ActiveDocument."
                + self.baseFace[0].Name
                + ".Shape.Faces["
                + str(self.baseFace[1])
                + "]"
            )
            AuraCADGui.doCommand("pl = DraftGeomUtils.placement_from_face(face, vec_z = wp.axis)")
        else:
            AuraCADGui.doCommand("pl = AuraCAD.Placement()")
            AuraCADGui.doCommand("pl.Rotation = AuraCAD.Rotation(wp.u, wp.axis, -wp.v, 'XZY')")

        AuraCADGui.doCommand(
            "pl.Base = AuraCAD.Vector("
            + str(point.x)
            + ", "
            + str(point.y)
            + ", "
            + str(point.z)
            + ")"
        )

        if self.baseFace is not None:
            host = self.baseFace[0]
        elif obj:
            host = obj
        else:
            host = None

        if self.Preset >= len(WindowPresets):
            preset = False
            # library object
            col = self.doc.Objects
            path = self.librarypresets[self.Preset - len(WindowPresets)][1]
            AuraCADGui.doCommand("AuraCADGui.ActiveDocument.mergeProject(" + repr(path) + ")")
            # find the latest added window
            nol = self.doc.Objects
            for o in nol[len(col) :]:
                if Draft.getType(o) == "Window":
                    if Draft.getType(o.Base) != "Sketcher::SketchObject":
                        _wrn(
                            translate(
                                "Arch", "Window not based on sketch. Window not aligned or resized."
                            )
                        )
                        self.Include = False
                        break
                    AuraCADGui.doCommand("win = AuraCAD.ActiveDocument.getObject('" + o.Name + "')")
                    AuraCADGui.doCommand("win.Base.Placement = pl")
                    # Historically, this normal was deduced by the orientation of the Base Sketch and hardcoded in the Normal property.
                    # Now with the new AutoNormalReversed property/flag, set True as default, the auto Normal previously in opposite direction to is now consistent with that previously hardcoded.
                    # With the normal set to 'auto', window object would not suffer weird shape if the Base Sketch is rotated by some reason.
                    # Keep the property be 'auto' (0,0,0) here.
                    # AuraCADGui.doCommand("win.Normal = pl.Rotation.multVec(AuraCAD.Vector(0, 0, -1))")
                    AuraCADGui.doCommand("win.Width = " + str(self.Width))
                    AuraCADGui.doCommand("win.Height = " + str(self.Height))
                    AuraCADGui.doCommand("win.Base.recompute()")
                    if not self.has_width_and_height_constraint(o.Base):
                        _wrn(
                            translate(
                                "Arch",
                                "No Width and/or Height constraint in window sketch. Window not resized.",
                            )
                        )
                    break
            else:
                _wrn(translate("Arch", "No window found. Cannot continue."))
                self.Include = False

        else:
            # preset
            preset = True
            wp = ""
            for p in self.wparams:
                wp += ", " + p.lower() + "=" + str(getattr(self, p))
            import ArchSketchObject

            if (
                host
                and hasattr(host, "Base")
                and Draft.getType(host.Base) == "ArchSketch"
                and hasattr(ArchSketchObject, "attachToHost")
                and hasattr(AuraCAD, "ArchSketchLock")
                and AuraCAD.ArchSketchLock
            ):
                if self.Include:
                    # Window base sketch's placement stay at origin is good if addon exists and self.Include
                    #
                    # Put Sketch in 'upright' position to ensure the opening symbol on plan (SymbolPlan enabled) is correct
                    # - see https://github.com/AuraCAD/AuraCAD/issues/24903#issuecomment-3475455946
                    # placement = AuraCAD.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))
                    # TODO 2025.11.1 : To improve the algorithm to be more robust to allow the Base Sketch in any orientation but without problem
                    AuraCADGui.doCommand(
                        "pl90 = AuraCAD.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))"
                    )
                    AuraCADGui.doCommand(
                        "win = Arch.makeWindowPreset('"
                        + WindowPresets[self.Preset]
                        + "' "
                        + wp
                        + ", placement=pl90"
                        + ")"
                    )
                else:
                    # Window base sketch's placement follow getPoint placement if addon exists but NOT self.Include
                    AuraCADGui.doCommand(
                        "win = Arch.makeWindowPreset('"
                        + WindowPresets[self.Preset]
                        + "' "
                        + wp
                        + ", placement=pl"
                    )
                    AuraCADGui.doCommand("win.AttachToAxisOrSketch = 'None'")
                AuraCADGui.doCommand("AuraCADGui.Selection.addSelection(win)")
                w = AuraCADGui.Selection.getSelection()[0]
                AuraCADGui.doCommand("AuraCAD.SketchArchPl = pl")
                wPl = AuraCAD.SketchArchPl
                SketchArch = True
            else:
                AuraCADGui.doCommand(
                    "win = Arch.makeWindowPreset('"
                    + WindowPresets[self.Preset]
                    + "' "
                    + wp
                    + ", placement = pl)"
                )
                SketchArch = False

        if self.Include:
            if Draft.getType(host) in ALLOWEDHOSTS:
                AuraCADGui.doCommand("win.Hosts = [AuraCAD.ActiveDocument." + host.Name + "]")
                siblings = host.Proxy.getSiblings(host)
                for sibling in siblings:
                    AuraCADGui.doCommand(
                        "win.Hosts = win.Hosts + [AuraCAD.ActiveDocument." + sibling.Name + "]"
                    )
                if SketchArch:
                    ArchSketchObject.attachToHost(w, target=host, pl=wPl)

        self.doc.commitTransaction()
        self.doc.recompute()
        # gui_utils.end_all_events()  # Causes a crash on Linux.
        self.tracker.finalize()
        return

    def update(self, point, info):
        "this function is called by the Snapper when the mouse is moved"

        delta = AuraCAD.Vector(self.Width / 2, self.W1 / 2, self.Height / 2)
        delta = delta.add(AuraCAD.Vector(0, 0, self.SillHeight))

        if self.baseFace is None:
            rot = AuraCAD.Rotation(self.wp.u, self.wp.v, -self.wp.axis, "XZY")
            self.tracker.setRotation(rot)
        if info:
            if "Face" in info["Component"]:
                import DraftGeomUtils

                o = self.doc.getObject(info["Object"])
                self.baseFace = [o, int(info["Component"][4:]) - 1]
                # print("switching to ",o.Label," face ",self.baseFace[1])
                f = o.Shape.Faces[self.baseFace[1]]
                p = DraftGeomUtils.placement_from_face(f, vec_z=self.wp.axis, rotated=True)
                rot = p.Rotation
                self.tracker.setRotation(rot)
        r = self.tracker.trans.rotation.getValue().getValue()
        if r != (0, 0, 0, 1):
            delta = AuraCAD.Rotation(r[0], r[1], r[2], r[3]).multVec(
                AuraCAD.Vector(delta.x, -delta.y, -delta.z)
            )
        self.tracker.pos(point.add(delta))

    def taskbox(self):
        "sets up a taskbox widget"

        from draftutils import params
        from PySide import QtCore, QtGui, QtSvgWidgets
        from ArchWindowPresets import WindowPresets

        w = QtGui.QWidget()
        ui = AuraCADGui.UiLoader()
        w.setWindowTitle(translate("Arch", "Window Options"))
        grid = QtGui.QGridLayout(w)

        # include box
        include = QtGui.QCheckBox(translate("Arch", "Auto include in host object"))
        include.setChecked(True)
        grid.addWidget(include, 0, 0, 1, 2)
        if hasattr(include, "checkStateChanged"):  # Qt version >= 6.7.0
            include.checkStateChanged.connect(self.setInclude)
        else:  # Qt version < 6.7.0
            include.stateChanged.connect(self.setInclude)

        # sill height
        labels = QtGui.QLabel(translate("Arch", "Sill height"))
        values = ui.createWidget("Gui::InputField")
        grid.addWidget(labels, 1, 0, 1, 1)
        grid.addWidget(values, 1, 1, 1, 1)
        values.valueChanged.connect(self.setSillHeight)

        # check for Parts library and Arch presets

        # because of the use of AuraCADGui.doCommand() backslashes in the
        # paths in librarypresets need to be double escaped "\\\\", so let's
        # use forward slashes instead...
        self.librarypresets = []
        librarypath = AuraCAD.ParamGet("User parameter:Plugins/parts_library").GetString(
            "destination", ""
        )
        # librarypath should have only forward slashes already, but let's use replace() anyway just to be sure:
        librarypath = librarypath.replace("\\", "/") + "/Architectural Parts"
        presetdir = AuraCAD.getUserAppDataDir().replace("\\", "/") + "/Arch"
        for path in [librarypath, presetdir]:
            if os.path.isdir(path):
                for wtype in ["Windows", "Doors"]:
                    wdir = path + "/" + wtype
                    if os.path.isdir(wdir):
                        for subtype in os.listdir(wdir):
                            subdir = wdir + "/" + subtype
                            if os.path.isdir(subdir):
                                for subfile in os.listdir(subdir):
                                    if os.path.isfile(
                                        subdir + "/" + subfile
                                    ) and subfile.lower().endswith(".auracadstd"):
                                        self.librarypresets.append(
                                            [
                                                wtype + " - " + subtype + " - " + subfile[:-6],
                                                subdir + "/" + subfile,
                                            ]
                                        )

        # presets box
        labelp = QtGui.QLabel(translate("Arch", "Preset"))
        valuep = QtGui.QComboBox()
        valuep.setMinimumContentsLength(6)
        valuep.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        valuep.addItems(WindowPresets)
        valuep.setCurrentIndex(self.Preset)
        grid.addWidget(labelp, 2, 0, 1, 1)
        grid.addWidget(valuep, 2, 1, 1, 1)
        valuep.currentIndexChanged.connect(self.setPreset)
        for it in self.librarypresets:
            valuep.addItem(it[0])

        # image display
        self.pic = QtGui.QLabel()
        grid.addWidget(self.pic, 3, 0, 1, 2)
        self.pic.setFixedHeight(128)
        self.pic.hide()

        # SVG display
        self.im = QtSvgWidgets.QSvgWidget(":/ui/ParametersWindowFixed.svg")
        self.im.setMaximumWidth(200)
        self.im.setMinimumHeight(120)
        grid.addWidget(self.im, 4, 0, 1, 2)
        # self.im.hide()

        # parameters
        i = 5
        for param in self.wparams:
            lab = QtGui.QLabel(translate("Arch", param))
            setattr(self, "val" + param, ui.createWidget("Gui::InputField"))
            wid = getattr(self, "val" + param)
            if param == "W1":
                wid.setText(AuraCAD.Units.Quantity(self.W1, AuraCAD.Units.Length).UserString)
            elif param == "Width":
                wid.setText(AuraCAD.Units.Quantity(self.Width, AuraCAD.Units.Length).UserString)
            elif param == "Height":
                wid.setText(AuraCAD.Units.Quantity(self.Height, AuraCAD.Units.Length).UserString)
            else:
                n = params.get_param_arch("Window" + param)
                wid.setText(AuraCAD.Units.Quantity(n, AuraCAD.Units.Length).UserString)
                setattr(self, param, n)
            grid.addWidget(lab, i, 0, 1, 1)
            grid.addWidget(wid, i, 1, 1, 1)
            i += 1
            valueChanged = self.getValueChanged(param)
            AuraCAD.wid = wid
            QtCore.QObject.connect(
                getattr(self, "val" + param), QtCore.SIGNAL("valueChanged(double)"), valueChanged
            )

        # restore saved states
        if self.doormode:
            i = params.get_param_arch("DoorPreset")
            d = params.get_param_arch("DoorSill")
        else:
            i = params.get_param_arch("WindowPreset")
            d = params.get_param_arch("WindowSill")
        if i < valuep.count():
            valuep.setCurrentIndex(i)
        values.setText(AuraCAD.Units.Quantity(d, AuraCAD.Units.Length).UserString)

        return w

    def getValueChanged(self, p):

        return lambda d: self.setParams(p, d)

    def setSillHeight(self, d):

        from draftutils import params

        self.SillHeight = d
        if self.doormode:
            params.set_param_arch("DoorSill", d)
        else:
            params.set_param_arch("WindowSill", d)

    def setInclude(self, i):

        self.Include = bool(getattr(i, "value", i))

    def setParams(self, param, d):

        from draftutils import params

        setattr(self, param, d)
        self.tracker.length(self.Width)
        self.tracker.height(self.Height)
        self.tracker.width(self.W1)
        prefix = "Door" if self.doormode and param in ("Width", "Height") else "Window"
        params.set_param_arch(prefix + param, d)

    def setPreset(self, i):

        from PySide import QtGui
        from draftutils import params
        from ArchWindowPresets import WindowPresets

        self.Preset = i
        if self.doormode:
            params.set_param_arch("DoorPreset", i)
        else:
            params.set_param_arch("WindowPreset", i)
        if i >= 0:
            AuraCADGui.Snapper.setSelectMode(False)
            self.tracker.length(self.Width)
            self.tracker.height(self.Height)
            self.tracker.width(self.W1)
            self.tracker.on()
            self.pic.hide()
            self.im.show()
            if i == 0:
                self.im.load(":/ui/ParametersWindowFixed.svg")
            elif i in [1, 9]:
                self.im.load(":/ui/ParametersWindowSimple.svg")
            elif i in [2, 4, 8]:
                self.im.load(":/ui/ParametersWindowDouble.svg")
            elif i == 3:
                self.im.load(":/ui/ParametersWindowStash.svg")
            elif i in [5, 6]:
                self.im.load(":/ui/ParametersDoorSimple.svg")
            elif i == 7:
                self.im.load(":/ui/ParametersDoorGlass.svg")
            elif i == 10:
                self.im.load(":/ui/ParametersOpening.svg")
            else:
                # From Library
                self.im.hide()
                path = self.librarypresets[i - len(WindowPresets)][1]
                if path.lower().endswith(".auracadstd"):
                    try:
                        import tempfile
                        import zipfile
                    except Exception:
                        pass
                    else:
                        zfile = zipfile.ZipFile(path)
                        files = zfile.namelist()
                        # check for meta-file if it's really a AuraCAD document
                        if files[0] == "Document.xml":
                            image = "thumbnails/Thumbnail.png"
                            if image in files:
                                image = zfile.read(image)
                                thumbfile = tempfile.mkstemp(suffix=".png")[1]
                                thumb = open(thumbfile, "wb")
                                thumb.write(image)
                                thumb.close()
                                im = QtGui.QPixmap(thumbfile)
                                self.pic.setPixmap(im)
                                self.pic.show()
            # for param in self.wparams:
            #    getattr(self,"val"+param).setEnabled(True)
        else:
            AuraCADGui.Snapper.setSelectMode(True)
            self.tracker.off()
            self.im.hide()
            for param in self.wparams:
                getattr(self, "val" + param).setEnabled(False)


AuraCADGui.addCommand("Arch_Window", Arch_Window())
