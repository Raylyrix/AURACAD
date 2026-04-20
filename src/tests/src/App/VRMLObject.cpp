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

#include <gtest/gtest.h>
#include "gmock/gmock.h"

#include <App/Application.h>
#include <App/Document.h>
#include <App/VRMLObject.h>
#include <Base/FileInfo.h>
#include <src/App/InitApplication.h>

// NOLINTBEGIN

class VRMLObjectTest: public ::testing::Test
{
protected:
    static void SetUpTestSuite()
    {
        tests::initApplication();
    }

    void SetUp() override
    {
        document = App::GetApplication().openDocument(fileName().c_str());
    }

    void TearDown() override
    {
        if (document) {
            App::GetApplication().closeDocument(document->getName());
        }
    }

    std::string fileName() const
    {
        std::string resDir(DATADIR);
        resDir.append("/tests/TestVRMLTextures.auracadStd");
        return resDir;
    }

    App::Document* getDocument() const
    {
        return document;
    }

private:
    App::Document* document {};
};

TEST_F(VRMLObjectTest, loadVRMLWithTextures)
{
    App::Document* doc = getDocument();
    ASSERT_TRUE(doc);

    auto vrml = dynamic_cast<App::VRMLObject*>(doc->getActiveObject());
    ASSERT_TRUE(vrml);

    auto res = vrml->Resources.getValues();
    EXPECT_EQ(res.size(), 6);
    EXPECT_EQ(res[0], std::string("AuraCAD/AuraCAD1.png"));
    EXPECT_EQ(res[1], std::string("AuraCAD/AuraCAD2.png"));
    EXPECT_EQ(res[2], std::string("AuraCAD/AuraCAD3.png"));
    EXPECT_EQ(res[3], std::string("AuraCAD/AuraCAD4.png"));
    EXPECT_EQ(res[4], std::string("AuraCAD/AuraCAD5.png"));
    EXPECT_EQ(res[5], std::string("AuraCAD/AuraCAD6.png"));

    auto url = vrml->Urls.getValues();
    EXPECT_EQ(url.size(), 6);
    for (const auto& it : url) {
        Base::FileInfo fi(it);
        EXPECT_TRUE(fi.isFile());
        EXPECT_TRUE(fi.exists());
    }
}

// NOLINTEND
