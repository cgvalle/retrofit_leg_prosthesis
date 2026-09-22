# 4. Raspberry Pi setup

All the software runs on one Raspberry Pi 4. The processes exchange data through an MQTT broker (nanomq) on the same Pi. The broker also lets a laptop on the same network watch the signals live.

## 1. Operating system

1. Flash **Raspberry Pi OS Lite (64-bit)** with Raspberry Pi Imager.
2. In the Imager's advanced options, set the hostname (e.g. `retrofit-leg`), create a user, enter your Wi-Fi details and **enable SSH**.
3. Boot, SSH in, and update:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git python3-venv python3-dev i2c-tools
```

## 2. Enable I²C and hardware access

```bash
sudo raspi-config nonint do_i2c 0      # enable I2C
sudo usermod -aG gpio,i2c,dialout $USER
sudo reboot
```

With the encoder connected, `i2cdetect -y 1` should show a device at **0x36**.

> The motor code uses `RPi.GPIO`, which works on the Raspberry Pi 4. It does **not** work on a Raspberry Pi 5.

## 3. Install the software

```bash
git clone https://github.com/cgvalle/retrofit_leg_prosthesis.git && cd retrofit_leg_prosthesis/software
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

**BrainFlow** is the library that talks to the OpenBCI board. If `pip install brainflow` does not ship working ARM64 binaries for your OS version (`python -c "from brainflow.board_shim import BoardShim"` fails), build it from source:

```bash
sudo apt install -y cmake build-essential libboost-all-dev
git clone https://github.com/brainflow-dev/brainflow.git && cd brainflow
mkdir build && cd build && cmake .. && make -j4 && sudo make install
cd ../python_package && pip install .
```

## 4. MQTT broker

Install Docker ([official instructions for Debian](https://docs.docker.com/engine/install/debian/)), then:

```bash
cd retrofit_leg_prosthesis/software
docker compose up -d          # starts nanomq on port 1883 (restarts on boot)
```

MQTT topics used:

| Topic | Payload | Producer → consumer |
|---|---|---|
| `data` | float32 array, shape (14, N): 8 EMG, 3 accel, time, packet, marker | `leg.io.stream` → inference, recorder, plots |
| `marker` | integer. During training: 0 = idle, 1 = relax, 2 = contract. During control: the current knee-angle reference | `estimulos/test.py` or the controllers → `leg.io.stream` (stored in the marker channel) |

The broker host defaults to `127.0.0.1`. To run a process on another machine (e.g. the live plot on a laptop), set `export LEG_BROKER_HOST=retrofit-leg.local`.

## 5. Bench tests

Run these with the actuator **decoupled from the user**:

```bash
python test_code/encoder.py          # prints raw and normalised knee angle
python test_code/motor_direction.py  # f / b / s / q to move the motor
python test_code/pid_control.py      # runs the PID loop to a fixed target
```

### Encoder calibration

The knee angle runs from **0° (fully extended) to 85° (flexed)**. `leg/models/motor_pid.py` maps the raw AS5600 angle linearly, using two calibration points:

```python
ESTIRADA = 235   # raw encoder angle (deg) with the knee fully extended
CONTRAIDA = 170  # raw encoder angle (deg) at 90° of knee flexion
```

Move the knee by hand to full extension and then to 90° flexion (measure with a goniometer), read the `raw:` value from `test_code/encoder.py` at each position, and put those numbers into `motor_pid.py`. The controller never commands more than 85°. The raw range must not cross the encoder's 0°/360° wrap point; rotate the magnet if it does.

## 6. Optional: Docker for everything

`docker-compose.cyton.yml` runs the broker, the OpenBCI stream and the inference as containers. `docker/Dockerfile.cyton` expects the BrainFlow source as `brainflow/master.zip` in the build context (download it from GitHub). The inference container copies `model.pkl` from `software/` at build time, so rebuild the image after retraining.
