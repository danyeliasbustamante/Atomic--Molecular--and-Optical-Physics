# AMOP — Active Matter & Optical Physics Sandbox

Collection of minimal, well-commented codes for **Atomic, Molecular, and Optical Physics (AMOP)** and **Active Matter**.  
This repo currently includes a Vicsek-type alignment model for self-propelled particles and utilities to visualize order formation, trajectories, and the order–disorder transition.

> **Why this repo?** Reproducible, didactic scripts that bridge physics ideas (light–matter, collective motion, symmetry/geometry) with clean numerical experiments and publication-grade figures.

---

## Contents

- [Overview](#overview)
- [Key ideas](#key-ideas)
- [Results & Figures](#results--figures)
  - [A. Vicsek-type alignment (animation)](#a-vicsek-type-alignment-animation)
  - [B. Time evolution of global order Φ](#b-time-evolution-of-global-order-φ)
  - [C. Order–disorder transition vs noise η](#c-orderdisorder-transition-vs-noise-η)
  - [D. Example trajectories](#d-example-trajectories)
- [Reproduce the figures](#reproduce-the-figures)
- [Parameters & model](#parameters--model)
- [Project structure](#project-structure)
- [Cite & references](#cite--references)
- [License](#license)

---

## Overview

We simulate \(N\) self-propelled particles with constant speed \(v\) in a 2D periodic box.  
At each step, each particle aligns to the **average heading of neighbors** within radius \(R\), plus angular noise of amplitude \(\eta\).  
The global **order parameter** is

$$
\Phi(t)=\frac{1}{N}\left\lVert \sum_{i=1}^{N}\mathbf{v}_i(t)\right\rVert \big/ v,
$$

so \(\Phi \in [0,1]\) measures alignment (1 = full order, 0 = disorder).

---

## Key ideas

- **Local rules → global order.** Increasing neighborhood alignment and reducing noise drives a non-equilibrium phase transition to collective motion.
- **Order parameter \(\Phi\).** A compact scalar that diagnoses the degree of flocking.
- **Noise sweep.** Averaging \(\Phi\) over time and seeds across \(\eta\) reveals the order–disorder curve and fluctuations near the transition.
- **Trajectories.** Pathlines clarify kinematics beyond \(\Phi\) (clustering, banding, persistence).

---

## Results & Figures

**Example snapshot.** Final configuration of an active particle system (Vicsek-type). Each arrow is a particle’s position and orientation.  
**Example values:** \(P \approx 0.89\) (polarization), \(S \approx 0.71\) (2D nematic order).

![Active particles simulation](figures/amop_demo_20250923-173425.png)

### A. Vicsek-type alignment (animation)

![Vicsek animation](figures/anim_vicsek.gif)

**What to look for.** Random headings at start, then rapid coarsening into a coherently moving cluster.  
**Interpretation.** For fixed \((N, v, R)\) and moderate noise \((\eta)\), the system self-organizes: headings synchronize and center-of-mass drift emerges.

---

### B. Time evolution of global order \(\Phi\)

<img src="figures/order_parameter.png" width="800" alt="Order parameter vs time">

**Caption.** \(\Phi(t)\) rises from near 0 to \(\approx 1\) and then fluctuates weakly around a plateau.  
**Takeaway.** Transient alignment gives way to a steady ordered phase; the time-to-plateau shrinks when \(\eta\) is smaller or density is larger.

---

### C. Order–disorder transition vs noise \(\eta\)

<img src="figures/phi_vs_eta.png" width="560" alt="Phi vs eta with error bars">

**Caption.** Long-time average \(\langle \Phi \rangle\) vs noise amplitude \(\eta\). Markers show the mean over seeds; error bars show sample variability.  
**Takeaway.** Clear monotonic loss of order with noise. The knee indicates the transition region; error bars grow near criticality (enhanced fluctuations).

---

### D. Example trajectories

<img src="figures/tracks_three.png" width="680" alt="Trajectories of selected particles">

**Caption.** Trajectories of three tagged particles (colored), drawn over faded tracks of the rest.  
**Takeaway.** Persistent, nearly parallel motion in the ordered phase; curvature and scattering increase as \(\eta\) rises.

---

## Reproduce the figures

```bash
# 1) Create environment (Python ≥3.10 recommended)
python -m venv .venv
# Windows:
#   .venv\Scripts\activate
# macOS/Linux:
#   source .venv/bin/activate
pip install -r requirements.txt

# 2) (Option A) Reproduce everything
python run_all.py

# 2) (Option B) Generate specific artifacts

# 2.1) Example snapshot (creates figures/amop_demo_*.png)
python demo.py
# or:
python -m examples.run_example

# 2.2) Vicsek animation
python vicsek_alignment.py --save figures/anim_vicsek.gif

# 2.3) Order–disorder curve Φ(η)
python phi_vs_eta.py --out figures/phi_vs_eta.png

