// SPDX-License-Identifier: LGPL-2.1-or-later

/***************************************************************************
 *   Copyright (c) 2006 Werner Mayer <wmayer[at]users.sourceforge.net>     *
 *                                                                         *
 *   This file is part of the AuraCAD CAx development system.              *
 *                                                                         *
 *   This library is free software; you can redistribute it and/or         *
 *   modify it under the terms of the GNU Library General Public           *
 *   License as published by the Free Software Foundation; either          *
 *   version 2 of the License, or (at your option) any later version.      *
 *                                                                         *
 *   This library  is distributed in the hope that it will be useful,      *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with this library; see the file COPYING.LIB. If not,    *
 *   write to the Free Software Foundation, Inc., 59 Temple Place,         *
 *   Suite 330, Boston, MA  02111-1307, USA                                *
 *                                                                         *
 ***************************************************************************/

#include <auracadConfig.h>

#include <algorithm>
#include <limits>
#ifdef AuraCAD_OS_WIN32
# include <windows.h>
#endif
#ifdef AuraCAD_OS_MACOSX
# include <OpenGL/gl.h>
# include <OpenGL/glu.h>
#else
# include <GL/gl.h>
# include <GL/glu.h>
#endif
#include <Inventor/SbLine.h>
#include <Inventor/SoPickedPoint.h>
#include <Inventor/SoPrimitiveVertex.h>
#include <Inventor/actions/SoCallbackAction.h>
#include <Inventor/actions/SoGetBoundingBoxAction.h>
#include <Inventor/actions/SoGetPrimitiveCountAction.h>
#include <Inventor/actions/SoGLRenderAction.h>
#include <Inventor/actions/SoPickAction.h>
#include <Inventor/actions/SoSearchAction.h>
#include <Inventor/bundles/SoMaterialBundle.h>
#include <Inventor/bundles/SoTextureCoordinateBundle.h>
#include <Inventor/details/SoFaceDetail.h>
#include <Inventor/details/SoLineDetail.h>
#include <Inventor/misc/SoState.h>

#include <Base/Console.h>
#include <Base/Exception.h>
#include <Gui/SoauracadInteractiveElement.h>
#include <Gui/Selection/SoauracadSelectionAction.h>
#include <Mod/Mesh/App/Core/Algorithm.h>
#include <Mod/Mesh/App/Core/Elements.h>
#include <Mod/Mesh/App/Core/Grid.h>
#include <Mod/Mesh/App/Core/MeshKernel.h>

#include "SoauracadMeshObject.h"


using namespace MeshGui;

class SoOutputStreambuf: public std::streambuf
{
public:
    explicit SoOutputStreambuf(SoOutput* o)
        : out(o)
    {}

protected:
    int overflow(int c = EOF) override
    {
        if (c != EOF) {
            char z = static_cast<char>(c);
            out->write(z);
        }
        return c;
    }
    std::streamsize xsputn(const char* s, std::streamsize num) override
    {
        out->write(s);
        return num;
    }

private:
    SoOutput* out;
};

class SoOutputStream: public std::ostream
{
public:
    explicit SoOutputStream(SoOutput* o)
        : std::ostream(nullptr)
        , buf(o)
    {
        this->rdbuf(&buf);
    }

private:
    SoOutputStreambuf buf;
};

class SoInputStreambuf: public std::streambuf
{
public:
    explicit SoInputStreambuf(SoInput* o)
        : inp(o)
    {
        setg(buffer + pbSize, buffer + pbSize, buffer + pbSize);
    }

protected:
    int underflow() override
    {
        if (gptr() < egptr()) {
            return *gptr();
        }

        int numPutback {};
        numPutback = gptr() - eback();
        if (numPutback > pbSize) {
            numPutback = pbSize;
        }

        memcpy(buffer + (pbSize - numPutback), gptr() - numPutback, numPutback);

        int num = 0;
        for (int i = 0; i < bufSize; i++) {
            char c {};
            SbBool ok = inp->get(c);
            if (ok) {
                num++;
                buffer[pbSize + i] = c;
                if (c == '\n') {
                    break;
                }
            }
            else if (num == 0) {
                return EOF;
            }
        }

        setg(buffer + (pbSize - numPutback), buffer + pbSize, buffer + pbSize + num);

        return *gptr();
    }

private:
    static const int pbSize = 4;
    static const int bufSize = 1024;
    char buffer[bufSize + pbSize] {};
    SoInput* inp;
};

class SoInputStream: public std::istream
{
public:
    explicit SoInputStream(SoInput* o)
        : std::istream(nullptr)
        , buf(o)
    {
        this->rdbuf(&buf);
    }
    ~SoInputStream() override = default;
    SoInputStream(const SoInputStream&) = delete;
    SoInputStream(SoInputStream&&) = delete;
    SoInputStream& operator=(const SoInputStream&) = delete;
    SoInputStream& operator=(SoInputStream&&) = delete;

private:
    SoInputStreambuf buf;
};

// Defines all required member variables and functions for a
// single-value field
SO_SFIELD_SOURCE(
    SoSFMeshObject,
    Base::Reference<const Mesh::MeshObject>,
    Base::Reference<const Mesh::MeshObject>
)


void SoSFMeshObject::initClass()
{
    // This macro takes the name of the class and the name of the
    // parent class
    SO_SFIELD_INIT_CLASS(SoSFMeshObject, SoSField);
}

// This reads the value of a field from a file. It returns false if the value could not be read
// successfully.
SbBool SoSFMeshObject::readValue(SoInput* in)
{
    if (!in->isBinary()) {
        SoInputStream str(in);
        MeshCore::MeshKernel kernel;
        MeshCore::MeshInput(kernel).LoadMeshNode(str);
        value = new Mesh::MeshObject(kernel);

        // We need to trigger the notification chain here, as this function
        // can be used on a node in a scene graph in any state -- not only
        // during initial scene graph import.
        this->valueChanged();

        return true;
    }

    int32_t countPt {};
    in->read(countPt);
    std::vector<float> verts(countPt);
    in->readBinaryArray(verts.data(), countPt);

    MeshCore::MeshPointArray rPoints;
    rPoints.reserve(countPt / 3);
    for (auto it = verts.begin(); it != verts.end();) {
        Base::Vector3f p;
        p.x = *it;
        ++it;
        p.y = *it;
        ++it;
        p.z = *it;
        ++it;
        rPoints.push_back(p);
    }

    int32_t countFt {};
    in->read(countFt);
    std::vector<int32_t> faces(countFt);
    in->readBinaryArray(faces.data(), countFt);

    MeshCore::MeshFacetArray rFacets;
    rFacets.reserve(countFt / 3);
    for (auto it = faces.begin(); it != faces.end();) {
        MeshCore::MeshFacet f;
        f._aulPoints[0] = *it;
        ++it;
        f._aulPoints[1] = *it;
        ++it;
        f._aulPoints[2] = *it;
        ++it;
        rFacets.push_back(f);
    }

    MeshCore::MeshKernel kernel;
    kernel.Adopt(rPoints, rFacets, true);
    value = new Mesh::MeshObject(kernel);

    // We need to trigger the notification chain here, as this function
    // can be used on a node in a scene graph in any state -- not only
    // during initial scene graph import.
    this->valueChanged();

    return true;
}

// This writes the value of a field to a file.
void SoSFMeshObject::writeValue(SoOutput* out) const
{
    if (!value) {
        int32_t count = 0;
        out->write(count);
        out->write(count);
        return;
    }

    if (!out->isBinary()) {
        SoOutputStream str(out);
        MeshCore::MeshOutput(value->getKernel()).SaveMeshNode(str);
        return;
    }

    const MeshCore::MeshPointArray& rPoints = value->getKernel().GetPoints();
    std::vector<float> verts;
    verts.reserve(3 * rPoints.size());
    for (const auto& rPoint : rPoints) {
        verts.push_back(rPoint.x);
        verts.push_back(rPoint.y);
        verts.push_back(rPoint.z);
    }

    int32_t countPt = (int32_t)verts.size();
    out->write(countPt);
    out->writeBinaryArray(verts.data(), countPt);

    const MeshCore::MeshFacetArray& rFacets = value->getKernel().GetFacets();
    std::vector<uint32_t> faces;
    faces.reserve(3 * rFacets.size());
    for (const auto& rFacet : rFacets) {
        faces.push_back((int32_t)rFacet._aulPoints[0]);
        faces.push_back((int32_t)rFacet._aulPoints[1]);
        faces.push_back((int32_t)rFacet._aulPoints[2]);
    }

    int32_t countFt = (int32_t)faces.size();
    out->write(countFt);
    out->writeBinaryArray((const int32_t*)faces.data(), countFt);
}

