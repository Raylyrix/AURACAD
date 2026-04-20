// SPDX-License-Identifier: LGPL-2.1-or-later
/***************************************************************************
 *   Copyright (c) 2005 JÃ¼rgen Riegel <juergen.riegel@web.de>              *
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


#include <Inventor/actions/SoSearchAction.h>
#include <Inventor/actions/SoGetBoundingBoxAction.h>
#include <Inventor/elements/SoComplexityElement.h>
#include <Inventor/elements/SoComplexityTypeElement.h>
#include <Inventor/elements/SoCoordinateElement.h>
#include <Inventor/elements/SoFontNameElement.h>
#include <Inventor/elements/SoFontSizeElement.h>
#include <Inventor/elements/SoModelMatrixElement.h>
#include <Inventor/elements/SoProfileCoordinateElement.h>
#include <Inventor/elements/SoProfileElement.h>
#include <Inventor/elements/SoProjectionMatrixElement.h>
#include <Inventor/elements/SoShapeStyleElement.h>
#include <Inventor/elements/SoSwitchElement.h>
#include <Inventor/elements/SoUnitsElement.h>
#include <Inventor/elements/SoViewingMatrixElement.h>
#include <Inventor/elements/SoViewportRegionElement.h>
#include <Inventor/elements/SoViewVolumeElement.h>
#include <Inventor/nodes/SoBaseColor.h>
#include <Inventor/nodes/SoCallback.h>
#include <Inventor/nodes/SoCamera.h>
#include <Inventor/nodes/SoComplexity.h>
#include <Inventor/nodes/SoCoordinate3.h>
#include <Inventor/nodes/SoCoordinate4.h>
#include <Inventor/nodes/SoCube.h>
#include <Inventor/nodes/SoDrawStyle.h>
#include <Inventor/nodes/SoFont.h>
#include <Inventor/nodes/SoIndexedLineSet.h>
#include <Inventor/nodes/SoIndexedFaceSet.h>
#include <Inventor/nodes/SoLightModel.h>
#include <Inventor/nodes/SoMatrixTransform.h>
#include <Inventor/nodes/SoPointSet.h>
#include <Inventor/nodes/SoProfile.h>
#include <Inventor/nodes/SoProfileCoordinate2.h>
#include <Inventor/nodes/SoProfileCoordinate3.h>
#include <Inventor/nodes/SoSeparator.h>
#include <Inventor/nodes/SoSwitch.h>
#include <Inventor/nodes/SoTransformation.h>


#include "SoauracadSelectionAction.h"
#include "SoauracadSelection.h"
#include "SoFullPathHelper.h"


using namespace Gui;


SO_ACTION_SOURCE(SoauracadPreselectionAction)

/**
 * The order of the defined SO_ACTION_ADD_METHOD statements is very important. First the base
 * classes and afterwards subclasses of them must be listed, otherwise the registered methods
 * of subclasses will be overridden. For more details see the thread in the Coin3d forum
 * https://www.coin3d.org/pipermail/coin-discuss/2004-May/004346.html.
 * This means that \c SoSwitch must be listed after \c SoGroup and \c SoauracadSelection after
 * \c SoSeparator because both classes inherits the others.
 */
void SoauracadPreselectionAction::initClass()
{
    SO_ACTION_INIT_CLASS(SoauracadPreselectionAction, SoAction);

    SO_ENABLE(SoauracadPreselectionAction, SoSwitchElement);

    SO_ACTION_ADD_METHOD(SoNode, nullAction);

    SO_ENABLE(SoauracadPreselectionAction, SoModelMatrixElement);
    SO_ENABLE(SoauracadPreselectionAction, SoShapeStyleElement);
    SO_ENABLE(SoauracadPreselectionAction, SoComplexityElement);
    SO_ENABLE(SoauracadPreselectionAction, SoComplexityTypeElement);
    SO_ENABLE(SoauracadPreselectionAction, SoCoordinateElement);
    SO_ENABLE(SoauracadPreselectionAction, SoFontNameElement);
    SO_ENABLE(SoauracadPreselectionAction, SoFontSizeElement);
    SO_ENABLE(SoauracadPreselectionAction, SoProfileCoordinateElement);
    SO_ENABLE(SoauracadPreselectionAction, SoProfileElement);
    SO_ENABLE(SoauracadPreselectionAction, SoSwitchElement);
    SO_ENABLE(SoauracadPreselectionAction, SoUnitsElement);
    SO_ENABLE(SoauracadPreselectionAction, SoViewVolumeElement);
    SO_ENABLE(SoauracadPreselectionAction, SoViewingMatrixElement);
    SO_ENABLE(SoauracadPreselectionAction, SoViewportRegionElement);


    SO_ACTION_ADD_METHOD(SoCallback, callDoAction);
    SO_ACTION_ADD_METHOD(SoComplexity, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate4, callDoAction);
    SO_ACTION_ADD_METHOD(SoFont, callDoAction);
    SO_ACTION_ADD_METHOD(SoGroup, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfile, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate2, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoTransformation, callDoAction);
    SO_ACTION_ADD_METHOD(SoSwitch, callDoAction);

    SO_ACTION_ADD_METHOD(SoSeparator, callDoAction);
    SO_ACTION_ADD_METHOD(SoauracadSelection, callDoAction);

    SO_ACTION_ADD_METHOD(SoIndexedLineSet, callDoAction);
    SO_ACTION_ADD_METHOD(SoIndexedFaceSet, callDoAction);
    SO_ACTION_ADD_METHOD(SoPointSet, callDoAction);
}

void SoauracadPreselectionAction::finish()
{
    atexit_cleanup();
}


SoauracadPreselectionAction::SoauracadPreselectionAction(const SelectionChanges& SelCh)
    : SelChange(SelCh)
{
    SO_ACTION_CONSTRUCTOR(SoauracadPreselectionAction);
}


SoauracadPreselectionAction::~SoauracadPreselectionAction() = default;


void SoauracadPreselectionAction::beginTraversal(SoNode* node)
{
    traverse(node);
}

