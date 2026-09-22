# 2. Mechanical build

The add-on is a linear actuator mounted **in parallel** with the passive knee. A ball screw joins a point fixed to the thigh side of the 3R15 (**A**) to a point fixed to the shank (**B**). When the screw gets longer the knee extends, and when it gets shorter the knee flexes. The knee, socket, alignment and load path are left untouched, so the module can be removed and the user gets their passive prosthesis back.

![Overview](img/prosthesis_overview.png)

## Geometry

Coordinates are measured from the knee centre **K** in the sagittal plane (mm):

| Symbol | Value | Meaning |
|---|---|---|
| a1 | 90 | Thigh attachment A, vertical distance above K |
| a2 | 50 | Thigh attachment A, horizontal offset |
| k1 | 295 | Shank attachment B, vertical distance below K (280 + 15) |
| k2 | 50 | Shank attachment B, horizontal offset |
| screw length | 384 mm at 1° flexion → 294 mm at 64° | Travel used for walking |

With these dimensions the knee reaches 0° (full extension) at 385 mm and about 75° flexion at 275 mm.

The moment arm of the screw about the knee is

```
r⊥ = |x_A·y_B − y_A·x_B| / |AB|
```

and the knee torque is `τ_K = F · r⊥`, where `F = 2π·τ_motor·η_screw / L`.

`hardware/mechanical/sizing/torque_calculation.py` reproduces Table 1 of the paper:

| Knee angle | Screw length | Motor torque needed for 44.3 N·m at the knee |
|---|---|---|
| 1° | 384 mm | 1.53 N·m |
| 5° | 380 mm | 1.40 N·m |
| 37.4° | 339 mm | 0.89 N·m |
| 64.1° | 294 mm | 0.77 N·m |

The load case is 0.49 N·m/kg (peak extension moment in level walking) × 90.36 kg (user + prosthesis). If you change the attachment points, edit the constants at the top of the script and re-run it to check your motor.

## Parts

| File | Part | Suggested process |
|---|---|---|
| `cad/step/motor_adapter.step` | Motor flange / shaft adapter | CNC, aluminium 6061 |
| `cad/step/ballscrew_nut_adapter.step`, `cad/stl/ballscrew_nut_adapter.stl` | Adapter from the SFU1610 flange nut to the thigh-side attachment | CNC, aluminium or steel |
| `cad/stl/rail_connector.stl` | Rail / screw connector | CNC or 3D print (check the loads) |
| `cad/step/D2.step`, `D3.step`, `D3_v2.step` | Brackets (D3 v2 supersedes D3) | CNC, aluminium |
| `cad/stl/electronics_box.stl` | Housing for the Raspberry Pi and E-stop, mounted below the socket | FDM, PETG |
| `cad/inventor/*` | Autodesk Inventor sources for the electronics box (2025 revision) | — |

Renders are in `hardware/mechanical/renders/`. The Inventor assembly `raspi.iam` references the vendor models of the Raspberry Pi 4, the 626-2Z bearing and the LAY37 button. Those are not redistributed here; download them from the vendors or replace them in the assembly.

## Assembly sequence

1. **Strip the host prosthesis** down to the 3R15 knee plus its upper and lower tubes. Record the alignment (tube lengths, clamp rotations) so it can be restored exactly.
2. **Motor end (shank side).** Bolt the motor adapter and the BK12 fixed support to the lower tube. The BK12 takes the axial load, so it must sit at the motor end. Couple the motor output shaft to the screw with the set-screw coupling. Tighten the set screw on a flat and secure it with threadlocker.
3. **Free end (thigh side).** Mount the BF12 floating support. Fix the ball-screw nut to the nut adapter, and fix that to the thigh-side attachment (point A) on the upper stem.
4. **Check the range by hand** before powering anything. Turn the screw to run the knee from full extension to at least 85° flexion. Nothing may collide, and the screw must not bottom out on the nut at either end. Measure the screw length at full extension and at full flexion.
5. **Mount the AS5600 encoder** on the knee axis, or on an external arm linking the upper and lower stems, with the diametric magnet centred on the sensor at the gap recommended in its datasheet (about 0.5–3 mm).
6. **Mount the electronics box** below the socket (the white box in the photo) and route the cables along the tubes with strain relief. The battery and PDB enclosure goes on the lateral side of the shank.
7. **Restore the original alignment** with the prosthetist. The module adds about 4 kg, mostly distal. Check it with the user standing, before any powered test.

> [!IMPORTANT]
> The worm gear cannot be back-driven. Once the motor is mounted **the user can no longer swing the shank freely**, and the knee holds whatever angle it was last driven to, even with the E-stop pressed. Plan the first powered tests with the prosthesis off the user (see [08](08_safety.md)).
