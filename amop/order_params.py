from __future__ import annotations
import numpy as np
from typing import Tuple

def _as_unit(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    if v.ndim != 2:
        raise ValueError("Esperaba un arreglo de shape (N, d)")
    norms = np.linalg.norm(v, axis=1, keepdims=True)
    norms = np.where(norms == 0.0, 1.0, norms)
    return v / norms

def polarization(vectors: np.ndarray) -> float:
    """
    Polarización en d=2 o d=3: |<u>| donde u son vectores unitarios.
    Retorna un escalar en [0,1].
    """
    u = _as_unit(vectors)
    return float(np.linalg.norm(u.mean(axis=0)))

def nematic_order_2d(angles: np.ndarray) -> Tuple[float, float]:
    """
    Orden nemático en 2D para ángulos theta (rad).
    Retorna (S, psi) donde S ∈ [0,1] y psi es el director (rad).
    Fórmulas estándar: 
      c2 = <cos(2θ)>, s2 = <sin(2θ)>
      S = sqrt(c2^2 + s2^2)
      psi = 0.5 * atan2(s2, c2)
    """
    th = np.asarray(angles, dtype=float)
    if th.ndim != 1:
        raise ValueError("angles debe ser 1D (N,)")
    c2 = np.mean(np.cos(2 * th))
    s2 = np.mean(np.sin(2 * th))
    S = float(np.hypot(c2, s2))
    psi = 0.5 * np.arctan2(s2, c2)
    return S, float(psi)
