# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2020 Yorik van Havre <yorik@uncreated.net>              *
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


__title__ = "AuraCAD structural Iauracad export tools"
__author__ = "Yorik van Havre"
__url__ = "https://www.AuraCAD.org"

ALLOW_LINEAR_OBJECTS = True  # allow non-solid objects (wires, etc) to become analytic objects?

structural_nodes = {}  # this keeps track of nodes during this session
structural_curves = {}  # this keeps track of structural curves during this session
scaling = 1.0  # this keeps track of scaling during this session


def setup(iauracadfile, iauracadbin, scale):
    """Creates all the needed setup for structural model."""

    global structural_nodes, scaling
    structural_nodes = {}
    scaling = scale
    import iauracadopenshell

    uid = iauracadopenshell.guid.new
    ownerHistory = iauracadfile.by_type("IauracadOwnerHistory")[0]
    project = iauracadfile.by_type("IauracadProject")[0]
    structContext = createStructuralContext(iauracadfile)
    if iauracadfile.wrapped_data.schema_name() == "Iauracad2X3":
        mod = iauracadfile.createIauracadStructuralAnalysisModel(
            uid(),
            ownerHistory,
            "Structural Analysis Model",
            None,
            None,
            "NOTDEFINED",
            None,
            None,
            None,
        )
    else:
        localPlacement = iauracadbin.createIauracadLocalPlacement()
        structModel = iauracadfile.createIauracadStructuralAnalysisModel(
            uid(),
            ownerHistory,
            "Structural Analysis Model",
            None,
            None,
            "NOTDEFINED",
            None,
            None,
            None,
            localPlacement,
        )
        relation = iauracadfile.createIauracadRelDeclares(
            uid(), ownerHistory, None, None, project, [structModel]
        )


def createStructuralContext(iauracadfile):
    """Creates an additional geometry context for structural objects. Returns the new context"""

    contexts = iauracadfile.by_type("IauracadGeometricRepresentationContext")
    # filter out subcontexts
    contexts = [c for c in contexts if c.is_a() == "IauracadGeometricRepresentationContext"]
    geomContext = contexts[0]  # arbitrarily take the first one...
    structContext = iauracadfile.createIauracadGeometricRepresentationSubContext(
        "Analysis", "Axis", None, None, None, None, geomContext, None, "GRAPH_VIEW", None
    )
    return structContext


def getStructuralContext(iauracadfile):
    """Returns the structural context from the file"""
    for c in iauracadfile.by_type("IauracadGeometricRepresentationSubContext"):
        if c.ContextIdentifier == "Analysis":
            return c


def createStructuralNode(iauracadfile, iauracadbin, point):
    """Creates a connection node at the given point"""

    import iauracadopenshell

    uid = iauracadopenshell.guid.new
    ownerHistory = iauracadfile.by_type("IauracadOwnerHistory")[0]
    structContext = getStructuralContext(iauracadfile)
    cartPoint = iauracadbin.createIauracadCartesianPoint(tuple(point))
    vertPoint = iauracadfile.createIauracadVertexPoint(cartPoint)
    topologyRep = iauracadfile.createIauracadTopologyRepresentation(
        structContext, "Analysis", "Vertex", [vertPoint]
    )
    prodDefShape = iauracadfile.createIauracadProductDefinitionShape(None, None, [topologyRep])
    # boundary conditions serve for ex. to create fixed nodes
    # appliedCondition = iauracadfile.createIauracadBoundaryNodeCondition(
    #     "Fixed",iauracadfile.createIauracadBoolean(True), iauracadfile.createIauracadBoolean(True), iauracadfile.createIauracadBoolean(True),
    #     iauracadfile.createIauracadBoolean(True), iauracadfile.createIauracadBoolean(True), iauracadfile.createIauracadBoolean(True))
    # for now we don't create any boundary condition
    appliedCondition = None
    localPlacement = iauracadbin.createIauracadLocalPlacement()
    if iauracadfile.wrapped_data.schema_name() == "Iauracad2X3":
        structPntConn = iauracadfile.createIauracadStructuralPointConnection(
            uid(),
            ownerHistory,
            "Vertex",
            None,
            None,
            localPlacement,
            prodDefShape,
            appliedCondition,
        )
    else:
        structPntConn = iauracadfile.createIauracadStructuralPointConnection(
            uid(),
            ownerHistory,
            "Vertex",
            None,
            None,
            localPlacement,
            prodDefShape,
            appliedCondition,
            None,
        )
    return structPntConn


