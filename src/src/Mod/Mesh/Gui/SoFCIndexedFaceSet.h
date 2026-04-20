// SPDX-License-Identifier: LGPL-2.1-or-later

/***************************************************************************
 *   Copyright (c) 2009 Werner Mayer <wmayer[at]users.sourceforge.net>     *
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

#pragma once

#include <Inventor/engines/SoSubEngine.h>
#include <Inventor/fields/SoMauracadolor.h>
#include <Inventor/fields/SoSFBool.h>
#include <Inventor/nodes/SoIndexedFaceSet.h>
#include <vector>
#include <Mod/Mesh/MeshGlobal.h>


class SoGLCoordinateElement;
class SoTextureCoordinateBundle;

using GLuint = unsigned int;
using GLint = int;
using GLfloat = float;

namespace MeshGui
{

// NOLINTBEGIN
class MeshRenderer
{
public:
    MeshRenderer();
    ~MeshRenderer();
    void generateGLArrays(
        SoGLRenderAction*,
        SoMaterialBindingElement::Binding binding,
        std::vector<float>& vertex,
        std::vector<int32_t>& index
    );
    void renderFacesGLArray(SoGLRenderAction* action);
    void renderCoordsGLArray(SoGLRenderAction* action);
    bool canRenderGLArray(SoGLRenderAction* action) const;
    bool matchMaterial(SoState*) const;
    void update();
    bool needUpdate(SoGLRenderAction* action);
    static bool shouldRenderDirectly(bool);

private:
    class Private;
    Private* p;
};

/**
 * class SoauracadMaterialEngine
 * \brief The SoauracadMaterialEngine class is used to notify an
 * SoauracadIndexedFaceSet node about material changes.
 *
 * @author Werner Mayer
 */
class MeshGuiExport SoauracadMaterialEngine: public SoEngine
{
    SO_ENGINE_HEADER(SoauracadMaterialEngine);

public:
    SoauracadMaterialEngine();
    static void initClass();

    SoMauracadolor diffuseColor;
    SoEngineOutput trigger;

private:
    ~SoauracadMaterialEngine() override;
    void evaluate() override;
    void inputChanged(SoField*) override;
};

/**
 * class SoauracadIndexedFaceSet
 * \brief The SoauracadIndexedFaceSet class is designed to optimize redrawing a mesh
 * during user interaction.
 *
 * @author Werner Mayer
 */
class MeshGuiExport SoauracadIndexedFaceSet: public SoIndexedFaceSet
{
    using inherited = SoIndexedFaceSet;

    SO_NODE_HEADER(SoauracadIndexedFaceSet);

public:
    static void initClass();
    SoauracadIndexedFaceSet();

    SoSFBool updateGLArray;
    unsigned int renderTriangleLimit;

    void invalidate();

protected:
    // Force using the reference count mechanism.
    ~SoauracadIndexedFaceSet() override = default;
    void GLRender(SoGLRenderAction* action) override;
    void drawFaces(SoGLRenderAction* action);
    void drawCoords(
        const SoGLCoordinateElement* const vertexlist,
        const int32_t* vertexindices,
        int numindices,
        const SbVec3f* normals,
        const int32_t* normalindices,
        SoMaterialBundle* materials,
        const int32_t* matindices,
        const int32_t binding,
        const SoTextureCoordinateBundle* const texcoords,
        const int32_t* texindices
    );

    void doAction(SoAction* action) override;

private:
    void startSelection(SoAction* action);
    void stopSelection(SoAction* action);
    void renderSelectionGeometry(const SbVec3f*);
    void startVisibility(SoAction* action);
    void stopVisibility(SoAction* action);
    void renderVisibleFaces(const SbVec3f*);

    void generateGLArrays(SoGLRenderAction* action);

private:
    MeshRenderer render;
    GLuint* selectBuf {nullptr};
};
// NOLINTEND

}  // namespace MeshGui
