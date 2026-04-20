# AuraCAD - Professional CAD System
# Built on FreeCAD

<div align="center">
<img width="400" src="docs/logo.png" alt="AuraCAD">
</div>

---

## Build Status

| Platform | Status |
|----------|--------|
| Linux | ![Build](https://github.com/Raylyrix/AURACAD/workflows/Build/badge.svg) |
| Windows | ![Build](https://github.com/Raylyrix/AURACAD/workflows/Build/badge.svg) |
| Docker | ![Docker](https://github.com/Raylyrix/AURACAD/workflows/Docker/badge.svg) |

---

## Getting Started

### Quick Build (Linux)

```bash
git clone https://github.com/Raylyrix/AURACAD.git
cd AURACAD/src
mkdir build && cd build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja
./bin/AuraCAD
```

### Docker

```bash
docker build -t auracad:latest .
docker run -it auracad:latest
```

### GitHub Actions

Builds run automatically on push to main branch.

---

## License

See LICENSE file in src/ directory.

---

*AuraCAD - Professional CAD for Industry*