void SoauracadPreselectionAction::callDoAction(SoAction* action, SoNode* node)
{
    node->doAction(action);
}

// ---------------------------------------------------------------

SO_ACTION_SOURCE(SoauracadSelectionAction)

/**
 * The order of the defined SO_ACTION_ADD_METHOD statements is very important. First the base
 * classes and afterwards subclasses of them must be listed, otherwise the registered methods
 * of subclasses will be overridden. For more details see the thread in the Coin3d forum
 * https://www.coin3d.org/pipermail/coin-discuss/2004-May/004346.html.
 * This means that \c SoSwitch must be listed after \c SoGroup and \c SoauracadSelection after
 * \c SoSeparator because both classes inherits the others.
 */
void SoauracadSelectionAction::initClass()
{
    SO_ACTION_INIT_CLASS(SoauracadSelectionAction, SoAction);

    SO_ENABLE(SoauracadSelectionAction, SoSwitchElement);

    SO_ACTION_ADD_METHOD(SoNode, nullAction);

    SO_ENABLE(SoauracadSelectionAction, SoModelMatrixElement);
    SO_ENABLE(SoauracadSelectionAction, SoShapeStyleElement);
    SO_ENABLE(SoauracadSelectionAction, SoComplexityElement);
    SO_ENABLE(SoauracadSelectionAction, SoComplexityTypeElement);
    SO_ENABLE(SoauracadSelectionAction, SoCoordinateElement);
    SO_ENABLE(SoauracadSelectionAction, SoFontNameElement);
    SO_ENABLE(SoauracadSelectionAction, SoFontSizeElement);
    SO_ENABLE(SoauracadSelectionAction, SoProfileCoordinateElement);
    SO_ENABLE(SoauracadSelectionAction, SoProfileElement);
    SO_ENABLE(SoauracadSelectionAction, SoSwitchElement);
    SO_ENABLE(SoauracadSelectionAction, SoUnitsElement);
    SO_ENABLE(SoauracadSelectionAction, SoViewVolumeElement);
    SO_ENABLE(SoauracadSelectionAction, SoViewingMatrixElement);
    SO_ENABLE(SoauracadSelectionAction, SoViewportRegionElement);


    SO_ACTION_ADD_METHOD(SoCallback, callDoAction);
    SO_ACTION_ADD_METHOD(SoComplexity, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate4, callDoAction);
    SO_ACTION_ADD_METHOD(SoFont, callDoAction);
    SO_ACTION_ADD_METHOD(SoGroup, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfile, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate2, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoTransformation, callDoAction);
    SO_ACTION_ADD_METHOD(SoSwitch, callDoAction);

    SO_ACTION_ADD_METHOD(SoSeparator, callDoAction);
    SO_ACTION_ADD_METHOD(SoauracadSelection, callDoAction);

    SO_ACTION_ADD_METHOD(SoIndexedLineSet, callDoAction);
    SO_ACTION_ADD_METHOD(SoIndexedFaceSet, callDoAction);
    SO_ACTION_ADD_METHOD(SoPointSet, callDoAction);
}

void SoauracadSelectionAction::finish()
{
    atexit_cleanup();
}


SoauracadSelectionAction::SoauracadSelectionAction(const SelectionChanges& SelCh)
    : SelChange(SelCh)
{
    SO_ACTION_CONSTRUCTOR(SoauracadSelectionAction);
}


SoauracadSelectionAction::~SoauracadSelectionAction() = default;


void SoauracadSelectionAction::beginTraversal(SoNode* node)
{
    traverse(node);
}

void SoauracadSelectionAction::callDoAction(SoAction* action, SoNode* node)
{
    node->doAction(action);
}

// ---------------------------------------------------------------

SO_ACTION_SOURCE(SoauracadEnableSelectionAction)

/**
 * The order of the defined SO_ACTION_ADD_METHOD statements is very important. First the base
 * classes and afterwards subclasses of them must be listed, otherwise the registered methods
 * of subclasses will be overridden. For more details see the thread in the Coin3d forum
 * https://www.coin3d.org/pipermail/coin-discuss/2004-May/004346.html.
 * This means that \c SoSwitch must be listed after \c SoGroup and \c SoauracadSelection after
 * \c SoSeparator because both classes inherits the others.
 */
void SoauracadEnableSelectionAction::initClass()
{
    SO_ACTION_INIT_CLASS(SoauracadEnableSelectionAction, SoAction);

    SO_ENABLE(SoauracadEnableSelectionAction, SoSwitchElement);

    SO_ACTION_ADD_METHOD(SoNode, nullAction);

    SO_ENABLE(SoauracadEnableSelectionAction, SoModelMatrixElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoShapeStyleElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoComplexityElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoComplexityTypeElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoCoordinateElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoFontNameElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoFontSizeElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoProfileCoordinateElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoProfileElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoSwitchElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoUnitsElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoViewVolumeElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoViewingMatrixElement);
    SO_ENABLE(SoauracadEnableSelectionAction, SoViewportRegionElement);


    SO_ACTION_ADD_METHOD(SoCallback, callDoAction);
    SO_ACTION_ADD_METHOD(SoComplexity, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate4, callDoAction);
    SO_ACTION_ADD_METHOD(SoFont, callDoAction);
    SO_ACTION_ADD_METHOD(SoGroup, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfile, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate2, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoTransformation, callDoAction);
    SO_ACTION_ADD_METHOD(SoSwitch, callDoAction);

    SO_ACTION_ADD_METHOD(SoSeparator, callDoAction);
    SO_ACTION_ADD_METHOD(SoauracadSelection, callDoAction);
}

void SoauracadEnableSelectionAction::finish()
{
    atexit_cleanup();
}


SoauracadEnableSelectionAction::SoauracadEnableSelectionAction(const SbBool& sel)
    : enabled(sel)
{
    SO_ACTION_CONSTRUCTOR(SoauracadEnableSelectionAction);
}


SoauracadEnableSelectionAction::~SoauracadEnableSelectionAction() = default;


void SoauracadEnableSelectionAction::beginTraversal(SoNode* node)
{
    traverse(node);
}

