# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2022 Yorik van Havre <yorik@uncreated.net>              *
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


import AuraCAD
import AuraCADGui
import ArchBuildingPart

translate = AuraCAD.Qt.translate


class iAuraCAD_vp_object:
    """Base class for all blenderbim view providers"""

    def attach(self, vobj):
        self.Object = vobj.Object

    def getDisplayModes(self, obj):
        return []

    def getDefaultDisplayMode(self):
        return "FlatLines"

    def setDisplayMode(self, mode):
        return mode

    def onChanged(self, vobj, prop):
        if prop == "Visibility":
            for child in vobj.Object.Group:
                child.ViewObject.Visibility = vobj.Visibility
            return True
        elif prop == "LineColor" and vobj.Object.ShapeMode == "Coin":
            lc = vobj.LineColor
            basenode = vobj.RootNode.getChild(2).getChild(0)
            if basenode.getNumChildren() == 5:
                basenode[4][0][3].diffuseColor.setValue(lc[0], lc[1], lc[2])
        elif prop == "LineWidth" and vobj.Object.ShapeMode == "Coin":
            basenode = vobj.RootNode.getChild(2).getChild(0)
            if basenode.getNumChildren() == 5:
                basenode[4][0][4].lineWidth = vobj.LineWidth

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def updateData(self, obj, prop):
        if prop == "Shape" and getattr(obj, "Group", None):
            colors = []
            for child in obj.Group:
                if hasattr(child.ViewObject, "DiffuseColor"):
                    colors.extend(child.ViewObject.DiffuseColor)
            if colors:
                obj.ViewObject.DiffuseColor = colors

    def getIcon(self):
        return get_icon(self)

    def claimChildren(self):
        if hasattr(self.Object, "Group"):
            return self.Object.Group
        return []

    def setupContextMenu(self, vobj, menu):
        from . import iAuraCAD_tools  # lazy import
        from . import iAuraCAD_psets
        from . import iAuraCAD_materials
        from . import iAuraCAD_types
        from PySide import QtGui  # lazy import

        if AuraCADGui.activeWorkbench().name() != "BIMWorkbench":
            return

        icon = QtGui.QIcon(":/icons/Iauracad.svg")
        element = iAuraCAD_tools.get_iAuraCAD_element(vobj.Object)
        iAuraCAD_menu = None

        # Iauracad actions
        actions = []
        if element.is_a("IauracadSpatialElement"):
            if AuraCADGui.ActiveDocument.ActiveView.getActiveObject("NativeIauracad") == vobj.Object:
                t = translate("BIM", "Deactivate Container")
            else:
                t = translate("BIM", "Make Active Container")
            action_activate = QtGui.QAction(icon, t, menu)
            action_activate.triggered.connect(self.activate)
            menu.addAction(action_activate)
        if self.hasChildren(vobj.Object):
            action_expand = QtGui.QAction(icon, translate("BIM", "Expand Children"), menu)
            action_expand.triggered.connect(self.expandChildren)
            actions.append(action_expand)
        if vobj.Object.Group:
            action_shrink = QtGui.QAction(icon, translate("BIM", "Collapse Children"), menu)
            action_shrink.triggered.connect(self.collapseChildren)
            actions.append(action_shrink)
        if vobj.Object.ShapeMode == "Shape":
            t = translate("BIM", "Remove Shape")
        else:
            t = translate("BIM", "Load Shape")
        action_shape = QtGui.QAction(icon, t, menu)
        action_shape.triggered.connect(self.switchShape)
        actions.append(action_shape)
        if vobj.Object.ShapeMode == "None":
            action_coin = QtGui.QAction(icon, translate("BIM", "Load Representation"), menu)
            action_coin.triggered.connect(self.switchCoin)
            actions.append(action_coin)
        if element and iAuraCAD_tools.has_representation(element):
            action_geom = QtGui.QAction(icon, translate("BIM", "Add Geometry Properties"), menu)
            action_geom.triggered.connect(self.addGeometryProperties)
            actions.append(action_geom)
        action_tree = QtGui.QAction(icon, translate("BIM", "Show Geometry Tree"), menu)
        action_tree.triggered.connect(self.showTree)
        actions.append(action_tree)
        if iAuraCAD_psets.has_psets(self.Object):
            action_props = QtGui.QAction(icon, translate("BIM", "Expand Property Sets"), menu)
            action_props.triggered.connect(self.showProps)
            actions.append(action_props)
        if iAuraCAD_materials.get_material(self.Object):
            action_material = QtGui.QAction(icon, translate("BIM", "Load Material"), menu)
            action_material.triggered.connect(self.addMaterial)
            actions.append(action_material)
        if iAuraCAD_types.is_typable(self.Object):
            action_type = QtGui.QAction(icon, translate("BIM", "Convert to Type"), menu)
            action_type.triggered.connect(self.convertToType)
            actions.append(action_type)
        if actions:
            iAuraCAD_menu = QtGui.QMenu("Iauracad")
            iAuraCAD_menu.setIcon(icon)
            iAuraCAD_menu.addActions(actions)
            menu.addMenu(iAuraCAD_menu)

        # generic actions
        ficon = QtGui.QIcon.fromTheme("folder", QtGui.QIcon(":/icons/folder.svg"))
        action_group = QtGui.QAction(ficon, translate("BIM", "New Group"), menu)
        action_group.triggered.connect(self.createGroup)
        menu.addAction(action_group)

        # return submenu for derivated classes
        return iAuraCAD_menu

    def hasChildren(self, obj):
        """Returns True if this Iauracad object can be decomposed"""

        from . import iAuraCAD_tools  # lazy import

        iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
        if iauracadfile:
            return iAuraCAD_tools.can_expand(obj, iauracadfile)
        return False

    def expandChildren(self, obj=None):
        """Creates children of this object"""

        from . import iAuraCAD_tools  # lazy import
        from PySide import QtCore, QtGui

        if not obj:
            obj = self.Object
        iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
        nc = []
        if iauracadfile:
            nc = iAuraCAD_tools.create_children(
                obj, iauracadfile, recursive=False, assemblies=True, expand=False
            )
        obj.Document.recompute()
        AuraCADGui.updateGui()

        # expand the item in the tree view
        mw = AuraCADGui.getMainWindow()
        tree = mw.findChild(QtGui.QDockWidget, "Model")
        model = tree.findChild(QtGui.QWidget, "Model")
        splitter = model.findChild(QtGui.QSplitter)
        if splitter and len(splitter.children()) > 1:
            if splitter.children()[1].children():
                tree = splitter.children()[1].children()[0]
                it = tree.findItems(obj.Label, QtCore.Qt.MatchRecursive, 0)
                if it:
                    it[0].setExpanded(True)
                    for i in range(it[0].childCount()):
                        it[0].child(i).setExpanded(True)
        return nc

    def collapseChildren(self):
        """Collapses the children of this object"""

        objs = self.Object.Group
        for o in objs:
            objs.extend(self.getOwnChildren(o))
        for o in objs:
            if hasattr(o, "Proxy"):
                # this prevents to trigger the deletion inside the Iauracad file
                o.Proxy.nodelete = True
        names = [o.Name for o in objs]
        for name in names:
            self.Object.Document.removeObject(name)
        self.Object.Document.recompute()

    def getOwnChildren(self, obj):
        """Recursively gets the children only used by this object"""
        children = []
        for child in obj.OutList:
            if len(child.InList) == 1 and child.InList[0] == obj:
                children.append(child)
                children.extend(self.getOwnChildren(child))
        return children

    def switchShape(self):
        """Switch this object between shape and coin"""

        if self.Object.ShapeMode == "Shape":
            self.Object.ShapeMode = "Coin"
            import Part  # lazy loading

            self.Object.Shape = Part.Shape()
        else:
            self.Object.ShapeMode = "Shape"
        self.Object.Document.recompute()
        self.Object.ViewObject.DiffuseColor = self.Object.ViewObject.DiffuseColor
        self.Object.ViewObject.signalChangeIcon()

    def switchCoin(self):
        """Switch this object between coin and no representation"""

        changed = []
        if self.Object.ShapeMode == "None":
            self.Object.ShapeMode = "Coin"
            changed.append(self.Object.ViewObject)
        # reveal children
        for child in self.Object.OutListRecursive:
            if getattr(child, "ShapeMode", 0) == 2:
                child.ShapeMode = 1
                changed.append(child.ViewObject)
        self.Object.Document.recompute()
        for vobj in changed:
            vobj.DiffuseColor = vobj.DiffuseColor

    def addGeometryProperties(self):
        """Adds geometry properties to this object"""

        from . import iAuraCAD_geometry  # lazy loading

        iAuraCAD_geometry.add_geom_properties(self.Object)

    def addMaterial(self):
        """Adds a material to this object"""

        from . import iAuraCAD_materials  # lazy loading

        iAuraCAD_materials.show_material(self.Object)
        self.Object.Document.recompute()

    def showTree(self):
        """Shows a dialog with a geometry tree for the object"""

        from . import iAuraCAD_tools  # lazy loading
        from . import iAuraCAD_tree  # lazy loading

        element = iAuraCAD_tools.get_iAuraCAD_element(self.Object)
        if element:
            iAuraCAD_tree.show_geometry_tree(element)

    def showProps(self):
        """Expands property sets"""

        from . import iAuraCAD_psets  # lazy loading

        iAuraCAD_psets.show_psets(self.Object)
        self.Object.Document.recompute()

    def canDragObjects(self):
        """Whether children can be removed by d&d"""

        return True

    def canDropObjects(self):
        """Whether objects can be added here by d&d or drop only"""

        return True

    def canDragObject(self, dragged_object):
        """Whether the given object can be removed by d&d"""

        return True

    def canDropObject(self, incoming_object):
        """Whether the object can be dropped here by d&d or drop only"""

        return True  # in principle, any object can be dropped and become Iauracad

    def dragObject(self, vobj, dragged_object):
        """Remove a child from the view provider by d&d"""

        from . import iAuraCAD_tools  # lazy import

        parent = vobj.Object
        iAuraCAD_tools.deaggregate(dragged_object, parent)

    def dropObject(self, vobj, incoming_object):
        """Add an object to the view provider by d&d"""

        from PySide import QtCore  # lazy import

        # delay the action to prevent the object to be deleted
        # before the end of the drop
        QtCore.QTimer.singleShot(100, lambda: self.onDrop(incoming_object))

    def onDrop(self, incoming_object):
        """Delayed action to be taken when dropping an object"""

        from . import iAuraCAD_tools  # lazy import

        iAuraCAD_tools.aggregate(incoming_object, self.Object)
        if self.hasChildren(self.Object):
            self.expandChildren(self.Object)

    def activate(self):
        """Marks this container as active"""

        if AuraCADGui.ActiveDocument.ActiveView.getActiveObject("NativeIauracad") == self.Object:
            AuraCADGui.ActiveDocument.ActiveView.setActiveObject("NativeIauracad", None)
        else:
            AuraCADGui.ActiveDocument.ActiveView.setActiveObject("NativeIauracad", self.Object)

    def createGroup(self):
        """Creates a group under this object"""

        from . import iAuraCAD_tools  # lazy import

        group = self.Object.Document.addObject("App::DocumentObjectGroup", "Group")
        iAuraCAD_tools.aggregate(group, self.Object)
        self.Object.Document.recompute()

    def doubleClicked(self, vobj):
        """On double-click"""

        self.expandProperties(vobj)

    def expandProperties(self, vobj):
        """Expands everything that needs to be expanded"""

        from . import iAuraCAD_geometry  # lazy import
        from . import iAuraCAD_tools  # lazy import
        from . import iAuraCAD_psets  # lazy import
        from . import iAuraCAD_materials  # lazy import
        from . import iAuraCAD_layers  # lazy import
        from . import iAuraCAD_types  # lazy import
        from . import iAuraCAD_classification  # lazy import

        # generic data loading
        iAuraCAD_geometry.add_geom_properties(vobj.Object)
        iAuraCAD_psets.show_psets(vobj.Object)
        iAuraCAD_materials.show_material(vobj.Object)
        iAuraCAD_layers.add_layers(vobj.Object)
        iAuraCAD_types.show_type(vobj.Object)
        iAuraCAD_classification.show_classification(vobj.Object)

        # expand children
        if self.hasChildren(vobj.Object):
            self.expandChildren()
            return True

        # load shape
        element = iAuraCAD_tools.get_iAuraCAD_element(vobj.Object)
        if iAuraCAD_tools.has_representation(element):
            if vobj.Object.ShapeMode != "Shape":
                vobj.Object.ShapeMode = "Shape"
                vobj.Object.Document.recompute()
                return True
        return None

    def convertToType(self):
        """Converts this object to a type"""

        if not hasattr(self, "Object"):
            return
        from . import iAuraCAD_types

        iAuraCAD_types.convert_to_type(self.Object)
        self.Object.Document.recompute()


