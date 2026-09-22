# Hardware

| Folder | Content |
|---|---|
| `mechanical/cad/step` | Machined actuator parts: motor adapter, ball-screw nut adapter, brackets D2/D3 |
| `mechanical/cad/stl` | Ball-screw nut adapter, rail connector, 3D-printed electronics box |
| `mechanical/cad/inventor` | Autodesk Inventor sources for the electronics box (vendor models of the Pi, bearing and button not included) |
| `mechanical/renders` | Preview images of the STL parts |
| `mechanical/sizing` | Motor-torque sizing: Mathematica notebook, PDF printout and Python port (`python torque_calculation.py` reproduces Table 1 of the paper) |
| `electronics/pdb` | Power Distribution Board: Gerbers, EasyEDA sources, BOM, schematic and layout images |

Build instructions: [docs/02_mechanical_build.md](../docs/02_mechanical_build.md) and [docs/03_electronics.md](../docs/03_electronics.md).
