import numpy as np
from scipy import signal
import scipy.stats

# Optimized function for feature extraction
def features_v1(data, divide=3, fs=250):
    # data : (C, T) 
    # T: number of samples
    # C: number of channels
    # divide: number of segments to divide the signal

    C, T = data.shape
    result = []
    feature_names = []
    
    segment_size = T // divide  # Calculate segment size once

    for c in range(C):
        signal0 = data[c, :]

        # Full wave rectification
        rectified_signal = np.abs(signal0)

        # Hilbert envelope (compute for each channel only once)
        env = np.abs(signal.hilbert(signal0))

        # RMS
        rms = np.sqrt(np.mean(rectified_signal**2))
        result.append(rms)
        feature_names.append(f"rms_channel_{c}")

        # Variance
        var = np.var(rectified_signal)
        result.append(var)
        feature_names.append(f"var_channel_{c}")

        # Kurtosis and skewness
        kurt = scipy.stats.kurtosis(rectified_signal)
        skew = scipy.stats.skew(rectified_signal)
        result.extend([kurt, skew])
        feature_names.extend([f"kurt_channel_{c}", f"skew_channel_{c}"])

        # Zero crossings
        zc = np.sum(np.diff(np.sign(signal0)) != 0)
        result.append(zc)
        feature_names.append(f"zc_channel_{c}")

        # Hilbert envelope statistics
        mean_env = np.mean(env)
        std_env = np.std(env)
        max_env = np.max(env)
        min_env = np.min(env)

        result.extend([mean_env, std_env, max_env, min_env])
        feature_names.extend([f"mean_env_channel_{c}", f"std_env_channel_{c}", f"max_env_channel_{c}", f"min_env_channel_{c}"])

    return np.array(result), feature_names

