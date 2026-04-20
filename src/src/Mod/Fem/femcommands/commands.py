# ***************************************************************************
# *   Copyright (c) 2016 Bernd Hahnebach <bernd@bimstatik.org>              *
# *                                                                         *
# *   This file is part of the AuraCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__title__ = "AuraCAD FEM command definitions"
__author__ = "Bernd Hahnebach"
__url__ = "https://www.AuraCAD.org"

## @package commands
#  \ingroup FEM
#  \brief AuraCAD FEM command definitions

import AuraCAD
import AuraCADGui
from AuraCAD import Qt

from .manager import CommandManager
from femtools.femutils import expandParentObject
from femtools.femutils import is_of_type
from femsolver.settings import get_default_solver

# Python command definitions:
# for C++ command definitions see src/Mod/Fem/Command.cpp
# TODO, may be even more generic class creation
# with type() and identifier instead of class for
# the commands which add new document objects.
# see https://www.python-course.eu/python3_classes_and_type.php
# Translation:
# some information in the regard of translation can be found in forum post
# https://forum.AuraCAD.org/viewtopic.php?f=18&t=62449&p=543845#p543593


class _Analysis(CommandManager):
    "The FEM_Analysis command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_Analysis", "New Analysis")
        self.accel = "S, A"
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_Analysis", "Creates an analysis container with default solver"
        )
        self.is_active = "with_document"

    def Activated(self):
        AuraCAD.ActiveDocument.openTransaction("Create Analysis")
        AuraCADGui.addModule("FemGui")
        AuraCADGui.addModule("ObjectsFem")
        AuraCADGui.doCommand("ObjectsFem.makeAnalysis(AuraCAD.ActiveDocument, 'Analysis')")
        AuraCADGui.doCommand("FemGui.setActiveAnalysis(AuraCAD.ActiveDocument.ActiveObject)")
        AuraCAD.ActiveDocument.commitTransaction()
        def_solver = get_default_solver()
        if def_solver:
            AuraCAD.ActiveDocument.openTransaction("Create default solver")
            cmd = ""
            match def_solver:
                case "CalculiX":
                    cmd = "FEM_SolverCalculiX"
                case "Elmer":
                    cmd = "FEM_SolverElmer"
                case "Mystran":
                    cmd = "FEM_SolverMystran"
                case "Z88":
                    cmd = "FEM_SolverZ88"

            if cmd:
                AuraCADGui.doCommand(f'AuraCADGui.runCommand("{cmd}")')

            AuraCADGui.doCommand(
                "AuraCADGui.ActiveDocument.toggleTreeItem(FemGui.getActiveAnalysis(), 2)"
            )
            AuraCAD.ActiveDocument.commitTransaction()

        AuraCAD.ActiveDocument.recompute()


class _ClippingPlaneAdd(CommandManager):
    "The FEM_ClippingPlaneAdd command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_ClippingPlaneAdd", "Clipping Plane on Face")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ClippingPlaneAdd", "Adds a clipping plane on a selected face"
        )
        self.is_active = "with_document"

    def GetResources(self):
        resources = super().GetResources()
        resources["CmdType"] = "ForEdit | Alter3DView"
        return resources

    def Activated(self):
        from pivy import coin
        from femtools.femutils import getBoundBoxOfAllDocumentShapes
        from femtools.femutils import getSelectedFace

        overallboundbox = getBoundBoxOfAllDocumentShapes(AuraCAD.ActiveDocument)
        # print(overallboundbox)
        if overallboundbox:
            min_bb_length = min(
                {
                    overallboundbox.XLength,
                    overallboundbox.YLength,
                    overallboundbox.ZLength,
                }
            )
        else:
            min_bb_length = 10.0  # default

        dbox = min_bb_length * 0.2

        aFace = getSelectedFace(AuraCADGui.Selection.getSelectionEx())
        if aFace:
            f_CoM = aFace.CenterOfMass
            f_uvCoM = aFace.Surface.parameter(f_CoM)  # u,v at CoM for normalAt calculation
            f_normal = aFace.normalAt(f_uvCoM[0], f_uvCoM[1])
        else:
            f_CoM = AuraCAD.Vector(0, 0, 0)
            f_normal = AuraCAD.Vector(0, 0, 1)

        coin_normal_vector = coin.SbVec3f(-f_normal.x, -f_normal.y, -f_normal.z)
        coin_bound_box = coin.SbBox3f(
            f_CoM.x - dbox,
            f_CoM.y - dbox,
            f_CoM.z - dbox * 0.15,
            f_CoM.x + dbox,
            f_CoM.y + dbox,
            f_CoM.z + dbox * 0.15,
        )
        clip_plane = coin.SoClipPlaneManip()
        clip_plane.setValue(coin_bound_box, coin_normal_vector, 1)
        AuraCADGui.ActiveDocument.ActiveView.getSceneGraph().insertChild(clip_plane, 1)


class _ClippingPlaneRemoveAll(CommandManager):
    "The FEM_ClippingPlaneRemoveAll command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_ClippingPlaneRemoveAll", "Remove All Clipping Planes"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ClippingPlaneRemoveAll", "Removes all clipping planes"
        )
        self.is_active = "with_document"

    def GetResources(self):
        resources = super().GetResources()
        resources["CmdType"] = "ForEdit | Alter3DView"
        return resources

    def Activated(self):
        line1 = "for node in list(sg.getChildren()):\n"
        line2 = "    if isinstance(node, coin.SoClipPlane):\n"
        line3 = "        sg.removeChild(node)"
        AuraCADGui.doCommand("from pivy import coin")
        AuraCADGui.doCommand("sg = Gui.ActiveDocument.ActiveView.getSceneGraph()")
        AuraCADGui.doCommand("nodes = sg.getChildren()")
        AuraCADGui.doCommand(line1 + line2 + line3)


class _ConstantVacuumPermittivity(CommandManager):
    "The FEM_ConstantVacuumPermittivity command definition"

    def __init__(self):
        super().__init__()
        self.pixmap = "fem-solver-analysis-thermomechanical.svg"
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstantVacuumPermittivity", "Constant Vacuum Permittivity"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstantVacuumPermittivity",
            "Creates a constant vacuum permittivity to overwrite standard value",
        )
        self.is_active = "with_document"
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_noset_edit"


