import numpy as np
from amop import polarization, nematic_order_2d

def test_polarization_rotation_invariance():
    rng = np.random.default_rng(0)
    angles = rng.uniform(-np.pi, np.pi, size=500)
    v = np.c_[np.cos(angles), np.sin(angles)]
    P0 = polarization(v)

    phi = 1.234
    R = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])
    v_rot = v @ R.T
    P1 = polarization(v_rot)

    assert np.isclose(P0, P1, atol=1e-12)

def test_nematic_invariance_to_pi_shift():
    rng = np.random.default_rng(1)
    th = rng.uniform(-np.pi, np.pi, size=500)
    S0, psi0 = nematic_order_2d(th)
    S1, psi1 = nematic_order_2d(th + np.pi)  # nemático es invariante a giro de π
    assert np.isclose(S0, S1, atol=1e-12)
    # el director puede cambiar por ~π/2, comprobamos que S es el mismo
