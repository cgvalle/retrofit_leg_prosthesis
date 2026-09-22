# Software: `leg` package

Runs on a Raspberry Pi 4. Setup: [docs/04_raspberry_pi_setup.md](../docs/04_raspberry_pi_setup.md).

```bash
docker compose up -d                          # MQTT broker (nanomq)

python -m leg.io.stream                       # OpenBCI Cyton -> filtered EMG -> MQTT "data"
python -m leg.simulation.synthetic_stream     # same, from the BrainFlow synthetic board (no hardware)
python -m leg.plots.stream_plot               # live EMG plot

python -m leg.io.store_stream                 # record to recordings/<name>.npy
python -m estimulos.test                      # relax / contract cue sequence for training data
python -m leg.models.train <name> [<name> ...]   # train -> model.pkl

python -m leg.models.realtime_inference       # EMG-driven knee control (--debug: no motor)
python -m leg.models.gait_csv_sender          # predefined gait-pattern control (--debug: no motor)
```

| Path | Purpose |
|---|---|
| `leg/parameters.py` | MQTT host (`LEG_BROKER_HOST`), channel layout, sample rate |
| `leg/io/stream.py` | Cyton configuration, stateful 20–120 Hz band-pass + 50 Hz notch, auto-reconnect |
| `leg/models/features.py` | 9 features per channel (RMS, VAR, kurtosis, skewness, ZC, Hilbert-envelope mean/std/max/min) |
| `leg/models/split.py` | Windowing (25 samples) and train/test split |
| `leg/models/motor_pid.py` | AS5600 reading, encoder calibration, PID, BTS7960 drive (GPIO 13 / 18) |
| `test_code/` | Stand-alone bench tests for the encoder, motor direction, PWM and PID |
| `knee_angle_gait*.csv` | Reference trajectories for gait-pattern mode |
