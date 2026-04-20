# SPDX-License-Identifier: LGPL-2.1-or-later

# this directory is the entry point for namespace modules. Any package
# installed to a directory "AuraCAD" which is in sys.path can be imported
# with "from AuraCAD import package" and is checked for a init_gui.py
# module, which is imported at startup. (AuraCADGuiInit.py)

add_subdirectory(AuraCAD)