class _ConstraintBodyHeatSource(CommandManager):
    "The FEM_ConstraintBodyHeatSource command definition"

    def __init__(self):
        super().__init__()
        self.pixmap = "FEM_ConstraintBodyHeatSource"
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_ConstraintBodyHeatSource", "Body Heat Source")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintBodyHeatSource", "Creates a body heat source"
        )
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ConstraintCentrif(CommandManager):
    "The FEM_ConstraintCentrif command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_ConstraintCentrif", "Centrifugal Load")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_ConstraintCentrif", "Creates a centrifugal load")
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ConstraintCurrentDensity(CommandManager):
    "The FEM_ConstraintCurrentDensity command definition"

    def __init__(self):
        super().__init__()
        self.pixmap = "FEM_ConstraintCurrentDensity"
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintCurrentDensity", "Current Density Boundary Condition"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintCurrentDensity",
            "Creates a current density boundary condition",
        )
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ConstraintElectricChargeDensity(CommandManager):
    "The FEM_ConstraintElectricChargeDensity command definition"

    def __init__(self):
        super().__init__()
        self.pixmap = "FEM_ConstraintElectricChargeDensity"
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintElectricChargeDensity", "Electric Charge Density"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintElectricChargeDensity", "Creates an electric charge density"
        )
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ConstraintElectromagnetic(CommandManager):
    "The FEM_ConstraintElectromagnetic command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintElectromagnetic",
            "Electromagnetic Boundary Condition",
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintElectromagnetic",
            "Creates an electromagnetic boundary condition",
        )
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ConstraintFlowVelocity(CommandManager):
    "The FEM_ConstraintFlowVelocity command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintFlowVelocity", "Flow Velocity Boundary Condition"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintFlowVelocity", "Creates a flow velocity boundary condition"
        )
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ConstraintInitialFlowVelocity(CommandManager):
    "The FEM_ConstraintInitialFlowVelocity command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintInitialFlowVelocity", "Initial Flow Velocity Condition"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintInitialFlowVelocity",
            "Creates an initial flow velocity condition",
        )
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ConstraintInitialPressure(CommandManager):
    "The FEM_ConstraintInitialPressure command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintInitialPressure", "Initial Pressure Condition"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintInitialPressure", "Creates an initial pressure condition"
        )
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ConstraintMagnetization(CommandManager):
    "The FEM_ConstraintMagnetization command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintMagnetization", "Magnetization Boundary Condition"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintMagnetization", "Creates a magnetization boundary condition"
        )
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ConstraintSectionPrint(CommandManager):
    "The FEM_ConstraintSectionPrint command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_ConstraintSectionPrint", "Section Print Feature")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ConstraintSectionPrint", "Creates a section print feature"
        )
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ConstraintSelfWeight(CommandManager):
    "The FEM_ConstraintSelfWeight command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_ConstraintSelfWeight", "Gravity Load")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_ConstraintSelfWeight", "Creates a gravity load")
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_noset_edit"


class _ConstraintTie(CommandManager):
    "The FEM_ConstraintTie command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_ConstraintTie", "Tie Constraint")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_ConstraintTie", "Creates a tie constraint")
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ElementFluid1D(CommandManager):
    "The FEM_ElementFluid1D command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_ElementFluid1D", "Fluid Section for 1D Flow")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ElementFluid1D", "Creates a fluid section for 1D flow"
        )
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ElementGeometry1D(CommandManager):
    "The Fem_ElementGeometry1D command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_ElementGeometry1D", "Beam Cross Section")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_ElementGeometry1D", "Creates a beam cross section")
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ElementGeometry2D(CommandManager):
    "The FEM_ElementGeometry2D command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_ElementGeometry2D", "Shell Plate Thickness")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ElementGeometry2D", "Creates a shell plate thickness"
        )
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _ElementRotation1D(CommandManager):
    "The Fem_ElementRotation1D command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_ElementRotation1D", "Beam Rotation")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_ElementRotation1D", "Creates a beam rotation")
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_noset_edit"


class _EquationDeformation(CommandManager):
    "The FEM_EquationDeformation command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_EquationDeformation", "Deformation Equation")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_EquationDeformation",
            "Creates an equation for deformation (nonlinear elasticity)",
        )
        self.is_active = "with_solver_elmer"
        self.do_activated = "add_obj_on_gui_selobj_expand_noset_edit"


class _EquationElasticity(CommandManager):
    "The FEM_EquationElasticity command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_EquationElasticity", "Elasticity Equation")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_EquationElasticity", "Creates an equation for elasticity (stress)"
        )
        self.is_active = "with_solver_elmer"
        self.do_activated = "add_obj_on_gui_selobj_expand_noset_edit"


class _EquationElectricforce(CommandManager):
    "The FEM_EquationElectricforce command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_EquationElectricforce", "Electricforce Equation")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_EquationElectricforce", "Creates an equation for electric forces"
        )
        self.is_active = "with_solver_elmer"
        self.do_activated = "add_obj_on_gui_selobj_expand_noset_edit"


class _EquationElectrostatic(CommandManager):
    "The FEM_EquationElectrostatic command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_EquationElectrostatic", "Electrostatic Equation")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_EquationElectrostatic", "Creates an equation for electrostatic"
        )
        self.is_active = "with_solver_elmer"
        self.do_activated = "add_obj_on_gui_selobj_expand_noset_edit"


class _EquationFlow(CommandManager):
    "The FEM_EquationFlow command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_EquationFlow", "Flow Equation")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_EquationFlow", "Creates an equation for flow")
        self.is_active = "with_solver_elmer"
        self.do_activated = "add_obj_on_gui_selobj_expand_noset_edit"


class _EquationFlux(CommandManager):
    "The FEM_EquationFlux command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_EquationFlux", "Flux Equation")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_EquationFlux", "Creates an equation for flux")
        self.is_active = "with_solver_elmer"
        self.do_activated = "add_obj_on_gui_selobj_expand_noset_edit"


