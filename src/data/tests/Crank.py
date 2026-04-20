#import rpdb2
#rpdb2.start_embedded_debugger("test")
import AuraCAD
import Part
import Draft
from AuraCAD import Base

circ1= Part.makeCircle(
    5,
    AuraCAD.Vector(10,18,10), AuraCAD.Vector(1,0,0))

circ2 = Part.makeCircle(5)

def DrawMyPart(points, extrude):
    obj1 = Draft.makeWire(points,closed=True,face=True,support=None)
    face1 = Part.Face(obj1.Shape)
    body1= face1.extrude(extrude)
    Part.show(body1)

# part1
DrawMyPart([
    AuraCAD.Vector(0,0,0),
    AuraCAD.Vector(45,0,0),
    AuraCAD.Vector(45,20,0),
    AuraCAD.Vector(0,20,0),
    ], Base.Vector(0,0,4))
DrawMyPart([
    AuraCAD.Vector(0,20,0),
    AuraCAD.Vector(0,180,0),
    AuraCAD.Vector(25,180,0),
    AuraCAD.Vector(25,20,0),
    ], Base.Vector(0,0,4))
DrawMyPart([
    AuraCAD.Vector(0,180,0),
    AuraCAD.Vector(0,200,0),
    AuraCAD.Vector(45,200,0),
    AuraCAD.Vector(45,180,0),
    ], Base.Vector(0,0,4))

DrawMyPart([
    AuraCAD.Vector(25,20,0),
    AuraCAD.Vector(25,180,0),
     AuraCAD.Vector(25,180,9.2),
     AuraCAD.Vector(25,20,9.2),
    ], Base.Vector(0,0,4))


# part2
points=[
    AuraCAD.Vector(45,200,0),
    AuraCAD.Vector(68,200,25),
    AuraCAD.Vector(68,0,25),
    AuraCAD.Vector(45,0,0),
    AuraCAD.Vector(45,200,0),
]
DrawMyPart([
    AuraCAD.Vector(45,200,0),
    AuraCAD.Vector(68,200,25),
    AuraCAD.Vector(68,180,25),
    AuraCAD.Vector(45,180,0),
    ], Base.Vector(0,0,4))
DrawMyPart([
    AuraCAD.Vector(68,180,25),
    AuraCAD.Vector(56.7,180,13),
    AuraCAD.Vector(56.7,20,13),
    AuraCAD.Vector(68,20,25),
    ], Base.Vector(0,0,4))
DrawMyPart([
    AuraCAD.Vector(45,0,0),
    AuraCAD.Vector(68,0,25),
    AuraCAD.Vector(68,20,25),
    AuraCAD.Vector(45,20,0),
    ], Base.Vector(0,0,4))

DrawMyPart([
     AuraCAD.Vector(25,20,0),
     AuraCAD.Vector(45,20,0),
     AuraCAD.Vector(45,20,9.2),
     AuraCAD.Vector(25,20,9.2),
     ], Base.Vector(0,0,4))
DrawMyPart([
     AuraCAD.Vector(25,180,0),
     AuraCAD.Vector(45,180,0),
     AuraCAD.Vector(45,180,9.2),
     AuraCAD.Vector(25,180,9.2),
     ], Base.Vector(0,0,4))


# part3
DrawMyPart([
    AuraCAD.Vector(68,200,25),
    AuraCAD.Vector(68,200,35),
    AuraCAD.Vector(68,0,35),
    AuraCAD.Vector(68,0,25),
    AuraCAD.Vector(68,200,25),
    ], Base.Vector(0,0,4))


circ1= Draft.makeCircle(
    5,
    Base.Placement(10,18,10),
    AuraCAD.Vector(1,0,0))

circ2 = Draft.makeCircle(5)