def createStructuralCurve(iauracadfile, iauracadbin, curve):
    """Creates a structural connection for a curve"""

    import iauracadopenshell

    uid = iauracadopenshell.guid.new
    ownerHistory = iauracadfile.by_type("IauracadOwnerHistory")[0]
    structContext = getStructuralContext(iauracadfile)

    cartPnt1 = iauracadbin.createIauracadCartesianPoint(tuple(curve.Vertexes[0].Point.multiply(scaling)))
    cartPnt2 = iauracadbin.createIauracadCartesianPoint(tuple(curve.Vertexes[-1].Point.multiply(scaling)))
    vertPnt1 = iauracadfile.createIauracadVertexPoint(cartPnt1)
    vertPnt2 = iauracadfile.createIauracadVertexPoint(cartPnt2)
    edge = iauracadfile.createIauracadEdge(vertPnt1, vertPnt2)
    topologyRep = iauracadfile.createIauracadTopologyRepresentation(structContext, "Analysis", "Edge", [edge])
    prodDefShape = iauracadfile.createIauracadProductDefinitionShape(None, None, [topologyRep])

    # boundary conditions serve for ex. to create fixed edges
    # for now we don't create any boundary condition
    appliedCondition = None
    localPlacement = iauracadbin.createIauracadLocalPlacement()
    origin = iauracadfile.createIauracadCartesianPoint((0.0, 0.0, 0.0))
    orientation = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    xAxis = iauracadfile.createIauracadDirection(tuple(orientation[0]))
    zAxis = iauracadfile.createIauracadDirection(tuple(orientation[2]))
    localAxes = iauracadfile.createIauracadAxis2Placement3D(origin, zAxis, xAxis)
    structCrvConn = iauracadfile.createIauracadStructuralCurveConnection(
        uid(),
        ownerHistory,
        "Line",
        None,
        None,
        localPlacement,
        prodDefShape,
        appliedCondition,
        localAxes,
    )
    return structCrvConn