class _EquationHeat(CommandManager):
    "The FEM_EquationHeat command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_EquationHeat", "Heat Equation")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_EquationHeat", "Creates an equation for heat")
        self.is_active = "with_solver_elmer"
        self.do_activated = "add_obj_on_gui_selobj_expand_noset_edit"


class _EquationMagnetodynamic(CommandManager):
    "The FEM_EquationMagnetodynamic command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_EquationMagnetodynamic", "Magnetodynamic Equation"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_EquationMagnetodynamic",
            "Creates an equation for magnetodynamic forces",
        )
        self.is_active = "with_solver_elmer"
        self.do_activated = "add_obj_on_gui_selobj_expand_noset_edit"


class _EquationMagnetodynamic2D(CommandManager):
    "The FEM_EquationMagnetodynamic2D command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_EquationMagnetodynamic2D", "Magnetodynamic 2D Equation"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_EquationMagnetodynamic2D",
            "Creates an equation for 2D magnetodynamic forces",
        )
        self.is_active = "with_solver_elmer"
        self.do_activated = "add_obj_on_gui_selobj_expand_noset_edit"


class _EquationStaticCurrent(CommandManager):
    "The FEM_EquationStaticCurrent command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_EquationStaticCurrent", "Static Current Equation")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_EquationStaticCurrent", "Creates an equation for static current"
        )
        self.is_active = "with_solver_elmer"
        self.do_activated = "add_obj_on_gui_selobj_expand_noset_edit"


class _Examples(CommandManager):
    "The FEM_Examples command definition"

    def __init__(self):
        super().__init__()
        self.pixmap = "FemWorkbench"
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_Examples", "FEM Examples")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_Examples", "Opens the FEM examples")
        self.is_active = "always"

    def Activated(self):
        AuraCADGui.addModule("femexamples.examplesgui")
        AuraCADGui.doCommand("femexamples.examplesgui.show_examplegui()")


class _MaterialEditor(CommandManager):
    "The FEM_MaterialEditor command definition"

    def __init__(self):
        super().__init__()
        self.pixmap = "Arch_Material_Group"
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MaterialEditor", "Material Editor")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MaterialEditor", "Opens the AuraCAD material editor"
        )
        self.is_active = "always"

    def Activated(self):
        AuraCADGui.addModule("MaterialEditor")
        AuraCADGui.doCommand("MaterialEditor.openEditor()")


class _MaterialFluid(CommandManager):
    "The FEM_MaterialFluid command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MaterialFluid", "Fluid Material")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_MaterialFluid", "Creates a fluid material")
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _MaterialMechanicalNonlinear(CommandManager):
    "The FEM_MaterialMechanicalNonlinear command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_MaterialMechanicalNonlinear", "Non-Linear Mechanical Material"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MaterialMechanicalNonlinear", "Add non-linear mechanical properties to material"
        )

    def IsActive(self):
        return self.material_solid_selected() and (self.selobj.Nonlinear is None)

    def Activated(self):
        # add a nonlinear material
        AuraCAD.ActiveDocument.openTransaction("Create FemMaterialMechanicalNonlinear")
        AuraCADGui.addModule("ObjectsFem")
        lin_mat_obj = f"AuraCAD.ActiveDocument.getObject('{self.selobj.Name}')"
        command_to_run = (
            f"ObjectsFem.makeMaterialMechanicalNonlinear(AuraCAD.ActiveDocument, {lin_mat_obj})"
        )
        AuraCADGui.doCommand(command_to_run)

        expandParentObject()
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCADGui.Selection.clearSelection()
        AuraCAD.ActiveDocument.recompute()


class _MaterialReinforced(CommandManager):
    "The FEM_MaterialReinforced command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_MaterialReinforced", "Reinforced Material (Concrete)"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MaterialReinforced",
            "Creates a material for reinforced matrix material such as concrete",
        )
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _MaterialSolid(CommandManager):
    "The FEM_MaterialSolid command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MaterialSolid", "Solid Material")
        self.accel = "M, S"
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_MaterialSolid", "Creates a solid material")
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_set_edit"


class _FEMMesh2Mesh(CommandManager):
    "The FEM_FEMMesh2Mesh command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_FEMMesh2Mesh", "FEM Mesh to Mesh")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_FEMMesh2Mesh", "Converts the surface of a FEM mesh to a mesh"
        )
        self.is_active = "with_femmesh_andor_res"

    def Activated(self):
        AuraCAD.ActiveDocument.openTransaction("Create Mesh from FEMMesh")
        if self.selobj and not self.selobj2:  # no result object selected
            AuraCADGui.addModule("femmesh.femmesh2mesh")
            AuraCADGui.doCommand(
                "out_mesh = femmesh.femmesh2mesh.femmesh_2_mesh("
                "AuraCAD.ActiveDocument.{}.FemMesh)".format(self.selobj.Name)
            )
            AuraCADGui.addModule("Mesh")
            AuraCADGui.doCommand("Mesh.show(Mesh.Mesh(out_mesh))")
            AuraCADGui.doCommand(
                "AuraCAD.ActiveDocument." + self.selobj.Name + ".ViewObject.hide()"
            )
        if self.selobj and self.selobj2:
            femmesh = self.selobj
            res = self.selobj2
            AuraCADGui.addModule("femmesh.femmesh2mesh")
            AuraCADGui.doCommand(
                "out_mesh = femmesh.femmesh2mesh.femmesh_2_mesh("
                "AuraCAD.ActiveDocument.{}.FemMesh, AuraCAD.ActiveDocument.{})".format(
                    femmesh.Name, res.Name
                )
            )
            AuraCADGui.addModule("Mesh")
            AuraCADGui.doCommand("Mesh.show(Mesh.Mesh(out_mesh))")
            AuraCADGui.doCommand("AuraCAD.ActiveDocument." + femmesh.Name + ".ViewObject.hide()")
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCADGui.Selection.clearSelection()
        AuraCAD.ActiveDocument.recompute()


