"""
Pequeño ejemplo: corre una simulación, calcula parámetros de orden
y los imprime. Si tienes matplotlib instalado, grafica trayectorias.
"""
import numpy as np
from amop import simulate_active_particles, polarization, nematic_order_2d, set_seed

def main():
    set_seed(42)
    out = simulate_active_particles(n=300, steps=300, L=30.0, speed=0.15, eta=0.6, radius=1.2)
    angles = out["angles"][-1]
    vel = out["velocities"][-1]

    P = polarization(vel)
    S, psi = nematic_order_2d(angles)
    print(f"Polarización P ≈ {P:.3f}")
    print(f"Nematic S ≈ {S:.3f}, director psi ≈ {psi:.3f} rad")

    try:
        import matplotlib.pyplot as plt
        pos = out["positions"][-1]
        plt.figure()
        plt.quiver(pos[:,0], pos[:,1], np.cos(angles), np.sin(angles), angles, pivot="mid", scale=20)
        plt.title(f"AMOP demo — P={P:.2f}, S={S:.2f}")
        plt.xlabel("x"); plt.ylabel("y"); plt.axis("equal"); plt.tight_layout()
        plt.show()
    except Exception as e:
        print("(Opcional) Instala matplotlib para ver una figura. Motivo:", e)

if __name__ == "__main__":
    main()