// -------------------------------------------------------

SO_ELEMENT_SOURCE(SoauracadMeshObjectElement)

void SoauracadMeshObjectElement::initClass()
{
    SO_ELEMENT_INIT_CLASS(SoauracadMeshObjectElement, inherited);
}

void SoauracadMeshObjectElement::init(SoState* state)
{
    inherited::init(state);
    this->mesh = nullptr;
}

SoauracadMeshObjectElement::~SoauracadMeshObjectElement() = default;

void SoauracadMeshObjectElement::set(SoState* const state, SoNode* const node, const Mesh::MeshObject* const mesh)
{
    SoauracadMeshObjectElement* elem = static_cast<SoauracadMeshObjectElement*>(
        SoReplacedElement::getElement(state, classStackIndex, node)
    );
    if (elem) {
        elem->mesh = mesh;
        elem->nodeId = node->getNodeId();
    }
}

const Mesh::MeshObject* SoauracadMeshObjectElement::get(SoState* const state)
{
    return SoauracadMeshObjectElement::getInstance(state)->mesh;
}

const SoauracadMeshObjectElement* SoauracadMeshObjectElement::getInstance(SoState* state)
{
    return static_cast<const SoauracadMeshObjectElement*>(
        SoElement::getConstElement(state, classStackIndex)
    );
}

void SoauracadMeshObjectElement::print(FILE* /* file */) const
{}

// -------------------------------------------------------

SO_NODE_SOURCE(SoauracadMeshPickNode)

/*!
  Constructor.
*/
SoauracadMeshPickNode::SoauracadMeshPickNode()
{
    SO_NODE_CONSTRUCTOR(SoauracadMeshPickNode);

    SO_NODE_ADD_FIELD(mesh, (nullptr));
}

/*!
  Destructor.
*/
SoauracadMeshPickNode::~SoauracadMeshPickNode()
{
    delete meshGrid;
}

// Doc from superclass.
void SoauracadMeshPickNode::initClass()
{
    SO_NODE_INIT_CLASS(SoauracadMeshPickNode, SoNode, "Node");
}

void SoauracadMeshPickNode::notify(SoNotList* list)
{
    SoField* f = list->getLastField();
    if (f == &mesh) {
        const Mesh::MeshObject* meshObject = mesh.getValue();
        if (meshObject) {
            MeshCore::MeshAlgorithm alg(meshObject->getKernel());
            float fAvgLen = alg.GetAverageEdgeLength();
            delete meshGrid;
            meshGrid = new MeshCore::MeshFacetGrid(meshObject->getKernel(), 5.0F * fAvgLen);
        }
    }
}

// Doc from superclass.
void SoauracadMeshPickNode::rayPick(SoRayPickAction* /*action*/)
{}

// Doc from superclass.
void SoauracadMeshPickNode::pick(SoPickAction* action)
{
    SoRayPickAction* raypick = static_cast<SoRayPickAction*>(action);
    raypick->setObjectSpace();

    const Mesh::MeshObject* meshObject = mesh.getValue();
    MeshCore::MeshAlgorithm alg(meshObject->getKernel());

    const SbLine& line = raypick->getLine();
    const SbVec3f& pos = line.getPosition();
    const SbVec3f& dir = line.getDirection();
    Base::Vector3f pt(pos[0], pos[1], pos[2]);
    Base::Vector3f dr(dir[0], dir[1], dir[2]);
    Mesh::FacetIndex index {};
    if (alg.NearestFacetOnRay(pt, dr, *meshGrid, pt, index)) {
        SoPickedPoint* pp = raypick->addIntersection(SbVec3f(pt.x, pt.y, pt.z));
        if (pp) {
            SoFaceDetail* det = new SoFaceDetail();
            det->setFaceIndex(index);
            pp->setDetail(det, this);
        }
    }
}

// -------------------------------------------------------

SO_NODE_SOURCE(SoauracadMeshGridNode)

/*!
  Constructor.
*/
SoauracadMeshGridNode::SoauracadMeshGridNode()
{
    SO_NODE_CONSTRUCTOR(SoauracadMeshGridNode);

    SO_NODE_ADD_FIELD(minGrid, (SbVec3f(0, 0, 0)));
    SO_NODE_ADD_FIELD(maxGrid, (SbVec3f(0, 0, 0)));
    SO_NODE_ADD_FIELD(lenGrid, (SbVec3s(0, 0, 0)));
}

/*!
  Destructor.
*/
SoauracadMeshGridNode::~SoauracadMeshGridNode() = default;

// Doc from superclass.
void SoauracadMeshGridNode::initClass()
{
    SO_NODE_INIT_CLASS(SoauracadMeshGridNode, SoNode, "Node");
}

void SoauracadMeshGridNode::GLRender(SoGLRenderAction* /*action*/)
{
    const SbVec3f& min = minGrid.getValue();
    const SbVec3f& max = maxGrid.getValue();
    const SbVec3s& len = lenGrid.getValue();
    short u {}, v {}, w {};
    len.getValue(u, v, w);
    float minX {}, minY {}, minZ {};
    min.getValue(minX, minY, minZ);
    float maxX {}, maxY {}, maxZ {};
    max.getValue(maxX, maxY, maxZ);
    float dx = (maxX - minX) / (float)u;
    float dy = (maxY - minY) / (float)v;
    float dz = (maxZ - minZ) / (float)w;
    glColor3f(0.0F, 1.0F, 0.0);
    glBegin(GL_LINES);
    for (short i = 0; i < u + 1; i++) {
        for (short j = 0; j < v + 1; j++) {
            float p[3];
            p[0] = i * dx + minX;
            p[1] = j * dy + minY;
            p[2] = minZ;
            glVertex3fv(p);

            p[0] = i * dx + minX;
            p[1] = j * dy + minY;
            p[2] = maxZ;
            glVertex3fv(p);
        }
    }
    for (short i = 0; i < u + 1; i++) {
        for (short j = 0; j < w + 1; j++) {
            float p[3];
            p[0] = i * dx + minX;
            p[1] = minY;
            p[2] = j * dz + minZ;
            glVertex3fv(p);

            p[0] = i * dx + minX;
            p[1] = maxY;
            p[2] = j * dz + minZ;
            glVertex3fv(p);
        }
    }
    for (short i = 0; i < v + 1; i++) {
        for (short j = 0; j < w + 1; j++) {
            float p[3];
            p[0] = minX;
            p[1] = i * dy + minY;
            p[2] = j * dz + minZ;
            glVertex3fv(p);

            p[0] = maxX;
            p[1] = i * dy + minY;
            p[2] = j * dz + minZ;
            glVertex3fv(p);
        }
    }
    glEnd();
}

// -------------------------------------------------------

SO_NODE_SOURCE(SoauracadMeshObjectNode)

/*!
  Constructor.
*/
SoauracadMeshObjectNode::SoauracadMeshObjectNode()
{
    SO_NODE_CONSTRUCTOR(SoauracadMeshObjectNode);

    SO_NODE_ADD_FIELD(mesh, (nullptr));
}

/*!
  Destructor.
*/
SoauracadMeshObjectNode::~SoauracadMeshObjectNode() = default;

// Doc from superclass.
void SoauracadMeshObjectNode::initClass()
{
    SO_NODE_INIT_CLASS(SoauracadMeshObjectNode, SoNode, "Node");

    SO_ENABLE(SoGetBoundingBoxAction, SoauracadMeshObjectElement);
    SO_ENABLE(SoGLRenderAction, SoauracadMeshObjectElement);
    SO_ENABLE(SoPickAction, SoauracadMeshObjectElement);
    SO_ENABLE(SoCallbackAction, SoauracadMeshObjectElement);
    SO_ENABLE(SoGetPrimitiveCountAction, SoauracadMeshObjectElement);
}

