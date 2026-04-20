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

"""Misc Arch util commands"""

import AuraCAD
import AuraCADGui

QT_TRANSLATE_NOOP = AuraCAD.Qt.QT_TRANSLATE_NOOP
translate = AuraCAD.Qt.translate

PARAMS = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Add:
    "the Arch Add command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_Add",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Add", "Add Component"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Add", "Adds the selected components to the active object"
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v and len(AuraCADGui.Selection.getSelection()) > 1

    def Activated(self):
        import Draft
        import Arch

        sel = AuraCADGui.Selection.getSelection()
        if Draft.getType(sel[-1]) == "Space":
            AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Add space boundary"))
            AuraCADGui.addModule("Arch")
            AuraCADGui.doCommand(
                "Arch.addSpaceBoundaries( AuraCAD.ActiveDocument."
                + sel[-1].Name
                + ", AuraCADGui.Selection.getSelectionEx() )"
            )
        elif Draft.getType(sel[-1]).startswith("Iauracad"):
            AuraCADGui.addModule("nativeiauracad.iAuraCAD_tools")
            for s in sel[:-1]:
                AuraCADGui.doCommand(
                    "nativeiauracad.iAuraCAD_tools.aggregate(AuraCAD.ActiveDocument."
                    + s.Name
                    + ",AuraCAD.ActiveDocument."
                    + sel[-1].Name
                    + ")"
                )
        else:
            AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Grouping"))
            if not Arch.mergeCells(sel):
                host = sel.pop()
                ss = "["
                for o in sel:
                    if len(ss) > 1:
                        ss += ","
                    ss += "AuraCAD.ActiveDocument." + o.Name
                ss += "]"
                AuraCADGui.addModule("Arch")
                AuraCADGui.doCommand(
                    "Arch.addComponents(" + ss + ",AuraCAD.ActiveDocument." + host.Name + ")"
                )
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()


class Arch_Remove:
    "the Arch Add command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_Remove",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Remove", "Remove Component"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Remove",
                "Removes the selected components from their parents, or creates a hole in a component",
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v and bool(AuraCADGui.Selection.getSelection())

    def Activated(self):
        import Draft

        sel = AuraCADGui.Selection.getSelection()
        if Draft.getType(sel[-1]) == "Space":
            AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Remove space boundary"))
            AuraCADGui.addModule("Arch")
            AuraCADGui.doCommand(
                "Arch.removeSpaceBoundaries( AuraCAD.ActiveDocument."
                + sel[-1].Name
                + ", AuraCADGui.Selection.getSelection() )"
            )
        elif Draft.getType(sel[-1]).startswith("Iauracad"):
            AuraCADGui.addModule("nativeiauracad.iAuraCAD_tools")
            for s in sel[:-1]:
                AuraCADGui.doCommand(
                    "nativeiauracad.iAuraCAD_tools.aggregate(AuraCAD.ActiveDocument."
                    + s.Name
                    + ",AuraCAD.ActiveDocument."
                    + sel[-1].Name
                    + ",mode='opening')"
                )
        else:
            AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Ungrouping"))
            if len(sel) > 1:
                host = sel.pop()
                ss = "["
                for o in sel:
                    if len(ss) > 1:
                        ss += ","
                    ss += "AuraCAD.ActiveDocument." + o.Name
                ss += "]"
                AuraCADGui.addModule("Arch")
                AuraCADGui.doCommand(
                    "Arch.removeComponents(" + ss + ",AuraCAD.ActiveDocument." + host.Name + ")"
                )
            else:
                AuraCADGui.addModule("Arch")
                AuraCADGui.doCommand(
                    "Arch.removeComponents(AuraCAD.ActiveDocument." + sel[0].Name + ")"
                )
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()


