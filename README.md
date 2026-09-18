# 1D SU(2) Gauge-Coupled Fokker-Planck System Solver

Companion codebase for research manuscript:
> **De Cosmo, Di Natale, and Cieri (2026)**, *"A Gauge-Inspired Coupled Fokker–Planck System for Multistate Stochastic Dynamics: Formalism and 1-D Numerical Implementation"*.

---

## 1. Repository Files

* `fokker_plank_coupled_solver_1D.py`: Core numerical solver engine implementing the Inverted Operator-Splitting scheme and MPDATA advective transport algorithm.
* `fokker_plank_coupled_plot.py`: Post-processing visualization script to display static initial/final probability distribution profiles and diagnostic force breakdown.
* `fokker_plank_coupled_animated_plot.py`: Interactive visualization script generating real-time animations of the temporal evolution of all coupled probability sectors.

---

## 2. Governing Equations & Numerical Algorithm

The code solves a coupled triplet of non-linear Fokker-Planck equations for sectors $a \in \{1, 2, 3\}$:

$$\frac{\partial P_a}{\partial t} = -\frac{\partial}{\partial x} \left[ v_a(x) P_a \right] + D_a \frac{\partial^2 P_a}{\partial x^2} + I_a[P, J, g]$$

where:
* $P_a(x,t)$: Probability density distribution of sector $a$.
* $v_a(x)$: Spatially dependent deterministic drift velocity field.
* $D_a$: Constant diffusion coefficient for sector $a$.
* $J_a(x,t)$: Local physical probability current density, defined as:
  $$J_a(x,t) = v_a(x) P_a(x,t) - D_a \frac{\partial P_a(x,t)}{\partial x}$$
* $I_a(x,t)$: Non-local gauge coupling source term containing spatial domain integrals ($\Gamma$) and time-memory accumulators ($\Theta$).
* $g$: Global non-Abelian $SU(2)$ gauge coupling constant. Setting $g = 0.0$ recovers uncoupled Fokker-Planck evolution.

### Numerical Strategy (Inverted Operator-Splitting + MPDATA)

1. **Phase I (Pre-conditioning)**: Physical spatial diffusion and non-local gauge interaction source terms ($\mathcal{O}(g)$ and $\mathcal{O}(g^2)$) are integrated to generate an intermediate pre-conditioned state $\widetilde{P}_a$.
2. **Phase II (Advective Transport)**: Pure advective transport under drift velocity $v_a(x)$ is resolved using the two-step MPDATA scheme (Donor-Cell upwinding followed by an antidiffusive pseudo-velocity correction).
3. **Phase III (Physical Constraints)**: Numerical underflows are clipped to a positive floor ($P_a \ge 10^{-12}$) and global total probability is scaled to enforce $\sum_a \int_{\Omega} P_a \, \mathrm{d}x = 3$.

---
