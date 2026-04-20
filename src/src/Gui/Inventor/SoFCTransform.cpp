// SPDX-License-Identifier: LGPL-2.1-or-later

/***************************************************************************
 *   Copyright (c) 2024 Werner Mayer <wmayer[at]users.sourceforge.net>     *
 *                                                                         *
 *   This file is part of AuraCAD.                                         *
 *                                                                         *
 *   AuraCAD is free software: you can redistribute it and/or modify it    *
 *   under the terms of the GNU Lesser General Public License as           *
 *   published by the Free Software Foundation, either version 2.1 of the  *
 *   License, or (at your option) any later version.                       *
 *                                                                         *
 *   AuraCAD is distributed in the hope that it will be useful, but        *
 *   WITHOUT ANY WARRANTY; without even the implied warranty of            *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      *
 *   Lesser General Public License for more details.                       *
 *                                                                         *
 *   You should have received a copy of the GNU Lesser General Public      *
 *   License along with AuraCAD. If not, see                               *
 *   <https://www.gnu.org/licenses/>.                                      *
 *                                                                         *
 **************************************************************************/


#include <Inventor/actions/SoCallbackAction.h>
#include <Inventor/actions/SoGetBoundingBoxAction.h>
#include <Inventor/actions/SoGetPrimitiveCountAction.h>
#include <Inventor/actions/SoGLRenderAction.h>
#include <Inventor/actions/SoPickAction.h>
#include <Inventor/elements/SoModelMatrixElement.h>

#include "SoauracadTransform.h"


using namespace Gui;

SO_NODE_SOURCE(SoauracadTransform)

void SoauracadTransform::initClass()
{
    SO_NODE_INIT_CLASS(SoauracadTransform, SoTransform, "Transform");
}

SoauracadTransform::SoauracadTransform()
{
    SO_NODE_CONSTRUCTOR(SoauracadTransform);
}

void SoauracadTransform::GLRender(SoGLRenderAction* action)
{
    SoauracadTransform::doAction(action);
}

void SoauracadTransform::callback(SoCallbackAction* action)
{
    SoauracadTransform::doAction(action);
}

void SoauracadTransform::pick(SoPickAction* action)
{
    SoauracadTransform::doAction(action);
}

void SoauracadTransform::getPrimitiveCount(SoGetPrimitiveCountAction* action)
{
    SoauracadTransform::doAction(action);
}

void SoauracadTransform::getBoundingBox(SoGetBoundingBoxAction* action)
{
    SoauracadTransform::doAction(action);
}

void SoauracadTransform::doAction(SoAction* action)
{
    SbMatrix matrix;
    matrix.setTransform(
        this->translation.getValue(),
        this->rotation.getValue(),
        this->scaleFactor.getValue(),
        this->scaleOrientation.getValue(),
        this->center.getValue()
    );

    // This is different to SoTransform::doAction() where model matrix
    // is always set
    if (matrix != SbMatrix::identity()) {
        SoModelMatrixElement::mult(action->getState(), this, matrix);
    }
}