void SoauracadEnableSelectionAction::callDoAction(SoAction* action, SoNode* node)
{
    node->doAction(action);
}

// ---------------------------------------------------------------

SO_ACTION_SOURCE(SoauracadEnablePreselectionAction)

/**
 * The order of the defined SO_ACTION_ADD_METHOD statements is very important. First the base
 * classes and afterwards subclasses of them must be listed, otherwise the registered methods
 * of subclasses will be overridden. For more details see the thread in the Coin3d forum
 * https://www.coin3d.org/pipermail/coin-discuss/2004-May/004346.html.
 * This means that \c SoSwitch must be listed after \c SoGroup and \c SoauracadSelection after
 * \c SoSeparator because both classes inherits the others.
 */
void SoauracadEnablePreselectionAction::initClass()
{
    SO_ACTION_INIT_CLASS(SoauracadEnablePreselectionAction, SoAction);

    SO_ENABLE(SoauracadEnablePreselectionAction, SoSwitchElement);

    SO_ACTION_ADD_METHOD(SoNode, nullAction);

    SO_ENABLE(SoauracadEnablePreselectionAction, SoModelMatrixElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoShapeStyleElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoComplexityElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoComplexityTypeElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoCoordinateElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoFontNameElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoFontSizeElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoProfileCoordinateElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoProfileElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoSwitchElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoUnitsElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoViewVolumeElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoViewingMatrixElement);
    SO_ENABLE(SoauracadEnablePreselectionAction, SoViewportRegionElement);


    SO_ACTION_ADD_METHOD(SoCallback, callDoAction);
    SO_ACTION_ADD_METHOD(SoComplexity, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate4, callDoAction);
    SO_ACTION_ADD_METHOD(SoFont, callDoAction);
    SO_ACTION_ADD_METHOD(SoGroup, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfile, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate2, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoTransformation, callDoAction);
    SO_ACTION_ADD_METHOD(SoSwitch, callDoAction);

    SO_ACTION_ADD_METHOD(SoSeparator, callDoAction);
    SO_ACTION_ADD_METHOD(SoauracadSelection, callDoAction);
}

void SoauracadEnablePreselectionAction::finish()
{
    atexit_cleanup();
}


SoauracadEnablePreselectionAction::SoauracadEnablePreselectionAction(const SbBool& sel)
    : enabled(sel)
{
    SO_ACTION_CONSTRUCTOR(SoauracadEnablePreselectionAction);
}


SoauracadEnablePreselectionAction::~SoauracadEnablePreselectionAction() = default;


void SoauracadEnablePreselectionAction::beginTraversal(SoNode* node)
{
    traverse(node);
}

void SoauracadEnablePreselectionAction::callDoAction(SoAction* action, SoNode* node)
{
    node->doAction(action);
}

// ---------------------------------------------------------------

SO_ACTION_SOURCE(SoauracadSelectionColorAction)

/**
 * The order of the defined SO_ACTION_ADD_METHOD statements is very important. First the base
 * classes and afterwards subclasses of them must be listed, otherwise the registered methods
 * of subclasses will be overridden. For more details see the thread in the Coin3d forum
 * https://www.coin3d.org/pipermail/coin-discuss/2004-May/004346.html.
 * This means that \c SoSwitch must be listed after \c SoGroup and \c SoauracadSelection after
 * \c SoSeparator because both classes inherits the others.
 */
void SoauracadSelectionColorAction::initClass()
{
    SO_ACTION_INIT_CLASS(SoauracadSelectionColorAction, SoAction);

    SO_ENABLE(SoauracadSelectionColorAction, SoSwitchElement);

    SO_ACTION_ADD_METHOD(SoNode, nullAction);

    SO_ENABLE(SoauracadSelectionColorAction, SoModelMatrixElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoShapeStyleElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoComplexityElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoComplexityTypeElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoCoordinateElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoFontNameElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoFontSizeElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoProfileCoordinateElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoProfileElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoSwitchElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoUnitsElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoViewVolumeElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoViewingMatrixElement);
    SO_ENABLE(SoauracadSelectionColorAction, SoViewportRegionElement);


    SO_ACTION_ADD_METHOD(SoCallback, callDoAction);
    SO_ACTION_ADD_METHOD(SoComplexity, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate4, callDoAction);
    SO_ACTION_ADD_METHOD(SoFont, callDoAction);
    SO_ACTION_ADD_METHOD(SoGroup, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfile, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate2, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoTransformation, callDoAction);
    SO_ACTION_ADD_METHOD(SoSwitch, callDoAction);

    SO_ACTION_ADD_METHOD(SoSeparator, callDoAction);
    SO_ACTION_ADD_METHOD(SoauracadSelection, callDoAction);
}

void SoauracadSelectionColorAction::finish()
{
    atexit_cleanup();
}


SoauracadSelectionColorAction::SoauracadSelectionColorAction(const SoSauracadolor& col)
    : selectionColor(col)
{
    SO_ACTION_CONSTRUCTOR(SoauracadSelectionColorAction);
}


SoauracadSelectionColorAction::~SoauracadSelectionColorAction() = default;


void SoauracadSelectionColorAction::beginTraversal(SoNode* node)
{
    traverse(node);
}

void SoauracadSelectionColorAction::callDoAction(SoAction* action, SoNode* node)
{
    node->doAction(action);
}

// ---------------------------------------------------------------

SO_ACTION_SOURCE(SoauracadHighlightColorAction)

/**
 * The order of the defined SO_ACTION_ADD_METHOD statements is very important. First the base
 * classes and afterwards subclasses of them must be listed, otherwise the registered methods
 * of subclasses will be overridden. For more details see the thread in the Coin3d forum
 * https://www.coin3d.org/pipermail/coin-discuss/2004-May/004346.html.
 * This means that \c SoSwitch must be listed after \c SoGroup and \c SoauracadSelection after
 * \c SoSeparator because both classes inherits the others.
 */
