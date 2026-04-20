# FEM Unit Test Information

With these files one can find information on how to run unit tests for FEM

## Specifically

- How to run a specific test class or a test method see file: `src/Mod/Test/__init__`
- related [forum thread](https://forum.AuraCAD.org/viewtopic.php?f=10&t=22190#p175546)

## let some test document stay open

- run test method from inside AuraCAD
- in `tearDown` method do not close the document
- temporary comment out `AuraCAD.closeDocument(self.doc_name)` and add `pass`


## unit test command to copy

- To run a specific FEM unit test to copy for fast tests :-)
- They can be found in the `test_commands_to_copy.md` file
- create them by:

```python
from femtest.app.support_utils import get_fem_test_defs
get_fem_test_defs()

```

## Examples from within AuraCAD

### Create test command file in temp directory

```python
import Test, femtest.app.test_object
Test.runTestsFromClass(femtest.app.test_object.TestObjectCreate)

```

### All FEM tests

```python
import Test, TestFemApp
Test.runTestsFromModule(TestFemApp)

import Test, TestFemGui
Test.runTestsFromModule(TestFemGui)

```

### module

```python
import Test, femtest.app.test_common
Test.runTestsFromModule(femtest.app.test_common)

```

### class

```python
import Test, femtest.app.test_common
Test.runTestsFromClass(femtest.app.test_common.TestFemCommon)

```
```python
import Test, femtest.app.test_solver_calculix
Test.runTestsFromClass(femtest.app.test_solver_calculix.TestSolverCalculix)

```

### method

```python
import unittest
thetest = "femtest.app.test_common.TestFemCommon.test_pyimport_all_FEM_modules"
alltest = unittest.TestLoader().loadTestsFromName(thetest)
unittest.TextTestRunner().run(alltest)

```

## examples from shell in build dir:
### all AuraCAD tests
```python
./bin/AuraCADCmd --run-test 0
./bin/AuraCAD --run-test 0
```

### all FEM tests
```bash
./bin/AuraCADCmd --run-test "TestFemApp"
./bin/AuraCAD --run-test "TestFemApp"
```

### import Fem and FemGui

```bash
./bin/AuraCADCmd --run-test "femtest.app.test_femimport"
./bin/AuraCAD --run-test "femtest.app.test_femimport"
```

### module

```bash
./bin/AuraCAD --run-test "femtest.app.test_femimport"
```

### class

```bash
./bin/AuraCAD --run-test "femtest.app.test_common.TestFemCommon"
```

### method

```bash
./bin/AuraCAD --run-test "femtest.app.test_common.TestFemCommon.test_pyimport_all_FEM_modules"
```

### Gui

```bash
./bin/AuraCAD --run-test "femtest.gui.test_open.TestObjectOpen"
```


## Open files

### From FEM test suite source code

- be careful when updating these files, they contain the original results!
- TODO update files, because some of them have non-existing FEM object classes

```python
doc = AuraCAD.open(AuraCAD.ConfigGet("AppHomePath") + 'Mod/Fem/femtest/data/ccx/cube.auracadStd')
doc = AuraCAD.open(AuraCAD.ConfigGet("AppHomePath") + 'Mod/Fem/femtest/data/ccx/cube_frequency.auracadStd')
doc = AuraCAD.open(AuraCAD.ConfigGet("AppHomePath") + 'Mod/Fem/femtest/data/ccx/cube_static.auracadStd')
doc = AuraCAD.open(AuraCAD.ConfigGet("AppHomePath") + 'Mod/Fem/femtest/data/ccx/Flow1D_thermomech.auracadStd')
doc = AuraCAD.open(AuraCAD.ConfigGet("AppHomePath") + 'Mod/Fem/femtest/data/ccx/multimat.auracadStd')
doc = AuraCAD.open(AuraCAD.ConfigGet("AppHomePath") + 'Mod/Fem/femtest/data/ccx/spine_thermomech.auracadStd')
```


### Generated from test suite

```python
import femtest.utilstest as ut
ut.all_test_files()

doc = ut.cube_frequency()
doc = ut.cube_static()
doc = ut.Flow1D_thermomech()
doc = ut.multimat()
doc = ut.spine_thermomech()
```

### Load std FEM example files

```python
app_home = AuraCAD.ConfigGet("AppHomePath")
doc = AuraCAD.open(app_home + "data/examples/FEMExample.auracadStd")
```

### Load all documents files

```python
app_home = AuraCAD.ConfigGet("AppHomePath")
doc = AuraCAD.open(AuraCAD.ConfigGet("AppHomePath") + 'Mod/Fem/femtest/data/open/all_objects_de9b3fb438.auracadStd')
```