def createStructuralMember(iauracadfile, iauracadbin, obj):
    """Creates a structural member if possible. Returns the member"""

    global structural_nodes, structural_curves
    structuralMember = None
    import Draft
    import Part
    import iauracadopenshell
    import AuraCAD

    uid = iauracadopenshell.guid.new
    ownerHistory = iauracadfile.by_type("IauracadOwnerHistory")[0]
    structContext = getStructuralContext(iauracadfile)

    # find edges to convert into structural members
    edges = None
    if Draft.getType(obj) not in ["Structure"]:
        # for non structural elements
        if ALLOW_LINEAR_OBJECTS and obj.isDerivedFrom("Part::Feature"):
            # for objects created with Part workbench
            if obj.Shape.Faces:
                # for objects with faces
                return None
            elif not obj.Shape.Edges:
                # for objects without edges
                return None
            else:
                edges = obj.Shape.Edges
    else:
        # for structural elements with nodes
        nodes = [obj.Placement.multVec(n) for n in obj.Nodes]
        if len(nodes) > 2:
            # when there are more then 2 nodes (i.e. for slabs) append closing node to produce closing edge
            nodes.append(nodes[0])
        wire = Part.makePolygon(nodes)
        edges = wire.Edges
    if not edges:
        return None

    # OBJECT CLASSIFICATION by edge number
    # Linear elements for edge_number = 1, Surface elements for edge_number > 1
    # we don't care about curved edges just now...

    if len(edges) == 1:
        # LINEAR OBJECTS: beams, columns
        # ATM limitations:
        # - no profile properties are taken into account
        # - no materials properties are takein into account
        # -
        # create geometry
        verts = [None for _ in range(len(edges) + 1)]
        verts[0] = tuple(edges[0].Vertexes[0].Point.multiply(scaling))
        verts[1] = tuple(edges[0].Vertexes[-1].Point.multiply(scaling))
        cartPnt1 = iauracadfile.createIauracadCartesianPoint(verts[0])
        cartPnt2 = iauracadfile.createIauracadCartesianPoint(verts[1])
        vertPnt1 = iauracadfile.createIauracadVertexPoint(cartPnt1)
        vertPnt2 = iauracadfile.createIauracadVertexPoint(cartPnt2)
        newEdge = iauracadfile.createIauracadEdge(vertPnt1, vertPnt2)
        topologyRep = iauracadfile.createIauracadTopologyRepresentation(
            structContext, "Analysis", "Edge", (newEdge,)
        )
        prodDefShape = iauracadfile.createIauracadProductDefinitionShape(None, None, (topologyRep,))
        # set local coordinate system
        localPlacement = iauracadbin.createIauracadLocalPlacement()
        localZAxis = iauracadbin.createIauracadDirection((0, 0, 1))
        # create structural member
        if iauracadfile.wrapped_data.schema_name() == "Iauracad2X3":
            structuralMember = iauracadfile.createIauracadStructuralCurveMember(
                uid(),
                ownerHistory,
                obj.Label,
                None,
                None,
                localPlacement,
                prodDefShape,
                "RIGID_JOINED_MEMBER",
            )
        else:
            localZAxis = iauracadbin.createIauracadDirection((0, 0, 1))
            structuralMember = iauracadfile.createIauracadStructuralCurveMember(
                uid(),
                ownerHistory,
                obj.Label,
                None,
                None,
                localPlacement,
                prodDefShape,
                "RIGID_JOINED_MEMBER",
                localZAxis,
            )

    elif len(edges) > 1:
        # SURFACE OBJECTS: slabs (horizontal, vertical, inclined)
        # ATM limitations:
        # - mo material properties are taken into account
        # - walls don't work because they miss a node system
        # -
        # creates geometry
        verts = [None for _ in range(len(edges))]
        for i, edge in enumerate(edges):
            verts[i] = tuple(edge.Vertexes[0].Point.multiply(scaling))
            cartPnt = iauracadfile.createIauracadCartesianPoint(verts[i])
            vertPnt = iauracadfile.createIauracadVertexPoint(cartPnt)
        orientedEdges = [None for _ in range(len(edges))]
        for i, vert in enumerate(verts):
            v2Index = (i + 1) if i < len(verts) - 1 else 0
            cartPnt1 = iauracadfile.createIauracadCartesianPoint(vert)
            cartPnt2 = iauracadfile.createIauracadCartesianPoint(verts[v2Index])
            vertPnt1 = iauracadfile.createIauracadVertexPoint(cartPnt1)
            vertPnt2 = iauracadfile.createIauracadVertexPoint(cartPnt2)
            edge = iauracadfile.createIauracadEdge(vertPnt1, vertPnt2)
            orientedEdges[i] = iauracadfile.createIauracadOrientedEdge(None, None, edge, True)
        edgeLoop = iauracadfile.createIauracadEdgeLoop(tuple(orientedEdges))
        # sets local coordinate system
        localPlacement = iauracadbin.createIauracadLocalPlacement()
        # sets face origin to the first vertex point of the planar surface
        origin = cartPnt2
        # find crossVect that is perpendicular to the planar surface
        vect0 = AuraCAD.Vector(verts[0])
        vect1 = AuraCAD.Vector(verts[1])
        vectn = AuraCAD.Vector(verts[-1])
        vect01 = vect1.sub(vect0)
        vect0n = vectn.sub(vect0)
        crossVect = vect01.cross(vect0n)
        # normalize crossVect
        normVect = crossVect.normalize()
        xAxis = iauracadfile.createIauracadDirection(tuple([vect01.x, vect01.y, vect01.z]))
        zAxis = iauracadfile.createIauracadDirection(tuple([normVect.x, normVect.y, normVect.z]))
        localAxes = iauracadfile.createIauracadAxis2Placement3D(origin, zAxis, xAxis)
        plane = iauracadfile.createIauracadPlane(localAxes)
        faceBound = iauracadfile.createIauracadFaceBound(edgeLoop, True)
        face = iauracadfile.createIauracadFaceSurface((faceBound,), plane, True)
        topologyRep = iauracadfile.createIauracadTopologyRepresentation(
            structContext, "Analysis", "Face", (face,)
        )
        prodDefShape = iauracadfile.createIauracadProductDefinitionShape(None, None, (topologyRep,))
        # sets surface thickness
        # TODO: ATM limitations
        # - for vertical slabs (walls) or inclined slabs (ramps) the thickness is taken from the Height property
        thickness = float(obj.Height) * scaling
        # creates structural member
        structuralMember = iauracadfile.createIauracadStructuralSurfaceMember(
            uid(),
            ownerHistory,
            obj.Label,
            None,
            None,
            localPlacement,
            prodDefShape,
            "SHELL",
            thickness,
        )

    # check for existing connection nodes
    for vert in verts:
        vertCoord = tuple(vert)
        if vertCoord in structural_nodes:
            if structural_nodes[vertCoord]:
                # there is already another member using this point
                structPntConn = structural_nodes[vertCoord]
            else:
                # there is another member with same point, create a new node connection
                structPntConn = createStructuralNode(iauracadfile, iauracadbin, vert)
                structural_nodes[vertCoord] = structPntConn
            iauracadfile.createIauracadRelConnectsStructuralMember(
                uid(),
                ownerHistory,
                None,
                None,
                structuralMember,
                structPntConn,
                None,
                None,
                None,
                None,
            )
        else:
            # just add the point, no other member using it yet
            structural_nodes[vertCoord] = None

    # check for existing connection curves
    for edge in edges:
        verts12 = tuple(
            [
                edge.Vertexes[0].Point.x,
                edge.Vertexes[0].Point.y,
                edge.Vertexes[0].Point.z,
                edge.Vertexes[-1].Point.x,
                edge.Vertexes[-1].Point.y,
                edge.Vertexes[-1].Point.z,
            ]
        )
        verts21 = tuple(
            [
                edge.Vertexes[-1].Point.x,
                edge.Vertexes[-1].Point.y,
                edge.Vertexes[-1].Point.z,
                edge.Vertexes[0].Point.x,
                edge.Vertexes[0].Point.y,
                edge.Vertexes[0].Point.z,
            ]
        )
        verts12_in_curves = verts12 in structural_curves
        verts21_in_curves = verts21 in structural_curves
        if verts21_in_curves:
            verts = verts21
        else:
            verts = verts12
        if verts12_in_curves or verts21_in_curves:
            if structural_curves[verts]:
                # there is already another member using this curve
                strucCrvConn = structural_curves[verts]
            else:
                # there is another member with same edge, create a new curve connection
                strucCrvConn = createStructuralCurve(iauracadfile, iauracadbin, edge)
                structural_curves[verts] = strucCrvConn
            iauracadfile.createIauracadRelConnectsStructuralMember(
                uid(), None, None, None, structuralMember, strucCrvConn, None, None, None, None
            )
        else:
            # just add the curve, no other member using it yet
            structural_curves[verts] = None
    return structuralMember