void SoauracadHighlightColorAction::initClass()
{
    SO_ACTION_INIT_CLASS(SoauracadHighlightColorAction, SoAction);

    SO_ENABLE(SoauracadHighlightColorAction, SoSwitchElement);

    SO_ACTION_ADD_METHOD(SoNode, nullAction);

    SO_ENABLE(SoauracadHighlightColorAction, SoModelMatrixElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoShapeStyleElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoComplexityElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoComplexityTypeElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoCoordinateElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoFontNameElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoFontSizeElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoProfileCoordinateElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoProfileElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoSwitchElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoUnitsElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoViewVolumeElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoViewingMatrixElement);
    SO_ENABLE(SoauracadHighlightColorAction, SoViewportRegionElement);


    SO_ACTION_ADD_METHOD(SoCallback, callDoAction);
    SO_ACTION_ADD_METHOD(SoComplexity, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate4, callDoAction);
    SO_ACTION_ADD_METHOD(SoFont, callDoAction);
    SO_ACTION_ADD_METHOD(SoGroup, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfile, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate2, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoTransformation, callDoAction);
    SO_ACTION_ADD_METHOD(SoSwitch, callDoAction);

    SO_ACTION_ADD_METHOD(SoSeparator, callDoAction);
    SO_ACTION_ADD_METHOD(SoauracadSelection, callDoAction);
}

void SoauracadHighlightColorAction::finish()
{
    atexit_cleanup();
}


SoauracadHighlightColorAction::SoauracadHighlightColorAction(const SoSauracadolor& col)
    : highlightColor(col)
{
    SO_ACTION_CONSTRUCTOR(SoauracadHighlightColorAction);
}


SoauracadHighlightColorAction::~SoauracadHighlightColorAction() = default;


void SoauracadHighlightColorAction::beginTraversal(SoNode* node)
{
    traverse(node);
}

void SoauracadHighlightColorAction::callDoAction(SoAction* action, SoNode* node)
{
    node->doAction(action);
}

// ---------------------------------------------------------------

SO_ACTION_SOURCE(SoauracadDocumentAction)

/**
 * The order of the defined SO_ACTION_ADD_METHOD statements is very important. First the base
 * classes and afterwards subclasses of them must be listed, otherwise the registered methods
 * of subclasses will be overridden. For more details see the thread in the Coin3d forum
 * https://www.coin3d.org/pipermail/coin-discuss/2004-May/004346.html.
 * This means that \c SoSwitch must be listed after \c SoGroup and \c SoauracadSelection after
 * \c SoSeparator because both classes inherits the others.
 */
void SoauracadDocumentAction::initClass()
{
    SO_ACTION_INIT_CLASS(SoauracadDocumentAction, SoAction);

    SO_ENABLE(SoauracadDocumentAction, SoSwitchElement);

    SO_ACTION_ADD_METHOD(SoNode, nullAction);

    SO_ENABLE(SoauracadDocumentAction, SoModelMatrixElement);
    SO_ENABLE(SoauracadDocumentAction, SoShapeStyleElement);
    SO_ENABLE(SoauracadDocumentAction, SoComplexityElement);
    SO_ENABLE(SoauracadDocumentAction, SoComplexityTypeElement);
    SO_ENABLE(SoauracadDocumentAction, SoCoordinateElement);
    SO_ENABLE(SoauracadDocumentAction, SoFontNameElement);
    SO_ENABLE(SoauracadDocumentAction, SoFontSizeElement);
    SO_ENABLE(SoauracadDocumentAction, SoProfileCoordinateElement);
    SO_ENABLE(SoauracadDocumentAction, SoProfileElement);
    SO_ENABLE(SoauracadDocumentAction, SoSwitchElement);
    SO_ENABLE(SoauracadDocumentAction, SoUnitsElement);
    SO_ENABLE(SoauracadDocumentAction, SoViewVolumeElement);
    SO_ENABLE(SoauracadDocumentAction, SoViewingMatrixElement);
    SO_ENABLE(SoauracadDocumentAction, SoViewportRegionElement);


    SO_ACTION_ADD_METHOD(SoCallback, callDoAction);
    SO_ACTION_ADD_METHOD(SoComplexity, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate4, callDoAction);
    SO_ACTION_ADD_METHOD(SoFont, callDoAction);
    SO_ACTION_ADD_METHOD(SoGroup, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfile, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate2, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoTransformation, callDoAction);
    SO_ACTION_ADD_METHOD(SoSwitch, callDoAction);

    SO_ACTION_ADD_METHOD(SoSeparator, callDoAction);
    SO_ACTION_ADD_METHOD(SoauracadSelection, callDoAction);
}

void SoauracadDocumentAction::finish()
{
    atexit_cleanup();
}


SoauracadDocumentAction::SoauracadDocumentAction(const SoSFString& docName)
    : documentName(docName)
{
    SO_ACTION_CONSTRUCTOR(SoauracadDocumentAction);
}


SoauracadDocumentAction::~SoauracadDocumentAction() = default;


void SoauracadDocumentAction::beginTraversal(SoNode* node)
{
    traverse(node);
}

void SoauracadDocumentAction::callDoAction(SoAction* action, SoNode* node)
{
    node->doAction(action);
}


// ---------------------------------------------------------------

SO_ACTION_SOURCE(SoauracadDocumentObjectAction)

/**
 * The order of the defined SO_ACTION_ADD_METHOD statements is very important. First the base
 * classes and afterwards subclasses of them must be listed, otherwise the registered methods
 * of subclasses will be overridden. For more details see the thread in the Coin3d forum
 * https://www.coin3d.org/pipermail/coin-discuss/2004-May/004346.html.
 * This means that \c SoSwitch must be listed after \c SoGroup and \c SoauracadSelection after
 * \c SoSeparator because both classes inherits the others.
 */
