"""Generate a simulated ECG signal.

Used in the NumPy session. The signal is entirely synthetic: it is built from
mathematical curves, not recorded from anyone. No patient data is used in this
course, and none should ever be committed to a repository.

    from ecg_signal import simulate
    t, signal = simulate(seconds=10, bpm=72)

A real ECG beat has three visible parts, and this builds each one as a bump of
a different height and width:

    P wave    small bump, atria contracting
    QRS       tall sharp spike, ventricles contracting
    T wave    medium bump, ventricles recovering

The tall spike in the middle of QRS is the R peak. Counting R peaks over a
known duration is how you measure heart rate, which is the exercise this
signal exists for.
"""
import numpy as np

SAMPLE_RATE = 250          # samples per second, typical for a clinical monitor
DEFAULT_BPM = 72

# (centre relative to the start of a beat, height in mV, width in seconds)
WAVES = (
    (0.20, 0.12, 0.025),   # P
    (0.36, -0.15, 0.008),  # Q
    (0.38, 1.20, 0.008),   # R, the tall spike
    (0.40, -0.25, 0.008),  # S
    (0.58, 0.30, 0.040),   # T
)


def _bump(t, centre, height, width):
    """One smooth bump (a Gaussian) centred at `centre`."""
    return height * np.exp(-0.5 * ((t - centre) / width) ** 2)


def simulate(seconds=10.0, bpm=DEFAULT_BPM, sample_rate=SAMPLE_RATE,
             noise=0.02, seed=0):
    """Return (time, signal), both 1-D NumPy arrays of the same length.

    seconds     how long the recording is
    bpm         beats per minute
    sample_rate how many measurements per second
    noise       size of the random wobble; set to 0 for a clean signal
    seed        fixes the random noise so everyone sees the same picture
    """
    if seconds <= 0:
        raise ValueError("seconds must be positive")
    if bpm <= 0:
        raise ValueError("bpm must be positive")

    t = np.linspace(0, seconds, int(seconds * sample_rate), endpoint=False)
    beat_length = 60.0 / bpm

    # Where we are within the current beat, for every point in time.
    phase = np.mod(t, beat_length)

    signal = np.zeros_like(t)
    for centre, height, width in WAVES:
        signal += _bump(phase, centre * beat_length / 0.833, height, width)

    if noise:
        rng = np.random.default_rng(seed)
        signal += rng.normal(0, noise, size=signal.shape)

    return t, signal


def r_peaks(signal, threshold=0.6):
    """Indices where the signal rises above `threshold` and is a local maximum.

    This is the simplest possible peak finder and it is good enough for a
    clean simulated signal. Real ECG analysis needs considerably more care.
    """
    above = signal > threshold
    higher_than_before = np.r_[True, signal[1:] > signal[:-1]]
    higher_than_after = np.r_[signal[:-1] > signal[1:], True]
    return np.where(above & higher_than_before & higher_than_after)[0]


def heart_rate(signal, sample_rate=SAMPLE_RATE, threshold=0.6):
    """Estimated beats per minute, from the spacing between R peaks."""
    peaks = r_peaks(signal, threshold)
    if len(peaks) < 2:
        raise ValueError("need at least two peaks to estimate a rate")
    gaps_in_seconds = np.diff(peaks) / sample_rate
    return float(60.0 / gaps_in_seconds.mean())


if __name__ == "__main__":
    t, signal = simulate(seconds=10, bpm=72)
    print("samples        :", signal.size)
    print("duration       : {:.1f} s".format(t[-1]))
    print("R peaks found  :", len(r_peaks(signal)))
    print("estimated rate : {:.1f} bpm".format(heart_rate(signal)))
