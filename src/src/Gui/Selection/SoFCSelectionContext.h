// SPDX-License-Identifier: LGPL-2.1-or-later
/****************************************************************************
 *   Copyright (c) 2018 Zheng Lei (realthunder) <realthunder.dev@gmail.com> *
 *                                                                          *
 *   This file is part of the AuraCAD CAx development system.               *
 *                                                                          *
 *   This library is free software; you can redistribute it and/or          *
 *   modify it under the terms of the GNU Library General Public            *
 *   License as published by the Free Software Foundation; either           *
 *   version 2 of the License, or (at your option) any later version.       *
 *                                                                          *
 *   This library  is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
 *   GNU Library General Public License for more details.                   *
 *                                                                          *
 *   You should have received a copy of the GNU Library General Public      *
 *   License along with this library; see the file COPYING.LIB. If not,     *
 *   write to the Free Software Foundation, Inc., 59 Temple Place,          *
 *   Suite 330, Boston, MA  02111-1307, USA                                 *
 *                                                                          *
 ****************************************************************************/

#pragma once

#include <limits>
#include <map>
#include <memory>
#include <set>
#include <vector>
#include <Inventor/SbColor.h>

#include <App/Material.h>

class SoState;

namespace Gui
{

class SoauracadSelectionRoot;
struct SoauracadSelectionContextBase;
using SoauracadSelectionContextBasePtr = std::shared_ptr<SoauracadSelectionContextBase>;

struct GuiExport SoauracadSelectionContextBase
{
    virtual ~SoauracadSelectionContextBase() = default;
    using MergeFunc = int(
        int status,
        SoauracadSelectionContextBasePtr& output,
        SoauracadSelectionContextBasePtr input,
        SoNode* node
    );
};

struct SoauracadSelectionContext;
using SoauracadSelectionContextPtr = std::shared_ptr<SoauracadSelectionContext>;

struct GuiExport SoauracadSelectionContext: SoauracadSelectionContextBase
{
    int highlightIndex = -1;
    std::set<int> selectionIndex;
    SbColor selectionColor;
    SbColor highlightColor;
    std::shared_ptr<int> counter;

    ~SoauracadSelectionContext() override;

    bool isSelected() const
    {
        return !selectionIndex.empty();
    }

    void selectAll()
    {
        selectionIndex.clear();
        selectionIndex.insert(-1);
    }

    bool isSelectAll() const
    {
        return !selectionIndex.empty() && *selectionIndex.begin() < 0;
    }

    bool isHighlighted() const
    {
        return highlightIndex >= 0;
    }

    bool isHighlightAll() const
    {
        return highlightIndex == std::numeric_limits<int>::max()
            && (selectionIndex.empty() || isSelectAll());
    }

    void highlightAll()
    {
        highlightIndex = std::numeric_limits<int>::max();
    }

    void removeHighlight()
    {
        highlightIndex = -1;
    }

    bool removeIndex(int index);
    bool checkGlobal(SoauracadSelectionContextPtr ctx);

    virtual SoauracadSelectionContextBasePtr copy()
    {
        return std::make_shared<SoauracadSelectionContext>(*this);
    }

    static MergeFunc merge;
};

struct SoauracadSelectionContextEx;
using SoauracadSelectionContextExPtr = std::shared_ptr<SoauracadSelectionContextEx>;

struct GuiExport SoauracadSelectionContextEx: SoauracadSelectionContext
{
    std::map<int, Base::Color> colors;
    float trans0 = 0.0;

    bool setColors(const std::map<std::string, Base::Color>& colors, const std::string& element);
    uint32_t packColor(const Base::Color& c, bool& hasTransparency);
    bool applyColor(int idx, std::vector<uint32_t>& packedColors, bool& hasTransparency);
    bool isSingleColor(uint32_t& color, bool& hasTransparency);

    SoauracadSelectionContextBasePtr copy() override
    {
        return std::make_shared<SoauracadSelectionContextEx>(*this);
    }

    static MergeFunc merge;
};

class SoHighlightElementAction;
class SoSelectionElementAction;

class GuiExport SoauracadSelectionCounter
{
public:
    SoauracadSelectionCounter();
    virtual ~SoauracadSelectionCounter();
    bool checkRenderCache(SoState* state);
    void checkAction(SoHighlightElementAction* hlaction);
    void checkAction(SoSelectionElementAction* selaction, SoauracadSelectionContextPtr ctx);

protected:
    std::shared_ptr<int> counter;
    bool hasSelection {false};
    bool hasPreselection {false};
    static int cachingMode;
};

}  // namespace Gui