void SoauracadDocumentObjectAction::initClass()
{
    SO_ACTION_INIT_CLASS(SoauracadDocumentObjectAction, SoAction);

    SO_ENABLE(SoauracadDocumentObjectAction, SoSwitchElement);

    SO_ACTION_ADD_METHOD(SoNode, nullAction);

    SO_ENABLE(SoauracadDocumentObjectAction, SoModelMatrixElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoShapeStyleElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoComplexityElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoComplexityTypeElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoCoordinateElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoFontNameElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoFontSizeElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoProfileCoordinateElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoProfileElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoSwitchElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoUnitsElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoViewVolumeElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoViewingMatrixElement);
    SO_ENABLE(SoauracadDocumentObjectAction, SoViewportRegionElement);

    SO_ACTION_ADD_METHOD(SoCallback, callDoAction);
    SO_ACTION_ADD_METHOD(SoComplexity, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate4, callDoAction);
    SO_ACTION_ADD_METHOD(SoFont, callDoAction);
    SO_ACTION_ADD_METHOD(SoGroup, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfile, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate2, callDoAction);
    SO_ACTION_ADD_METHOD(SoProfileCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoTransformation, callDoAction);
    SO_ACTION_ADD_METHOD(SoSwitch, callDoAction);

    SO_ACTION_ADD_METHOD(SoSeparator, callDoAction);
    SO_ACTION_ADD_METHOD(SoauracadSelection, callDoAction);
}

void SoauracadDocumentObjectAction::finish()
{
    atexit_cleanup();
}

SoauracadDocumentObjectAction::SoauracadDocumentObjectAction()
{
    SO_ACTION_CONSTRUCTOR(SoauracadDocumentObjectAction);
}

SoauracadDocumentObjectAction::~SoauracadDocumentObjectAction() = default;

void SoauracadDocumentObjectAction::beginTraversal(SoNode* node)
{
    traverse(node);
}

void SoauracadDocumentObjectAction::callDoAction(SoAction* action, SoNode* node)
{
    node->doAction(action);
}

void SoauracadDocumentObjectAction::setHandled()
{
    this->_handled = true;
}

SbBool SoauracadDocumentObjectAction::isHandled() const
{
    return this->_handled;
}

// ---------------------------------------------------------------

SO_ACTION_SOURCE(SoGLSelectAction)

/**
 * The order of the defined SO_ACTION_ADD_METHOD statements is very important. First the base
 * classes and afterwards subclasses of them must be listed, otherwise the registered methods
 * of subclasses will be overridden. For more details see the thread in the Coin3d forum
 * https://www.coin3d.org/pipermail/coin-discuss/2004-May/004346.html.
 * This means that \c SoSwitch must be listed after \c SoGroup and \c SoauracadSelection after
 * \c SoSeparator because both classes inherits the others.
 */
void SoGLSelectAction::initClass()
{
    SO_ACTION_INIT_CLASS(SoGLSelectAction, SoAction);

    SO_ENABLE(SoGLSelectAction, SoSwitchElement);

    SO_ACTION_ADD_METHOD(SoNode, nullAction);

    SO_ENABLE(SoGLSelectAction, SoModelMatrixElement);
    SO_ENABLE(SoGLSelectAction, SoProjectionMatrixElement);
    SO_ENABLE(SoGLSelectAction, SoCoordinateElement);
    SO_ENABLE(SoGLSelectAction, SoViewVolumeElement);
    SO_ENABLE(SoGLSelectAction, SoViewingMatrixElement);
    SO_ENABLE(SoGLSelectAction, SoViewportRegionElement);

    SO_ACTION_ADD_METHOD(SoCamera, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate4, callDoAction);
    SO_ACTION_ADD_METHOD(SoGroup, callDoAction);
    SO_ACTION_ADD_METHOD(SoSwitch, callDoAction);
    SO_ACTION_ADD_METHOD(SoShape, callDoAction);
    SO_ACTION_ADD_METHOD(SoIndexedFaceSet, callDoAction);

    SO_ACTION_ADD_METHOD(SoSeparator, callDoAction);
    SO_ACTION_ADD_METHOD(SoauracadSelection, callDoAction);
}

SoGLSelectAction::SoGLSelectAction(const SbViewportRegion& region, const SbViewportRegion& select)
    : vpregion(region)
    , vpselect(select)
{
    SO_ACTION_CONSTRUCTOR(SoGLSelectAction);
}

SoGLSelectAction::~SoGLSelectAction() = default;

const SbViewportRegion& SoGLSelectAction::getViewportRegion() const
{
    return this->vpselect;
}

void SoGLSelectAction::beginTraversal(SoNode* node)
{
    SoViewportRegionElement::set(this->getState(), this->vpregion);
    traverse(node);
}

void SoGLSelectAction::callDoAction(SoAction* action, SoNode* node)
{
    node->doAction(action);
}

void SoGLSelectAction::setHandled()
{
    this->_handled = true;
}

SbBool SoGLSelectAction::isHandled() const
{
    return this->_handled;
}

// ---------------------------------------------------------------

SO_ACTION_SOURCE(SoVisibleFaceAction)

/**
 * The order of the defined SO_ACTION_ADD_METHOD statements is very important. First the base
 * classes and afterwards subclasses of them must be listed, otherwise the registered methods
 * of subclasses will be overridden. For more details see the thread in the Coin3d forum
 * https://www.coin3d.org/pipermail/coin-discuss/2004-May/004346.html.
 * This means that \c SoSwitch must be listed after \c SoGroup and \c SoauracadSelection after
 * \c SoSeparator because both classes inherits the others.
 */
void SoVisibleFaceAction::initClass()
{
    SO_ACTION_INIT_CLASS(SoVisibleFaceAction, SoAction);

    SO_ENABLE(SoVisibleFaceAction, SoSwitchElement);

    SO_ACTION_ADD_METHOD(SoNode, nullAction);

    SO_ENABLE(SoVisibleFaceAction, SoModelMatrixElement);
    SO_ENABLE(SoVisibleFaceAction, SoProjectionMatrixElement);
    SO_ENABLE(SoVisibleFaceAction, SoCoordinateElement);
    SO_ENABLE(SoVisibleFaceAction, SoViewVolumeElement);
    SO_ENABLE(SoVisibleFaceAction, SoViewingMatrixElement);
    SO_ENABLE(SoVisibleFaceAction, SoViewportRegionElement);


    SO_ACTION_ADD_METHOD(SoCamera, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate4, callDoAction);
    SO_ACTION_ADD_METHOD(SoGroup, callDoAction);
    SO_ACTION_ADD_METHOD(SoSwitch, callDoAction);
    SO_ACTION_ADD_METHOD(SoShape, callDoAction);
    SO_ACTION_ADD_METHOD(SoIndexedFaceSet, callDoAction);

    SO_ACTION_ADD_METHOD(SoSeparator, callDoAction);
    SO_ACTION_ADD_METHOD(SoauracadSelection, callDoAction);
}