class iAuraCAD_vp_document(iAuraCAD_vp_object):
    """View provider for the Iauracad document object"""

    def getIcon(self):
        iconpath = ":/icons/IAuraCAD_document.svg"
        if self.Object.Modified:
            if not hasattr(self, "modicon"):
                self.modicon = overlay(iconpath, ":/icons/media-record.svg")
            return self.modicon
        else:
            return iconpath

    def setupContextMenu(self, vobj, menu):

        from PySide import QtGui  # lazy import

        if AuraCADGui.activeWorkbench().name() != "BIMWorkbench":
            return

        iAuraCAD_menu = super().setupContextMenu(vobj, menu)
        if not iAuraCAD_menu:
            iAuraCAD_menu = menu

        icon = QtGui.QIcon(":/icons/Iauracad.svg")
        if vobj.Object.Modified:
            action_diff = QtGui.QAction(icon, translate("BIM", "View Diff"), menu)
            action_diff.triggered.connect(self.diff)
            iAuraCAD_menu.addAction(action_diff)
            if vobj.Object.IauracadFilePath:
                action_save = QtGui.QAction(icon, translate("BIM", "Save Iauracad File"), menu)
                action_save.triggered.connect(self.save)
                iAuraCAD_menu.addAction(action_save)
        action_saveas = QtGui.QAction(icon, translate("BIM", "Save Iauracad File Asâ€¦"), menu)
        action_saveas.triggered.connect(self.saveas)
        iAuraCAD_menu.addAction(action_saveas)

    def save(self):
        """Saves the associated Iauracad file"""

        from . import iAuraCAD_tools  # lazy import

        iAuraCAD_tools.save(self.Object)
        self.Object.Document.recompute()

    def saveas(self):
        """Saves the associated Iauracad file to another file"""

        from . import iAuraCAD_tools  # lazy import

        sf = get_filepath(self.Object)
        if sf:
            iAuraCAD_tools.save(self.Object)
            self.replace_file(self.Object, sf)
            self.Object.Document.recompute()

    def replace_file(self, obj, newfile):
        """Asks the user if the attached file path needs to be replaced"""

        from PySide import QtGui  # lazy import

        msg = "Replace the stored Iauracad file path in object "
        msg += self.Object.Label + " with the new one: "
        msg += newfile
        msg += " ?"
        dlg = QtGui.QMessageBox.question(
            None,
            "Replace Iauracad File Path?",
            msg,
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No,
        )
        if dlg == QtGui.QMessageBox.Yes:
            self.Object.IauracadFilePath = newfile
            self.Object.Modified = False
            return True
        else:
            return False

    def schema_warning(self):
        from PySide import QtGui  # lazy import

        msg = "Warning: This operation will change the whole Iauracad file contents "
        msg += "and will not give versionable results. It is best to not do "
        msg += "this while you are in the middle of a project. "
        msg += "Continue anyway?"
        dlg = QtGui.QMessageBox.question(
            None,
            "Replace Iauracad File Schema?",
            msg,
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No,
        )
        if dlg == QtGui.QMessageBox.Yes:
            return True
        else:
            return False

    def diff(self):
        from . import iAuraCAD_diff

        diff = iAuraCAD_diff.get_diff(self.Object)
        iAuraCAD_diff.show_diff(diff)