// Doc from superclass.
void SoauracadMeshObjectNode::doAction(SoAction* action)
{
    SoauracadMeshObjectElement::set(action->getState(), this, mesh.getValue());
}

// Doc from superclass.
void SoauracadMeshObjectNode::GLRender(SoGLRenderAction* action)
{
    SoauracadMeshObjectNode::doAction(action);
}

// Doc from superclass.
void SoauracadMeshObjectNode::callback(SoCallbackAction* action)
{
    SoauracadMeshObjectNode::doAction(action);
}

// Doc from superclass.
void SoauracadMeshObjectNode::pick(SoPickAction* action)
{
    SoauracadMeshObjectNode::doAction(action);
}

// Doc from superclass.
void SoauracadMeshObjectNode::getBoundingBox(SoGetBoundingBoxAction* action)
{
    SoauracadMeshObjectNode::doAction(action);
}

// Doc from superclass.
void SoauracadMeshObjectNode::getPrimitiveCount(SoGetPrimitiveCountAction* action)
{
    SoauracadMeshObjectNode::doAction(action);
}

// Helper functions: draw vertices
inline void glVertex(const MeshCore::MeshPoint& _v)
{
    float v[3];
    v[0] = _v.x;
    v[1] = _v.y;
    v[2] = _v.z;
    glVertex3fv(v);
}

// Helper functions: draw normal
inline void glNormal(const Base::Vector3f& _n)
{
    float n[3];
    n[0] = _n.x;
    n[1] = _n.y;
    n[2] = _n.z;
    glNormal3fv(n);
}

// Helper functions: draw normal
inline void glNormal(float* n)
{
    glNormal3fv(n);
}

// Helper function: convert Vec to SbVec3f
inline SbVec3f sbvec3f(const Base::Vector3f& _v)
{
    return {_v.x, _v.y, _v.z};
}

SO_NODE_SOURCE(SoauracadMeshObjectShape)

void SoauracadMeshObjectShape::initClass()
{
    SO_NODE_INIT_CLASS(SoauracadMeshObjectShape, SoShape, "Shape");
}

SoauracadMeshObjectShape::SoauracadMeshObjectShape()
    : renderTriangleLimit(std::numeric_limits<unsigned>::max())
{
    SO_NODE_CONSTRUCTOR(SoauracadMeshObjectShape);
    setName(SoauracadMeshObjectShape::getClassTypeId().getName());
}

SoauracadMeshObjectShape::~SoauracadMeshObjectShape() = default;

void SoauracadMeshObjectShape::notify(SoNotList* node)
{
    inherited::notify(node);
    updateGLArray = true;
}

#define RENDER_GLARRAYS

/**
 * Either renders the complete mesh or only a subset of the points.
 */
void SoauracadMeshObjectShape::GLRender(SoGLRenderAction* action)
{
    if (shouldGLRender(action)) {
        SoState* state = action->getState();

        // Here we must save the model and projection matrices because
        // we need them later for picking
        glGetFloatv(GL_MODELVIEW_MATRIX, this->modelview);
        glGetFloatv(GL_PROJECTION_MATRIX, this->projection);

        SbBool mode = Gui::SoauracadInteractiveElement::get(state);
        const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
        if (!mesh || mesh->countPoints() == 0) {
            return;
        }

        Binding mbind = this->findMaterialBinding(state);

        SoMaterialBundle mb(action);
        // SoTextureCoordinateBundle tb(action, true, false);

        SbBool needNormals = !mb.isColorOnly() /* || tb.isFunction()*/;
        mb.sendFirst();  // make sure we have the correct material

        SbBool ccw = true;
        if (SoShapeHintsElement::getVertexOrdering(state) == SoShapeHintsElement::CLOCKWISE) {
            ccw = false;
        }

        if (!mode || mesh->countFacets() <= this->renderTriangleLimit) {
            if (mbind != OVERALL) {
                drawFaces(mesh, &mb, mbind, needNormals, ccw);
            }
            else {
#ifdef RENDER_GLARRAYS
                if (updateGLArray) {
                    updateGLArray = false;
                    generateGLArrays(state);
                }
                renderFacesGLArray(action);
#else
                drawFaces(mesh, 0, mbind, needNormals, ccw);
#endif
            }
        }
        else {
#if 0 && defined(RENDER_GLARRAYS)
            renderCoordsGLArray(action);
#else
            drawPoints(mesh, needNormals, ccw);
#endif
        }
    }
}

/**
 * Translates current material binding into the internal Binding enum.
 */
SoauracadMeshObjectShape::Binding SoauracadMeshObjectShape::findMaterialBinding(SoState* const state) const
{
    Binding binding = OVERALL;
    SoMaterialBindingElement::Binding matbind = SoMaterialBindingElement::get(state);

    switch (matbind) {
        case SoMaterialBindingElement::OVERALL:
            binding = OVERALL;
            break;
        case SoMaterialBindingElement::PER_VERTEX:
            binding = PER_VERTEX_INDEXED;
            break;
        case SoMaterialBindingElement::PER_VERTEX_INDEXED:
            binding = PER_VERTEX_INDEXED;
            break;
        case SoMaterialBindingElement::PER_PART:
        case SoMaterialBindingElement::PER_FACE:
            binding = PER_FACE_INDEXED;
            break;
        case SoMaterialBindingElement::PER_PART_INDEXED:
        case SoMaterialBindingElement::PER_FACE_INDEXED:
            binding = PER_FACE_INDEXED;
            break;
        default:
            break;
    }
    return binding;
}

/**
 * Renders the triangles of the complete mesh.
 * FIXME: Do it the same way as Coin did to have only one implementation which is controlled by
 * defines
 * FIXME: Implement using different values of transparency for each vertex or face
 */
void SoauracadMeshObjectShape::drawFaces(
    const Mesh::MeshObject* mesh,
    SoMaterialBundle* mb,
    Binding bind,
    SbBool needNormals,
    SbBool ccw
) const
{
    const MeshCore::MeshPointArray& rPoints = mesh->getKernel().GetPoints();
    const MeshCore::MeshFacetArray& rFacets = mesh->getKernel().GetFacets();
    bool perVertex = (mb && bind == PER_VERTEX_INDEXED);
    bool perFace = (mb && bind == PER_FACE_INDEXED);

    if (needNormals) {
        glBegin(GL_TRIANGLES);
        if (ccw) {
            // counterclockwise ordering
            for (auto it = rFacets.begin(); it != rFacets.end(); ++it) {
                const MeshCore::MeshPoint& v0 = rPoints[it->_aulPoints[0]];
                const MeshCore::MeshPoint& v1 = rPoints[it->_aulPoints[1]];
                const MeshCore::MeshPoint& v2 = rPoints[it->_aulPoints[2]];

                // Calculate the normal n = (v1-v0)x(v2-v0)
                float n[3];
                n[0] = (v1.y - v0.y) * (v2.z - v0.z) - (v1.z - v0.z) * (v2.y - v0.y);
                n[1] = (v1.z - v0.z) * (v2.x - v0.x) - (v1.x - v0.x) * (v2.z - v0.z);
                n[2] = (v1.x - v0.x) * (v2.y - v0.y) - (v1.y - v0.y) * (v2.x - v0.x);

                if (perFace) {
                    mb->send(it - rFacets.begin(), true);
                }
                glNormal(n);
                if (perVertex) {
                    mb->send(it->_aulPoints[0], true);
                }
                glVertex(v0);
                if (perVertex) {
                    mb->send(it->_aulPoints[1], true);
                }
                glVertex(v1);
                if (perVertex) {
                    mb->send(it->_aulPoints[2], true);
                }
                glVertex(v2);
            }
        }
        else {
            // clockwise ordering
            for (const auto& rFacet : rFacets) {
                const MeshCore::MeshPoint& v0 = rPoints[rFacet._aulPoints[0]];
                const MeshCore::MeshPoint& v1 = rPoints[rFacet._aulPoints[1]];
                const MeshCore::MeshPoint& v2 = rPoints[rFacet._aulPoints[2]];

                // Calculate the normal n = -(v1-v0)x(v2-v0)
                float n[3];
                n[0] = -((v1.y - v0.y) * (v2.z - v0.z) - (v1.z - v0.z) * (v2.y - v0.y));
                n[1] = -((v1.z - v0.z) * (v2.x - v0.x) - (v1.x - v0.x) * (v2.z - v0.z));
                n[2] = -((v1.x - v0.x) * (v2.y - v0.y) - (v1.y - v0.y) * (v2.x - v0.x));

                glNormal(n);
                glVertex(v0);
                glVertex(v1);
                glVertex(v2);
            }
        }
        glEnd();
    }
    else {
        glBegin(GL_TRIANGLES);
        for (const auto& rFacet : rFacets) {
            glVertex(rPoints[rFacet._aulPoints[0]]);
            glVertex(rPoints[rFacet._aulPoints[1]]);
            glVertex(rPoints[rFacet._aulPoints[2]]);
        }
        glEnd();
    }
}