class _MeshBoundaryLayer(CommandManager):
    "The FEM_MeshBoundaryLayer command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MeshBoundaryLayer", "2D Boundary Layer")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshBoundaryLayer",
            "Adds a structured layer of mesh elmenets on 2D model boundaries",
        )
        self.is_active = "with_gmsh_femmesh"
        self.do_activated = "add_obj_on_gui_selobj_set_edit"


class _MeshClear(CommandManager):
    "The FEM_MeshClear command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MeshClear", "Clear FEM Mesh")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_MeshClear", "Clears the mesh of a FEM mesh object")
        self.is_active = "with_femmesh"

    def Activated(self):
        AuraCAD.ActiveDocument.openTransaction("Clear FEM mesh")
        AuraCADGui.addModule("Fem")
        AuraCADGui.doCommand(
            "AuraCAD.ActiveDocument." + self.selobj.Name + ".FemMesh = Fem.FemMesh()"
        )
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCADGui.Selection.clearSelection()
        AuraCAD.ActiveDocument.recompute()


class _MeshClearGroups(CommandManager):
    "The FEM_MeshClearGroups command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MeshClearGroups", "Clear Mesh Groups")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_MeshClearGroups", "Remove groups from FEM mesh")
        self.is_active = "with_femmesh"

    def Activated(self):
        AuraCAD.ActiveDocument.openTransaction("ClearGroups FEM mesh")
        AuraCADGui.addModule("Fem")
        grps = "AuraCAD.ActiveDocument." + self.selobj.Name + ".FemMesh.Groups"
        remove_func = "AuraCAD.ActiveDocument." + self.selobj.Name + ".FemMesh.removeGroup"
        AuraCADGui.doCommand(f"tuple(map({remove_func}, {grps}))")
        AuraCAD.Console.PrintMessage(
            f"Groups cleared: Now {self.selobj.Name} has {self.selobj.FemMesh.GroupCount} groups\n"
        )
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCADGui.Selection.clearSelection()
        AuraCAD.ActiveDocument.recompute()


class _MeshDisplayInfo(CommandManager):
    "The FEM_MeshDisplayInfo command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MeshDisplayInfo", "Display Mesh Info")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_MeshDisplayInfo", "Displays FEM mesh information")
        self.is_active = "with_femmesh"

    def Activated(self):
        AuraCAD.ActiveDocument.openTransaction("Display FEM mesh info")
        AuraCADGui.doCommand("print(AuraCAD.ActiveDocument." + self.selobj.Name + ".FemMesh)")
        AuraCADGui.addModule("PySide")
        AuraCADGui.doCommand(
            "mesh_info = str(AuraCAD.ActiveDocument." + self.selobj.Name + ".FemMesh)"
        )
        AuraCADGui.doCommand(
            "PySide.QtGui.QMessageBox.information(None, 'FEM Mesh Info', mesh_info)"
        )
        AuraCAD.ActiveDocument.commitTransaction()
        AuraCADGui.Selection.clearSelection()
        AuraCAD.ActiveDocument.recompute()


class _MeshGmshFromShape(CommandManager):
    "The FEM_MeshGmshFromShape command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MeshGmshFromShape", "Mesh From Shape by Gmsh")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshGmshFromShape", "Creates a FEM mesh from a shape by Gmsh mesher"
        )
        self.is_active = "with_part_feature"

    def Activated(self):
        # a mesh could be made with and without an analysis,
        # we're going to check not for an analysis in command manager module
        AuraCAD.ActiveDocument.openTransaction("Create FEM mesh by Gmsh")
        mesh_obj_name = "FEMMeshGmsh"
        # if requested by some people add Preference for this
        # mesh_obj_name = self.selobj.Name + "_Mesh"
        AuraCADGui.addModule("ObjectsFem")
        AuraCADGui.doCommand(
            "ObjectsFem.makeMeshGmsh(AuraCAD.ActiveDocument, '" + mesh_obj_name + "')"
        )
        AuraCADGui.doCommand(
            "AuraCAD.ActiveDocument.ActiveObject.Shape = AuraCAD.ActiveDocument.{}".format(
                self.selobj.Name
            )
        )
        AuraCADGui.doCommand("AuraCAD.ActiveDocument.ActiveObject.ElementOrder = '2nd'")
        # SecondOrderLinear gives much better meshes in the regard of
        # nonpositive jacobians but on curved faces the constraint nodes
        # will no longer found thus standard will be False
        # https://forum.AuraCAD.org/viewtopic.php?t=41738
        # https://forum.AuraCAD.org/viewtopic.php?f=18&t=45260&start=20#p389494
        AuraCADGui.doCommand("AuraCAD.ActiveDocument.ActiveObject.SecondOrderLinear = False")

        # Gmsh mesh object could be added without an active analysis
        # but if there is an active analysis move it in there
        import FemGui

        if FemGui.getActiveAnalysis():
            AuraCADGui.addModule("FemGui")
            AuraCADGui.doCommand(
                "FemGui.getActiveAnalysis().addObject(AuraCAD.ActiveDocument.ActiveObject)"
            )
        AuraCADGui.doCommand(
            "AuraCADGui.ActiveDocument.setEdit(AuraCAD.ActiveDocument.ActiveObject.Name)"
        )
        AuraCADGui.Selection.clearSelection()


class _MeshGroup(CommandManager):
    "The FEM_MeshGroup command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MeshGroup", "Mesh Group")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_MeshGroup", "Creates a mesh group")
        self.is_active = "with_gmsh_femmesh"
        self.do_activated = "add_obj_on_gui_selobj_set_edit"