class iAuraCAD_vp_group:
    """View provider for the Iauracad group object"""

    def attach(self, vobj):
        self.Object = vobj.Object

    def getIcon(self):
        from PySide import QtGui  # lazy loading
        import Draft_rc
        import Arch_rc

        if "Layer" in self.Object.Name:
            return ":/icons/Draft_Layer.svg"
        elif "Material" in self.Object.Name:
            return ":/icons/Arch_Material_Group.svg"
        elif not hasattr(self, "modicon"):
            self.modicon = overlay(
                QtGui.QIcon.fromTheme("folder", QtGui.QIcon(":/icons/folder.svg")),
                ":/icons/Iauracad.svg",
            )
        return self.modicon


class iAuraCAD_vp_material:
    """View provider for the Iauracad group object"""

    def attach(self, vobj):
        self.Object = vobj.Object

    def getDisplayModes(self, obj):
        return []

    def getDefaultDisplayMode(self):
        return "Default"

    def setDisplayMode(self, mode):
        return mode

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def getIcon(self):
        if hasattr(self, "icondata"):
            return self.icondata
        else:
            import Arch_rc

            return ":/icons/Arch_Material.svg"

    def updateData(self, obj, prop):
        from PySide import QtCore, QtGui  # lazy loading

        if hasattr(self.Object, "Color"):
            c = self.Object.Color
            matcolor = QtGui.QColor(int(c[0] * 255), int(c[1] * 255), int(c[2] * 255))
            darkcolor = QtGui.QColor(int(c[0] * 125), int(c[1] * 125), int(c[2] * 125))
        else:
            matcolor = QtGui.QColor(200, 200, 200)
            darkcolor = QtGui.QColor(120, 120, 120)
        im = QtGui.QImage(48, 48, QtGui.QImage.Format_ARGB32)
        im.fill(QtCore.Qt.transparent)
        pt = QtGui.QPainter(im)
        pt.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine, QtCore.Qt.FlatCap))
        gradient = QtGui.QLinearGradient(0, 0, 48, 48)
        gradient.setColorAt(0, matcolor)
        gradient.setColorAt(1, darkcolor)
        pt.setBrush(QtGui.QBrush(gradient))
        pt.drawEllipse(6, 6, 36, 36)
        pt.setPen(QtGui.QPen(QtCore.Qt.white, 1, QtCore.Qt.SolidLine, QtCore.Qt.FlatCap))
        pt.setBrush(QtGui.QBrush(QtCore.Qt.white, QtCore.Qt.SolidPattern))
        pt.drawEllipse(12, 12, 12, 12)
        pt.end()
        ba = QtCore.QByteArray()
        b = QtCore.QBuffer(ba)
        b.open(QtCore.QIODevice.WriteOnly)
        im.save(b, "XPM")
        self.icondata = ba.data().decode("latin1")

    def claimChildren(self):
        if hasattr(self.Object, "Group"):
            return self.Object.Group
        return []

    def setupContextMenu(self, vobj, menu):
        from . import iAuraCAD_tools  # lazy import
        from . import iAuraCAD_psets
        from PySide import QtGui  # lazy import

        if AuraCADGui.activeWorkbench().name() != "BIMWorkbench":
            return

        icon = QtGui.QIcon(":/icons/Iauracad.svg")
        if iAuraCAD_psets.has_psets(self.Object):
            action_props = QtGui.QAction(icon, translate("BIM", "Expand Property Sets"), menu)
            action_props.triggered.connect(self.showProps)
            menu.addAction(action_props)

    def showProps(self):
        """Expands property sets"""

        from . import iAuraCAD_psets  # lazy loading

        iAuraCAD_psets.show_psets(self.Object)
        self.Object.Document.recompute()