/**
 * Renders the gravity points of a subset of triangles.
 */
void SoauracadMeshObjectShape::drawPoints(const Mesh::MeshObject* mesh, SbBool needNormals, SbBool ccw) const
{
    const MeshCore::MeshPointArray& rPoints = mesh->getKernel().GetPoints();
    const MeshCore::MeshFacetArray& rFacets = mesh->getKernel().GetFacets();
    int mod = rFacets.size() / renderTriangleLimit + 1;

    float size = std::min<float>((float)mod, 3.0F);
    glPointSize(size);

    if (needNormals) {
        glBegin(GL_POINTS);
        int ct = 0;
        if (ccw) {
            for (auto it = rFacets.begin(); it != rFacets.end(); ++it, ct++) {
                if (ct % mod == 0) {
                    const MeshCore::MeshPoint& v0 = rPoints[it->_aulPoints[0]];
                    const MeshCore::MeshPoint& v1 = rPoints[it->_aulPoints[1]];
                    const MeshCore::MeshPoint& v2 = rPoints[it->_aulPoints[2]];

                    // Calculate the normal n = (v1-v0)x(v2-v0)
                    float n[3];
                    n[0] = (v1.y - v0.y) * (v2.z - v0.z) - (v1.z - v0.z) * (v2.y - v0.y);
                    n[1] = (v1.z - v0.z) * (v2.x - v0.x) - (v1.x - v0.x) * (v2.z - v0.z);
                    n[2] = (v1.x - v0.x) * (v2.y - v0.y) - (v1.y - v0.y) * (v2.x - v0.x);

                    // Calculate the center point p=(v0+v1+v2)/3
                    float p[3];
                    p[0] = (v0.x + v1.x + v2.x) / 3.0F;
                    p[1] = (v0.y + v1.y + v2.y) / 3.0F;
                    p[2] = (v0.z + v1.z + v2.z) / 3.0F;
                    glNormal3fv(n);
                    glVertex3fv(p);
                }
            }
        }
        else {
            for (auto it = rFacets.begin(); it != rFacets.end(); ++it, ct++) {
                if (ct % mod == 0) {
                    const MeshCore::MeshPoint& v0 = rPoints[it->_aulPoints[0]];
                    const MeshCore::MeshPoint& v1 = rPoints[it->_aulPoints[1]];
                    const MeshCore::MeshPoint& v2 = rPoints[it->_aulPoints[2]];

                    // Calculate the normal n = -(v1-v0)x(v2-v0)
                    float n[3];
                    n[0] = -((v1.y - v0.y) * (v2.z - v0.z) - (v1.z - v0.z) * (v2.y - v0.y));
                    n[1] = -((v1.z - v0.z) * (v2.x - v0.x) - (v1.x - v0.x) * (v2.z - v0.z));
                    n[2] = -((v1.x - v0.x) * (v2.y - v0.y) - (v1.y - v0.y) * (v2.x - v0.x));

                    // Calculate the center point p=(v0+v1+v2)/3
                    float p[3];
                    p[0] = (v0.x + v1.x + v2.x) / 3.0F;
                    p[1] = (v0.y + v1.y + v2.y) / 3.0F;
                    p[2] = (v0.z + v1.z + v2.z) / 3.0F;
                    glNormal3fv(n);
                    glVertex3fv(p);
                }
            }
        }
        glEnd();
    }
    else {
        glBegin(GL_POINTS);
        int ct = 0;
        for (auto it = rFacets.begin(); it != rFacets.end(); ++it, ct++) {
            if (ct % mod == 0) {
                const MeshCore::MeshPoint& v0 = rPoints[it->_aulPoints[0]];
                const MeshCore::MeshPoint& v1 = rPoints[it->_aulPoints[1]];
                const MeshCore::MeshPoint& v2 = rPoints[it->_aulPoints[2]];
                // Calculate the center point p=(v0+v1+v2)/3
                float p[3];
                p[0] = (v0.x + v1.x + v2.x) / 3.0F;
                p[1] = (v0.y + v1.y + v2.y) / 3.0F;
                p[2] = (v0.z + v1.z + v2.z) / 3.0F;
                glVertex3fv(p);
            }
        }
        glEnd();
    }
}

void SoauracadMeshObjectShape::generateGLArrays(SoState* state)
{
    const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);

    this->index_array.resize(0);
    this->vertex_array.resize(0);

    std::vector<float> face_vertices;
    std::vector<int32_t> face_indices;

    const MeshCore::MeshKernel& kernel = mesh->getKernel();
    const MeshCore::MeshPointArray& cP = kernel.GetPoints();
    const MeshCore::MeshFacetArray& cF = kernel.GetFacets();

    // Flat shading
    face_vertices.reserve(3 * cF.size() * 6);  // duplicate each vertex
    face_indices.resize(3 * cF.size());

    int indexed = 0;
    for (const auto& it : cF) {
        Base::Vector3f n = kernel.GetFacet(it).GetNormal();
        for (Mesh::PointIndex ptIndex : it._aulPoints) {
            face_vertices.push_back(n.x);
            face_vertices.push_back(n.y);
            face_vertices.push_back(n.z);
            const Base::Vector3f& v = cP[ptIndex];
            face_vertices.push_back(v.x);
            face_vertices.push_back(v.y);
            face_vertices.push_back(v.z);

            face_indices[indexed] = indexed;
            indexed++;
        }
    }
    this->index_array.swap(face_indices);
    this->vertex_array.swap(face_vertices);
}

void SoauracadMeshObjectShape::renderFacesGLArray(SoGLRenderAction* action)
{
    (void)action;
    GLsizei cnt = static_cast<GLsizei>(index_array.size());

    glEnableClientState(GL_NORMAL_ARRAY);
    glEnableClientState(GL_VERTEX_ARRAY);

    glInterleavedArrays(GL_N3F_V3F, 0, vertex_array.data());
    glDrawElements(GL_TRIANGLES, cnt, GL_UNSIGNED_INT, index_array.data());

    glDisableClientState(GL_VERTEX_ARRAY);
    glDisableClientState(GL_NORMAL_ARRAY);
}

void SoauracadMeshObjectShape::renderCoordsGLArray(SoGLRenderAction* action)
{
    (void)action;
    int cnt = index_array.size();

    glEnableClientState(GL_NORMAL_ARRAY);
    glEnableClientState(GL_VERTEX_ARRAY);

    glInterleavedArrays(GL_N3F_V3F, 0, vertex_array.data());
    glDrawElements(GL_POINTS, cnt, GL_UNSIGNED_INT, index_array.data());

    glDisableClientState(GL_VERTEX_ARRAY);
    glDisableClientState(GL_NORMAL_ARRAY);
}

void SoauracadMeshObjectShape::doAction(SoAction* action)
{
    if (action->getTypeId() == Gui::SoGLSelectAction::getClassTypeId()) {
        SoNode* node = action->getNodeAppliedTo();
        if (!node) {  // on no node applied
            return;
        }

        // The node we have is the parent of this node and the coordinate node
        // thus we search there for it.
        SoSearchAction sa;
        sa.setInterest(SoSearchAction::FIRST);
        sa.setSearchingAll(false);
        sa.setType(SoauracadMeshObjectNode::getClassTypeId(), 1);
        sa.apply(node);
        SoPath* path = sa.getPath();
        if (!path) {
            return;
        }

        // make sure we got the node we wanted
        SoNode* coords = path->getNodeFromTail(0);
        if (!(coords && coords->getTypeId().isDerivedFrom(SoauracadMeshObjectNode::getClassTypeId()))) {
            return;
        }
        const Mesh::MeshObject* mesh = static_cast<SoauracadMeshObjectNode*>(coords)->mesh.getValue();
        startSelection(action, mesh);
        renderSelectionGeometry(mesh);
        stopSelection(action, mesh);
    }

    inherited::doAction(action);
}

