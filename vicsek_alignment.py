# vicsek_alignment.py
# Modelo de alineamiento tipo Vicsek (materia activa) con fronteras periódicas.
# Requiere: numpy, matplotlib (y pillow si guardas GIF).

import argparse, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --------------------------- Utilidades ---------------------------

def make_dirs(path="figures"):
    os.makedirs(path, exist_ok=True)
    return path

def minimum_image_deltas(pos, L):
    """
    Devuelve matrices dx, dy (NxN) con imagen mínima en caja periódica de lado L.
    """
    x = pos[:, 0]; y = pos[:, 1]
    dx = x[:, None] - x[None, :]
    dy = y[:, None] - y[None, :]
    dx -= L * np.round(dx / L)
    dy -= L * np.round(dy / L)
    return dx, dy

def order_parameter(theta):
    """
    Phi = |<e^{i theta}>|, con |v_i|=1 (orientaciones unitarias).
    """
    cx = np.cos(theta).mean()
    sy = np.sin(theta).mean()
    return np.hypot(cx, sy)

# --------------------------- Simulador ---------------------------

class VicsekSim:
    def __init__(self, N=300, L=20.0, v0=0.3, R=1.0, eta=0.2, dt=1.0, seed=0):
        rng = np.random.default_rng(None if seed is None else seed)
        self.N, self.L, self.v0, self.R, self.eta, self.dt = N, L, v0, R, eta, dt
        self.rng = rng
        self.pos = rng.uniform(0, L, size=(N, 2))
        self.theta = rng.uniform(0, 2*np.pi, size=N)

    def step(self):
        # 1) Vecinos (imagen mínima)
        dx, dy = minimum_image_deltas(self.pos, self.L)
        dist2 = dx*dx + dy*dy
        neigh = dist2 <= (self.R * self.R)  # incluye a sí mismo

        # 2) Dirección promedio local
        cos_th = np.cos(self.theta)
        sin_th = np.sin(self.theta)
        Sx = (neigh * cos_th[None, :]).sum(axis=1)
        Sy = (neigh * sin_th[None, :]).sum(axis=1)
        mean_angle = np.arctan2(Sy, Sx)

        # 3) Ruido uniforme en [-eta/2, +eta/2]
        noise = self.eta * (self.rng.random(self.N) - 0.5)

        # 4) Actualizar orientaciones y posiciones
        self.theta = mean_angle + noise
        v = self.v0 * np.column_stack((np.cos(self.theta), np.sin(self.theta)))
        self.pos = (self.pos + v * self.dt) % self.L

    def run(self, steps=1000, record_every=1):
        hist_pos, phi = [], []
        for t in range(steps):
            self.step()
            if (t % record_every) == 0:
                hist_pos.append(self.pos.copy())
                phi.append(order_parameter(self.theta))
        return np.array(hist_pos), np.array(phi)

# --------------------------- Visualizaciones ---------------------------

def _unwrap_track(xs, ys, L):
    """Desenrolla trayectoria por imagen mínima."""
    dx = np.diff(xs); dx -= L * np.round(dx / L)
    dy = np.diff(ys); dy -= L * np.round(dy / L)
    xs_corr = np.concatenate([[xs[0]], xs[0] + np.cumsum(dx)])
    ys_corr = np.concatenate([[ys[0]], ys[0] + np.cumsum(dy)])
    return xs_corr, ys_corr

def _anchor_to_box(xs_corr, ys_corr, L):
    """Traslada por múltiplos de L para que el punto final quede en [0, L)."""
    kx = np.floor(xs_corr[-1] / L)
    ky = np.floor(ys_corr[-1] / L)
    xs_plot = xs_corr - kx * L
    ys_plot = ys_corr - ky * L
    xs_plot[-1] = np.mod(xs_plot[-1], L)
    ys_plot[-1] = np.mod(ys_plot[-1], L)
    return xs_plot, ys_plot

