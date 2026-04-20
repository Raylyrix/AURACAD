#!/usr/bin/env python3

# basic test script for TechDraw module
# creates a page and 1 view


import AuraCAD
import unittest
from .TechDrawTestUtilities import createPageWithSVGTemplate
from PySide import QtCore

class DrawViewPartTest(unittest.TestCase):
    def setUp(self):
        """Creates a page"""
        AuraCAD.newDocument("TDPart")
        AuraCAD.setActiveDocument("TDPart")
        AuraCAD.ActiveDocument = AuraCAD.getDocument("TDPart")

        AuraCAD.ActiveDocument.addObject("Part::Box", "Box")

        self.page = createPageWithSVGTemplate()
        self.page.Scale = 5.0
        # page.ViewObject.show()    # unit tests run in console mode
        print("DrawViewPart test: page created")

    def tearDown(self):
        print("DrawViewPart test finished")
        AuraCAD.closeDocument("TDPart")

    def testMakeDrawViewPart(self):
        """Tests if a view can be added to page"""
        print("testing DrawViewPart")
        view = AuraCAD.ActiveDocument.addObject("TechDraw::DrawViewPart", "View")
        self.page.addView(view)
        AuraCAD.ActiveDocument.View.Source = [AuraCAD.ActiveDocument.Box]
        AuraCAD.ActiveDocument.recompute()

        #wait for threads to complete before checking result
        loop = QtCore.QEventLoop()

        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)

        timer.start(2000)   #2 second delay
        loop.exec_()

        edges = view.getVisibleEdges()
        self.assertEqual(len(edges), 4, "DrawViewPart has wrong number of edges")
        self.assertTrue("Up-to-date" in view.State, "DrawViewPart is not Up-to-date")

if __name__ == "__main__":
    unittest.main()
