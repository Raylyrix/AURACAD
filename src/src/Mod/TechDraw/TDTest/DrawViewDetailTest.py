#!/usr/bin/env python3

# test script for DrawViewDetail
# creates a page, a view and a detail view


import AuraCAD
import unittest
from .TechDrawTestUtilities import createPageWithSVGTemplate
from PySide import QtCore

class DrawViewDetailTest(unittest.TestCase):
    def setUp(self):
        """Creates a page"""
        AuraCAD.newDocument("TDPart")
        AuraCAD.setActiveDocument("TDPart")
        AuraCAD.ActiveDocument = AuraCAD.getDocument("TDPart")

        AuraCAD.ActiveDocument.addObject("Part::Box", "Box")

        self.page = createPageWithSVGTemplate()
        self.page.Scale = 5.0
        # page.ViewObject.show()    # unit tests run in console mode
        print("DrawViewDetail test: page created")

        self.view = AuraCAD.ActiveDocument.addObject("TechDraw::DrawViewPart", "View")
        self.page.addView(self.view)
        AuraCAD.ActiveDocument.View.Source = [AuraCAD.ActiveDocument.Box]
        AuraCAD.ActiveDocument.recompute()

        #wait for threads to complete before checking result
        loop = QtCore.QEventLoop()

        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)

        timer.start(2000)   #2 second delay
        loop.exec_()
        print("DrawViewDetail test: view created")

    def tearDown(self):
        print("DrawViewDetail test finished")
        AuraCAD.closeDocument("TDPart")

    def testMakeDrawViewPart(self):
        """Tests if a view can be added to page"""
        print("testing DrawViewDetail")

        detail = AuraCAD.ActiveDocument.addObject(
            "TechDraw::DrawViewDetail", "Detail"
        )
        detail.BaseView = self.view
        detail.Direction = self.view.Direction
        detail.XDirection = self.view.XDirection
        self.page.addView(detail)
        AuraCAD.ActiveDocument.recompute()
        print("DrawViewDetail test: Detail created")

        #wait for threads to complete before checking result
        loop = QtCore.QEventLoop()

        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)

        timer.start(2000)   #2 second delay
        loop.exec_()

        edges = detail.getVisibleEdges()

        self.assertEqual(len(edges), 4, "DrawViewDetail has wrong number of edges")
        self.assertTrue("Up-to-date" in detail.State, "DrawViewDetail is not Up-to-date")

if __name__ == "__main__":
    unittest.main()