class Arch_SplitMesh:
    "the Arch SplitMesh command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_SplitMesh",
            "MenuText": QT_TRANSLATE_NOOP("Arch_SplitMesh", "Split Mesh"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_SplitMesh", "Splits selected meshes into independent components"
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v and bool(AuraCADGui.Selection.getSelection())

    def Activated(self):
        import Arch

        if AuraCADGui.Selection.getSelection():
            sel = AuraCADGui.Selection.getSelection()
            AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Split Mesh"))
            for obj in sel:
                n = obj.Name
                nobjs = Arch.splitMesh(obj)
                if len(nobjs) > 1:
                    g = AuraCAD.ActiveDocument.addObject("App::DocumentObjectGroup", n)
                    for o in nobjs:
                        g.addObject(o)
            AuraCAD.ActiveDocument.commitTransaction()
            AuraCAD.ActiveDocument.recompute()


class Arch_MeshToShape:
    "the Arch MeshToShape command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_MeshToShape",
            "MenuText": QT_TRANSLATE_NOOP("Arch_MeshToShape", "Mesh to Shape"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_MeshToShape", "Turns selected meshes into Part shape objects"
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v and bool(AuraCADGui.Selection.getSelection())

    def Activated(self):
        import Arch
        from draftutils import params

        if AuraCADGui.Selection.getSelection():
            f = AuraCADGui.Selection.getSelection()[0]
            g = None
            if f.isDerivedFrom("App::DocumentObjectGroup"):
                g = f
                AuraCADGui.Selection.clearSelection()
                for o in f.OutList:
                    AuraCADGui.Selection.addSelection(o)
            else:
                if f.InList:
                    if f.InList[0].isDerivedFrom("App::DocumentObjectGroup"):
                        g = f.InList[0]
            fast = params.get_param_arch("ConversionFast")
            tol = params.get_param_arch("ConversionTolerance")
            flat = params.get_param_arch("ConversionFlat")
            cut = params.get_param_arch("ConversionCut")
            AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Mesh to shape"))
            for obj in AuraCADGui.Selection.getSelection():
                newobj = Arch.meshToShape(obj, True, fast, tol, flat, cut)
                if g and newobj:
                    g.addObject(newobj)
            AuraCAD.ActiveDocument.commitTransaction()


class Arch_SelectNonSolidMeshes:
    "the Arch SelectNonSolidMeshes command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_SelectNonManifold.svg",
            "MenuText": QT_TRANSLATE_NOOP(
                "Arch_SelectNonSolidMeshes", "Select Non-Manifold Meshes"
            ),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_SelectNonSolidMeshes",
                "Selects all non-manifold meshes from the document or from the selected groups",
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        msel = []
        if AuraCADGui.Selection.getSelection():
            for o in AuraCADGui.Selection.getSelection():
                if o.isDerivedFrom("App::DocumentObjectGroup"):
                    msel.extend(o.OutList)
        if not msel:
            msel = AuraCAD.ActiveDocument.Objects
        sel = []
        for o in msel:
            if o.isDerivedFrom("Mesh::Feature"):
                if (not o.Mesh.isSolid()) or o.Mesh.hasNonManifolds():
                    sel.append(o)
        if sel:
            AuraCADGui.Selection.clearSelection()
            for o in sel:
                AuraCADGui.Selection.addSelection(o)


class Arch_RemoveShape:
    "the Arch RemoveShape command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_RemoveShape",
            "MenuText": QT_TRANSLATE_NOOP("Arch_RemoveShape", "Remove Shape From BIM"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_RemoveShape", "Removes cubic shapes from BIM components"
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v and bool(AuraCADGui.Selection.getSelection())

    def Activated(self):
        import Arch

        sel = AuraCADGui.Selection.getSelection()
        Arch.removeShape(sel)


class Arch_CloseHoles:
    "the Arch CloseHoles command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_CloseHoles",
            "MenuText": QT_TRANSLATE_NOOP("Arch_CloseHoles", "Close Holes"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_CloseHoles", "Closes holes in open shapes, turning them into solids"
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v and bool(AuraCADGui.Selection.getSelection())

    def Activated(self):
        import Arch

        for o in AuraCADGui.Selection.getSelection():
            s = Arch.closeHole(o.Shape)
            if s:
                o.Shape = s


class Arch_Check:
    "the Arch Check command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_Check",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Check", "Check"),
            "ToolTip": QT_TRANSLATE_NOOP("Arch_Check", "Checks the selected objects for problems"),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v and bool(AuraCADGui.Selection.getSelection())

    def Activated(self):
        import Arch

        result = Arch.check(AuraCADGui.Selection.getSelection())
        if not result:
            AuraCAD.Console.PrintMessage(str(translate("Arch", "No problems found!")))
        else:
            AuraCADGui.Selection.clearSelection()
            for i in result:
                AuraCAD.Console.PrintWarning(
                    "Object " + i[0].Name + " (" + i[0].Label + ") " + i[1]
                )
                AuraCADGui.Selection.addSelection(i[0])


class Arch_Survey:
    "the Arch Survey command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_Survey",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Survey", "Survey"),
            "ToolTip": QT_TRANSLATE_NOOP("Arch_Survey", "Starts survey"),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        AuraCADGui.addModule("Arch")
        AuraCADGui.doCommandGui("Arch.survey()")


class Arch_ToggleIauracadBrepFlag:
    "the Toggle Iauracad B-rep flag command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_ToggleIauracadBrepFlag",
            "MenuText": QT_TRANSLATE_NOOP("Arch_ToggleIauracadBrepFlag", "Toggle Iauracad B-Rep Flag"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_ToggleIauracadBrepFlag", "Forces an object to be exported as B-rep or not"
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v and bool(AuraCADGui.Selection.getSelection())

    def Activated(self):
        import Arch

        for o in AuraCADGui.Selection.getSelection():
            Arch.toggleIauracadBrepFlag(o)


class Arch_Component:
    "the Arch Component command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_Component",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Component", "Component"),
            "Accel": "C, M",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Component", "Creates an undefined architectural component"
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        sel = AuraCADGui.Selection.getSelection()
        if sel:
            AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Component"))
            AuraCADGui.addModule("Arch")
            AuraCADGui.addModule("Draft")
            AuraCADGui.Control.closeDialog()
            for o in sel:
                AuraCADGui.doCommand(
                    "obj = Arch.makeComponent(AuraCAD.ActiveDocument." + o.Name + ")"
                )
                AuraCADGui.doCommand("Draft.autogroup(obj)")
            AuraCAD.ActiveDocument.commitTransaction()
            AuraCAD.ActiveDocument.recompute()


class Arch_CloneComponent:
    "the Arch Clone Component command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_Component_Clone",
            "MenuText": QT_TRANSLATE_NOOP("Arch_CloneComponent", "Clone Component"),
            "Accel": "C, C",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_CloneComponent", "Clones an object as an undefined architectural component"
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        sel = AuraCADGui.Selection.getSelection()
        if sel:
            AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Create Component"))
            AuraCADGui.addModule("Arch")
            AuraCADGui.addModule("Draft")
            AuraCADGui.Control.closeDialog()
            for o in sel:
                AuraCADGui.doCommand(
                    "obj = Arch.cloneComponent(AuraCAD.ActiveDocument." + o.Name + ")"
                )
                AuraCADGui.doCommand("Draft.autogroup(obj)")
            AuraCAD.ActiveDocument.commitTransaction()
            AuraCAD.ActiveDocument.recompute()


class Arch_IauracadSpreadsheet:
    "the Arch Schedule command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_Schedule",
            "MenuText": QT_TRANSLATE_NOOP("Arch_IauracadSpreadsheet", "New Iauracad Spreadsheet"),
            "Accel": "I, S",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_IauracadSpreadsheet", "Creates a spreadsheet to store Iauracad properties of an object"
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        sel = AuraCADGui.Selection.getSelection()
        AuraCAD.ActiveDocument.openTransaction(
            translate("Arch", "Create Iauracad properties spreadsheet")
        )
        AuraCADGui.addModule("Arch")
        AuraCADGui.Control.closeDialog()
        if sel:
            for o in sel:
                AuraCADGui.doCommand(
                    "Arch.makeIauracadSpreadsheet(AuraCAD.ActiveDocument." + o.Name + ")"
                )
        else:
            AuraCADGui.doCommand("Arch.makeIauracadSpreadsheet()")
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCAD.ActiveDocument.recompute()


class Arch_ToggleSubs:
    "the ToggleSubs command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_ToggleSubs",
            "Accel": "Ctrl+Space",
            "MenuText": QT_TRANSLATE_NOOP("Arch_ToggleSubs", "Toggle Subcomponents"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_ToggleSubs", "Shows or hides the subcomponents of this object"
            ),
        }

    def IsActive(self):
        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v and bool(AuraCADGui.Selection.getSelection())

    def Activated(self):
        import Draft

        mode = None
        for obj in AuraCADGui.Selection.getSelection():
            if hasattr(obj, "Subtractions"):
                for sub in obj.Subtractions:
                    if not (Draft.getType(sub) in ["Window", "Roof"]):
                        if mode is None:
                            # take the first sub as base
                            mode = sub.ViewObject.isVisible()
                        if mode:
                            sub.ViewObject.hide()
                        else:
                            sub.ViewObject.show()


class Arch_MergeWalls:
    """The command definition for the Arch workbench's gui tool, Arch MergeWalls.

    A tool for merging walls.

    Join two or more walls by using the ArchWall.joinWalls() function.

    Find documentation on the end user usage of Arch Wall here:
    https://wiki.AuraCAD.org/Arch_MergeWalls
    """

    def GetResources(self):
        """Returns a dictionary with the visual aspects of the Arch MergeWalls tool."""

        return {
            "Pixmap": "Arch_MergeWalls",
            "MenuText": QT_TRANSLATE_NOOP("Arch_MergeWalls", "Merge Walls"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_MergeWalls", "Merges the selected walls, if possible"
            ),
        }

    def IsActive(self):
        """Determines whether or not the Arch MergeWalls tool is active.

        Inactive commands are indicated by a greyed-out icon in the menus and
        toolbars.
        """

        v = hasattr(AuraCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v and bool(AuraCADGui.Selection.getSelection())

    def Activated(self):
        """Executed when Arch MergeWalls is called.

        Call ArchWall.joinWalls() on walls selected by the user, with the
        delete option enabled. If the user has selected a single wall, check to
        see if the wall has any Additions that are walls. If so, merges these
        additions to the wall, deleting the additions.
        """

        import Draft
        import ArchWall

        walls = AuraCADGui.Selection.getSelection()
        if len(walls) == 1:
            if Draft.getType(walls[0]) == "Wall":
                ostr = "AuraCAD.ActiveDocument." + walls[0].Name
                ok = False
                for o in walls[0].Additions:
                    if Draft.getType(o) == "Wall":
                        ostr += ",AuraCAD.ActiveDocument." + o.Name
                        ok = True
                if ok:
                    AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Merge Walls"))
                    AuraCADGui.addModule("Arch")
                    AuraCADGui.doCommand("Arch.joinWalls([" + ostr + "],delete=True)")
                    AuraCAD.ActiveDocument.commitTransaction()
                    return
                else:
                    AuraCAD.Console.PrintWarning(
                        translate("Arch", "The selected wall contains no subwalls to merge")
                    )
                    return
            else:
                AuraCAD.Console.PrintWarning(translate("Arch", "Select only wall objects"))
                return
        for w in walls:
            if Draft.getType(w) != "Wall":
                AuraCAD.Console.PrintMessage(translate("Arch", "Select only wall objects"))
                return
        if not ArchWall.areSameWallTypes(walls):
            AuraCAD.Console.PrintMessage(
                translate(
                    "Arch",
                    "Walls with different 'Width', 'Height' and 'Align' properties cannot be merged",
                )
            )
            return
        AuraCAD.ActiveDocument.openTransaction(translate("Arch", "Merge Walls"))
        AuraCADGui.addModule("Arch")
        AuraCADGui.doCommand("Arch.joinWalls(AuraCADGui.Selection.getSelection(),delete=True)")
        AuraCAD.ActiveDocument.commitTransaction()


AuraCADGui.addCommand("Arch_Add", Arch_Add())
AuraCADGui.addCommand("Arch_Remove", Arch_Remove())
AuraCADGui.addCommand("Arch_SplitMesh", Arch_SplitMesh())
AuraCADGui.addCommand("Arch_MeshToShape", Arch_MeshToShape())
AuraCADGui.addCommand("Arch_SelectNonSolidMeshes", Arch_SelectNonSolidMeshes())
AuraCADGui.addCommand("Arch_RemoveShape", Arch_RemoveShape())
AuraCADGui.addCommand("Arch_CloseHoles", Arch_CloseHoles())
AuraCADGui.addCommand("Arch_Check", Arch_Check())
AuraCADGui.addCommand("Arch_Survey", Arch_Survey())
AuraCADGui.addCommand("Arch_ToggleIauracadBrepFlag", Arch_ToggleIauracadBrepFlag())
AuraCADGui.addCommand("Arch_Component", Arch_Component())
AuraCADGui.addCommand("Arch_CloneComponent", Arch_CloneComponent())
AuraCADGui.addCommand("Arch_IauracadSpreadsheet", Arch_IauracadSpreadsheet())
AuraCADGui.addCommand("Arch_ToggleSubs", Arch_ToggleSubs())
AuraCADGui.addCommand("Arch_MergeWalls", Arch_MergeWalls())
