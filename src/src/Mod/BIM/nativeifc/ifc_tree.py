# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2023 Yorik van Havre <yorik@uncreated.net>              *
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

"""This NativeIauracad module handles the retrieval and display of geometry compositions of objects"""

import AuraCAD

TAB = 2


def get_geometry_tree(element, prefix=""):
    """Returns a list of elements representing an object's representation"""

    result = [prefix + str(element)]
    prefix += TAB * " "
    if getattr(element, "Representation", None):
        reps = element.Representation
        result.append(prefix + str(reps))
        prefix += prefix
        for rep in reps.Representations:
            result.extend(get_geometry_tree(rep, prefix))
    elif getattr(element, "Items", None):
        for it in element.Items:
            result.extend(get_geometry_tree(it, prefix))
    elif element.is_a("IauracadPolyline"):
        for p in element.Points:
            result.append(prefix + str(p))
    elif element.is_a("IauracadExtrudedAreaSolid"):
        result.append(prefix + str(element.ExtrudedDirection))
        result.extend(get_geometry_tree(element.SweptArea, prefix))
    elif element.is_a("IauracadArbitraryClosedProfileDef"):
        result.extend(get_geometry_tree(element.OuterCurve, prefix))
    elif element.is_a("IauracadArbitraryProfileDefWithVoids"):
        result.extend(get_geometry_tree(element.OuterCurve, prefix))
        for inn in element.InnerCurves:
            result.extend(get_geometry_tree(inn, prefix))
    elif element.is_a("IauracadMappedItem"):
        result.extend(get_geometry_tree(element.MappingSource[1], prefix))
    elif element.is_a("IauracadBooleanClippingResult"):
        result.extend(get_geometry_tree(element.FirstOperand, prefix))
        result.extend(get_geometry_tree(element.SecondOperand, prefix))
    elif element.is_a("IauracadBooleanResult"):
        result.extend(get_geometry_tree(element.FirstOperand, prefix))
        result.extend(get_geometry_tree(element.SecondOperand, prefix))
    elif element.is_a("IauracadHalfSpaceSolid"):
        result.extend(get_geometry_tree(element.BaseSurface, prefix))
    return result


def print_geometry_tree(element):
    """Same as get_geometry_tree but printed"""

    for line in get_geometry_tree(element):
        print(line)


def show_geometry_tree(element):
    """Same as get_geometry_tree but in a Qt dialog"""

    import Arch_rc
    import AuraCADGui  # lazy import
    from . import iAuraCAD_tools
    from PySide import QtWidgets

    if isinstance(element, AuraCAD.DocumentObject):
        element = iAuraCAD_tools.get_iAuraCAD_element(element)
        if not element:
            return
    dlg = AuraCADGui.PySideUic.loadUi(":/ui/dialogTree.ui")
    tops = {}
    for line in get_geometry_tree(element):
        psize = (len(line) - len(line.lstrip())) / TAB
        wline = QtWidgets.QTreeWidgetItem([line.lstrip()])
        if not psize:
            dlg.geomtree.addTopLevelItem(wline)
        else:
            parent = tops[psize - 1]
            parent.addChild(wline)
        tops[psize] = wline
    dlg.geomtree.expandAll()
    dlg.setWindowTitle(dlg.windowTitle() + " " + element.Name)
    dlg.geomtree.currentItemChanged.connect(show_properties)
    dlg.proptree.itemChanged.connect(edit_property)
    result = dlg.exec_()
    if result:
        props = [r.split("::") for r in dlg.proptree.toolTip().split(";;;;") if r]
        if not props:
            return
        obj = iAuraCAD_tools.get_object(element)
        iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
        modified = False
        for prop in props:
            elt = iauracadfile[int(prop[0])]
            attrib = prop[1]
            if attrib not in dir(elt):
                print("DEBUG: Unknown attribute:", attrib)
                continue
            value = prop[3]
            if isfloat(getattr(elt, attrib)):
                try:
                    value = float(value)
                except:
                    print("DEBUG: wrong value for", attrib, ":", value)
                    continue
            iAuraCAD_tools.set_attribute(iauracadfile, elt, attrib, value)
            modified = True
        if modified:
            obj.touch()
            proj = iAuraCAD_tools.get_project(obj)
            proj.Modified = True
            obj.Document.recompute()