SoVisibleFaceAction::SoVisibleFaceAction()
{
    SO_ACTION_CONSTRUCTOR(SoVisibleFaceAction);
}

SoVisibleFaceAction::~SoVisibleFaceAction() = default;

void SoVisibleFaceAction::beginTraversal(SoNode* node)
{
    traverse(node);
}

void SoVisibleFaceAction::callDoAction(SoAction* action, SoNode* node)
{
    node->doAction(action);
}

void SoVisibleFaceAction::setHandled()
{
    this->_handled = true;
}

SbBool SoVisibleFaceAction::isHandled() const
{
    return this->_handled;
}

// ---------------------------------------------------------------


SO_ACTION_SOURCE(SoUpdateVBOAction)

/**
 * The order of the defined SO_ACTION_ADD_METHOD statements is very important. First the base
 * classes and afterwards subclasses of them must be listed, otherwise the registered methods
 * of subclasses will be overridden. For more details see the thread in the Coin3d forum
 * https://www.coin3d.org/pipermail/coin-discuss/2004-May/004346.html.
 * This means that \c SoSwitch must be listed after \c SoGroup and \c SoauracadSelection after
 * \c SoSeparator because both classes inherits the others.
 */
void SoUpdateVBOAction::initClass()
{
    SO_ACTION_INIT_CLASS(SoUpdateVBOAction, SoAction);

    SO_ENABLE(SoUpdateVBOAction, SoSwitchElement);

    SO_ACTION_ADD_METHOD(SoNode, nullAction);

    SO_ENABLE(SoUpdateVBOAction, SoModelMatrixElement);
    SO_ENABLE(SoUpdateVBOAction, SoProjectionMatrixElement);
    SO_ENABLE(SoUpdateVBOAction, SoCoordinateElement);
    SO_ENABLE(SoUpdateVBOAction, SoViewVolumeElement);
    SO_ENABLE(SoUpdateVBOAction, SoViewingMatrixElement);
    SO_ENABLE(SoUpdateVBOAction, SoViewportRegionElement);


    SO_ACTION_ADD_METHOD(SoCamera, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate3, callDoAction);
    SO_ACTION_ADD_METHOD(SoCoordinate4, callDoAction);
    SO_ACTION_ADD_METHOD(SoGroup, callDoAction);
    SO_ACTION_ADD_METHOD(SoSwitch, callDoAction);
    SO_ACTION_ADD_METHOD(SoShape, callDoAction);
    SO_ACTION_ADD_METHOD(SoIndexedFaceSet, callDoAction);

    SO_ACTION_ADD_METHOD(SoSeparator, callDoAction);
    SO_ACTION_ADD_METHOD(SoauracadSelection, callDoAction);
}

SoUpdateVBOAction::SoUpdateVBOAction()
{
    SO_ACTION_CONSTRUCTOR(SoUpdateVBOAction);
}

SoUpdateVBOAction::~SoUpdateVBOAction() = default;

void SoUpdateVBOAction::finish()
{
    atexit_cleanup();
}

void SoUpdateVBOAction::beginTraversal(SoNode* node)
{
    traverse(node);
}

void SoUpdateVBOAction::callDoAction(SoAction* action, SoNode* node)
{
    node->doAction(action);
}

// ---------------------------------------------------------------

namespace Gui
{
class SoBoxSelectionRenderActionP
{
public:
    SoBoxSelectionRenderActionP(SoBoxSelectionRenderAction* master)
        : master(master)
    {}

    SoBoxSelectionRenderAction* master;
    SoSearchAction* searchaction {nullptr};
    SoSearchAction* selectsearch {nullptr};
    SoSearchAction* camerasearch {nullptr};
    SoGetBoundingBoxAction* bboxaction {nullptr};
    SoBaseColor* basecolor {nullptr};
    SoTempPath* postprocpath {nullptr};
    SoPath* highlightPath {nullptr};
    SoSeparator* localRoot {nullptr};
    SoMatrixTransform* xform {nullptr};
    SoCube* cube {nullptr};
    SoDrawStyle* drawstyle {nullptr};
    SoColorPacker colorpacker;

    void initBoxGraph();
    void updateBbox(const SoPath* path);
};

}  // namespace Gui

#undef PRIVATE
#define PRIVATE(p) ((p)->pimpl)
#undef PUBLIC
#define PUBLIC(p) ((p)->master)

// used to initialize the internal storage class with variables
void SoBoxSelectionRenderActionP::initBoxGraph()
{
    this->localRoot = new SoSeparator;
    this->localRoot->ref();
    this->localRoot->renderCaching = SoSeparator::OFF;
    this->localRoot->boundingBoxCaching = SoSeparator::OFF;

    this->xform = new SoMatrixTransform;
    this->cube = new SoCube;

    this->drawstyle = new SoDrawStyle;
    this->drawstyle->style = SoDrawStyleElement::LINES;
    this->basecolor = new SoBaseColor;

    auto lightmodel = new SoLightModel;
    lightmodel->model = SoLightModel::BASE_COLOR;

    auto complexity = new SoComplexity;
    complexity->textureQuality = 0.0f;
    complexity->type = SoComplexityTypeElement::BOUNDING_BOX;

    this->localRoot->addChild(this->drawstyle);
    this->localRoot->addChild(this->basecolor);

    this->localRoot->addChild(lightmodel);
    this->localRoot->addChild(complexity);

    this->localRoot->addChild(this->xform);
    this->localRoot->addChild(this->cube);
}