def plot_three_trajectories(hist_pos, L, idx=(0,1,2), outdir="figures"):
    """Traza 3 trayectorias (desenrolladas y ancladas) + fondo tenue."""
    T, N, _ = hist_pos.shape
    outdir = make_dirs(outdir)
    fig, ax = plt.subplots(figsize=(6, 6), dpi=120)

    # Fondo tenue
    sample = np.linspace(0, N-1, min(50, N), dtype=int)
    for j in sample:
        xs, ys = hist_pos[:, j, 0], hist_pos[:, j, 1]
        xs_corr, ys_corr = _unwrap_track(xs, ys, L)
        ax.plot(xs_corr, ys_corr, alpha=0.08, linewidth=0.8)

    # Destacadas
    colors = ['C3', 'C0', 'C2']
    for k, j in enumerate(idx):
        xs, ys = hist_pos[:, j, 0], hist_pos[:, j, 1]
        xs_corr, ys_corr = _unwrap_track(xs, ys, L)
        xs_plot, ys_plot = _anchor_to_box(xs_corr, ys_corr, L)
        ax.plot(xs_plot, ys_plot, linewidth=2.2, label=f"Partícula {j}", color=colors[k % len(colors)])
        ax.scatter(xs_plot[-1], ys_plot[-1], s=30, color=colors[k % len(colors)])

    ax.set_title("Trajectories of 3 particles (neighbor alignment)")
    ax.set_xlim(0, L); ax.set_ylim(0, L); ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(loc="upper right")
    fig.tight_layout()
    outpath = os.path.join(outdir, "tracks_three.png")
    fig.savefig(outpath, bbox_inches="tight"); plt.close(fig)
    print(f"[OK] Guardado: {outpath}")

def plot_order(phi, dt, record_every=1, outdir="figures"):
    outdir = make_dirs(outdir)
    t = np.arange(len(phi)) * dt * record_every
    fig, ax = plt.subplots(figsize=(7, 3), dpi=120)
    ax.plot(t, phi, linewidth=2)
    ax.set_xlabel("Time")
    ax.set_ylabel(r"Global order $\Phi$")
    ax.set_title("Order evolution (alignment)")
    ax.grid(True, alpha=0.3); fig.tight_layout()
    outpath = os.path.join(outdir, "order_parameter.png")
    fig.savefig(outpath, bbox_inches="tight"); plt.close(fig)
    print(f"[OK] Guardado: {outpath}")

def animate(sim, frames=400, interval=30, out_gif="figures/anim_vicsek.gif", show=False):
    make_dirs(os.path.dirname(out_gif) or ".")
    fig, ax = plt.subplots(figsize=(6,6), dpi=120)
    scat = ax.scatter(sim.pos[:,0], sim.pos[:,1], s=12)
    ax.set_xlim(0, sim.L); ax.set_ylim(0, sim.L); ax.set_aspect('equal', adjustable='box')
    ax.set_title("Vicsek-type alignment (animation)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")


    def update(_):
        sim.step()
        scat.set_offsets(sim.pos)
        return scat,

    ani = FuncAnimation(fig, update, frames=frames, interval=interval, blit=True)
    try:
        ani.save(out_gif, writer="pillow", fps=max(1, int(1000/interval)))
        print(f"[OK] Animación guardada en: {out_gif}")
    except Exception as e:
        print(f"[WARN] No se pudo guardar GIF (¿falta pillow?). Error: {e}")
        if show: plt.show()
    plt.close(fig)

# --------------------------- Barrido en eta ---------------------------

def sweep_eta(etas, N=300, L=20.0, v0=0.3, R=1.0, dt=1.0, burn_in=1000, avg_steps=1000, reps=3, seed0=0):
    """
    Recorre valores de eta y devuelve (etas, phi_mean, phi_std), promediando
    en régimen estacionario tras burn-in y sobre 'reps' semillas.
    """
    etas = list(etas)
    phi_mean = np.zeros(len(etas))
    phi_std  = np.zeros(len(etas))
    rng = np.random.default_rng(seed0)

    for k, eta in enumerate(etas):
        vals = []
        for r in range(reps):
            sim = VicsekSim(N=N, L=L, v0=v0, R=R, eta=eta, dt=dt,
                            seed=int(rng.integers(1, 10_000_000)))
            # burn-in
            for _ in range(burn_in):
                sim.step()
            # promedio estacionario
            acc = 0.0
            for _ in range(avg_steps):
                sim.step()
                acc += order_parameter(sim.theta)
            vals.append(acc / avg_steps)
        phi_mean[k] = np.mean(vals)
        phi_std[k]  = np.std(vals, ddof=1) if reps > 1 else 0.0
        print(f"[sweep] eta={eta:.3f} -> Phi={phi_mean[k]:.3f} ± {phi_std[k]:.3f}")
    return np.array(etas), phi_mean, phi_std