def isfloat(s):
    """Tells if the given string is a number"""

    try:
        float(s)
    except ValueError:
        return False
    print(s)
    return True


def show_properties(current, previous):
    """Displays object properties"""

    import AuraCADGui
    from . import iAuraCAD_tools  # lazy loading
    from PySide import QtCore, QtWidgets

    iauracadid = int(current.text(0).split("=", 1)[0].strip(" ").strip("#"))
    sel = AuraCADGui.Selection.getSelection()
    if len(sel) != 1:
        return
    obj = sel[0]
    iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
    if not iauracadfile:
        return
    elt = iauracadfile[iauracadid]
    box = current.treeWidget().parentWidget().widget(1)
    box.setTitle("#" + str(iauracadid) + ": " + elt.is_a())
    props = [p for p in dir(elt) if p[0].isupper()]
    # allow only numeric values?
    # props = [p for p in  props if isfloat(str(getattr(elt,p)))]
    props = [p for p in props if not str(getattr(elt, p)).startswith("#")]
    props = [p for p in props if not str(getattr(elt, p)).startswith("(")]
    props = [p for p in props if p not in ["Position", "LayerAssignments", "StyledByItem"]]
    proptree = box.children()[0].itemAt(0).widget()
    proptree.clear()
    proptree.setHorizontalHeaderLabels(["Property", "Value"])
    proptree.setRowCount(len(props))
    for i, prop in enumerate(props):
        value = str(getattr(elt, prop))
        if value == "None":
            value = ""
        r1 = QtWidgets.QTableWidgetItem(prop)
        r1.setFlags(QtCore.Qt.ItemIsSelectable)
        proptree.setItem(i, 0, r1)
        r2 = QtWidgets.QTableWidgetItem(value)
        r2.setToolTip(value)
        if value.startswith("#") or value.startswith("(") or prop == "GlobalId":
            r2.setFlags(QtCore.Qt.ItemIsSelectable)
        proptree.setItem(i, 1, r2)
    if "Position" in dir(elt):
        i = proptree.rowCount()
        proptree.setRowCount(i + 6)
        position = AuraCAD.Vector(elt.Position.Location.Coordinates)
        axis = AuraCAD.Vector(elt.Position.Axis.DirectionRatios)
        xref = AuraCAD.Vector(elt.Position.RefDirection.DirectionRatios)
        rotation = AuraCAD.Rotation(axis, xref, AuraCAD.Vector(), "ZXY").toEulerAngles("XYZ")
        rotation = AuraCAD.Vector(rotation)
        for c in ["x", "y", "z"]:
            r1 = QtWidgets.QTableWidgetItem("Position " + c.upper())
            r1.setFlags(QtCore.Qt.ItemIsSelectable)
            proptree.setItem(i, 0, r1)
            v = str(getattr(position, c))
            r2 = QtWidgets.QTableWidgetItem(v)
            r2.setToolTip(v)
            proptree.setItem(i, 1, r2)
            i += 1
        for c in ["x", "y", "z"]:
            r1 = QtWidgets.QTableWidgetItem("Rotation " + c.upper())
            r1.setFlags(QtCore.Qt.ItemIsSelectable)
            proptree.setItem(i, 0, r1)
            v = str(getattr(rotation, c))
            r2 = QtWidgets.QTableWidgetItem(v)
            r2.setToolTip(v)
            proptree.setItem(i, 1, r2)
            i += 1


def edit_property(item):
    """Edits the value of a property"""

    if item.toolTip() and (item.text() != item.toolTip()):
        old = item.toolTip()
        new = item.text()
        table = item.tableWidget()
        prop = table.item(item.row(), 0).text()
        dlg = table.parent().parent().parent()
        line = dlg.geomtree.currentItem().text(0)
        iauracadid = line.split("=", 1)[0].strip(" ").strip("#")
        strid = ";;;;" + "::".join([str(i) for i in [iauracadid, prop, old, new]])
        dlg.proptree.setToolTip(dlg.proptree.toolTip() + strid)