class iAuraCAD_vp_buildingpart(iAuraCAD_vp_object, ArchBuildingPart.ViewProviderBuildingPart):
    """A vp that inherits the Arch BuildingPart vp, but keeps aggregating properties of iauracad vp"""

    def __init__(self, vobj):
        ArchBuildingPart.ViewProviderBuildingPart.__init__(self, vobj)

    def attach(self, vobj):
        ArchBuildingPart.ViewProviderBuildingPart.attach(self, vobj)


def overlay(icon1, icon2):
    """Overlays icon2 onto icon1"""

    from PySide import QtCore, QtGui  # lazy loading

    if isinstance(icon1, QtGui.QIcon):
        baseicon = icon1.pixmap(32, 32)
        baseicon = QtGui.QImage(
            baseicon.toImage().convertToFormat(QtGui.QImage.Format_ARGB32_Premultiplied)
        )
    elif isinstance(icon1, str):
        baseicon = QtGui.QImage(icon1)
    if isinstance(icon2, str):
        overlay = QtGui.QImage(icon2)
    width = baseicon.width() / 2
    overlay = overlay.scaled(width, width)
    painter = QtGui.QPainter()
    painter.begin(baseicon)
    painter.drawImage(1, 1, overlay)
    painter.end()
    ba = QtCore.QByteArray()
    b = QtCore.QBuffer(ba)
    b.open(QtCore.QIODevice.WriteOnly)
    baseicon.save(b, "XPM")
    return ba.data().decode("latin1")


