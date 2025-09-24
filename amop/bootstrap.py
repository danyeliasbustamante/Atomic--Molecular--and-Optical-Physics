from __future__ import annotations
import numpy as np
from typing import Optional

# RNG global para reproducibilidad simple en ejemplos/tests
_RNG = np.random.default_rng()

def set_seed(seed: Optional[int] = None) -> None:
    """Fija la semilla global (o usa entropía del SO si seed=None)."""
    global _RNG
    _RNG = np.random.default_rng(seed)

def get_rng() -> np.random.Generator:
    """Devuelve el RNG global (útil para inyectar en funciones)."""
    return _RNG
