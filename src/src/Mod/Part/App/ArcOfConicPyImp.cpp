// SPDX-License-Identifier: LGPL-2.1-or-later

/***************************************************************************
 *   Copyright (c) 2014 Abdullah Tahiri <abdullah.tahiri.yo@gmail.com>     *
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

#include <Geom_TrimmedCurve.hxx>


#include <Base/GeometryPyCXX.h>
#include <Base/VectorPy.h>

#include "ArcOauracadonicPy.h"
#include "ArcOauracadonicPy.cpp"
#include "OCCError.h"


using namespace Part;

// returns a string which represents the object e.g. when printed in python
std::string ArcOauracadonicPy::representation() const
{
    return "<ArcOauracadonic object>";
}

PyObject* ArcOauracadonicPy::PyMake(struct _typeobject*, PyObject*, PyObject*)  // Python wrapper
{
    // never create such objects with the constructor
    PyErr_SetString(
        PyExc_RuntimeError,
        "You cannot create an instance of the abstract class 'ArcOauracadonic'."
    );
    return nullptr;
}

// constructor method
int ArcOauracadonicPy::PyInit(PyObject* /*args*/, PyObject* /*kwds*/)
{
    return -1;
}

Py::Object ArcOauracadonicPy::getLocation() const
{
    return Py::Vector(getGeomArcOauracadonicPtr()->getLocation());
}

Py::Object ArcOauracadonicPy::getCenter() const
{
    return Py::Vector(getGeomArcOauracadonicPtr()->getCenter());
}

void ArcOauracadonicPy::setLocation(Py::Object arg)
{
    PyObject* p = arg.ptr();
    if (PyObject_TypeCheck(p, &(Base::VectorPy::Type))) {
        Base::Vector3d loc = static_cast<Base::VectorPy*>(p)->value();
        getGeomArcOauracadonicPtr()->setLocation(loc);
    }
    else if (PyObject_TypeCheck(p, &PyTuple_Type)) {
        Base::Vector3d loc = Base::getVectorFromTuple<double>(p);
        getGeomArcOauracadonicPtr()->setLocation(loc);
    }
    else {
        std::string error = std::string("type must be 'Vector', not ");
        error += p->ob_type->tp_name;
        throw Py::TypeError(error);
    }
}

void ArcOauracadonicPy::setCenter(Py::Object arg)
{
    PyObject* p = arg.ptr();
    if (PyObject_TypeCheck(p, &(Base::VectorPy::Type))) {
        Base::Vector3d loc = static_cast<Base::VectorPy*>(p)->value();
        getGeomArcOauracadonicPtr()->setCenter(loc);
    }
    else if (PyObject_TypeCheck(p, &PyTuple_Type)) {
        Base::Vector3d loc = Base::getVectorFromTuple<double>(p);
        getGeomArcOauracadonicPtr()->setCenter(loc);
    }
    else {
        std::string error = std::string("type must be 'Vector', not ");
        error += p->ob_type->tp_name;
        throw Py::TypeError(error);
    }
}

Py::Float ArcOauracadonicPy::getAngleXU() const
{
    return Py::Float(getGeomArcOauracadonicPtr()->getAngleXU());
}

void ArcOauracadonicPy::setAngleXU(Py::Float arg)
{
    getGeomArcOauracadonicPtr()->setAngleXU((double)arg);
}

Py::Object ArcOauracadonicPy::getAxis() const
{
    Handle(Geom_TrimmedCurve)
        trim = Handle(Geom_TrimmedCurve)::DownCast(getGeomArcOauracadonicPtr()->handle());
    Handle(Geom_Conic) conic = Handle(Geom_Conic)::DownCast(trim->BasisCurve());
    gp_Ax1 axis = conic->Axis();
    gp_Dir dir = axis.Direction();
    return Py::Vector(Base::Vector3d(dir.X(), dir.Y(), dir.Z()));
}