void SoauracadMeshObjectShape::startSelection(SoAction* action, const Mesh::MeshObject* mesh)
{
    Gui::SoGLSelectAction* doaction = static_cast<Gui::SoGLSelectAction*>(action);
    const SbViewportRegion& vp = doaction->getViewportRegion();
    int x = vp.getViewportOriginPixels()[0];
    int y = vp.getViewportOriginPixels()[1];
    int w = vp.getViewportSizePixels()[0];
    int h = vp.getViewportSizePixels()[1];

    unsigned int bufSize = 5 * mesh->countFacets();  // make the buffer big enough
    this->selectBuf = new GLuint[bufSize];

    glSelectBuffer(bufSize, selectBuf);
    glRenderMode(GL_SELECT);

    glInitNames();
    glPushName(-1);

    GLint viewport[4];
    glGetIntegerv(GL_VIEWPORT, viewport);
    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    if (w > 0 && h > 0) {
        glTranslatef(
            (viewport[2] - 2 * (x - viewport[0])) / w,
            (viewport[3] - 2 * (y - viewport[1])) / h,
            0
        );
        glScalef(viewport[2] / w, viewport[3] / h, 1.0);
    }
    glMultMatrixf(/*mp*/ this->projection);
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadMatrixf(this->modelview);
}

void SoauracadMeshObjectShape::stopSelection(SoAction* action, const Mesh::MeshObject* mesh)
{
    // restoring the original projection matrix
    glPopMatrix();
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    glMatrixMode(GL_MODELVIEW);
    glFlush();

    // returning to normal rendering mode
    GLint hits = glRenderMode(GL_RENDER);

    unsigned int bufSize = 5 * mesh->countFacets();
    std::vector<std::pair<double, unsigned int>> hit;
    GLuint index = 0;
    for (GLint ii = 0; ii < hits && index < bufSize; ii++) {
        GLint ct = (GLint)selectBuf[index];
        hit.emplace_back(selectBuf[index + 1] / 4294967295.0, selectBuf[index + 3]);
        index = index + ct + 3;
    }

    delete[] selectBuf;
    selectBuf = nullptr;
    std::sort(hit.begin(), hit.end());

    Gui::SoGLSelectAction* doaction = static_cast<Gui::SoGLSelectAction*>(action);
    doaction->indices.reserve(hit.size());
    for (GLint ii = 0; ii < hits; ii++) {
        doaction->indices.push_back(hit[ii].second);
    }
}

void SoauracadMeshObjectShape::renderSelectionGeometry(const Mesh::MeshObject* mesh)
{
    int auracadnt = 0;
    const MeshCore::MeshPointArray& rPoints = mesh->getKernel().GetPoints();
    const MeshCore::MeshFacetArray& rFacets = mesh->getKernel().GetFacets();
    MeshCore::MeshFacetArray::_TConstIterator it_end = rFacets.end();
    for (MeshCore::MeshFacetArray::_TConstIterator it = rFacets.begin(); it != it_end; ++it) {
        const MeshCore::MeshPoint& v0 = rPoints[it->_aulPoints[0]];
        const MeshCore::MeshPoint& v1 = rPoints[it->_aulPoints[1]];
        const MeshCore::MeshPoint& v2 = rPoints[it->_aulPoints[2]];
        glLoadName(auracadnt);
        glBegin(GL_TRIANGLES);
        glVertex(v0);
        glVertex(v1);
        glVertex(v2);
        glEnd();
        auracadnt++;
    }
}


/**
 * Calculates picked point based on primitives generated by subclasses.
 */
void SoauracadMeshObjectShape::rayPick(SoRayPickAction* action)
{
    inherited::rayPick(action);
}

/** Sets the point indices, the geometric points and the normal for each triangle.
 * If the number of triangles exceeds \a renderTriangleLimit then only a triangulation of
 * a rough model is filled in instead. This is due to performance issues.
 * \see createTriangleDetail().
 */
void SoauracadMeshObjectShape::generatePrimitives(SoAction* action)
{
    SoState* state = action->getState();
    const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
    if (!mesh) {
        return;
    }
    const MeshCore::MeshPointArray& rPoints = mesh->getKernel().GetPoints();
    const MeshCore::MeshFacetArray& rFacets = mesh->getKernel().GetFacets();
    if (rPoints.size() < 3) {
        return;
    }
    if (rFacets.empty()) {
        return;
    }

    // get material binding
    Binding mbind = this->findMaterialBinding(state);

    // Create the information when moving over or picking into the scene
    SoPrimitiveVertex vertex;
    SoPointDetail pointDetail;
    SoFaceDetail faceDetail;

    vertex.setDetail(&pointDetail);

    beginShape(action, TRIANGLES, &faceDetail);
    try {
        for (const auto& rFacet : rFacets) {
            const MeshCore::MeshPoint& v0 = rPoints[rFacet._aulPoints[0]];
            const MeshCore::MeshPoint& v1 = rPoints[rFacet._aulPoints[1]];
            const MeshCore::MeshPoint& v2 = rPoints[rFacet._aulPoints[2]];

            // Calculate the normal n = (v1-v0)x(v2-v0)
            SbVec3f n;
            n[0] = (v1.y - v0.y) * (v2.z - v0.z) - (v1.z - v0.z) * (v2.y - v0.y);
            n[1] = (v1.z - v0.z) * (v2.x - v0.x) - (v1.x - v0.x) * (v2.z - v0.z);
            n[2] = (v1.x - v0.x) * (v2.y - v0.y) - (v1.y - v0.y) * (v2.x - v0.x);

            // Set the normal
            vertex.setNormal(n);

            // Vertex 0
            if (mbind == PER_VERTEX_INDEXED || mbind == PER_FACE_INDEXED) {
                pointDetail.setMaterialIndex(rFacet._aulPoints[0]);
                vertex.setMaterialIndex(rFacet._aulPoints[0]);
            }
            pointDetail.setCoordinateIndex(rFacet._aulPoints[0]);
            vertex.setPoint(sbvec3f(v0));
            shapeVertex(&vertex);

            // Vertex 1
            if (mbind == PER_VERTEX_INDEXED || mbind == PER_FACE_INDEXED) {
                pointDetail.setMaterialIndex(rFacet._aulPoints[1]);
                vertex.setMaterialIndex(rFacet._aulPoints[1]);
            }
            pointDetail.setCoordinateIndex(rFacet._aulPoints[1]);
            vertex.setPoint(sbvec3f(v1));
            shapeVertex(&vertex);

            // Vertex 2
            if (mbind == PER_VERTEX_INDEXED || mbind == PER_FACE_INDEXED) {
                pointDetail.setMaterialIndex(rFacet._aulPoints[2]);
                vertex.setMaterialIndex(rFacet._aulPoints[2]);
            }
            pointDetail.setCoordinateIndex(rFacet._aulPoints[2]);
            vertex.setPoint(sbvec3f(v2));
            shapeVertex(&vertex);

            // Increment for the next face
            faceDetail.incFaceIndex();
        }
    }
    catch (const Base::MemoryException&) {
        Base::Console().log("Not enough memory to generate primitives\n");
    }

    endShape();
}

/**
 * If the number of triangles exceeds \a renderTriangleLimit 0 is returned.
 * This means that the client programmer needs to implement itself to get the
 * index of the picked triangle. If the number of triangles doesn't exceed
 * \a renderTriangleLimit SoShape::createTriangleDetail() gets called.
 * Against the default OpenInventor implementation which returns 0 as well
 * Coin3d fills in the point and face indices.
 */
