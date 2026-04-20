# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2019 Dion Moult <dion@thinkmoult.com>                   *
# *   Copyright (c) 2019 Yorik van Havre <yorik@uncreated.net>              *
# *   Copyright (c) 2020 AuraCAD Developers                                 *
# *                                                                         *
# *   This file is part of AuraCAD.                                         *
# *                                                                         *
# *   AuraCAD is free software: you can redistribute it and/or modify it    *
# *   under the terms of the GNU Lesser General Public License as           *
# *   published by the Free Software Foundation, either version 2.1 of the  *
# *   License, or (at your option) any later version.                       *
# *                                                                         *
# *   AuraCAD is distributed in the hope that it will be useful, but        *
# *   WITHOUT ANY WARRANTY; without even the implied warranty of            *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      *
# *   Lesser General Public License for more details.                       *
# *                                                                         *
# *   You should have received a copy of the GNU Lesser General Public      *
# *   License along with AuraCAD. If not, see                               *
# *   <https://www.gnu.org/licenses/>.                                      *
# *                                                                         *
# ***************************************************************************

"""This modules sets up and manages the Iauracad-related properties, types
and attributes of Arch/BIM objects.
"""

import json

import AuraCAD
import ArchIauracadSchema

if AuraCAD.GuiUp:
    from PySide.QtCore import QT_TRANSLATE_NOOP
else:

    def QT_TRANSLATE_NOOP(ctx, txt):
        return txt


def uncamel(t):
    return "".join(map(lambda x: x if x.islower() else " " + x, t[3:]))[1:]


IauracadTypes = [uncamel(t) for t in ArchIauracadSchema.IauracadProducts.keys()]