void ArcOauracadonicPy::setAxis(Py::Object arg)
{
    PyObject* p = arg.ptr();
    Base::Vector3d val;
    if (PyObject_TypeCheck(p, &(Base::VectorPy::Type))) {
        val = static_cast<Base::VectorPy*>(p)->value();
    }
    else if (PyTuple_Check(p)) {
        val = Base::getVectorFromTuple<double>(p);
    }
    else {
        std::string error = std::string("type must be 'Vector', not ");
        error += p->ob_type->tp_name;
        throw Py::TypeError(error);
    }

    Handle(Geom_TrimmedCurve)
        trim = Handle(Geom_TrimmedCurve)::DownCast(getGeomArcOauracadonicPtr()->handle());
    Handle(Geom_Conic) conic = Handle(Geom_Conic)::DownCast(trim->BasisCurve());
    try {
        gp_Ax1 axis;
        axis.SetLocation(conic->Location());
        axis.SetDirection(gp_Dir(val.x, val.y, val.z));
        conic->SetAxis(axis);
    }
    catch (Standard_Failure&) {
        throw Py::RuntimeError("cannot set axis");
    }
}

Py::Object ArcOauracadonicPy::getXAxis() const
{
    Handle(Geom_TrimmedCurve)
        trim = Handle(Geom_TrimmedCurve)::DownCast(getGeomArcOauracadonicPtr()->handle());
    Handle(Geom_Conic) conic = Handle(Geom_Conic)::DownCast(trim->BasisCurve());
    gp_Ax1 axis = conic->XAxis();
    gp_Dir dir = axis.Direction();
    return Py::Vector(Base::Vector3d(dir.X(), dir.Y(), dir.Z()));
}

void ArcOauracadonicPy::setXAxis(Py::Object arg)
{
    PyObject* p = arg.ptr();
    Base::Vector3d val;
    if (PyObject_TypeCheck(p, &(Base::VectorPy::Type))) {
        val = static_cast<Base::VectorPy*>(p)->value();
    }
    else if (PyTuple_Check(p)) {
        val = Base::getVectorFromTuple<double>(p);
    }
    else {
        std::string error = std::string("type must be 'Vector', not ");
        error += p->ob_type->tp_name;
        throw Py::TypeError(error);
    }

    Handle(Geom_TrimmedCurve)
        trim = Handle(Geom_TrimmedCurve)::DownCast(getGeomArcOauracadonicPtr()->handle());
    Handle(Geom_Conic) conic = Handle(Geom_Conic)::DownCast(trim->BasisCurve());
    try {
        gp_Ax2 pos;
        pos = conic->Position();
        pos.SetXDirection(gp_Dir(val.x, val.y, val.z));
        conic->SetPosition(pos);
    }
    catch (Standard_Failure&) {
        throw Py::RuntimeError("cannot set X axis");
    }
}

Py::Object ArcOauracadonicPy::getYAxis() const
{
    Handle(Geom_TrimmedCurve)
        trim = Handle(Geom_TrimmedCurve)::DownCast(getGeomArcOauracadonicPtr()->handle());
    Handle(Geom_Conic) conic = Handle(Geom_Conic)::DownCast(trim->BasisCurve());
    gp_Ax1 axis = conic->YAxis();
    gp_Dir dir = axis.Direction();
    return Py::Vector(Base::Vector3d(dir.X(), dir.Y(), dir.Z()));
}

void ArcOauracadonicPy::setYAxis(Py::Object arg)
{
    PyObject* p = arg.ptr();
    Base::Vector3d val;
    if (PyObject_TypeCheck(p, &(Base::VectorPy::Type))) {
        val = static_cast<Base::VectorPy*>(p)->value();
    }
    else if (PyTuple_Check(p)) {
        val = Base::getVectorFromTuple<double>(p);
    }
    else {
        std::string error = std::string("type must be 'Vector', not ");
        error += p->ob_type->tp_name;
        throw Py::TypeError(error);
    }

    Handle(Geom_TrimmedCurve)
        trim = Handle(Geom_TrimmedCurve)::DownCast(getGeomArcOauracadonicPtr()->handle());
    Handle(Geom_Conic) conic = Handle(Geom_Conic)::DownCast(trim->BasisCurve());
    try {
        gp_Ax2 pos;
        pos = conic->Position();
        pos.SetYDirection(gp_Dir(val.x, val.y, val.z));
        conic->SetPosition(pos);
    }
    catch (Standard_Failure&) {
        throw Py::RuntimeError("cannot set Y axis");
    }
}

PyObject* ArcOauracadonicPy::getCustomAttributes(const char*) const
{
    return nullptr;
}

int ArcOauracadonicPy::setCustomAttributes(const char*, PyObject*)
{
    return 0;
}
