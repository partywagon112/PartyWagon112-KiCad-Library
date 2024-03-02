#!/bin/bash

mkdir kicad-latest

git submodule add "https://gitlab.com/kicad/libraries/kicad-symbols.git" kicad-latest/symbols
git submodule add "https://gitlab.com/kicad/libraries/kicad-footprints.git" kicad-latest/footprints
git submodule add "https://gitlab.com/kicad/libraries/kicad-packages3d.git" kicad-latest/3dmodels
