from __future__ import annotations
import numpy as np
from typing import Dict, Optional, Tuple
from .bootstrap import get_rng

def _wrap_box(x: np.ndarray, L: float) -> np.ndarray:
    return (x + L) % L

def simulate_active_particles(
    n: int = 200,
    steps: int = 200,
    L: float = 20.0,
    speed: float = 0.1,
    eta: float = 0.5,
    radius: float = 1.0,
    seed: Optional[int] = None,
) -> Dict[str, np.ndarray]:
    """
    Simulación mínima tipo Vicsek en 2D con condiciones periódicas.
    - n: # de partículas
    - steps: # de iteraciones
    - L: tamaño de la caja (LxL)
    - speed: módulo de la velocidad
    - eta: amplitud de ruido angular uniforme en [-eta/2, eta/2]
    - radius: radio de interacción métrica
    - seed: semilla local (opcional)

    Retorna un dict con:
      positions: (steps+1, n, 2)
      angles:    (steps+1, n)
      velocities:(steps+1, n, 2)
    """
    rng = np.random.default_rng(seed) if seed is not None else get_rng()

    # estados iniciales
    pos = rng.uniform(0, L, size=(n, 2))
    ang = rng.uniform(-np.pi, np.pi, size=n)

    positions = np.empty((steps + 1, n, 2), dtype=float)
    angles = np.empty((steps + 1, n), dtype=float)
    velocities = np.empty((steps + 1, n, 2), dtype=float)

    positions[0] = pos
    angles[0] = ang
    velocities[0] = np.c_[np.cos(ang), np.sin(ang)] * speed

    for t in range(1, steps + 1):
        # vecinos por distancia (O(N^2), suficiente para ejemplos pequeños)
        dx = pos[:, None, :] - pos[None, :, :]
        # distancias mínimas con condiciones periódicas
        dx = dx - np.round(dx / L) * L
        dist2 = np.sum(dx**2, axis=-1)
        mask = dist2 <= radius**2

        # promedio de direcciones de vecinos
        vx = np.cos(ang)
        vy = np.sin(ang)
        mean_vx = (mask @ vx) / np.clip(mask.sum(axis=1), 1, None)
        mean_vy = (mask @ vy) / np.clip(mask.sum(axis=1), 1, None)

        mean_ang = np.arctan2(mean_vy, mean_vx)

        # ruido
        noise = rng.uniform(-eta / 2.0, eta / 2.0, size=n)
        ang = mean_ang + noise

        vel = np.c_[np.cos(ang), np.sin(ang)] * speed
        pos = _wrap_box(pos + vel, L)

        positions[t] = pos
        angles[t] = ang
        velocities[t] = vel

    return {"positions": positions, "angles": angles, "velocities": velocities}
