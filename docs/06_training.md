# 6. Training the intent classifier

The controller needs a binary classifier: **0 = relaxed**, **1 = voluntary contraction**. Train it for each user, and retrain whenever the electrodes are repositioned.

## 1. Record labelled data

Three terminals on the Pi, with the user seated and wearing the socket:

```bash
# Terminal 1: EMG stream
python -m leg.io.stream

# Terminal 2: recorder (asks for a file name, press q + Enter to stop)
python -m leg.io.store_stream          # e.g. name: user01_session01

# Terminal 3: cue sequence
python -m estimulos.test
```

`estimulos/test.py` publishes markers on the `marker` topic, and the stream writes them into the recording's marker channel:

- It starts with marker **0** (idle), then shows a 4 s countdown.
- Then come **20 trials of 4 s**, alternating **"Relaja!" (relax, marker 1)** and **"Contrae!" (contract, marker 2)**. The prompt is shown on screen; translate the strings in `estimulos/test.py` if needed.
- It ends with marker **0**.

Stop the recorder after the "Fin del experimento" message. The file is saved as `recordings/<name>.npy` with shape `(14, samples)`: EMG C1–C8, accelerometer, time, packet counter, marker.

Record several sessions: different days, and seated as well as standing. Trials recorded only while seated generalise poorly to walking.

## 2. Train

```bash
python -m leg.models.train user01_session01 user01_session02
```

`leg/models/train.py` then does the following:

1. Keeps samples with marker 1 or 2, and maps 2 → class 1 (contraction) and 1 → class 0 (rest).
2. Cuts channels **C1–C4** into non-overlapping **0.1 s windows (25 samples)**. 20 % of the windows are held out at random for testing (seed 42).
3. Extracts **9 features per channel, 36 in total**, with `leg.models.features_v1`: RMS, variance, kurtosis, skewness, zero-crossings, and the mean, standard deviation, max and min of the Hilbert envelope. Windows with invalid (NaN or inf) features are removed.
4. Fits a pipeline: **feature normalisation** (z-score) → **ANOVA F-score selection of the top 10 features** (`--k` to change) → **Random Forest**. The forest's hyperparameters are tuned by grid search (`n_estimators` 10–100, `max_depth` None/10/20, `min_samples_split` 2/5; 3-fold CV).
5. Prints the cross-validation and held-out accuracy, the confusion matrix, per-class precision/recall/F1, and the selected features ranked by importance.
6. Saves the whole pipeline to **`model.pkl`** in the current directory. It takes all 36 features as input, so the controller needs no changes when `--k` changes.

Run the controller from the same directory so it finds `model.pkl`.

## Expected performance

On the paper's pilot, 645 training and 161 test windows gave:

| | Predicted rest | Predicted contraction |
|---|---|---|
| True rest | 68 | 17 |
| True contraction | 10 | 66 |

That is **83.2 % accuracy**, with contraction precision 0.80, recall 0.87 and F1 0.83. Accuracy was 84.9 % on steady windows but only 55.6 % on windows at a rest↔contraction transition. Keeping the top 10 features gave 83.7 % cross-validation accuracy, against 84.7 % with all 36. Performance plateaus at about 10 features, and envelope-amplitude features from C3 (gluteus medius) dominate the selection.

If you get well below about 80 %, check electrode contact first (see [05](05_emg_acquisition.md)). Then check that the user is making a clear, repeatable contraction rather than a small one.