// used to render shape and non-shape nodes (usually SoGroup or SoSeparator).
void SoBoxSelectionRenderActionP::updateBbox(const SoPath* path)
{
    if (!this->camerasearch) {
        this->camerasearch = new SoSearchAction;
    }

    // find camera used to render node
    this->camerasearch->setFind(SoSearchAction::TYPE);
    this->camerasearch->setInterest(SoSearchAction::LAST);
    this->camerasearch->setType(SoCamera::getClassTypeId());
    this->camerasearch->apply(const_cast<SoPath*>(path));

    if (!this->camerasearch->getPath()) {
        // if there is no camera there is no point rendering the bbox
        return;
    }
    this->localRoot->insertChild(this->camerasearch->getPath()->getTail(), 0);
    this->camerasearch->reset();

    if (!this->bboxaction) {
        this->bboxaction = new SoGetBoundingBoxAction(SbViewportRegion(100, 100));
    }
    this->bboxaction->setViewportRegion(PUBLIC(this)->getViewportRegion());
    this->bboxaction->apply(const_cast<SoPath*>(path));

    SbXfBox3f& box = this->bboxaction->getXfBoundingBox();

    if (!box.isEmpty()) {
        // set cube size
        float x, y, z;
        box.getSize(x, y, z);
        this->cube->width = x;
        this->cube->height = y;
        this->cube->depth = z;

        SbMatrix transform = box.getTransform();  // clazy:exclude=rule-of-two-soft

        // get center (in the local bbox coordinate system)
        SbVec3f center = box.SbBox3f::getCenter();

        // if center != (0,0,0), move the cube
        if (center != SbVec3f(0.0f, 0.0f, 0.0f)) {
            SbMatrix t;
            t.setTranslate(center);
            transform.multLeft(t);
        }
        this->xform->matrix = transform;

        PUBLIC(this)->SoGLRenderAction::apply(this->localRoot);
    }
    // remove camera
    this->localRoot->removeChild(0);
}

SO_ACTION_SOURCE(SoBoxSelectionRenderAction)

// Overridden from parent class.
void SoBoxSelectionRenderAction::initClass()
{
    SO_ACTION_INIT_CLASS(SoBoxSelectionRenderAction, SoGLRenderAction);
}

SoBoxSelectionRenderAction::SoBoxSelectionRenderAction()
    : inherited(SbViewportRegion())
{
    this->constructorCommon();
}

SoBoxSelectionRenderAction::SoBoxSelectionRenderAction(const SbViewportRegion& viewportregion)
    : inherited(viewportregion)
{
    this->constructorCommon();
}

//
// private. called by both constructors
//
void SoBoxSelectionRenderAction::constructorCommon()
{
    SO_ACTION_CONSTRUCTOR(SoBoxSelectionRenderAction);

    PRIVATE(this) = new SoBoxSelectionRenderActionP(this);

    // Initialize local variables
    PRIVATE(this)->initBoxGraph();

    this->hlVisible = false;

    PRIVATE(this)->basecolor->rgb.setValue(1.0f, 0.0f, 0.0f);
    PRIVATE(this)->drawstyle->linePattern = 0xffff;
    PRIVATE(this)->drawstyle->lineWidth = 1.0f;
    PRIVATE(this)->searchaction = nullptr;
    PRIVATE(this)->selectsearch = nullptr;
    PRIVATE(this)->camerasearch = nullptr;
    PRIVATE(this)->bboxaction = nullptr;

    // SoBase-derived objects should be dynamically allocated.
    PRIVATE(this)->postprocpath = new SoTempPath(32);
    PRIVATE(this)->postprocpath->ref();
    PRIVATE(this)->highlightPath = nullptr;
}

SoBoxSelectionRenderAction::~SoBoxSelectionRenderAction()
{
    // clear highlighting node
    if (PRIVATE(this)->highlightPath) {
        PRIVATE(this)->highlightPath->unref();
    }
    PRIVATE(this)->postprocpath->unref();
    PRIVATE(this)->localRoot->unref();

    delete PRIVATE(this)->searchaction;
    delete PRIVATE(this)->selectsearch;
    delete PRIVATE(this)->camerasearch;
    delete PRIVATE(this)->bboxaction;
    delete PRIVATE(this);
}

void SoBoxSelectionRenderAction::apply(SoNode* node)
{
    SoGLRenderAction::apply(node);
    if (this->hlVisible) {
        if (!PRIVATE(this)->searchaction) {
            PRIVATE(this)->searchaction = new SoSearchAction;
        }
        PRIVATE(this)->searchaction->setType(SoauracadSelection::getClassTypeId());
        PRIVATE(this)->searchaction->setInterest(SoSearchAction::ALL);
        PRIVATE(this)->searchaction->apply(node);
        const SoPathList& pathlist = PRIVATE(this)->searchaction->getPaths();
        if (pathlist.getLength() > 0) {
            for (int i = 0; i < pathlist.getLength(); i++) {
                SoPath* path = pathlist[i];
                assert(path);
                auto selection = static_cast<SoauracadSelection*>(path->getTail());
                assert(selection->getTypeId().isDerivedFrom(SoauracadSelection::getClassTypeId()));
                if (selection->selected.getValue()
                    && selection->style.getValue() == SoauracadSelection::BOX) {
                    PRIVATE(this)->basecolor->rgb.setValue(selection->colorSelection.getValue());
                    if (!PRIVATE(this)->selectsearch) {
                        PRIVATE(this)->selectsearch = new SoSearchAction;
                    }
                    PRIVATE(this)->selectsearch->setType(SoShape::getClassTypeId());
                    PRIVATE(this)->selectsearch->setInterest(SoSearchAction::FIRST);
                    PRIVATE(this)->selectsearch->apply(selection);
                    SoPath* shapepath = PRIVATE(this)->selectsearch->getPath();
                    if (shapepath) {
                        SoPathList list;
                        list.append(shapepath);
                        this->drawBoxes(path, &list);
                    }
                    PRIVATE(this)->selectsearch->reset();
                }
                else if (
                    selection->isHighlighted()
                    && selection->selected.getValue() == SoauracadSelection::NOTSELECTED
                    && selection->style.getValue() == SoauracadSelection::BOX
                ) {
                    PRIVATE(this)->basecolor->rgb.setValue(selection->colorHighlight.getValue());

                    if (!PRIVATE(this)->selectsearch) {
                        PRIVATE(this)->selectsearch = new SoSearchAction;
                    }
                    PRIVATE(this)->selectsearch->setType(SoShape::getClassTypeId());
                    PRIVATE(this)->selectsearch->setInterest(SoSearchAction::FIRST);
                    PRIVATE(this)->selectsearch->apply(selection);
                    SoPath* shapepath = PRIVATE(this)->selectsearch->getPath();
                    if (shapepath) {
                        SoPathList list;
                        list.append(shapepath);
                        // clear old highlighting node if still active
                        if (PRIVATE(this)->highlightPath) {
                            PRIVATE(this)->highlightPath->unref();
                        }
                        PRIVATE(this)->highlightPath = path;
                        PRIVATE(this)->highlightPath->ref();
                        this->drawBoxes(path, &list);
                    }
                    PRIVATE(this)->selectsearch->reset();
                }
            }
        }
        PRIVATE(this)->searchaction->reset();
    }
}