SoDetail* SoauracadMeshObjectShape::createTriangleDetail(
    SoRayPickAction* action,
    const SoPrimitiveVertex* v1,
    const SoPrimitiveVertex* v2,
    const SoPrimitiveVertex* v3,
    SoPickedPoint* pp
)
{
    SoDetail* detail = inherited::createTriangleDetail(action, v1, v2, v3, pp);
    return detail;
}

/**
 * Sets the bounding box of the mesh to \a box and its center to \a center.
 */
void SoauracadMeshObjectShape::computeBBox(SoAction* action, SbBox3f& box, SbVec3f& center)
{
    SoState* state = action->getState();
    const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
    if (mesh && mesh->countPoints() > 0) {
        Base::BoundBox3f cBox = mesh->getKernel().GetBoundBox();
        box.setBounds(
            SbVec3f(cBox.MinX, cBox.MinY, cBox.MinZ),
            SbVec3f(cBox.MaxX, cBox.MaxY, cBox.MaxZ)
        );
        Base::Vector3f mid = cBox.GetCenter();
        center.setValue(mid.x, mid.y, mid.z);
    }
    else {
        box.setBounds(SbVec3f(0, 0, 0), SbVec3f(0, 0, 0));
        center.setValue(0.0F, 0.0F, 0.0F);
    }
}

/**
 * Adds the number of the triangles to the \a SoGetPrimitiveCountAction.
 */
void SoauracadMeshObjectShape::getPrimitiveCount(SoGetPrimitiveCountAction* action)
{
    if (!this->shouldPrimitiveCount(action)) {
        return;
    }
    SoState* state = action->getState();
    const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
    action->addNumTriangles(mesh->countFacets());
    action->addNumPoints(mesh->countPoints());
}

/**
 * Counts the number of triangles. If a mesh is not set yet it returns 0.
 */
unsigned int SoauracadMeshObjectShape::countTriangles(SoAction* action) const
{
    SoState* state = action->getState();
    const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
    return (unsigned int)mesh->countFacets();
}

// -------------------------------------------------------

SO_NODE_SOURCE(SoauracadMeshSegmentShape)

void SoauracadMeshSegmentShape::initClass()
{
    SO_NODE_INIT_CLASS(SoauracadMeshSegmentShape, SoShape, "Shape");
}

SoauracadMeshSegmentShape::SoauracadMeshSegmentShape()
    : renderTriangleLimit(std::numeric_limits<unsigned>::max())
{
    SO_NODE_CONSTRUCTOR(SoauracadMeshSegmentShape);
    SO_NODE_ADD_FIELD(index, (0));
}

/**
 * Either renders the complete mesh or only a subset of the points.
 */
void SoauracadMeshSegmentShape::GLRender(SoGLRenderAction* action)
{
    if (shouldGLRender(action)) {
        SoState* state = action->getState();

        SbBool mode = Gui::SoauracadInteractiveElement::get(state);
        const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
        if (!mesh) {
            return;
        }

        Binding mbind = this->findMaterialBinding(state);

        SoMaterialBundle mb(action);
        // SoTextureCoordinateBundle tb(action, true, false);

        SbBool needNormals = !mb.isColorOnly() /* || tb.isFunction()*/;
        mb.sendFirst();  // make sure we have the correct material

        SbBool ccw = true;
        if (SoShapeHintsElement::getVertexOrdering(state) == SoShapeHintsElement::CLOCKWISE) {
            ccw = false;
        }

        if (!mode || mesh->countFacets() <= this->renderTriangleLimit) {
            if (mbind != OVERALL) {
                drawFaces(mesh, &mb, mbind, needNormals, ccw);
            }
            else {
                drawFaces(mesh, nullptr, mbind, needNormals, ccw);
            }
        }
        else {
            drawPoints(mesh, needNormals, ccw);
        }
    }
}

/**
 * Translates current material binding into the internal Binding enum.
 */
SoauracadMeshSegmentShape::Binding SoauracadMeshSegmentShape::findMaterialBinding(SoState* const state) const
{
    Binding binding = OVERALL;
    SoMaterialBindingElement::Binding matbind = SoMaterialBindingElement::get(state);

    switch (matbind) {
        case SoMaterialBindingElement::OVERALL:
            binding = OVERALL;
            break;
        case SoMaterialBindingElement::PER_VERTEX:
            binding = PER_VERTEX_INDEXED;
            break;
        case SoMaterialBindingElement::PER_VERTEX_INDEXED:
            binding = PER_VERTEX_INDEXED;
            break;
        case SoMaterialBindingElement::PER_PART:
        case SoMaterialBindingElement::PER_FACE:
            binding = PER_FACE_INDEXED;
            break;
        case SoMaterialBindingElement::PER_PART_INDEXED:
        case SoMaterialBindingElement::PER_FACE_INDEXED:
            binding = PER_FACE_INDEXED;
            break;
        default:
            break;
    }
    return binding;
}

/**
 * Renders the triangles of the complete mesh.
 * FIXME: Do it the same way as Coin did to have only one implementation which is controlled by
 * defines
 * FIXME: Implement using different values of transparency for each vertex or face
 */
void SoauracadMeshSegmentShape::drawFaces(
    const Mesh::MeshObject* mesh,
    SoMaterialBundle* mb,
    Binding bind,
    SbBool needNormals,
    SbBool ccw
) const
{
    const MeshCore::MeshPointArray& rPoints = mesh->getKernel().GetPoints();
    const MeshCore::MeshFacetArray& rFacets = mesh->getKernel().GetFacets();
    if (mesh->countSegments() <= this->index.getValue()) {
        return;
    }
    const std::vector<Mesh::FacetIndex> rSegm = mesh->getSegment(this->index.getValue()).getIndices();
    bool perVertex = (mb && bind == PER_VERTEX_INDEXED);
    bool perFace = (mb && bind == PER_FACE_INDEXED);

    if (needNormals) {
        glBegin(GL_TRIANGLES);
        if (ccw) {
            // counterclockwise ordering
            for (Mesh::FacetIndex it : rSegm) {
                const MeshCore::MeshFacet& f = rFacets[it];
                const MeshCore::MeshPoint& v0 = rPoints[f._aulPoints[0]];
                const MeshCore::MeshPoint& v1 = rPoints[f._aulPoints[1]];
                const MeshCore::MeshPoint& v2 = rPoints[f._aulPoints[2]];

                // Calculate the normal n = (v1-v0)x(v2-v0)
                float n[3];
                n[0] = (v1.y - v0.y) * (v2.z - v0.z) - (v1.z - v0.z) * (v2.y - v0.y);
                n[1] = (v1.z - v0.z) * (v2.x - v0.x) - (v1.x - v0.x) * (v2.z - v0.z);
                n[2] = (v1.x - v0.x) * (v2.y - v0.y) - (v1.y - v0.y) * (v2.x - v0.x);

                if (perFace) {
                    mb->send(it, true);
                }
                glNormal(n);
                if (perVertex) {
                    mb->send(f._aulPoints[0], true);
                }
                glVertex(v0);
                if (perVertex) {
                    mb->send(f._aulPoints[1], true);
                }
                glVertex(v1);
                if (perVertex) {
                    mb->send(f._aulPoints[2], true);
                }
                glVertex(v2);
            }
        }
        else {
            // clockwise ordering
            for (Mesh::FacetIndex it : rSegm) {
                const MeshCore::MeshFacet& f = rFacets[it];
                const MeshCore::MeshPoint& v0 = rPoints[f._aulPoints[0]];
                const MeshCore::MeshPoint& v1 = rPoints[f._aulPoints[1]];
                const MeshCore::MeshPoint& v2 = rPoints[f._aulPoints[2]];

                // Calculate the normal n = -(v1-v0)x(v2-v0)
                float n[3];
                n[0] = -((v1.y - v0.y) * (v2.z - v0.z) - (v1.z - v0.z) * (v2.y - v0.y));
                n[1] = -((v1.z - v0.z) * (v2.x - v0.x) - (v1.x - v0.x) * (v2.z - v0.z));
                n[2] = -((v1.x - v0.x) * (v2.y - v0.y) - (v1.y - v0.y) * (v2.x - v0.x));

                glNormal(n);
                glVertex(v0);
                glVertex(v1);
                glVertex(v2);
            }
        }
        glEnd();
    }
    else {
        glBegin(GL_TRIANGLES);
        for (Mesh::FacetIndex it : rSegm) {
            const MeshCore::MeshFacet& f = rFacets[it];
            glVertex(rPoints[f._aulPoints[0]]);
            glVertex(rPoints[f._aulPoints[1]]);
            glVertex(rPoints[f._aulPoints[2]]);
        }
        glEnd();
    }
}

