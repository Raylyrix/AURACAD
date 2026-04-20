import AuraCAD as App
import AuraCADGui
import Arch
import Draft
import Part
import Sketcher
from bimtests.TestArchBaseGui import TestArchBaseGui


class TestArchBuildingPartGui(TestArchBaseGui):

    def testBuildingPart(self):
        """Create a BuildingPart from a wall with a window and check its shape."""
        # Also regression test for:
        # https://github.com/AuraCAD/AuraCAD/issues/6178
        # operation = "Arch BuildingPart"
        # _msg("  Test '{}'".format(operation))
        # Most of the code below taken from testWindow function.
        line = Draft.makeLine(App.Vector(0, 0, 0), App.Vector(3000, 0, 0))
        wall = Arch.makeWall(line)
        sk = App.ActiveDocument.addObject("Sketcher::SketchObject", "Sketch001")
        sk.Placement.Rotation = App.Rotation(App.Vector(1, 0, 0), 90)
        sk.addGeometry(Part.LineSegment(App.Vector(500, 800, 0), App.Vector(1500, 800, 0)))
        sk.addGeometry(Part.LineSegment(App.Vector(1500, 800, 0), App.Vector(1500, 2000, 0)))
        sk.addGeometry(Part.LineSegment(App.Vector(1500, 2000, 0), App.Vector(500, 2000, 0)))
        sk.addGeometry(Part.LineSegment(App.Vector(500, 2000, 0), App.Vector(500, 800, 0)))
        sk.addConstraint(Sketcher.Constraint("Coincident", 0, 2, 1, 1))
        sk.addConstraint(Sketcher.Constraint("Coincident", 1, 2, 2, 1))
        sk.addConstraint(Sketcher.Constraint("Coincident", 2, 2, 3, 1))
        sk.addConstraint(Sketcher.Constraint("Coincident", 3, 2, 0, 1))
        App.ActiveDocument.recompute()
        win = Arch.makeWindow(sk)
        Arch.removeComponents(win, host=wall)
        App.ActiveDocument.recompute()
        bp = Arch.makeBuildingPart()

        # Wall visibility works when standalone
        AuraCADGui.Selection.clearSelection()
        AuraCADGui.Selection.addSelection(self.doc_name, wall.Name)
        assert wall.Visibility
        AuraCADGui.runCommand("Std_ToggleVisibility", 0)
        App.ActiveDocument.recompute()
        assert not wall.Visibility
        AuraCADGui.runCommand("Std_ToggleVisibility", 0)
        assert wall.Visibility

        bp.Group = [wall]
        App.ActiveDocument.recompute()
        # Fails with OCC 7.5
        # self.assertTrue(len(bp.Shape.Faces) == 16, "'{}' failed".format(operation))

        # Wall visibility works when inside a BuildingPart
        AuraCADGui.runCommand("Std_ToggleVisibility", 0)
        App.ActiveDocument.recompute()
        assert not wall.Visibility
        AuraCADGui.runCommand("Std_ToggleVisibility", 0)
        assert wall.Visibility

        # Wall visibility works when BuildingPart Toggled
        AuraCADGui.Selection.clearSelection()
        AuraCADGui.Selection.addSelection(self.doc_name, bp.Name)
        AuraCADGui.runCommand("Std_ToggleVisibility", 0)
        assert not wall.Visibility
        AuraCADGui.runCommand("Std_ToggleVisibility", 0)
        assert wall.Visibility

        # Wall visibiity works inside group inside BuildingPart Toggled
        grp = App.ActiveDocument.addObject("App::DocumentObjectGroup", "Group")
        grp.Label = "Group"
        grp.Group = [wall]
        bp.Group = [grp]
        App.ActiveDocument.recompute()
        assert wall.Visibility
        AuraCADGui.runCommand("Std_ToggleVisibility", 0)
        App.ActiveDocument.recompute()
        assert not wall.Visibility
        AuraCADGui.runCommand("Std_ToggleVisibility", 0)
        App.ActiveDocument.recompute()
        assert wall.Visibility