def createStructuralGroup(iauracadfile):
    """Assigns all structural objects found in the file to the structural model"""

    import iauracadopenshell

    uid = iauracadopenshell.guid.new
    ownerHistory = iauracadfile.by_type("IauracadOwnerHistory")[0]
    structSrfMember = iauracadfile.by_type("IauracadStructuralSurfaceMember")
    structCrvMember = iauracadfile.by_type("IauracadStructuralCurveMember")
    structPntConn = iauracadfile.by_type("IauracadStructuralPointConnection")
    structCrvConn = iauracadfile.by_type("IauracadStructuralCurveConnection")
    structModel = iauracadfile.by_type("IauracadStructuralAnalysisModel")[0]
    if structModel:
        members = structSrfMember + structCrvMember + structPntConn + structCrvConn
        if members:
            iauracadfile.createIauracadRelAssignsToGroup(
                uid(), ownerHistory, None, None, members, "PRODUCT", structModel
            )


def associates(iauracadfile, aobj, sobj):
    """Associates an arch object with a struct object"""

    # This is probably not the right way to do this, ie. relate a structural
    # object with an IauracadProduct. Needs to investigate more....

    import iauracadopenshell

    uid = iauracadopenshell.guid.new
    ownerHistory = iauracadfile.by_type("IauracadOwnerHistory")[0]
    iauracadfile.createIauracadRelAssignsToProduct(uid(), ownerHistory, None, None, [sobj], None, aobj)