class _MeshNetgenFromShape(CommandManager):
    "The FEM_MeshNetgenFromShape command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MeshNetgenFromShape", "Mesh From Shape by Netgen")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshNetgenFromShape",
            "Creates a FEM mesh from a solid or face shape by Netgen internal mesher",
        )
        self.is_active = "with_part_feature"

    def Activated(self):
        # a mesh could be made with and without an analysis,
        # we're going to check not for an analysis in command manager module
        netgen_prefs = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Fem/Netgen")
        AuraCAD.ActiveDocument.openTransaction("Create FEM mesh Netgen")
        mesh_obj_name = "FEMMeshNetgen"
        # if requested by some people add Preference for this
        # mesh_obj_name = sel[0].Name + "_Mesh"
        AuraCADGui.addModule("ObjectsFem")
        if netgen_prefs.GetBool("UseLegacyNetgen", 1):
            AuraCADGui.doCommand(
                "ObjectsFem.makeMeshNetgenLegacy(AuraCAD.ActiveDocument, '" + mesh_obj_name + "')"
            )
        else:
            AuraCADGui.doCommand(
                "ObjectsFem.makeMeshNetgen(AuraCAD.ActiveDocument, '" + mesh_obj_name + "')"
            )
            AuraCADGui.doCommand("AuraCAD.ActiveDocument.ActiveObject.EndStep = 'OptimizeVolume'")

        AuraCADGui.doCommand(
            "AuraCAD.ActiveDocument.ActiveObject.Shape = AuraCAD.ActiveDocument.{}".format(
                self.selobj.Name
            )
        )
        AuraCADGui.doCommand("AuraCAD.ActiveDocument.ActiveObject.Fineness = 'Moderate'")

        # Netgen mesh object could be added without an active analysis
        # but if there is an active analysis move it in there
        import FemGui

        if FemGui.getActiveAnalysis():
            AuraCADGui.addModule("FemGui")
            AuraCADGui.doCommand(
                "FemGui.getActiveAnalysis().addObject(AuraCAD.ActiveDocument.ActiveObject)"
            )
        AuraCADGui.doCommand(
            "AuraCADGui.ActiveDocument.setEdit(AuraCAD.ActiveDocument.ActiveObject.Name)"
        )
        AuraCADGui.Selection.clearSelection()
        # a recompute immediately starts meshing when task panel is opened, this is not intended


class _MeshRegion(CommandManager):
    "The FEM_MeshRefinement command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MeshRegion", "Mesh Refinement")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_MeshRegion", "Creates a FEM mesh refinement")
        self.is_active = "with_femmesh"
        self.do_activated = "add_obj_on_gui_selobj_set_edit"


class _MeshDistance(CommandManager):
    "The FEM_MeshRefinement command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MeshDistance", "Distance-Based Refinement")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshDistance", "Sets mesh size based on the distance to vertices, edges, and faces"
        )
        self.is_active = "with_gmsh_femmesh"
        self.do_activated = "add_obj_on_gui_selobj_set_edit"


class _MeshManipulate(CommandManager):
    "The FEM_MeshManipulate command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MeshManipulate", "Manipulate Refinement")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshManipulate", "Allows to manipulate the output of a refinement in various ways"
        )
        self.is_active = "with_gmsh_femmesh"
        self.do_activated = "add_obj_on_gui_selobj_set_edit"


class _MeshAdvanced(CommandManager):
    "The FEM_MeshAdvanced command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MeshAdvanced", "Advanced Refinement Types")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshAdvanced", "Allows to define the mesh size by various advanced means"
        )
        self.is_active = "with_gmsh_femmesh"
        self.do_activated = "add_obj_on_gui_selobj_set_edit"


class _MeshShape(CommandManager):
    "The FEM_MeshRefinement command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_MeshShape", "Shape-Based Refinement")
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshSphere",
            "Sets mesh size within and outside of a geometric shape (box, sphere, cylinder)",
        )
        self.is_active = "with_gmsh_femmesh"
        self.do_activated = "add_obj_on_gui_selobj_set_edit"


class _MeshTransfiniteCurve(CommandManager):
    "The FEM_MeshTransfiniteCurve command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshTransfiniteCurve", "Structured Transfinite Curve"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshTransfiniteCurve",
            "Creates a fixed amount of nodes on an endge with a structured algorithm",
        )
        self.is_active = "with_gmsh_femmesh"
        self.do_activated = "add_obj_on_gui_selobj_set_edit"


class _MeshTransfiniteSurface(CommandManager):
    "The FEM_MeshTransfiniteSurface command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshTransfiniteSurface", "Structured Transfinite Surface"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshTransfiniteSurface", "Creates a structured mesh on a face"
        )
        self.is_active = "with_gmsh_femmesh"
        self.do_activated = "add_obj_on_gui_selobj_set_edit"


class _MeshTransfiniteVolume(CommandManager):
    "The FEM_MeshTransfiniteVolume command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshTransfiniteVolume", "Structured Transfinite Volume"
        )
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_MeshTransfiniteVolume",
            "Creates a structured mesh in a 4 or 5 sided volume bounded by transfinite surfaces",
        )
        self.is_active = "with_gmsh_femmesh"
        self.do_activated = "add_obj_on_gui_selobj_set_edit"


class _GMSHRefine:
    # Group command for all gmsh special refinements

    def GetCommands(self):
        return [
            "FEM_MeshDistance",
            "FEM_MeshBoundaryLayer",
            "FEM_MeshShape",
            "FEM_MeshManipulate",
            "FEM_MeshAdvanced",
            "FEM_MeshTransfiniteCurve",
            "FEM_MeshTransfiniteSurface",
            "FEM_MeshTransfiniteVolume",
        ]

    def GetDefaultCommand(self):
        return 0

    def GetResources(self):
        return {
            "MenuText": "GMSH Refinements",
            "ToolTip": "Mesh refinements for the GMSH mesh generation",
        }

    def IsActive(self):
        if not AuraCADGui.ActiveDocument:
            return False

        sel = AuraCADGui.Selection.getSelection()
        if len(sel) == 1 and sel[0].isDerivedFrom("Fem::FemMeshObject"):
            # must be GMSH mesh
            return is_of_type(sel[0], "Fem::FemMeshGmsh")

        return False


class _ResultShow(CommandManager):
    "The FEM_ResultShow command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_ResultShow", "Show Result")
        self.accel = "R, S"
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ResultShow", "Shows and visualizes the selected result data"
        )
        self.is_active = "with_selresult"

    def Activated(self):
        self.selobj.ViewObject.Document.setEdit(self.selobj.ViewObject, 0)


