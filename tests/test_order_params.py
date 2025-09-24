import numpy as np
from amop import polarization, nematic_order_2d

def test_polarization_extremes():
    # todo alineado
    th = np.zeros(500)
    v = np.c_[np.cos(th), np.sin(th)]
    assert np.isclose(polarization(v), 1.0, atol=1e-12)

    # direcciones opuestas mitad y mitad => P ~ 0
    th = np.concatenate([np.zeros(250), np.pi * np.ones(250)])
    v = np.c_[np.cos(th), np.sin(th)]
    assert polarization(v) < 1e-6

def test_nematic_aligned_bidirectional():
    # Nemático ideal: mitad en 0, mitad en π
    th = np.concatenate([np.zeros(500), np.pi * np.ones(500)])
    S, _ = nematic_order_2d(th)
    assert np.isclose(S, 1.0, atol=1e-12)

def test_nematic_random_uniform():
    rng = np.random.default_rng(2)
    th = rng.uniform(-np.pi, np.pi, size=2000)
    S, _ = nematic_order_2d(th)
    assert S < 0.1  # cercano a 0 para distribución uniforme
