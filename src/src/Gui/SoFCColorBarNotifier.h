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

#pragma once

#include <Base/Parameter.h>
#include <set>

namespace Gui
{

class SoauracadColorBarBase;

class GuiExport SoauracadColorBarNotifier: public ParameterGrp::ObserverType  // NOLINT
{
public:
    static SoauracadColorBarNotifier& instance();
    void attach(SoauracadColorBarBase* bar);
    void detach(SoauracadColorBarBase* bar);
    void OnChange(ParameterGrp::SubjectType& caller, ParameterGrp::MessageType reason) override;

private:
    SoauracadColorBarNotifier();
    ~SoauracadColorBarNotifier() override = default;

    AuraCAD_DISABLE_COPY_MOVE(SoauracadColorBarNotifier)

private:
    std::set<SoauracadColorBarBase*> bars;
    ParameterGrp::handle group;
};

}  // namespace Gui
