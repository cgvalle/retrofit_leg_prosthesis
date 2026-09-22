# 10. Known limitations and roadmap

## Limitations of this prototype

- **Actuator authority.** The 5840-31ZY motor gives 0.49 N·m, but level walking needs 0.77–1.53 N·m (`hardware/mechanical/sizing`). Assistance is partial, and fast tasks (stairs, obstacle clearance, high steps, sit-to-stand) are out of reach. At CYBATHLON 2024 only Slopes (both runs) and Wobbly Steps (run 2) were completed.
- **Non-back-drivable transmission.** It holds position without power, but it removes free pendular swing, so all knee motion has to come from the torque-limited motor.
- **Binary intent.** Contract/relax commands only change the reference in steps. There is no proportional control of speed, torque or impedance, and no automatic gait-phase detection.
- **EMG robustness.** Intermittent drop-outs of the OpenBCI stream were seen, with no conclusive cause. The classifier was validated offline on static trials (83.2 %), not during walking.
- **Mass.** The module adds about 4 kg, mostly distal, for a total of about 8 kg.
- **Evidence.** Everything was tested with a single participant.

## Software to-dos

- Watchdog: stop the motor if no EMG packet arrives within about 200 ms.
- End-of-travel protection: stall-current sensing through the BTS7960 `IS` pins, or limit switches.
- Soft-start PWM ramps. The driver currently switches straight to 100 % duty.

## Hardware roadmap (CPS-RTC internal design review, 2026)

- Battery: move from the 3S Li-ion Makita pack (16.2 Wh, 1–2 C) to a 4S LiPo (22.2 Wh, 35 C) with an external BMS and XT60 connector. The LTC3780 then runs in buck mode (≈95–96 % efficiency).
- Motor: a candidate is the maxon RE 30 (60 W, 12 V, 87 % peak efficiency) with a GP32 A planetary gearhead. Its high start-up current (about 61 A) needs a PWM soft start over 30–50 ms, because the 12 V rail is limited to 8–10 A. The review also recommends moving to a BLDC motor with a matching three-phase driver.
- Characterise the torque–speed demand of the knee for each task before choosing the next actuator.
- Mount the motor at the knee to reduce distal mass.
- Environment sensing (2D LiDAR, IMU) for terrain-aware control.
