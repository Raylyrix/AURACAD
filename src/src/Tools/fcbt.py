#!python
# SPDX-License-Identifier: LGPL-2.1-or-later

#  AuraCAD Build Tool
# (c) 2004 Juergen Riegel


import sys

help1 = """
AuraCAD Build Tool
Usage:
   auracadbt <command name> [command parameter]
possible commands are:
 - DistSrc         (DS)   Build a source Distr. of the current source tree
 - DistBin         (DB)   Build a binary Distr. of the current source tree
 - DistSetup       (DI)   Build a Setup Distr. of the current source tree
 - DistSetup       (DUI)  Build a User Setup Distr. of the current source tree
 - DistAll         (DA)   Run all three above modules
 - NextBuildNumber (NBN)  Increase the Build Number of this Version
 - CreateModule    (CM)   Insert a new AuraCAD Module in the module directory
 - CreatePyModule  (CP)   Insert a new AuraCAD Python Module in the module directory

For help on the modules type:
  auracadbt <command name> ?

"""

if len(sys.argv) < 2:
    sys.stdout.write(help1)
    sys.stdout.write("Insert command: ")
    sys.stdout.flush()
    CmdRaw = sys.stdin.readline()[:-1]
else:
    CmdRaw = sys.argv[1]

Cmd = CmdRaw.lower()


if Cmd == "distsrc" or Cmd == "ds":
    import auracadbt.DistSrc
elif Cmd == "distbin" or Cmd == "db":
    import auracadbt.DistBin
elif Cmd == "distsetup" or Cmd == "di":
    import auracadbt.DistSetup
elif Cmd == "distsetup" or Cmd == "dui":
    import auracadbt.DistUserSetup
elif Cmd == "distall" or Cmd == "da":
    import auracadbt.DistSrc
    import auracadbt.DistBin
    import auracadbt.DistSetup
elif Cmd == "nextbuildnumber" or Cmd == "nbn":
    import auracadbt.NextBuildNumber
elif Cmd == "createmodule" or Cmd == "cm":
    import auracadbt.CreateModule
elif Cmd == "createpymodule" or Cmd == "cp":
    import auracadbt.CreatePyModule
elif Cmd == "?" or Cmd == "help" or Cmd == "/h" or Cmd == "/?" or Cmd == "-h" or Cmd == "-help":
    sys.stdout.write(help1)
else:
    print(CmdRaw + " is an unknown command!\n")
    sys.exit(1)
