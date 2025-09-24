from pathlib import Path
import time

from amop import simulate_active_particles, polarization, nematic_order_2d

# --- rutas robustas ---
ROOT = Path(__file__).resolve().parent      # carpeta del script
FIGS = ROOT / "figures"
FIGS.mkdir(parents=True, exist_ok=True)     # crea figures/ si no existe

# --- simulación ---
out = simulate_active_particles(n=300, steps=300)
P = polarization(out["velocities"][-1])
S, psi = nematic_order_2d(out["angles"][-1])
print(P, S, psi)

# --- gráfico rápido + guardado ---
try:
    import numpy as np, matplotlib.pyplot as plt
    pos = out["positions"][-1]
    angles = out["angles"][-1]

    plt.figure()
    plt.quiver(pos[:,0], pos[:,1], np.cos(angles), np.sin(angles),
               angles, pivot="mid", scale=20)
    plt.title(f"AMOP demo — P={P:.2f}, S={S:.2f}")
    plt.xlabel("x"); plt.ylabel("y"); plt.axis("equal"); plt.tight_layout()

    # nombre de archivo con timestamp
    stamp = time.strftime("%Y%m%d-%H%M%S")
    fname = FIGS / f"amop_demo_{stamp}.png"
    plt.savefig(fname, dpi=200, bbox_inches="tight")
    print(f"[AMOP] Figura guardada en: {fname}")

    plt.show()   # opcional: mostrar en pantalla
    plt.close()
except Exception as e:
    print("Gráfico opcional (necesita matplotlib):", e)

