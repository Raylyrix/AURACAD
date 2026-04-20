#!/usr/bin/env python3

# test script for TechDraw module
# creates a page and a view
# adds 1 leader to view1
# adds 1 RTA to leader1


import AuraCAD
import os


def DLeaderTest():
    path = os.path.dirname(os.path.abspath(__file__))
    print("TDLead path: " + path)
    templateFileSpec = path + "/TestTemplate.svg"
    myHTMLText = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt; color:#ff0000;">Some Rich Text for testing.</span></p></body></html>"""

    AuraCAD.newDocument("TDLead")
    AuraCAD.setActiveDocument("TDLead")
    AuraCAD.ActiveDocument = AuraCAD.getDocument("TDLead")

    # make source feature
    AuraCAD.ActiveDocument.addObject("Part::Box", "Box")

    # make a page
    page = AuraCAD.ActiveDocument.addObject("TechDraw::DrawPage", "Page")
    AuraCAD.ActiveDocument.addObject("TechDraw::DrawSVGTemplate", "Template")
    AuraCAD.ActiveDocument.Template.Template = templateFileSpec
    AuraCAD.ActiveDocument.Page.Template = AuraCAD.ActiveDocument.Template
    page.Scale = 5.0
    # page.ViewObject.show()   # unit tests run in console mode

    # make Views
    view1 = AuraCAD.ActiveDocument.addObject("TechDraw::DrawViewPart", "View")
    AuraCAD.ActiveDocument.View.Source = [AuraCAD.ActiveDocument.Box]
    rc = page.addView(view1)
    view1.X = 148
    view1.Y = 105
    AuraCAD.ActiveDocument.recompute()

    # make leader
    print("making leader")
    leaderObj = AuraCAD.ActiveDocument.addObject(
        "TechDraw::DrawLeaderLine", "DrawLeaderLine"
    )
    leaderObj.LeaderParent = view1
    p0 = AuraCAD.Vector(0.0, 0.0, 0.0)
    p1 = AuraCAD.Vector(100.0, -100.0, 0.0)
    p2 = AuraCAD.Vector(500.0, -100.0, 0.0)
    leaderObj.WayPoints = [p0, p1, p2]
    leaderObj.StartSymbol = 0
    leaderObj.EndSymbol = 4
    print("adding leader to page")
    page.addView(leaderObj)
    leaderObj.X = 5
    leaderObj.Y = 5
    print("finished leader")

    # make RTA
    print("making RTA")
    blockObj = AuraCAD.ActiveDocument.addObject(
        "TechDraw::DrawRichAnno", "DrawRichAnno"
    )
    page.addView(blockObj)
    blockObj.AnnoParent = leaderObj
    blockObj.X = 5
    blockObj.Y = 5
    blockObj.AnnoText = myHTMLText

    AuraCAD.ActiveDocument.recompute()

    rc = False
    if ("Up-to-date" in leaderObj.State) and ("Up-to-date" in blockObj.State):
        rc = True

    AuraCAD.closeDocument("TDLead")
    return rc


if __name__ == "__main__":
    DLeaderTest()
