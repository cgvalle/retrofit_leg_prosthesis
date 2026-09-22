# 1. Bill of materials

Quantities are for one prosthesis. The table assumes the user already has a prescribed passive prosthesis built around an **Ottobock 3R15** knee. The add-on keeps that socket, knee, pylons and foot.

Items marked **TBD** could not be confirmed from the project records; measure them on your build.

## Host prosthesis (already prescribed to the user)

| Item | Qty | Notes |
|---|---|---|
| Ottobock 3R15 monocentric knee joint | 1 | Steel, 490 g, max. user mass 100 kg, flexion up to 150° |
| Custom socket | 1 | Made by the user's prosthetist. The EMG electrodes are embedded in its inner wall (see [05](05_emg_acquisition.md)) |
| Upper tube / stem | 1 | Aluminium, Ø 32.4 mm, 120 mm long (CYBATHLON 2024 build) |
| Lower tube / stem | 1 | Aluminium, Ø 32.4 mm, 320 mm long (CYBATHLON 2024 build) |
| Prosthetic foot and pyramid adapters | 1 set | Whatever the user already wears |

## Actuator

| Item | Qty | Notes |
|---|---|---|
| Brushed DC worm-gear motor, 12 V, **5840-31ZY**, 200 rpm variant (31:1) | 1 | 0.49 N·m nominal at 200 rpm, 2 A, 364 g. The worm gear is **self-locking**. See the torque note below |
| Ball-screw kit **SFU1610** (Ø16 mm, lead 10 mm, C5) with **BK12** fixed and **BF12** floating supports and a nut | 1 | Sold as a kit, cut to length. The prototype screw spans 294–384 mm between attachment points |
| Shaft coupling, motor → screw | 1 | Set-screw adapter, sized to the motor output shaft |
| Motor adapter (machined) | 1 | `hardware/mechanical/cad/step/motor_adapter.step` |
| Ball-screw nut adapter | 1 | `hardware/mechanical/cad/step/ballscrew_nut_adapter.step` (STL also provided) |
| Rail connector | 1 | `hardware/mechanical/cad/stl/rail_connector.stl` |
| Brackets D2 / D3 | 1 each | `hardware/mechanical/cad/step/D2.step`, `D3.step`, `D3_v2.step` |
| Fasteners (M3–M6), spacers | TBD | Depends on your knee and tube clamps |

> **Torque note.** The installed motor is **under-sized**: level walking needs 0.77–1.53 N·m at the motor shaft (see `hardware/mechanical/sizing/torque_calculation.py`), but the motor gives 0.49 N·m. The prototype therefore provides only partial assistance. If you are rebuilding the device, consider a stronger drive (see [10](10_limitations_and_roadmap.md)).

## Electronics

| Item | Qty | Notes |
|---|---|---|
| Raspberry Pi 4 Model B (2 GB or more) + microSD card (16 GB or more) | 1 | Runs all software |
| OpenBCI Cyton (8-ch, 250 Hz, 24-bit) + USB RF dongle | 1 | Only channels C1–C4 are used for control |
| AS5600 magnetic angle encoder breakout + diametric magnet | 1 | I²C address 0x36, 12-bit |
| Power Distribution Board (PDB) | 1 | Custom PCB. See `hardware/electronics/pdb/PDB_BOM.csv` for its parts (LTC3780, LM2596 and BTS7960 modules, SRD-05VDC relay, etc.) |
| Emergency-stop push button, self-locking (e.g. LAY37 series) | 1 | Wired to PDB connector CN9. Cuts **only** the motor supply |
| Battery: Makita 12 V max Li-ion, 1.5 Ah (3S, 10.8 V nominal) | 1–2 | About 2.5 h of walking per charge. Needs a Makita battery-slot adapter with a keyed connector |
| 3D-printed electronics box | 1 | `hardware/mechanical/cad/stl/electronics_box.stl` (91 × 63 × 117 mm). Holds the Pi and the E-stop |
| JST-XH 2.5 mm housings and crimp contacts, silicone wire (18 AWG for the motor, 24 AWG for signals) | — | |

## EMG consumables

| Item | Qty | Notes |
|---|---|---|
| Gold cup electrodes | 9 | 4 bipolar pairs + 1 common reference at the hip |
| Conductive paste (e.g. Ten20) | — | |
| Isopropyl alcohol wipes | — | Clean the skin before donning |

## Tools

- Access to a CNC mill or lathe, or a machining service, for the metal adapters.
- FDM 3D printer (PETG or ABS) for the electronics box.
- Soldering station and multimeter; a bench supply with current limit is strongly recommended for bring-up.
- PCB fabrication service (the Gerbers are ready for JLCPCB).