def get_filepath(project):
    """Saves the associated Iauracad file to another file"""

    from . import iAuraCAD_tools  # lazy import
    from PySide import QtGui  # lazy import

    sf = QtGui.QFileDialog.getSaveFileName(
        None,
        "Save an Iauracad File",
        project.IauracadFilePath,
        "Industry Foundation Classes (*.iauracad)",
    )
    if sf and sf[0]:
        sf = sf[0]
        if not sf.lower().endswith(".iauracad"):
            sf += ".iauracad"
        project.IauracadFilePath = sf
        return sf
    return None


def get_icon(vp):
    """Returns an icon for a view provider"""

    from PySide import QtCore, QtGui  # lazy import

    if hasattr(vp, "Object"):
        if hasattr(vp.Object, "IauracadClass"):
            rclass = vp.Object.IauracadClass.replace("StandardCase", "")
            rclass = vp.Object.IauracadClass.replace("Type", "")
            iauracadicon = ":/icons/Iauracad/" + rclass + ".svg"
            if QtCore.QFile.exists(iauracadicon):
                if getattr(vp, "iauracadclass", "") != rclass:
                    vp.iauracadclass = rclass
                    vp.iauracadicon = overlay(iauracadicon, ":/icons/Iauracad.svg")
                return getattr(vp, "iauracadicon", overlay(iauracadicon, ":/icons/Iauracad.svg"))
            elif vp.Object.IauracadClass == "IauracadGroup":
                return QtGui.QIcon.fromTheme("folder", QtGui.QIcon(":/icons/folder.svg"))
            elif vp.Object.ShapeMode == "Shape":
                return ":/icons/IAuraCAD_object.svg"
            else:
                return ":/icons/IAuraCAD_mesh.svg"
    return ":/icons/IAuraCAD_object.svg"