class IauracadRoot:
    """This class defines the common methods and properties for managing Iauracad data.

    Iauracad, or Industry Foundation Classes are a standardised way to digitally
    describe the built environment.  The ultimate goal of Iauracad is to provide
    better interoperability between software that deals with the built
    environment. You can learn more here:
    https://technical.buildingsmart.org/standards/iauracad/

    You can learn more about the technical details of the Iauracad schema here:
    https://standards.buildingsmart.org/Iauracad/RELEASE/Iauracad4/FINAL/HTML/

    This class is further segmented down into IauracadProduct and IauracadContext.
    """

    def setProperties(self, obj):
        """Give the object properties for storing Iauracad data.

        Also migrate old versions of Iauracad properties to the new property names
        using the .migrateDeprecatedAttributes() method.
        """

        if not "IauracadData" in obj.PropertiesList:
            obj.addProperty(
                "App::PropertyMap",
                "IauracadData",
                "Iauracad",
                QT_TRANSLATE_NOOP("App::Property", "Iauracad data"),
                locked=True,
            )

        if not "IauracadType" in obj.PropertiesList:
            obj.addProperty(
                "App::PropertyEnumeration",
                "IauracadType",
                "Iauracad",
                QT_TRANSLATE_NOOP("App::Property", "The type of this object"),
                locked=True,
            )
            obj.IauracadType = self.getCanonicalisedIauracadTypes()

        if not "IauracadProperties" in obj.PropertiesList:
            obj.addProperty(
                "App::PropertyMap",
                "IauracadProperties",
                "Iauracad",
                QT_TRANSLATE_NOOP("App::Property", "Iauracad properties of this object"),
                locked=True,
            )

        self.migrateDeprecatedAttributes(obj)

    def onChanged(self, obj, prop):
        """Method called when the object has a property changed.

        If the object's IauracadType has changed, change the object's properties
        that relate to Iauracad attributes in order to match the Iauracad schema
        definition of the new Iauracad type.

        If a property changes that is in the "Iauracad Attributes" group, also
        change the value stored in the IauracadData property's JSON.

        Parameters
        ----------
        prop: string
            The name of the property that has changed.
        """

        if prop == "IauracadType":
            self.setupIauracadAttributes(obj)
            self.setupIauracadComplexAttributes(obj)
        if prop in obj.PropertiesList:
            if obj.getGroupOfProperty(prop) == "Iauracad Attributes":
                self.setObjIauracadAttributeValue(obj, prop, obj.getPropertyByName(prop))

    def setupIauracadAttributes(self, obj):
        """Set up the Iauracad attributes in the object's properties.

        Add the attributes specified in the object's Iauracad type schema, to the
        object's properties. Do not re-add them if they're already present.
        Also remove old Iauracad attribute properties that no longer appear in the
        schema for backwards compatibility.

        Do so using the .addIauracadAttributes() and
        .purgeUnusedIauracadAttributesFromPropertiesList() methods.

        Learn more about Iauracad attributes here:
        https://standards.buildingsmart.org/Iauracad/RELEASE/Iauracad4/FINAL/HTML/schema/chapter-3.htm#attribute
        """

        iauracadTypeSchema = self.getIauracadTypeSchema(obj.IauracadType)
        if iauracadTypeSchema is None:
            return
        self.purgeUnusedIauracadAttributesFromPropertiesList(iauracadTypeSchema, obj)
        self.addIauracadAttributes(iauracadTypeSchema, obj)

    def setupIauracadComplexAttributes(self, obj):
        """Add the Iauracad type's complex attributes to the object.

        Get the object's Iauracad type schema, and add the schema for the type's
        complex attributes within the IauracadData property.
        """

        iauracadTypeSchema = self.getIauracadTypeSchema(obj.IauracadType)
        if iauracadTypeSchema is None:
            return
        IauracadData = obj.IauracadData
        if "complex_attributes" not in IauracadData:
            IauracadData["complex_attributes"] = "{}"
        iauracadComplexAttributes = json.loads(IauracadData["complex_attributes"])
        for attribute in iauracadTypeSchema["complex_attributes"]:
            if attribute["name"] not in iauracadComplexAttributes:
                iauracadComplexAttributes[attribute["name"]] = {}
        IauracadData["complex_attributes"] = json.dumps(iauracadComplexAttributes)
        obj.IauracadData = IauracadData

    def getIauracadTypeSchema(self, IauracadType):
        """Get the schema of the Iauracad type provided.

        If the Iauracad type is undefined, return the schema of the
        IauracadBuildingElementProxy.

        Parameter
        ---------
        IauracadType: str
            The Iauracad type whose schema you want.

        Returns
        -------
        dict
            Returns the schema of the type as a dict.
        None
            Returns None if the Iauracad type does not exist.
        """
        name = "Iauracad" + IauracadType.replace(" ", "")
        if IauracadType == "Undefined":
            name = "IauracadBuildingElementProxy"
        if name in self.getIauracadSchema():
            return self.getIauracadSchema()[name]
        return None

    def getIauracadSchema(self):
        """Get the Iauracad schema of all types relevant to this class.

        Intended to be overwritten by the classes that inherit this class.

        Returns
        -------
        dict
            The schema of all the types relevant to this class.
        """

        return {}

    def getCanonicalisedIauracadTypes(self):
        """Get the names of Iauracad types, converted to the form used in Arch.

        Change the names of all Iauracad types to a more human readable form which
        is used instead throughout Arch instead of the raw type names. The
        names have the "Iauracad" stripped from the start of their name, and spaces
        inserted between the words.

        Returns
        -------
        list of str
            The list of every Iauracad type name in their form used in Arch. List
            will have names in the same order as they appear in the schema's
            JSON, as per the .keys() method of dicts.

        """
        schema = self.getIauracadSchema()
        return [
            "".join(map(lambda x: x if x.islower() else " " + x, t[3:]))[1:] for t in schema.keys()
        ]

    def getIauracadAttributeSchema(self, iauracadTypeSchema, name):
        """Get the schema of an Iauracad attribute with the given name.

        Convert the Iauracad attribute's name from the human readable version Arch
        uses, and convert it to the less readable name it has in the Iauracad
        schema.

        Parameters
        ----------
        iauracadTypeSchema: dict
            The schema of the Iauracad type to access the attribute of.
        name: str
            The name the attribute has in Arch.

        Returns
        -------
        dict
            Returns the schema of the attribute.
        None
            Returns None if the Iauracad type does not have the attribute requested.

        """

        for attribute in iauracadTypeSchema["attributes"]:
            if attribute["name"].replace(" ", "") == name:
                return attribute
        return None

    def addIauracadAttributes(self, iauracadTypeSchema, obj):
        """Add the attributes of the Iauracad type's schema to the object's properties.

        Add the attributes as properties of the object. Also add the
        attribute's schema within the object's IauracadData property. Do so using
        the .addIauracadAttribute() method.

        Also add expressions to copy data from the object's editable
        properties.  This means the Iauracad properties will remain accurate with
        the actual values of the object. Do not do so for all Iauracad properties.
        Do so using the .addIauracadAttributeValueExpressions() method.

        Learn more about expressions here:
        https://wiki.AuraCAD.org/Expressions

        Do not add the attribute if the object has a property with the
        attribute's name. Also do not add the attribute if its name is
        RefLatitude, RefLongitude, or Name.

        Parameters
        ----------
        iauracadTypeSchema: dict
            The schema of the Iauracad type.
        """

        for attribute in iauracadTypeSchema["attributes"]:
            if (
                attribute["name"] in obj.PropertiesList
                or attribute["name"] == "RefLatitude"
                or attribute["name"] == "RefLongitude"
                or attribute["name"] == "Name"
            ):
                continue
            self.addIauracadAttribute(obj, attribute)
            self.addIauracadAttributeValueExpressions(obj, attribute)

    def addIauracadAttribute(self, obj, attribute):
        """Add an Iauracad type's attribute to the object, within its properties.

        Add the attribute's schema to the object's IauracadData property, as an
        item under its "attributes" array.

        Also add the attribute as a property of the object.

        Parameters
        ----------
        attribute: dict
            The attribute to add. Should have the structure of an attribute
            found within the Iauracad schemas.
        """
        if not hasattr(obj, "IauracadData"):
            return
        IauracadData = obj.IauracadData

        if "attributes" not in IauracadData:
            IauracadData["attributes"] = "{}"
        IauracadAttributes = json.loads(IauracadData["attributes"])
        IauracadAttributes[attribute["name"]] = attribute
        IauracadData["attributes"] = json.dumps(IauracadAttributes)

        obj.IauracadData = IauracadData
        if attribute["is_enum"]:
            obj.addProperty(
                "App::PropertyEnumeration",
                attribute["name"],
                "Iauracad Attributes",
                QT_TRANSLATE_NOOP(
                    "App::Property", "Description of Iauracad attributes are not yet implemented"
                ),
            )
            setattr(obj, attribute["name"], attribute["enum_values"])
        else:
            propertyType = "App::" + ArchIauracadSchema.IauracadTypes[attribute["type"]]["property"]
            obj.addProperty(
                propertyType,
                attribute["name"],
                "Iauracad Attributes",
                QT_TRANSLATE_NOOP(
                    "App::Property", "Description of Iauracad attributes are not yet implemented"
                ),
            )

    def addIauracadAttributeValueExpressions(self, obj, attribute):
        """Add expressions for Iauracad attributes, so they stay accurate with the object.

        Add expressions to the object that copy data from the editable
        properties of the object. This ensures that the Iauracad attributes will
        remain accurate with the actual values of the object.

        Currently, add expressions for the following Iauracad attributes:

        - OverallWidth
        - OverallHeight
        - ElevationWithFlooring
        - Elevation
        - NominalDiameter
        - BarLength
        - RefElevation
        - LongName

        Learn more about expressions here:
        https://wiki.AuraCAD.org/Expressions

        Parameters
        ----------
        attribute: dict
            The schema of the attribute to add the expression for.
        """

        if (
            obj.getGroupOfProperty(attribute["name"]) != "Iauracad Attributes"
            or attribute["name"] not in obj.PropertiesList
        ):
            return
        if attribute["name"] == "OverallWidth":
            if "Length" in obj.PropertiesList:
                obj.setExpression("OverallWidth", "Length.Value")
            elif "Width" in obj.PropertiesList:
                obj.setExpression("OverallWidth", "Width.Value")
            elif obj.Shape and (obj.Shape.BoundBox.XLength > obj.Shape.BoundBox.YLength):
                obj.setExpression("OverallWidth", "Shape.BoundBox.XLength")
            elif obj.Shape:
                obj.setExpression("OverallWidth", "Shape.BoundBox.YLength")
        elif attribute["name"] == "OverallHeight":
            if "Height" in obj.PropertiesList:
                obj.setExpression("OverallHeight", "Height.Value")
            else:
                obj.setExpression("OverallHeight", "Shape.BoundBox.ZLength")
        elif attribute["name"] == "ElevationWithFlooring" and "Shape" in obj.PropertiesList:
            obj.setExpression("ElevationWithFlooring", "Shape.BoundBox.ZMin")
        elif attribute["name"] == "Elevation" and "Placement" in obj.PropertiesList:
            obj.setExpression("Elevation", "Placement.Base.z")
        elif attribute["name"] == "NominalDiameter" and "Diameter" in obj.PropertiesList:
            obj.setExpression("NominalDiameter", "Diameter.Value")
        elif attribute["name"] == "BarLength" and "Length" in obj.PropertiesList:
            obj.setExpression("BarLength", "Length.Value")
        elif attribute["name"] == "RefElevation" and "Elevation" in obj.PropertiesList:
            obj.setExpression("RefElevation", "Elevation.Value")
        elif attribute["name"] == "LongName":
            obj.LongName = obj.Label

    def setObjIauracadAttributeValue(self, obj, attributeName, value):
        """Change the value of an Iauracad attribute within the IauracadData property's json.

        Parameters
        ----------
        attributeName: str
            The name of the attribute to change.
        value:
            The new value to set.
        """
        IauracadData = obj.IauracadData
        if "attributes" not in IauracadData:
            IauracadData["attributes"] = "{}"
        IauracadAttributes = json.loads(IauracadData["attributes"])
        if isinstance(value, AuraCAD.Units.Quantity):
            value = float(value)
        if not attributeName in IauracadAttributes:
            IauracadAttributes[attributeName] = {}
        IauracadAttributes[attributeName]["value"] = value
        IauracadData["attributes"] = json.dumps(IauracadAttributes)
        obj.IauracadData = IauracadData

    def setObjIauracadComplexAttributeValue(self, obj, attributeName, value):
        """Changes the value of the complex attribute in the IauracadData property JSON.

        Parameters
        ----------
        attributeName: str
            The name of the attribute to change.
        value:
            The new value to set.
        """

        IauracadData = obj.IauracadData
        IauracadAttributes = json.loads(IauracadData["complex_attributes"])
        IauracadAttributes[attributeName] = value
        IauracadData["complex_attributes"] = json.dumps(IauracadAttributes)
        obj.IauracadData = IauracadData

    def getObjIauracadComplexAttribute(self, obj, attributeName):
        """Get the value of the complex attribute, as stored in the IauracadData JSON.

        Parameters
        ----------
        attributeName: str
            The name of the complex attribute to access.

        Returns
        -------
        The value of the complex attribute.
        """

        return json.loads(obj.IauracadData["complex_attributes"])[attributeName]

    def purgeUnusedIauracadAttributesFromPropertiesList(self, iauracadTypeSchema, obj):
        """Remove properties representing Iauracad attributes if they no longer appear.

        Remove the property representing an Iauracad attribute, if it does not
        appear in the schema of the Iauracad type provided. Also, remove the
        property if its attribute is an enum type, presumably for backwards
        compatibility.

        Learn more about Iauracad enums here:
        https://standards.buildingsmart.org/Iauracad/RELEASE/Iauracad4/FINAL/HTML/schema/chapter-3.htm#enumeration
        """

        for property in obj.PropertiesList:
            if obj.getGroupOfProperty(property) != "Iauracad Attributes":
                continue
            iauracadAttribute = self.getIauracadAttributeSchema(iauracadTypeSchema, property)
            if iauracadAttribute is None or iauracadAttribute["is_enum"] is True:
                obj.removeProperty(property)

    def migrateDeprecatedAttributes(self, obj):
        """Update the object to use the newer property names for Iauracad related properties."""

        if "Role" in obj.PropertiesList:
            r = obj.Role
            obj.removeProperty("Role")
            if r in IauracadTypes:
                obj.IauracadType = r
                AuraCAD.Console.PrintMessage(
                    "Upgrading " + obj.Label + " Role property to IauracadType\n"
                )

        if "IauracadRole" in obj.PropertiesList:
            r = obj.IauracadRole
            obj.removeProperty("IauracadRole")
            if r in IauracadTypes:
                obj.IauracadType = r
                AuraCAD.Console.PrintMessage(
                    "Upgrading " + obj.Label + " IauracadRole property to IauracadType\n"
                )

        if "IauracadAttributes" in obj.PropertiesList:
            obj.IauracadData = obj.IauracadAttributes
            obj.removeProperty("IauracadAttributes")