class _ResultsPurge(CommandManager):
    "The FEM_ResultsPurge command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_ResultsPurge", "Purge Results")
        self.accel = "R, P"
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_ResultsPurge", "Purges all results from the active analysis"
        )
        self.is_active = "with_analysis"

    def Activated(self):
        import femresult.resulttools as resulttools

        AuraCAD.ActiveDocument.openTransaction("Purge FEM results")
        resulttools.purge_results(self.active_analysis)
        AuraCAD.ActiveDocument.commitTransaction()


class _SolverCalculixContextManager:

    def __init__(self, make_name, cli_obj_ref_name):
        self.make_name = make_name
        self.cli_name = cli_obj_ref_name

    def __enter__(self):
        ccx_prefs = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Fem/Ccx")
        AuraCAD.ActiveDocument.openTransaction("Create SolverCalculiX")
        AuraCADGui.addModule("ObjectsFem")
        AuraCADGui.addModule("FemGui")
        AuraCADGui.doCommand(
            f"{self.cli_name} = ObjectsFem.{self.make_name}(AuraCAD.ActiveDocument)"
        )
        AuraCADGui.doCommand(
            "{}.AnalysisType = {}".format(self.cli_name, ccx_prefs.GetInt("AnalysisType", 0))
        )
        AuraCADGui.doCommand(
            "{}.EigenmodesCount = {}".format(self.cli_name, ccx_prefs.GetInt("EigenmodesCount", 10))
        )
        AuraCADGui.doCommand(
            "{}.EigenmodeLowLimit = {}".format(
                self.cli_name, ccx_prefs.GetFloat("EigenmodeLowLimit", 0.0)
            )
        )
        AuraCADGui.doCommand(
            "{}.EigenmodeHighLimit = {}".format(
                self.cli_name, ccx_prefs.GetFloat("EigenmodeHighLimit", 1000000.0)
            )
        )
        AuraCADGui.doCommand(
            "{}.IncrementsMaximum = {}".format(
                self.cli_name, ccx_prefs.GetInt("StepMaxIncrements", 2000)
            )
        )
        AuraCADGui.doCommand(
            "{}.TimeInitialIncrement = {}".format(
                self.cli_name, ccx_prefs.GetFloat("TimeInitialIncrement", 1.0)
            )
        )
        AuraCADGui.doCommand(
            "{}.TimePeriod = {}".format(self.cli_name, ccx_prefs.GetFloat("TimePeriod", 1.0))
        )
        AuraCADGui.doCommand(
            "{}.TimeMinimumIncrement = {}".format(
                self.cli_name, ccx_prefs.GetFloat("TimeMinimumIncrement", 0.00001)
            )
        )
        AuraCADGui.doCommand(
            "{}.TimeMaximumIncrement = {}".format(
                self.cli_name, ccx_prefs.GetFloat("TimeMaximumIncrement", 1.0)
            )
        )
        AuraCADGui.doCommand(
            "{}.ThermoMechSteadyState = {}".format(
                self.cli_name, ccx_prefs.GetBool("StaticAnalysis", True)
            )
        )
        AuraCADGui.doCommand(
            "{}.IterationsControlParameterTimeUse = {}".format(
                self.cli_name, ccx_prefs.GetBool("UseNonCcxIterationParam", False)
            )
        )
        AuraCADGui.doCommand(
            "{}.SplitInputWriter = {}".format(
                self.cli_name, ccx_prefs.GetBool("SplitInputWriter", False)
            )
        )
        AuraCADGui.doCommand(
            "{}.MatrixSolverType = {}".format(self.cli_name, ccx_prefs.GetInt("Solver", 0))
        )
        AuraCADGui.doCommand(
            "{}.Output3d = {}".format(self.cli_name, ccx_prefs.GetBool("BeamShellOutput", True))
        )
        AuraCADGui.doCommand(
            "{}.GeometricalNonlinearity = {}".format(
                self.cli_name,
                ccx_prefs.GetBool("NonlinearGeometry", False),
            )
        )

        return self

    def __exit__(self, exc_type, exc_value, trace):
        AuraCADGui.doCommand(f"FemGui.getActiveAnalysis().addObject({self.cli_name})")
        AuraCAD.ActiveDocument.commitTransaction()
        # expand analysis object in tree view
        expandParentObject()
        AuraCAD.ActiveDocument.recompute()


class _SolverCcxTools(CommandManager):
    "The FEM_SolverCalculix ccx tools command definition"

    def __init__(self):
        super().__init__()
        self.pixmap = "FEM_SolverStandard"
        self.menutext = Qt.QT_TRANSLATE_NOOP(
            "FEM_SolverCalculiXCcxTools", "Solver CalculiX Standard"
        )
        self.accel = "S, X"
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_SolverCalculiXCcxTools",
            "Creates a standard FEM solver CalculiX with ccx tools",
        )
        self.is_active = "with_analysis"

    def Activated(self):
        with _SolverCalculixContextManager("makeSolverCalculiXCcxTools", "solver") as cm:
            AuraCADGui.doCommand(f"{cm.cli_name}.MaterialNonlinearity = True")


class _SolverCalculiX(CommandManager):
    "The FEM_SolverCalculiX command definition"

    def __init__(self):
        super().__init__()
        self.pixmap = "FEM_SolverStandard"
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_SolverCalculiX", "Solver CalculiX")
        self.accel = "S, C"
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_SolverCalculiX",
            "Creates a FEM solver CalculiX",
        )
        self.is_active = "with_analysis"

    def Activated(self):
        ccx_prefs = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Fem/Ccx")
        if ccx_prefs.GetBool("ResultAsPipeline", True):
            make_solver = "makeSolverCalculiX"
        else:
            make_solver = "makeSolverCalculiXCcxTools"

        with _SolverCalculixContextManager(make_solver, "solver") as cm:
            AuraCADGui.doCommand(f"{cm.cli_name}.MaterialNonlinearity = True")


class _SolverControl(CommandManager):
    "The FEM_SolverControl command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_SolverControl", "Solver Job Control")
        self.accel = "S, T"
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_SolverControl",
            "Changes solver attributes and runs the calculations for the selected solver",
        )
        self.is_active = "with_solver"

    def Activated(self):
        AuraCADGui.ActiveDocument.setEdit(self.selobj, 0)