/**
 * Renders the gravity points of a subset of triangles.
 */
void SoauracadMeshSegmentShape::drawPoints(const Mesh::MeshObject* mesh, SbBool needNormals, SbBool ccw) const
{
    const MeshCore::MeshPointArray& rPoints = mesh->getKernel().GetPoints();
    const MeshCore::MeshFacetArray& rFacets = mesh->getKernel().GetFacets();
    if (mesh->countSegments() <= this->index.getValue()) {
        return;
    }
    const std::vector<Mesh::FacetIndex> rSegm = mesh->getSegment(this->index.getValue()).getIndices();
    int mod = rSegm.size() / renderTriangleLimit + 1;

    float size = std::min<float>((float)mod, 3.0F);
    glPointSize(size);

    if (needNormals) {
        glBegin(GL_POINTS);
        int ct = 0;
        if (ccw) {
            for (auto it = rSegm.begin(); it != rSegm.end(); ++it, ct++) {
                if (ct % mod == 0) {
                    const MeshCore::MeshFacet& f = rFacets[*it];
                    const MeshCore::MeshPoint& v0 = rPoints[f._aulPoints[0]];
                    const MeshCore::MeshPoint& v1 = rPoints[f._aulPoints[1]];
                    const MeshCore::MeshPoint& v2 = rPoints[f._aulPoints[2]];

                    // Calculate the normal n = (v1-v0)x(v2-v0)
                    float n[3];
                    n[0] = (v1.y - v0.y) * (v2.z - v0.z) - (v1.z - v0.z) * (v2.y - v0.y);
                    n[1] = (v1.z - v0.z) * (v2.x - v0.x) - (v1.x - v0.x) * (v2.z - v0.z);
                    n[2] = (v1.x - v0.x) * (v2.y - v0.y) - (v1.y - v0.y) * (v2.x - v0.x);

                    // Calculate the center point p=(v0+v1+v2)/3
                    float p[3];
                    p[0] = (v0.x + v1.x + v2.x) / 3.0F;
                    p[1] = (v0.y + v1.y + v2.y) / 3.0F;
                    p[2] = (v0.z + v1.z + v2.z) / 3.0F;
                    glNormal3fv(n);
                    glVertex3fv(p);
                }
            }
        }
        else {
            for (auto it = rSegm.begin(); it != rSegm.end(); ++it, ct++) {
                if (ct % mod == 0) {
                    const MeshCore::MeshFacet& f = rFacets[*it];
                    const MeshCore::MeshPoint& v0 = rPoints[f._aulPoints[0]];
                    const MeshCore::MeshPoint& v1 = rPoints[f._aulPoints[1]];
                    const MeshCore::MeshPoint& v2 = rPoints[f._aulPoints[2]];

                    // Calculate the normal n = -(v1-v0)x(v2-v0)
                    float n[3];
                    n[0] = -((v1.y - v0.y) * (v2.z - v0.z) - (v1.z - v0.z) * (v2.y - v0.y));
                    n[1] = -((v1.z - v0.z) * (v2.x - v0.x) - (v1.x - v0.x) * (v2.z - v0.z));
                    n[2] = -((v1.x - v0.x) * (v2.y - v0.y) - (v1.y - v0.y) * (v2.x - v0.x));

                    // Calculate the center point p=(v0+v1+v2)/3
                    float p[3];
                    p[0] = (v0.x + v1.x + v2.x) / 3.0F;
                    p[1] = (v0.y + v1.y + v2.y) / 3.0F;
                    p[2] = (v0.z + v1.z + v2.z) / 3.0F;
                    glNormal3fv(n);
                    glVertex3fv(p);
                }
            }
        }
        glEnd();
    }
    else {
        glBegin(GL_POINTS);
        int ct = 0;
        for (auto it = rSegm.begin(); it != rSegm.end(); ++it, ct++) {
            if (ct % mod == 0) {
                const MeshCore::MeshFacet& f = rFacets[*it];
                const MeshCore::MeshPoint& v0 = rPoints[f._aulPoints[0]];
                const MeshCore::MeshPoint& v1 = rPoints[f._aulPoints[1]];
                const MeshCore::MeshPoint& v2 = rPoints[f._aulPoints[2]];
                // Calculate the center point p=(v0+v1+v2)/3
                float p[3];
                p[0] = (v0.x + v1.x + v2.x) / 3.0F;
                p[1] = (v0.y + v1.y + v2.y) / 3.0F;
                p[2] = (v0.z + v1.z + v2.z) / 3.0F;
                glVertex3fv(p);
            }
        }
        glEnd();
    }
}

/** Sets the point indices, the geometric points and the normal for each triangle.
 * If the number of triangles exceeds \a renderTriangleLimit then only a triangulation
 * of a rough model is filled in instead. This is due to performance issues.
 * \see createTriangleDetail().
 */
void SoauracadMeshSegmentShape::generatePrimitives(SoAction* action)
{
    SoState* state = action->getState();
    const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
    if (!mesh) {
        return;
    }
    const MeshCore::MeshPointArray& rPoints = mesh->getKernel().GetPoints();
    const MeshCore::MeshFacetArray& rFacets = mesh->getKernel().GetFacets();
    if (rPoints.size() < 3) {
        return;
    }
    if (rFacets.empty()) {
        return;
    }
    if (mesh->countSegments() <= this->index.getValue()) {
        return;
    }
    const std::vector<Mesh::FacetIndex> rSegm = mesh->getSegment(this->index.getValue()).getIndices();

    // get material binding
    Binding mbind = this->findMaterialBinding(state);

    // Create the information when moving over or picking into the scene
    SoPrimitiveVertex vertex;
    SoPointDetail pointDetail;
    SoFaceDetail faceDetail;

    vertex.setDetail(&pointDetail);

    beginShape(action, TRIANGLES, &faceDetail);
    try {
        for (Mesh::FacetIndex it : rSegm) {
            const MeshCore::MeshFacet& f = rFacets[it];
            const MeshCore::MeshPoint& v0 = rPoints[f._aulPoints[0]];
            const MeshCore::MeshPoint& v1 = rPoints[f._aulPoints[1]];
            const MeshCore::MeshPoint& v2 = rPoints[f._aulPoints[2]];

            // Calculate the normal n = (v1-v0)x(v2-v0)
            SbVec3f n;
            n[0] = (v1.y - v0.y) * (v2.z - v0.z) - (v1.z - v0.z) * (v2.y - v0.y);
            n[1] = (v1.z - v0.z) * (v2.x - v0.x) - (v1.x - v0.x) * (v2.z - v0.z);
            n[2] = (v1.x - v0.x) * (v2.y - v0.y) - (v1.y - v0.y) * (v2.x - v0.x);

            // Set the normal
            vertex.setNormal(n);

            // Vertex 0
            if (mbind == PER_VERTEX_INDEXED || mbind == PER_FACE_INDEXED) {
                pointDetail.setMaterialIndex(f._aulPoints[0]);
                vertex.setMaterialIndex(f._aulPoints[0]);
            }
            pointDetail.setCoordinateIndex(f._aulPoints[0]);
            vertex.setPoint(sbvec3f(v0));
            shapeVertex(&vertex);

            // Vertex 1
            if (mbind == PER_VERTEX_INDEXED || mbind == PER_FACE_INDEXED) {
                pointDetail.setMaterialIndex(f._aulPoints[1]);
                vertex.setMaterialIndex(f._aulPoints[1]);
            }
            pointDetail.setCoordinateIndex(f._aulPoints[1]);
            vertex.setPoint(sbvec3f(v1));
            shapeVertex(&vertex);

            // Vertex 2
            if (mbind == PER_VERTEX_INDEXED || mbind == PER_FACE_INDEXED) {
                pointDetail.setMaterialIndex(f._aulPoints[2]);
                vertex.setMaterialIndex(f._aulPoints[2]);
            }
            pointDetail.setCoordinateIndex(f._aulPoints[2]);
            vertex.setPoint(sbvec3f(v2));
            shapeVertex(&vertex);

            // Increment for the next face
            faceDetail.incFaceIndex();
        }
    }
    catch (const Base::MemoryException&) {
        Base::Console().log("Not enough memory to generate primitives\n");
    }

    endShape();
}

