import AuraCAD
from AuraCAD import Units
import unittest
from .TechDrawTestUtilities import createPageWithSVGTemplate


class DrawViewBalloonTest(unittest.TestCase):
    def setUp(self):
        """Creates a page and 2 views"""
        AuraCAD.newDocument("TDBalloon")
        AuraCAD.setActiveDocument("TDBalloon")
        AuraCAD.ActiveDocument = AuraCAD.getDocument("TDBalloon")

        # make source feature
        AuraCAD.ActiveDocument.addObject("Part::Box", "Box")
        AuraCAD.ActiveDocument.addObject("Part::Sphere", "Sphere")

        # make a page
        self.page = createPageWithSVGTemplate()
        self.page.Scale = 5.0
        # page.ViewObject.show()  # unit tests run in console mode

        # make Views
        self.view1 = AuraCAD.ActiveDocument.addObject("TechDraw::DrawViewPart", "View")
        AuraCAD.ActiveDocument.View.Source = [AuraCAD.ActiveDocument.Box]
        self.page.addView(self.view1)
        self.view1.X = Units.Quantity(30.0, Units.Length)
        self.view1.Y = Units.Quantity(150.0, Units.Length)
        self.view2 = AuraCAD.activeDocument().addObject(
            "TechDraw::DrawViewPart", "View001"
        )
        AuraCAD.activeDocument().View001.Source = [AuraCAD.activeDocument().Sphere]
        self.page.addView(self.view2)
        self.view2.X = Units.Quantity(220.0, Units.Length)
        self.view2.Y = Units.Quantity(150.0, Units.Length)
        AuraCAD.ActiveDocument.recompute()

    def tearDown(self):
        AuraCAD.closeDocument("TDBalloon")

    def testMakeDrawViewBalloon(self):
        """Tests if a DrawViewBalloon can be added to view"""
        print("Place balloon")
        balloon1 = AuraCAD.ActiveDocument.addObject(
            "TechDraw::DrawViewBalloon", "Balloon1"
        )
        balloon1.SourceView = self.view1
        # balloon1.OriginIsSet = 1  # OriginIsSet property removed March 2020
        balloon1.OriginX = self.view1.X + Units.Quantity(20.0, Units.Length)
        balloon1.OriginY = self.view1.Y + Units.Quantity(20.0, Units.Length)
        balloon1.Text = "1"
        balloon1.Y = balloon1.OriginX + Units.Quantity(20.0, Units.Length)
        balloon1.X = balloon1.OriginY + Units.Quantity(20.0, Units.Length)

        print("adding balloon1 to page")
        self.page.addView(balloon1)

        AuraCAD.ActiveDocument.recompute()
        self.assertTrue("Up-to-date" in balloon1.State)

        balloon2 = AuraCAD.ActiveDocument.addObject(
            "TechDraw::DrawViewBalloon", "Balloon2"
        )
        balloon2.SourceView = self.view2
        # balloon2.OriginIsSet = 1
        balloon2.OriginX = self.view2.X + Units.Quantity(20.0, Units.Length)
        balloon2.OriginY = self.view2.Y + Units.Quantity(20.0, Units.Length)
        balloon2.Text = "2"
        balloon2.Y = balloon2.OriginX + Units.Quantity(20.0, Units.Length)
        balloon2.X = balloon2.OriginY + Units.Quantity(20.0, Units.Length)

        print("adding balloon2 to page")
        self.page.addView(balloon2)

        AuraCAD.ActiveDocument.recompute()
        self.assertTrue("Up-to-date" in balloon2.State)


if __name__ == "__main__":
    unittest.main()