def parse_range(s):
    """
    'a:b:step' -> lista [a, a+step, ..., b] (incluye extremo si cae exacto)
    o lista separada por comas '0.0,0.2,0.4'.
    """
    s = s.strip()
    if ":" in s:
        a, b, h = (float(x) for x in s.split(":"))
        n = int(np.floor((b - a) / h + 0.5)) + 1
        return [a + i*h for i in range(n)]
    else:
        return [float(x) for x in s.split(",")]

def plot_phi_vs_eta(etas, phi_mean, phi_std, outpath="figures/phi_vs_eta.png"):
    make_dirs(os.path.dirname(outpath) or "figures")
    fig, ax = plt.subplots(figsize=(6,4), dpi=120)
    ax.errorbar(etas, phi_mean, yerr=phi_std, fmt='o-', linewidth=1.8, capsize=3)
    ax.set_xlabel(r"Noise $\eta$")
    ax.set_ylabel(r"Average order $\langle\Phi\rangle$")
    ax.set_title(r"Order–disorder transition (sweep in $\eta$)")
    ax.grid(True, alpha=0.3); fig.tight_layout()
    fig.savefig(outpath, bbox_inches="tight"); plt.close(fig)
    print(f"[OK] Guardado: {outpath}")

# --------------------------- CLI ---------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Simulación de alineamiento vecinal (modelo tipo Vicsek).")
    p.add_argument("--N", type=int, default=300)
    p.add_argument("--L", type=float, default=20.0)
    p.add_argument("--v0", type=float, default=0.3)
    p.add_argument("--R", type=float, default=1.0)
    p.add_argument("--eta", type=float, default=0.2)
    p.add_argument("--dt", type=float, default=1.0)
    p.add_argument("--steps", type=int, default=1500)
    p.add_argument("--record_every", type=int, default=1)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--no_plots", action="store_true")
    p.add_argument("--animate", action="store_true", help="(alias de --gif)", default=False)
    p.add_argument("--gif", action="store_true", help="Generar GIF de animación")
    p.add_argument("--idx", type=str, default="0,1,2")
    # >>> Barrido en eta <<<
    p.add_argument("--sweep_eta", type=str, default=None,
                   help="Formato: '0.0:1.0:0.05' o lista '0.0,0.2,0.4'")
    p.add_argument("--burn_in", type=int, default=1000)
    p.add_argument("--avg_steps", type=int, default=1000)
    p.add_argument("--reps", type=int, default=3)
    return p.parse_args()


# --------------------------- Main ---------------------------

def main():
    args = parse_args()

    # ---- Barrido en ruido eta (opcional) ----
    if args.sweep_eta is not None:
        etalist = parse_range(args.sweep_eta)
        etas, phi_mean, phi_std = sweep_eta(
            etalist, N=args.N, L=args.L, v0=args.v0, R=args.R, dt=args.dt,
            burn_in=args.burn_in, avg_steps=args.avg_steps, reps=args.reps, seed0=args.seed
        )
        plot_phi_vs_eta(etas, phi_mean, phi_std, outpath="figures/phi_vs_eta.png")
        # Puedes salir aquí si solo te interesa el barrido:
        # return

    # ---- Simulación base para figuras/animación ----
    sim = VicsekSim(N=args.N, L=args.L, v0=args.v0, R=args.R, eta=args.eta, dt=args.dt, seed=args.seed)

    # Figuras estáticas
    if not args.no_plots:
        hist_pos, phi = sim.run(steps=args.steps, record_every=args.record_every)
        # índices de 3 partículas
        try:
            idx = tuple(int(s.strip()) for s in args.idx.split(","))
            if len(idx) != 3: raise ValueError
            idx = tuple(max(0, min(sim.N-1, i)) for i in idx)
        except Exception:
            idx = (0,1,2)
        plot_three_trajectories(hist_pos, L=args.L, idx=idx)
        plot_order(phi, dt=args.dt, record_every=args.record_every)

    # Animación
    if args.gif:
        animate(sim, frames=400, interval=30, out_gif="figures/anim_vicsek.gif", show=False)

if __name__ == "__main__":
    main()