class _SolverElmer(CommandManager):
    "The FEM_SolverElmer command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_SolverElmer", "Solver Elmer")
        self.accel = "S, E"
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_SolverElmer", "Creates a FEM solver Elmer")
        self.is_active = "with_analysis"

    def Activated(self):
        AuraCAD.ActiveDocument.openTransaction(f"Create Fem SolverElmer")
        AuraCADGui.addModule("ObjectsFem")
        AuraCADGui.addModule("FemGui")
        # expand parent obj in tree view if selected
        expandParentObject()
        # add the object
        AuraCADGui.doCommand("ObjectsFem.makeSolverElmer(AuraCAD.ActiveDocument)")
        # select only added object
        AuraCADGui.doCommand(
            "FemGui.getActiveAnalysis().addObject(AuraCAD.ActiveDocument.ActiveObject)"
        )
        elmer_prefs = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Fem/Elmer")
        bin_out = elmer_prefs.GetBool("BinaryOutput", False)
        save_id = elmer_prefs.GetBool("SaveGeometryIndex", False)
        AuraCADGui.doCommand(
            "AuraCAD.ActiveDocument.ActiveObject.BinaryOutput = {}".format(bin_out)
        )
        AuraCADGui.doCommand(
            "AuraCAD.ActiveDocument.ActiveObject.SaveGeometryIndex = {}".format(save_id)
        )

        AuraCADGui.Selection.clearSelection()
        AuraCADGui.doCommand(
            "AuraCADGui.Selection.addSelection(AuraCAD.ActiveDocument.ActiveObject)"
        )


class _SolverMystran(CommandManager):
    "The FEM_SolverMystran command definition"

    def __init__(self):
        super().__init__()
        self.pixmap = "FEM_SolverMystran"
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_SolverMystran", "Solver Mystran")
        self.accel = "S, M"
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_SolverMystran", "Creates a FEM solver Mystran")
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_expand_noset_edit"


class _SolverRun(CommandManager):
    "The FEM_SolverRun command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_SolverRun", "Run Solver")
        self.accel = "S, R"
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_SolverRun", "Runs the calculations for the selected solver"
        )
        self.is_active = "with_solver"
        self.tool = None

    def Activated(self):
        from femsolver.run import run_fem_solver

        run_fem_solver(self.selobj)
        AuraCADGui.Selection.clearSelection()
        AuraCAD.ActiveDocument.recompute()


class _SolverZ88(CommandManager):
    "The FEM_SolverZ88 command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_SolverZ88", "Solver Z88")
        self.accel = "S, Z"
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_SolverZ88", "Creates a FEM solver Z88")
        self.is_active = "with_analysis"
        self.do_activated = "add_obj_on_gui_expand_noset_edit"

    def Activated(self):
        AuraCAD.ActiveDocument.openTransaction(f"Create Fem SolverZ88")
        AuraCADGui.addModule("ObjectsFem")
        AuraCADGui.addModule("FemGui")
        # expand parent obj in tree view if selected
        expandParentObject()
        # add the object
        AuraCADGui.doCommand("ObjectsFem.makeSolverZ88(AuraCAD.ActiveDocument)")
        # select only added object
        AuraCADGui.doCommand(
            "FemGui.getActiveAnalysis().addObject(AuraCAD.ActiveDocument.ActiveObject)"
        )
        z88_prefs = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Fem/Z88")
        solver_type = z88_prefs.GetString("Solver", "sorcg")
        maxgs = z88_prefs.GetInt("MaxGS", 100000000)
        maxkoi = z88_prefs.GetInt("MaxKOI", 2800000)

        AuraCADGui.doCommand(f"AuraCAD.ActiveDocument.ActiveObject.SolverType = '{solver_type}'")
        AuraCADGui.doCommand(f"AuraCAD.ActiveDocument.ActiveObject.MatrixMaximum = {maxgs}")
        AuraCADGui.doCommand(f"AuraCAD.ActiveDocument.ActiveObject.VectorMaximum = {maxkoi}")

        AuraCADGui.Selection.clearSelection()
        AuraCADGui.doCommand(
            "AuraCADGui.Selection.addSelection(AuraCAD.ActiveDocument.ActiveObject)"
        )


class _PostFilterGlyph(CommandManager):
    "The FEM_PostFilterGlyph command definition"

    def __init__(self):
        super().__init__()
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_PostFilterGlyph", "Glyph Filter")
        self.accel = "F, G"
        self.tooltip = Qt.QT_TRANSLATE_NOOP(
            "FEM_PostFilterGlyph",
            "Adds a post-processing filter that adds glyphs to the mesh vertices for vertex data visualization",
        )
        self.is_active = "with_vtk_selresult"
        self.do_activated = "add_filter_set_edit"


class _CompSolvers(CommandManager):
    def __init__(self):
        super().__init__()
        self.pixmap = ""
        self.menutext = Qt.QT_TRANSLATE_NOOP("FEM_CompSolvers", "Solvers")
        self.tooltip = Qt.QT_TRANSLATE_NOOP("FEM_CompSolvers", "Creates a FEM solver")
        self.is_active = "with_analysis"
        self.commands = [
            "FEM_SolverCalculiX",
            "FEM_SolverElmer",
            "FEM_SolverMystran",
            "FEM_SolverZ88",
        ]

    def Activated(self, i):
        AuraCADGui.runCommand(self.commands[i])

    def GetCommands(self):
        return self.commands

    def GetDefaultCommand(self):
        gen_prefs = AuraCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Fem/General")
        # DefaultSolver == 0 is "None"
        index = gen_prefs.GetInt("DefaultSolver", 0)
        return (index - 1) if index > 0 else 0


