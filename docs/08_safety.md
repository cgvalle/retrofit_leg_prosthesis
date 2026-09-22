# 8. Safety

This device moves a joint that a person is standing on. Treat every powered session as a clinical experiment: get ethics approval, have a prosthetist and an engineer present, and use a harness or parallel bars for early trials.

## Failure behaviour you must know

| Situation | What happens | Mitigation |
|---|---|---|
| E-stop pressed | The relay cuts the 12 V motor supply. The Pi keeps running. **The knee locks at its current angle** (the worm gear is self-locking) | Train the user and the assistant to press it. Test it at the start of every session |
| Battery empty or power lost | Same as the E-stop: the knee locks where it is. The passive 3R15 cannot swing | Check the charge (Makita gauge) before each session; one battery lasts about 2.5 h of walking |
| EMG stream stalls (dongle drop-out) | `leg.io.stream` tries to re-open the session, but **the inference keeps classifying the last buffer**, so the reference can drift to a limit | Watch the live plot and keep the E-stop ready. Adding a watchdog is on the roadmap |
| Control process crashes | Ctrl-C drives the knee to full extension, but an unhandled crash can leave a PWM pin in its last state | Keep the E-stop reachable. Bench-test after every software change |
| Misclassification | Each false prediction moves the reference 5° the wrong way (at most 50°/s) | Start with the prosthesis off the user, then in parallel bars |

## Before every session

- [ ] Battery charged; E-stop tested (0 V on the motor with the button pressed)
- [ ] All actuator fasteners and the screw coupling checked; no play at the nut or supports
- [ ] Encoder reads 0° at full extension and tracks flexion correctly up to 85° (`test_code/encoder.py`)
- [ ] Classifier trained or validated **today** with the electrodes as placed (see [06](06_training.md))
- [ ] Live EMG looks clean on all four channels
- [ ] Controller run in `--debug` mode first: the reference follows contract/relax as expected
- [ ] First motor movements done with the user seated and the foot off the ground

## Electrical

- Use a bench supply with current limiting for the first PDB power-up.
- The BTS7960 can source tens of amps. Watch its temperature under sustained load, and fuse the battery line.
- Li-ion packs: use the original charger, never charge unattended, and keep the pack in its impact-resistant case.

## Mechanical

- The actuator adds about 4 kg, mostly distal, which the user feels during fast leg movements.
- Check the ball screw's travel at both ends. At full extension the nut must not bottom out, because the motor has no end-stop sensing in the current software.