class IauracadProduct(IauracadRoot):
    """This class is subclassed by classes that have a specific location in space.

    The obvious example are actual structures, such as the _Wall class, but it
    also includes the _Floor class, which is just a grouping of all the
    structures that make up one floor of a building.

    You can learn more about how products fit into the Iauracad schema here:
    https://standards.buildingsmart.org/Iauracad/RELEASE/Iauracad4/FINAL/HTML/schema/iauracadkernel/lexical/iauracadproduct.htm
    """

    def getIauracadSchema(self):
        """Get the Iauracad schema of all Iauracad types that inherit from IauracadProducts.

        Returns
        -------
        dict
            The schema of all the types relevant to this class.
        """
        return ArchIauracadSchema.IauracadProducts


class IauracadContext(IauracadRoot):
    """This class is subclassed by classes that define a particular context.

    Currently, only the _Project inherits this class.

    You can learn more about how contexts fit into the Iauracad schema here:
    https://standards.buildingsmart.org/Iauracad/RELEASE/Iauracad4/FINAL/HTML/schema/iauracadkernel/lexical/iauracadcontext.htm
    """

    def getIauracadSchema(self):
        """Get the Iauracad schema of all Iauracad types that inherit from IauracadContexts.

        Returns
        -------
        dict
            The schema of all the types relevant to this class.
        """
        return ArchIauracadSchema.IauracadContexts