# the string in add command will be the page name on AuraCAD wiki
AuraCADGui.addCommand("FEM_Analysis", _Analysis())
AuraCADGui.addCommand("FEM_ClippingPlaneAdd", _ClippingPlaneAdd())
AuraCADGui.addCommand("FEM_ClippingPlaneRemoveAll", _ClippingPlaneRemoveAll())
AuraCADGui.addCommand("FEM_ConstantVacuumPermittivity", _ConstantVacuumPermittivity())
AuraCADGui.addCommand("FEM_ConstraintBodyHeatSource", _ConstraintBodyHeatSource())
AuraCADGui.addCommand("FEM_ConstraintCentrif", _ConstraintCentrif())
AuraCADGui.addCommand("FEM_ConstraintCurrentDensity", _ConstraintCurrentDensity())
AuraCADGui.addCommand("FEM_ConstraintElectricChargeDensity", _ConstraintElectricChargeDensity())
AuraCADGui.addCommand("FEM_ConstraintElectromagnetic", _ConstraintElectromagnetic())
AuraCADGui.addCommand("FEM_ConstraintFlowVelocity", _ConstraintFlowVelocity())
AuraCADGui.addCommand("FEM_ConstraintInitialFlowVelocity", _ConstraintInitialFlowVelocity())
AuraCADGui.addCommand("FEM_ConstraintInitialPressure", _ConstraintInitialPressure())
AuraCADGui.addCommand("FEM_ConstraintMagnetization", _ConstraintMagnetization())
AuraCADGui.addCommand("FEM_ConstraintSectionPrint", _ConstraintSectionPrint())
AuraCADGui.addCommand("FEM_ConstraintSelfWeight", _ConstraintSelfWeight())
AuraCADGui.addCommand("FEM_ConstraintTie", _ConstraintTie())
AuraCADGui.addCommand("FEM_ElementFluid1D", _ElementFluid1D())
AuraCADGui.addCommand("FEM_ElementGeometry1D", _ElementGeometry1D())
AuraCADGui.addCommand("FEM_ElementGeometry2D", _ElementGeometry2D())
AuraCADGui.addCommand("FEM_ElementRotation1D", _ElementRotation1D())
AuraCADGui.addCommand("FEM_EquationDeformation", _EquationDeformation())
AuraCADGui.addCommand("FEM_EquationElasticity", _EquationElasticity())
AuraCADGui.addCommand("FEM_EquationElectricforce", _EquationElectricforce())
AuraCADGui.addCommand("FEM_EquationElectrostatic", _EquationElectrostatic())
AuraCADGui.addCommand("FEM_EquationFlow", _EquationFlow())
AuraCADGui.addCommand("FEM_EquationFlux", _EquationFlux())
AuraCADGui.addCommand("FEM_EquationHeat", _EquationHeat())
AuraCADGui.addCommand("FEM_EquationMagnetodynamic", _EquationMagnetodynamic())
AuraCADGui.addCommand("FEM_EquationMagnetodynamic2D", _EquationMagnetodynamic2D())
AuraCADGui.addCommand("FEM_EquationStaticCurrent", _EquationStaticCurrent())
AuraCADGui.addCommand("FEM_Examples", _Examples())
AuraCADGui.addCommand("FEM_MaterialEditor", _MaterialEditor())
AuraCADGui.addCommand("FEM_MaterialFluid", _MaterialFluid())
AuraCADGui.addCommand("FEM_MaterialMechanicalNonlinear", _MaterialMechanicalNonlinear())
AuraCADGui.addCommand("FEM_MaterialReinforced", _MaterialReinforced())
AuraCADGui.addCommand("FEM_MaterialSolid", _MaterialSolid())
AuraCADGui.addCommand("FEM_FEMMesh2Mesh", _FEMMesh2Mesh())
AuraCADGui.addCommand("FEM_MeshBoundaryLayer", _MeshBoundaryLayer())
AuraCADGui.addCommand("FEM_MeshClear", _MeshClear())
AuraCADGui.addCommand("FEM_MeshClearGroups", _MeshClearGroups())
AuraCADGui.addCommand("FEM_MeshDisplayInfo", _MeshDisplayInfo())
AuraCADGui.addCommand("FEM_MeshGmshFromShape", _MeshGmshFromShape())
AuraCADGui.addCommand("FEM_MeshGroup", _MeshGroup())
AuraCADGui.addCommand("FEM_MeshNetgenFromShape", _MeshNetgenFromShape())
AuraCADGui.addCommand("FEM_MeshRegion", _MeshRegion())
AuraCADGui.addCommand("FEM_MeshDistance", _MeshDistance())
AuraCADGui.addCommand("FEM_MeshManipulate", _MeshManipulate())
AuraCADGui.addCommand("FEM_MeshAdvanced", _MeshAdvanced())
AuraCADGui.addCommand("FEM_MeshShape", _MeshShape())
AuraCADGui.addCommand("FEM_MeshTransfiniteCurve", _MeshTransfiniteCurve())
AuraCADGui.addCommand("FEM_MeshTransfiniteSurface", _MeshTransfiniteSurface())
AuraCADGui.addCommand("FEM_MeshTransfiniteVolume", _MeshTransfiniteVolume())
AuraCADGui.addCommand("FEM_MeshGMSHRefinement", _GMSHRefine())
AuraCADGui.addCommand("FEM_ResultShow", _ResultShow())
AuraCADGui.addCommand("FEM_ResultsPurge", _ResultsPurge())
AuraCADGui.addCommand("FEM_SolverCalculiXCcxTools", _SolverCcxTools())
AuraCADGui.addCommand("FEM_SolverCalculiX", _SolverCalculiX())
AuraCADGui.addCommand("FEM_SolverControl", _SolverControl())
AuraCADGui.addCommand("FEM_SolverElmer", _SolverElmer())
AuraCADGui.addCommand("FEM_SolverMystran", _SolverMystran())
AuraCADGui.addCommand("FEM_SolverRun", _SolverRun())
AuraCADGui.addCommand("FEM_SolverZ88", _SolverZ88())
AuraCADGui.addCommand("FEM_CompSolvers", _CompSolvers())

if "BUILD_FEM_VTK_PYTHON" in AuraCAD.__cmake__:
    AuraCADGui.addCommand("FEM_PostFilterGlyph", _PostFilterGlyph())

    # setup all visualization commands (register by importing)
    import femobjects.post_lineplot
    import femobjects.post_histogram
    import femobjects.post_table

    from femguiutils import post_visualization

    post_visualization.setup_commands("FEM_PostVisualization")
