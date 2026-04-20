// SPDX-License-Identifier: LGPL-2.1-or-later
/****************************************************************************
 *                                                                          *
 *   Copyright (c) 2026 The AuraCAD Project Association AISBL               *
 *                                                                          *
 *   This file is part of AuraCAD.                                          *
 *                                                                          *
 *   AuraCAD is free software: you can redistribute it and/or modify it     *
 *   under the terms of the GNU Lesser General Public License as            *
 *   published by the Free Software Foundation, either version 2.1 of the   *
 *   License, or (at your option) any later version.                        *
 *                                                                          *
 *   AuraCAD is distributed in the hope that it will be useful, but         *
 *   WITHOUT ANY WARRANTY; without even the implied warranty of             *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU       *
 *   Lesser General Public License for more details.                        *
 *                                                                          *
 *   You should have received a copy of the GNU Lesser General Public       *
 *   License along with AuraCAD. If not, see                                *
 *   <https://www.gnu.org/licenses/>.                                       *
 *                                                                          *
 ***************************************************************************/

#pragma once

#include <QObject>
#include <QRunnable>
#include <QString>

#include "DisplayedFilesModel.h"

namespace Start
{

class auracadstdInfoSourceSignals: public QObject
{
    Q_OBJECT
public:
Q_SIGNALS:
    void infoAvailable(const QString& filePath, const FileStats& stats, const QByteArray& thumbnail);
};

class auracadstdInfoSource: public QRunnable
{
    Q_DISABLE_COPY_MOVE(auracadstdInfoSource)

public:
    using Signals = auracadstdInfoSourceSignals;

    explicit auracadstdInfoSource(QString filePath);
    ~auracadstdInfoSource() override = default;

    void run() override;

    const Signals* signals() const
    {
        return &_signals;
    }

private:
    // Having a signal QObject as part of the QRunnable ensures signal connections
    // are properly cleaned up when the QRunnable gets destroyed as it finishes its work.
    Signals _signals;
    QString _filePath;
};

}  // namespace Start
