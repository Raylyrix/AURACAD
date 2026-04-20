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

#pragma once

#include <Inventor/SbColor.h>
#include <Inventor/actions/SoGLRenderAction.h>
#include <Inventor/fields/SoSauracadolor.h>
#include <Inventor/fields/SoSFString.h>
#include <vector>
#include <auracadGlobal.h>

class SoSFString;
class SoSauracadolor;

namespace Gui
{

class SelectionChanges;

/**
 * The SoauracadPreselectionAction class is used to inform an SoauracadSelection node
 * whether an object gets preselected.
 * @author JÃ¼rgen Riegel
 */
class GuiExport SoauracadPreselectionAction: public SoAction
{
    SO_ACTION_HEADER(SoauracadPreselectionAction);

public:
    SoauracadPreselectionAction(const SelectionChanges& SelCh);
    ~SoauracadPreselectionAction() override;

    static void initClass();
    static void finish();

    const SelectionChanges& SelChange;

protected:
    void beginTraversal(SoNode* node) override;

private:
    static void callDoAction(SoAction* action, SoNode* node);
};

/**
 * The SoauracadSelectionAction class is used to inform an SoauracadSelection node
 * whether an object gets selected.
 * @author JÃ¼rgen Riegel
 */
class GuiExport SoauracadSelectionAction: public SoAction
{
    SO_ACTION_HEADER(SoauracadSelectionAction);

public:
    SoauracadSelectionAction(const SelectionChanges& SelCh);
    ~SoauracadSelectionAction() override;

    static void initClass();
    static void finish();

    const SelectionChanges& SelChange;

protected:
    void beginTraversal(SoNode* node) override;

private:
    static void callDoAction(SoAction* action, SoNode* node);
};

/**
 * The SoauracadEnableSelectionAction class is used to inform an SoauracadSelection node
 * whether selection is enabled or disabled.
 * @author Werner Mayer
 */
class GuiExport SoauracadEnableSelectionAction: public SoAction
{
    SO_ACTION_HEADER(SoauracadEnableSelectionAction);

public:
    SoauracadEnableSelectionAction(const SbBool& sel);
    ~SoauracadEnableSelectionAction() override;

    SbBool enabled;

    static void initClass();
    static void finish();

protected:
    void beginTraversal(SoNode* node) override;

private:
    static void callDoAction(SoAction* action, SoNode* node);
};

/**
 * The SoauracadEnablePreselectionAction class is used to inform an SoauracadSelection node
 * whether preselection is enabled or disabled.
 * @author Werner Mayer
 */
class GuiExport SoauracadEnablePreselectionAction: public SoAction
{
    SO_ACTION_HEADER(SoauracadEnablePreselectionAction);

public:
    SoauracadEnablePreselectionAction(const SbBool& sel);
    ~SoauracadEnablePreselectionAction() override;

    SbBool enabled;

    static void initClass();
    static void finish();

protected:
    void beginTraversal(SoNode* node) override;

private:
    static void callDoAction(SoAction* action, SoNode* node);
};

/**
 * The SoauracadSelectionColorAction class is used to inform an SoauracadSelection node
 * which selection color is used.
 * @author Werner Mayer
 */
class GuiExport SoauracadSelectionColorAction: public SoAction
{
    SO_ACTION_HEADER(SoauracadSelectionColorAction);

public:
    SoauracadSelectionColorAction(const SoSauracadolor& col);
    ~SoauracadSelectionColorAction() override;

    SoSauracadolor selectionColor;

    static void initClass();
    static void finish();

protected:
    void beginTraversal(SoNode* node) override;

private:
    static void callDoAction(SoAction* action, SoNode* node);
};

/**
 * The SoauracadHighlightColorAction class is used to inform an SoauracadSelection node
 * which highlight color is used.
 * @author Werner Mayer
 */
class GuiExport SoauracadHighlightColorAction: public SoAction
{
    SO_ACTION_HEADER(SoauracadHighlightColorAction);

public:
    SoauracadHighlightColorAction(const SoSauracadolor& col);
    ~SoauracadHighlightColorAction() override;

    SoSauracadolor highlightColor;

