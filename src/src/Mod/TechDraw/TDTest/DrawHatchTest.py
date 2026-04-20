#!/usr/bin/env python3


import AuraCAD
import os
import unittest


class DrawHatchTest(unittest.TestCase):
    def setUp(self):
        """Creates a page and view"""
        self.path = os.path.dirname(os.path.abspath(__file__))
        print("TDHatch path: " + self.path)
        templateFileSpec = self.path + "/TestTemplate.svg"

        AuraCAD.newDocument("TDHatch")
        AuraCAD.setActiveDocument("TDHatch")
        AuraCAD.ActiveDocument = AuraCAD.getDocument("TDHatch")

        # make source feature
        box = AuraCAD.ActiveDocument.addObject("Part::Box", "Box")

        # make a page
        self.page = AuraCAD.ActiveDocument.addObject("TechDraw::DrawPage", "Page")
        AuraCAD.ActiveDocument.addObject("TechDraw::DrawSVGTemplate", "Template")
        AuraCAD.ActiveDocument.Template.Template = templateFileSpec
        AuraCAD.ActiveDocument.Page.Template = AuraCAD.ActiveDocument.Template
        self.page.Scale = 5.0
        # page.ViewObject.show()  #unit tests run in console mode

        # make Views
        self.view = AuraCAD.ActiveDocument.addObject("TechDraw::DrawViewPart", "View")
        AuraCAD.ActiveDocument.View.Source = [box]
        self.page.addView(self.view)
        AuraCAD.ActiveDocument.recompute()

    def tearDown(self):
        AuraCAD.closeDocument("TDHatch")

    def testMakeHatchCase(self):
        """Tests if hatch area can be added to view"""
        # make hatch
        print("making hatch")
        hatch = AuraCAD.ActiveDocument.addObject("TechDraw::DrawHatch", "Hatch")
        hatch.Source = (self.view, ["Face0"])
        hatchFileSpec = self.path + "/TestHatch.svg"
        # comment out to use default from preferences
        hatch.HatchPattern = (
            hatchFileSpec
        )
        print("finished hatch")
        AuraCAD.ActiveDocument.recompute()

        self.assertTrue("Up-to-date" in hatch.State)


if __name__ == "__main__":
    unittest.main()
