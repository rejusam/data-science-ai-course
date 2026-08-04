"""Tests for the simulated ECG generator used in the NumPy session."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                       / "modules" / "01a-programming-fundamentals"))

import ecg_signal  # noqa: E402


def test_shapes_match():
    t, signal = ecg_signal.simulate(seconds=4)
    assert t.shape == signal.shape
    assert t.ndim == 1


def test_sample_count_follows_rate_and_duration():
    _, signal = ecg_signal.simulate(seconds=4, sample_rate=100)
    assert signal.size == 400


def test_seed_makes_it_reproducible():
    _, a = ecg_signal.simulate(seconds=3, seed=7)
    _, b = ecg_signal.simulate(seconds=3, seed=7)
    assert np.array_equal(a, b)


def test_different_seeds_differ():
    _, a = ecg_signal.simulate(seconds=3, seed=1)
    _, b = ecg_signal.simulate(seconds=3, seed=2)
    assert not np.array_equal(a, b)


def test_noise_zero_is_clean():
    _, signal = ecg_signal.simulate(seconds=3, noise=0)
    _, again = ecg_signal.simulate(seconds=3, noise=0, seed=99)
    assert np.array_equal(signal, again)


def test_rejects_bad_duration():
    with pytest.raises(ValueError):
        ecg_signal.simulate(seconds=0)


def test_rejects_bad_bpm():
    with pytest.raises(ValueError):
        ecg_signal.simulate(bpm=-10)


@pytest.mark.parametrize("bpm,seconds,expected", [
    (60, 10, 10),
    (72, 10, 12),
    (120, 5, 10),
])
def test_peak_count_matches_beats(bpm, seconds, expected):
    _, signal = ecg_signal.simulate(seconds=seconds, bpm=bpm, noise=0)
    assert len(ecg_signal.r_peaks(signal)) == expected


@pytest.mark.parametrize("bpm", [50, 60, 72, 90, 120])
def test_heart_rate_recovers_the_input(bpm):
    _, signal = ecg_signal.simulate(seconds=20, bpm=bpm, noise=0)
    assert ecg_signal.heart_rate(signal) == pytest.approx(bpm, rel=0.02)


def test_heart_rate_survives_noise():
    _, signal = ecg_signal.simulate(seconds=20, bpm=72, noise=0.02)
    assert ecg_signal.heart_rate(signal) == pytest.approx(72, rel=0.05)


def test_heart_rate_needs_two_peaks():
    _, signal = ecg_signal.simulate(seconds=0.4, bpm=60, noise=0)
    with pytest.raises(ValueError):
        ecg_signal.heart_rate(signal)


def test_r_peaks_are_the_tallest_points():
    _, signal = ecg_signal.simulate(seconds=6, bpm=60, noise=0)
    peaks = ecg_signal.r_peaks(signal)
    assert signal[peaks].min() > 1.0  # R waves are ~1.2 mV