void SoBoxSelectionRenderAction::apply(SoPath* path)
{
    SoGLRenderAction::apply(path);
    SoNode* node = path->getTail();
    if (node && node->getTypeId() == SoauracadSelection::getClassTypeId()) {
        auto selection = static_cast<SoauracadSelection*>(node);

        // This happens when dehighlighting the current shape
        if (PRIVATE(this)->highlightPath == path) {
            PRIVATE(this)->highlightPath->unref();
            PRIVATE(this)->highlightPath = nullptr;
            // FIXME: Doing a redraw to remove the shown bounding box causes
            // some problems when moving the mouse from one shape to another
            // because this will destroy the box immediately
            selection->touch();  // force a redraw when dehighlighting
        }
        else if (
            selection->isHighlighted() && selection->selected.getValue() == SoauracadSelection::NOTSELECTED
            && selection->style.getValue() == SoauracadSelection::BOX
        ) {
            PRIVATE(this)->basecolor->rgb.setValue(selection->colorHighlight.getValue());

            if (!PRIVATE(this)->selectsearch) {
                PRIVATE(this)->selectsearch = new SoSearchAction;
            }
            PRIVATE(this)->selectsearch->setType(SoShape::getClassTypeId());
            PRIVATE(this)->selectsearch->setInterest(SoSearchAction::FIRST);
            PRIVATE(this)->selectsearch->apply(selection);
            SoPath* shapepath = PRIVATE(this)->selectsearch->getPath();
            if (shapepath) {
                SoPathList list;
                list.append(shapepath);
                // clear old highlighting node if still active
                if (PRIVATE(this)->highlightPath) {
                    PRIVATE(this)->highlightPath->unref();
                }
                PRIVATE(this)->highlightPath = path;
                PRIVATE(this)->highlightPath->ref();
                this->drawBoxes(path, &list);
            }
            PRIVATE(this)->selectsearch->reset();
        }
    }
}

void SoBoxSelectionRenderAction::apply(const SoPathList& pathlist, SbBool obeysrules)
{
    SoGLRenderAction::apply(pathlist, obeysrules);
}

void SoBoxSelectionRenderAction::setColor(const SbColor& color)
{
    PRIVATE(this)->basecolor->rgb = color;
}

const SbColor& SoBoxSelectionRenderAction::getColor()
{
    return PRIVATE(this)->basecolor->rgb[0];
}

void SoBoxSelectionRenderAction::setLinePattern(unsigned short pattern)
{
    PRIVATE(this)->drawstyle->linePattern = pattern;
}

unsigned short SoBoxSelectionRenderAction::getLinePattern() const
{
    return PRIVATE(this)->drawstyle->linePattern.getValue();
}

void SoBoxSelectionRenderAction::setLineWidth(const float width)
{
    PRIVATE(this)->drawstyle->lineWidth = width;
}

float SoBoxSelectionRenderAction::getLineWidth() const
{
    return PRIVATE(this)->drawstyle->lineWidth.getValue();
}

void SoBoxSelectionRenderAction::drawBoxes(SoPath* pathtothis, const SoPathList* pathlist)
{
    int i;
    int thispos = Gui::toFullPath(pathtothis)->getLength() - 1;
    assert(thispos >= 0);
    PRIVATE(this)->postprocpath->truncate(0);  // reset

    for (i = 0; i < thispos; i++) {
        PRIVATE(this)->postprocpath->append(pathtothis->getNode(i));
    }

    // we need to disable accumulation buffer antialiasing while
    // rendering selected objects
    int oldnumpasses = this->getNumPasses();
    this->setNumPasses(1);

    SoState* thestate = this->getState();
    thestate->push();

    for (i = 0; i < pathlist->getLength(); i++) {
        auto path = Gui::toFullPath((*pathlist)[i]);

        for (int j = 0; j < path->getLength(); j++) {
            PRIVATE(this)->postprocpath->append(path->getNode(j));
        }

        // Previously SoGLRenderAction was used to draw the bounding boxes
        // of shapes in selection paths, by overriding renderstyle state
        // elements to lines drawstyle and simply doing:
        //
        //   SoGLRenderAction::apply(PRIVATE(this)->postprocpath); // Bug
        //
        // This could have the unwanted side effect of rendering
        // non-selected shapes, as they could be part of the path (due to
        // being placed below SoGroup nodes (instead of SoSeparator
        // nodes)) up to the selected shape.
        //
        //
        // A better approach turned out to be to soup up and draw only the
        // bounding boxes of the selected shapes:
        PRIVATE(this)->updateBbox(PRIVATE(this)->postprocpath);

        // Remove temporary path from path buffer
        PRIVATE(this)->postprocpath->truncate(thispos);
    }

    this->setNumPasses(oldnumpasses);
    thestate->pop();
}


#undef PRIVATE
#undef PUBLIC