/**
 * Sets the bounding box of the mesh to \a box and its center to \a center.
 */
void SoauracadMeshSegmentShape::computeBBox(SoAction* action, SbBox3f& box, SbVec3f& center)
{
    box.setBounds(SbVec3f(0, 0, 0), SbVec3f(0, 0, 0));
    center.setValue(0.0F, 0.0F, 0.0F);

    SoState* state = action->getState();
    const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
    if (mesh && mesh->countSegments() > this->index.getValue()) {
        const Mesh::Segment& segm = mesh->getSegment(this->index.getValue());
        const std::vector<Mesh::FacetIndex>& indices = segm.getIndices();
        Base::BoundBox3f cBox;
        if (!indices.empty()) {
            const MeshCore::MeshPointArray& rPoint = mesh->getKernel().GetPoints();
            const MeshCore::MeshFacetArray& rFaces = mesh->getKernel().GetFacets();

            for (Mesh::FacetIndex index : indices) {
                const MeshCore::MeshFacet& face = rFaces[index];
                cBox.Add(rPoint[face._aulPoints[0]]);
                cBox.Add(rPoint[face._aulPoints[1]]);
                cBox.Add(rPoint[face._aulPoints[2]]);
            }

            box.setBounds(
                SbVec3f(cBox.MinX, cBox.MinY, cBox.MinZ),
                SbVec3f(cBox.MaxX, cBox.MaxY, cBox.MaxZ)
            );
            Base::Vector3f mid = cBox.GetCenter();
            center.setValue(mid.x, mid.y, mid.z);
        }
    }
}

/**
 * Adds the number of the triangles to the \a SoGetPrimitiveCountAction.
 */
void SoauracadMeshSegmentShape::getPrimitiveCount(SoGetPrimitiveCountAction* action)
{
    if (!this->shouldPrimitiveCount(action)) {
        return;
    }
    SoState* state = action->getState();
    const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
    if (mesh && mesh->countSegments() > this->index.getValue()) {
        const Mesh::Segment& segm = mesh->getSegment(this->index.getValue());
        action->addNumTriangles(segm.getIndices().size());
    }
}

// -------------------------------------------------------

SO_NODE_SOURCE(SoauracadMeshObjectBoundary)

void SoauracadMeshObjectBoundary::initClass()
{
    SO_NODE_INIT_CLASS(SoauracadMeshObjectBoundary, SoShape, "Shape");
}

SoauracadMeshObjectBoundary::SoauracadMeshObjectBoundary()
{
    SO_NODE_CONSTRUCTOR(SoauracadMeshObjectBoundary);
}

/**
 * Renders the open edges only.
 */
void SoauracadMeshObjectBoundary::GLRender(SoGLRenderAction* action)
{
    if (shouldGLRender(action)) {
        SoState* state = action->getState();
        const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
        if (!mesh) {
            return;
        }

        SoMaterialBundle mb(action);
        SoTextureCoordinateBundle tb(action, true, false);
        SoLazyElement::setLightModel(state, SoLazyElement::BASE_COLOR);
        mb.sendFirst();  // make sure we have the correct material

        drawLines(mesh);
    }
}

/**
 * Renders the triangles of the complete mesh.
 */
void SoauracadMeshObjectBoundary::drawLines(const Mesh::MeshObject* mesh) const
{
    const MeshCore::MeshPointArray& rPoints = mesh->getKernel().GetPoints();
    const MeshCore::MeshFacetArray& rFacets = mesh->getKernel().GetFacets();

    // When rendering open edges use the given line width * 3
    GLfloat lineWidth {};
    glGetFloatv(GL_LINE_WIDTH, &lineWidth);
    glLineWidth(3.0F * lineWidth);

    // Use the data structure directly and not through MeshFacetIterator as this
    // class is quite slowly (at least for rendering)
    glBegin(GL_LINES);
    for (const auto& rFacet : rFacets) {
        for (int i = 0; i < 3; i++) {
            if (rFacet._aulNeighbours[i] == MeshCore::FACET_INDEX_MAX) {
                glVertex(rPoints[rFacet._aulPoints[i]]);
                glVertex(rPoints[rFacet._aulPoints[(i + 1) % 3]]);
            }
        }
    }

    glEnd();
}

void SoauracadMeshObjectBoundary::generatePrimitives(SoAction* action)
{
    // do not create primitive information as an SoauracadMeshObjectShape
    // should already be used that delivers the information
    SoState* state = action->getState();
    const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
    if (!mesh) {
        return;
    }
    const MeshCore::MeshPointArray& rPoints = mesh->getKernel().GetPoints();
    const MeshCore::MeshFacetArray& rFacets = mesh->getKernel().GetFacets();

    // Create the information when moving over or picking into the scene
    SoPrimitiveVertex vertex;
    SoPointDetail pointDetail;
    SoLineDetail lineDetail;

    vertex.setDetail(&pointDetail);

    beginShape(action, LINES, &lineDetail);
    for (const auto& rFacet : rFacets) {
        for (int i = 0; i < 3; i++) {
            if (rFacet._aulNeighbours[i] == MeshCore::FACET_INDEX_MAX) {
                const MeshCore::MeshPoint& v0 = rPoints[rFacet._aulPoints[i]];
                const MeshCore::MeshPoint& v1 = rPoints[rFacet._aulPoints[(i + 1) % 3]];

                // Vertex 0
                pointDetail.setCoordinateIndex(rFacet._aulPoints[i]);
                vertex.setPoint(sbvec3f(v0));
                shapeVertex(&vertex);

                // Vertex 1
                pointDetail.setCoordinateIndex(rFacet._aulPoints[(i + 1) % 3]);
                vertex.setPoint(sbvec3f(v1));
                shapeVertex(&vertex);

                // Increment for the next open edge
                lineDetail.incLineIndex();
            }
        }
    }

    endShape();
}

/**
 * Sets the bounding box of the mesh to \a box and its center to \a center.
 */
void SoauracadMeshObjectBoundary::computeBBox(SoAction* action, SbBox3f& box, SbVec3f& center)
{
    SoState* state = action->getState();
    const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
    if (!mesh) {
        return;
    }
    const MeshCore::MeshPointArray& rPoints = mesh->getKernel().GetPoints();
    if (!rPoints.empty()) {
        Base::BoundBox3f cBox;
        for (const auto& rPoint : rPoints) {
            cBox.Add(rPoint);
        }
        box.setBounds(
            SbVec3f(cBox.MinX, cBox.MinY, cBox.MinZ),
            SbVec3f(cBox.MaxX, cBox.MaxY, cBox.MaxZ)
        );
        Base::Vector3f mid = cBox.GetCenter();
        center.setValue(mid.x, mid.y, mid.z);
    }
    else {
        box.setBounds(SbVec3f(0, 0, 0), SbVec3f(0, 0, 0));
        center.setValue(0.0F, 0.0F, 0.0F);
    }
}

/**
 * Adds the number of the triangles to the \a SoGetPrimitiveCountAction.
 */
void SoauracadMeshObjectBoundary::getPrimitiveCount(SoGetPrimitiveCountAction* action)
{
    if (!this->shouldPrimitiveCount(action)) {
        return;
    }
    SoState* state = action->getState();
    const Mesh::MeshObject* mesh = SoauracadMeshObjectElement::get(state);
    if (!mesh) {
        return;
    }
    const MeshCore::MeshFacetArray& rFaces = mesh->getKernel().GetFacets();

    // Count number of open edges first
    int ctEdges = 0;
    for (const auto& rFace : rFaces) {
        for (Mesh::FacetIndex nbIndex : rFace._aulNeighbours) {
            if (nbIndex == MeshCore::FACET_INDEX_MAX) {
                ctEdges++;
            }
        }
    }

    action->addNumLines(ctEdges);
}