    static void initClass();
    static void finish();

protected:
    void beginTraversal(SoNode* node) override;

private:
    static void callDoAction(SoAction* action, SoNode* node);
};

/**
 * The SoauracadDocumentAction class is used to inform an SoauracadSelection node
 * when a document has been renamed.
 * @author Werner Mayer
 */
class GuiExport SoauracadDocumentAction: public SoAction
{
    SO_ACTION_HEADER(SoauracadDocumentAction);

public:
    SoauracadDocumentAction(const SoSFString& docName);
    ~SoauracadDocumentAction() override;

    SoSFString documentName;

    static void initClass();
    static void finish();

protected:
    void beginTraversal(SoNode* node) override;

private:
    static void callDoAction(SoAction* action, SoNode* node);
};

/**
 * The SoauracadDocumentObjectAction class is used to get the name of the document,
 * object and component at a certain position of an SoauracadSelection node.
 * @author Werner Mayer
 */
class GuiExport SoauracadDocumentObjectAction: public SoAction
{
    SO_ACTION_HEADER(SoauracadDocumentObjectAction);

public:
    SoauracadDocumentObjectAction();
    ~SoauracadDocumentObjectAction() override;

    void setHandled();
    SbBool isHandled() const;

    static void initClass();
    static void finish();

protected:
    void beginTraversal(SoNode* node) override;

private:
    static void callDoAction(SoAction* action, SoNode* node);

public:
    SbString documentName;
    SbString objectName;
    SbString componentName;

private:
    SbBool _handled {false};
};

/**
 * The SoGLSelectAction class is used to get all data under a selected area.
 * @author Werner Mayer
 */
class GuiExport SoGLSelectAction: public SoAction
{
    SO_ACTION_HEADER(SoGLSelectAction);

public:
    SoGLSelectAction(const SbViewportRegion& region, const SbViewportRegion& select);
    ~SoGLSelectAction() override;

    void setHandled();
    SbBool isHandled() const;
    const SbViewportRegion& getViewportRegion() const;

    static void initClass();

protected:
    void beginTraversal(SoNode* node) override;

private:
    static void callDoAction(SoAction* action, SoNode* node);

public:
    std::vector<unsigned long> indices;

private:
    const SbViewportRegion& vpregion;
    const SbViewportRegion& vpselect;
    SbBool _handled {false};
};

/**
 * @author Werner Mayer
 */
class GuiExport SoVisibleFaceAction: public SoAction
{
    SO_ACTION_HEADER(SoVisibleFaceAction);

public:
    SoVisibleFaceAction();
    ~SoVisibleFaceAction() override;

    void setHandled();
    SbBool isHandled() const;

    static void initClass();

protected:
    void beginTraversal(SoNode* node) override;

private:
    static void callDoAction(SoAction* action, SoNode* node);

private:
    SbBool _handled {false};
};

class SoBoxSelectionRenderActionP;
/**
 * The SoBoxSelectionRenderAction class renders the scene with highlighted boxes around selections.
 * @author Werner Mayer
 */
class GuiExport SoBoxSelectionRenderAction: public SoGLRenderAction
{
    using inherited = SoGLRenderAction;

    SO_ACTION_HEADER(SoBoxSelectionRenderAction);

public:
    SoBoxSelectionRenderAction();
    SoBoxSelectionRenderAction(const SbViewportRegion& viewportregion);
    ~SoBoxSelectionRenderAction() override;

    static void initClass();

    void apply(SoNode* node) override;
    void apply(SoPath* path) override;
    void apply(const SoPathList& pathlist, SbBool obeysrules = false) override;
    void setVisible(SbBool b)
    {
        hlVisible = b;
    }
    SbBool isVisible() const
    {
        return hlVisible;
    }
    void setColor(const SbColor& color);
    const SbColor& getColor();
    void setLinePattern(unsigned short pattern);
    unsigned short getLinePattern() const;
    void setLineWidth(const float width);
    float getLineWidth() const;

protected:
    SbBool hlVisible;

private:
    void constructorCommon();
    void drawBoxes(SoPath* pathtothis, const SoPathList* pathlist);

    SoBoxSelectionRenderActionP* pimpl;
};

/**
 * Helper class no notify nodes to update VBO.
 * @author Werner Mayer
 */
class GuiExport SoUpdateVBOAction: public SoAction
{
    SO_ACTION_HEADER(SoUpdateVBOAction);

public:
    SoUpdateVBOAction();
    ~SoUpdateVBOAction() override;

    static void initClass();
    static void finish();

protected:
    void beginTraversal(SoNode* node) override;

private:
    static void callDoAction(SoAction* action, SoNode* node);
};

}  // namespace Gui
