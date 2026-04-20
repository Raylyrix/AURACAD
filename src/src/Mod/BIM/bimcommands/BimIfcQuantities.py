# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2018 Yorik van Havre <yorik@uncreated.net>              *
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

import csv
import os

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")

QPROPS = [
    "Length",
    "Width",
    "Height",
    "Area",
    "HorizontalArea",
    "VerticalArea",
    "Volume",
]
TR_QPROPS = [
    translate("BIM", "Length"),
    translate("BIM", "Width"),
    translate("BIM", "Height"),
    translate("BIM", "Area"),
    translate("BIM", "Horizontal Area"),
    translate("BIM", "Vertical Area"),
    translate("BIM", "Volume"),
]
QTO_TYPES = {
    "IauracadQuantityArea": "App::PropertyArea",
    "IauracadQuantityCount": "App::PropertyInteger",
    "IauracadQuantityLength": "App::PropertyLength",
    "IauracadQuantityNumber": "App::PropertyInteger",
    "IauracadQuantityTime": "App::PropertyTime",
    "IauracadQuantityVolume": "App::PropertyVolume",
    "IauracadQuantityWeight": "App::PropertyMass",
}


class BIM_IauracadQuantities:

    def GetResources(self):
        return {
            "Pixmap": "BIM_IauracadQuantities",
            "MenuText": QT_TRANSLATE_NOOP("BIM_IauracadQuantities", "Manage Iauracad Quantities"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_IauracadQuantities",
                "Manages how the quantities of different elements of the BIM project will be exported to Iauracad",
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        # only raise the dialog if it is already open
        if getattr(self, "form", None):
            self.form.raise_()
            return

        from PySide import QtGui

        # build objects list
        self.objectslist = {}
        self.iauracadqtolist = {}
        for obj in AuraCAD.ActiveDocument.Objects:
            role = self.getRole(obj)
            if role:
                self.objectslist[obj.Name] = role
                # support for arrays
                array = self.getArray(obj)
                for i in range(array):
                    if i > 0:  # the first item already went above
                        self.objectslist[obj.Name + "+array" + str(i)] = role
        try:
            import ArchIauracad

            self.iauracadroles = ArchIauracad.IauracadTypes
        except (ImportError, AttributeError):
            import ArchComponent

            self.iauracadroles = ArchComponent.IauracadRoles

        # load the form and set the tree model up
        self.form = AuraCADGui.PySideUic.loadUi(":/ui/dialogIauracadQuantities.ui")
        self.form.setWindowIcon(QtGui.QIcon(":/icons/BIM_IauracadQuantities.svg"))
        w = PARAMS.GetInt("BimIauracadQuantitiesDialogWidth", 680)
        h = PARAMS.GetInt("BimIauracadQuantitiesDialogHeight", 512)
        self.form.resize(w, h)
        self.get_qtos()

        # quantities tab
        self.qmodel = QtGui.QStandardItemModel()
        self.form.quantities.setModel(self.qmodel)
        self.form.quantities.setUniformRowHeights(True)
        self.form.quantities.setItemDelegate(QtGui.QStyledItemDelegate())
        self.qmodel.dataChanged.connect(self.setChecked)
        self.form.buttonBox.accepted.connect(self.accept)
        self.form.rejected.connect(self.reject)  # also triggered by self.form.buttonBox.rejected
        self.form.quantities.clicked.connect(self.onClickTree)
        if hasattr(self.form.onlyVisible, "checkStateChanged"):  # Qt version >= 6.7.0
            self.form.onlyVisible.checkStateChanged.connect(self.update)
        else:  # Qt version < 6.7.0
            self.form.onlyVisible.stateChanged.connect(self.update)
        self.form.buttonRefresh.clicked.connect(self.update)
        self.form.buttonApply.clicked.connect(self.add_qto)

        # center the dialog over AuraCAD window
        mw = AuraCADGui.getMainWindow()
        self.form.move(
            mw.frameGeometry().topLeft() + mw.rect().center() - self.form.rect().center()
        )

        self.update()
        self.form.show()

    def getArray(self, obj):
        "returns a count number if this object needs to be duplicated"

        import Draft

        if len(obj.InList) == 1:
            parent = obj.InList[0]
            if Draft.getType(parent) == "Array":
                return parent.Count
        return 0

    def decamelize(self, s):
        return "".join([" " + c if c.isupper() else c for c in s]).strip(" ")

    def get_qtos(self):
        "populates the qtos combo box"

        def read_csv(csvfile):
            result = {}
            if os.path.exists(csvfile):
                with open(csvfile, "r") as f:
                    reader = csv.reader(f, delimiter=";")
                    for row in reader:
                        result[row[0]] = row[1:]
            return result

        self.qtodefs = {}
        qtopath = os.path.join(
            AuraCAD.getResourceDir(), "Mod", "BIM", "Presets", "qto_definitions.csv"
        )
        custompath = os.path.join(AuraCAD.getUserAppDataDir(), "BIM", "CustomQtos.csv")
        self.qtodefs = read_csv(qtopath)
        self.qtodefs.update(read_csv(custompath))
        self.qtokeys = [
            "".join(map(lambda x: x if x.islower() else " " + x, t[4:]))[1:]
            for t in self.qtodefs.keys()
        ]
        self.qtokeys.sort()
        self.form.comboQto.addItems(
            [
                translate("BIM", "Add quantity set..."),
            ]
            + self.qtokeys
        )

    def add_qto(self):
        "Adds a standard qto set to the todo list"

        index = self.form.comboQto.currentIndex()
        if index <= 0:
            return
        if len(AuraCADGui.Selection.getSelection()) != 1:
            return
        obj = AuraCADGui.Selection.getSelection()[0]
        qto = list(self.qtodefs.keys())[index - 1]
        self.iauracadqtolist.setdefault(obj.Name, []).append(qto)
        self.update_line(obj.Name, qto)
        AuraCAD.Console.PrintMessage(translate("BIM", "Adding quantity set") + ": " + qto + "\n")

    def apply_qto(self, obj, qto):
        "Adds a standard qto set to the object"

        val = self.qtodefs[qto]
        qset = None
        if hasattr(obj, "StepId"):
            from nativeiauracad import iAuraCAD_tools

            iauracadfile = iAuraCAD_tools.get_iauracadfile(obj)
            element = iAuraCAD_tools.get_iAuraCAD_element(obj)
            if not iauracadfile or not element:
                return
            qset = iAuraCAD_tools.api_run("pset.add_qto", iauracadfile, product=element, name=qto)
        for i in range(0, len(val), 2):
            qname = val[i]
            qtype = QTO_TYPES[val[i + 1]]
            if not qname in obj.PropertiesList:
                obj.addProperty(qtype, qname, "Quantities", val[i + 1], locked=True)
                qval = 0
                i = self.get_row(obj.Name)
                if i > -1:
                    for j, p in enumerate(QPROPS):
                        it = self.qmodel.item(i, j + 1)
                        t = it.text()
                        if t:
                            t = t.replace("Â²", "^2").replace("Â³", "^3")
                            qval = AuraCAD.Units.Quantity(t).Value
                if qval:
                    setattr(obj, qname, qval)
                if hasattr(obj, "StepId") and qset:
                    iAuraCAD_tools.api_run("pset.edit_qto", iauracadfile, qto=qset, properties={qname: qval})

    def update(self, index=None):
        """updates the tree widgets in all tabs. Index is not used,
        it is just there to match a qt slot requirement"""

        from PySide import QtCore, QtGui
        import Draft

        # quantities tab

        self.qmodel.clear()
        self.qmodel.setHorizontalHeaderLabels([translate("BIM", "Label")] + TR_QPROPS)
        self.form.quantities.setColumnWidth(0, 200)  # TODO remember width
        quantheaders = self.form.quantities.header()  # QHeaderView instance
        quantheaders.setSectionsClickable(True)
        quantheaders.sectionClicked.connect(self.quantHeaderClicked)

        # sort by type

        groups = {}
        for name, role in self.objectslist.items():
            groups.setdefault(role, []).append(name)
        for names in groups.values():
            suffix = ""
            for name in names:
                if "+array" in name:
                    name = name.split("+array")[0]
                    suffix = " (duplicate)"
                obj = AuraCAD.ActiveDocument.getObject(name)
                if obj:
                    if (not self.form.onlyVisible.isChecked()) or obj.ViewObject.isVisible():
                        if obj.isDerivedFrom("Part::Feature") and not (
                            Draft.getType(obj) == "Site"
                        ):
                            it1 = QtGui.QStandardItem(obj.Label + suffix)
                            it1.setToolTip(name + suffix)
                            it1.setEditable(False)
                            it1.setIcon(obj.ViewObject.Icon)
                            props = []
                            for prop in QPROPS:
                                it = QtGui.QStandardItem()
                                val = None
                                if hasattr(obj, prop) and ("Hidden" not in obj.getEditorMode(prop)):
                                    val = self.get_text(obj, prop)
                                    it.setText(val)
                                    it.setCheckable(True)
                                if val != None:
                                    d = None
                                    if hasattr(obj, "IauracadAttributes"):
                                        d = obj.IauracadAttributes
                                    elif hasattr(obj, "IauracadData"):
                                        d = obj.IauracadData
                                    if d:
                                        if ("Export" + prop in d) and (
                                            d["Export" + prop] == "True"
                                        ):
                                            it.setCheckState(QtCore.Qt.Checked)
                                    elif self.has_qto(obj, prop):
                                        it.setCheckState(QtCore.Qt.Checked)
                                    if val == 0:
                                        it.setIcon(QtGui.QIcon(":/icons/warning.svg"))
                                self.set_editable(it, prop)
                                props.append(it)
                            self.qmodel.appendRow([it1] + props)

    def has_qto(self, obj, prop):
        """Says if the given object has the given prop in a qto set"""

        if not "StepId" in obj.PropertiesList:
            return False
        from nativeiauracad import iAuraCAD_tools

        element = iAuraCAD_tools.get_iAuraCAD_element(obj)
        if not element:
            return False
        for rel in getattr(element, "IsDefinedBy", []):
            pset = rel.RelatingPropertyDefinition
            if pset.is_a("IauracadElementQuantity"):
                if pset.Name in self.qtodefs:
                    if prop in self.qtodefs[pset.Name]:
                        return True
        return False

    def get_text(self, obj, prop):
        """Gets the text from a property"""

        val = getattr(obj, prop, "0")
        txt = val.getUserPreferred()[0].replace("^2", "Â²").replace("^3", "Â³")
        return txt

    def get_row(self, name):
        """Returns the row number corresponding to the given object name"""

        for i in range(self.qmodel.rowCount()):
            if self.qmodel.item(i).toolTip().split(" ")[0] == name:
                return i
        return -1

    def update_line(self, name, qto):
        """Updates a single line of the table, without updating
        the actual object"""

        from PySide import QtCore

        i = self.get_row(name)
        if i == -1:
            return
        obj = AuraCAD.ActiveDocument.getObject(name)
        qto_val = self.qtodefs[qto]
        for j, p in enumerate(QPROPS):
            it = self.qmodel.item(i, j + 1)
            if p in obj.PropertiesList:
                val = self.get_text(obj, p)
                it.setText(val)
                self.set_editable(it, p)
                it.setCheckable(True)
            elif p in qto_val:
                it.setText("0")
                it.setCheckable(True)
                it.setCheckState(QtCore.Qt.Checked)
                self.set_editable(it, p)

    def set_editable(self, it, prop):
        """Checks if the given prop should be editable, and sets it"""

        if prop in ["Area", "HorizontalArea", "VerticalArea", "Volume"]:
            it.setEditable(False)
        else:
            it.setEditable(True)

    def getRole(self, obj):
        """gets the Iauracad class of this object"""

        if hasattr(obj, "IauracadType"):
            return obj.IauracadType
        elif hasattr(obj, "IauracadRole"):
            return obj.IauracadRole
        elif hasattr(obj, "IauracadClass"):
            return obj.IauracadClass
        else:
            return None

    def accept(self):
        """OK pressed"""

        PARAMS.SetInt("BimIauracadQuantitiesDialogWidth", self.form.width())
        PARAMS.SetInt("BimIauracadQuantitiesDialogHeight", self.form.height())
        self.form.hide()
        changed = False
        if self.iauracadqtolist:
            if not changed:
                AuraCAD.ActiveDocument.openTransaction("Change quantities")
            changed = True
            for key, val in self.iauracadqtolist.items():
                obj = AuraCAD.ActiveDocument.getObject(key)
                if obj:
                    for qto in val:
                        self.apply_qto(obj, qto)
        for row in range(self.qmodel.rowCount()):
            name = self.qmodel.item(row, 0).toolTip()
            obj = AuraCAD.ActiveDocument.getObject(name)
            if obj:
                for i in range(len(QPROPS)):
                    item = self.qmodel.item(row, i + 1)
                    val = item.text()
                    sav = bool(item.checkState())
                    if i < 3:  # Length, Width, Height, value can be changed
                        if hasattr(obj, QPROPS[i]):
                            if getattr(obj, QPROPS[i]).getUserPreferred()[0] != val:
                                setattr(obj, QPROPS[i], val)
                                if not changed:
                                    AuraCAD.ActiveDocument.openTransaction("Change quantities")
                                changed = True
                    d = None
                    if hasattr(obj, "IauracadAttributes"):
                        d = obj.IauracadAttributes
                        att = "IauracadAttributes"
                    elif hasattr(obj, "IauracadData"):
                        d = obj.IauracadData
                        att = "IauracadData"
                    if d:
                        if sav:
                            if (not "Export" + QPROPS[i] in d) or (
                                d["Export" + QPROPS[i]] == "False"
                            ):
                                d["Export" + QPROPS[i]] = "True"
                                setattr(obj, att, d)
                                if not changed:
                                    AuraCAD.ActiveDocument.openTransaction("Change quantities")
                                changed = True
                        else:
                            if "Export" + QPROPS[i] in d:
                                if d["Export" + QPROPS[i]] == "True":
                                    d["Export" + QPROPS[i]] = "False"
                                    setattr(obj, att, d)
                                    if not changed:
                                        AuraCAD.ActiveDocument.openTransaction("Change quantities")
                                    changed = True
                    elif "StepId" not in obj.PropertiesList:
                        AuraCAD.Console.PrintError(
                            translate(
                                "BIM", "Cannot save quantities settings for object %1"
                            ).replace("%1", obj.Label)
                            + "\n"
                        )

        if changed:
            AuraCAD.ActiveDocument.commitTransaction()
            AuraCAD.ActiveDocument.recompute()

        return self.reject()

    def reject(self):
        self.form.hide()
        del self.form
        return True

    def setChecked(self, id1, id2):
        sel = self.form.quantities.selectedIndexes()
        state = self.qmodel.itemFromIndex(id1).checkState()
        if len(sel) > 7:
            for idx in sel:
                if idx.column() == id1.column():
                    item = self.qmodel.itemFromIndex(idx)
                    if item.checkState() != state:
                        item.setCheckState(state)

    def quantHeaderClicked(self, col):
        from PySide import QtCore

        sel = self.form.quantities.selectedIndexes()
        state = None
        if len(sel) > 7:
            for idx in sel:
                if idx.column() == col:
                    item = self.qmodel.itemFromIndex(idx)
                    if state is None:
                        # take the state to apply from the first selected item
                        state = QtCore.Qt.Checked
                        if item.checkState():
                            state = QtCore.Qt.Unchecked
                    item.setCheckState(state)

    def onClickTree(self, index=None):

        AuraCADGui.Selection.clearSelection()
        sel = self.form.quantities.selectedIndexes()
        for index in sel:
            if index.column() == 0:
                obj = AuraCAD.ActiveDocument.getObject(self.qmodel.itemFromIndex(index).toolTip())
                if obj:
                    AuraCADGui.Selection.addSelection(obj)


AuraCADGui.addCommand("BIM_IauracadQuantities", BIM_IauracadQuantities())
