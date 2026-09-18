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

## 3. Execution & Usage

Run standalone solver with terminal diagnostic logs:

    python fokker_plank_coupled_solver_1D.py

Generate static plots of final distribution profiles:

    python fokker_plank_coupled_plot.py

Run interactive real-time animation of time evolution:

    python fokker_plank_coupled_animated_plot.py

---

## 4. Parameter Configuration & Customization

All physical, numerical, and initial parameters are defined inside the `run_simulation()` function in `fokker_plank_coupled_solver_1D.py`:

### a) Grid & Integration Parameters

    Nx = 100               # Spatial grid resolution (number of nodes)
    x_vals = [0, 10]       # Spatial domain range [x_min, x_max]
    dt = 0.0004            # Time step size (seconds, satisfies CFL bound)
    t_final = 1.0          # Total simulation time (seconds)

### b) Gauge Coupling Parameter

    g = 0.2                # Interaction strength (g = 0.0 for uncoupled)

### c) Drift Velocity Fields $v_a(x)$

Arbitrary spatially dependent functions defined per sector.
Examples (Linear Ornstein-Uhlenbeck drift $v_a(x) = \alpha_a x$):

    drift_funcs = [
        lambda x: 0.3 * x,   # Sector 1 drift
        lambda x: 0.5 * x,   # Sector 2 drift
        lambda x: 0.7 * x    # Sector 3 drift
    ]

### d) Diffusion Coefficients $D_a$

Arbitrary positive scalar constants defined per sector.

    diff_coeffs = [0.10, 0.15, 0.20]  # [D_1, D_2, D_3]

### e) Initial Conditions $P_a(x,0)$

Arbitrary non-negative distribution profiles normalized to unit area.
Example (Identical unit Gaussians centered at $x = 5.0$):

    Ps = [init_gauss_1d(x_vals, cx=5.0, width=1.0, dx=dx) for _ in range(3)]

---

## 5. Citation

If you use this codebase in your research, please cite:

    @article{DeCosmo2026,
      author  = {De Cosmo, Francesco Pio and Di Natale, Gianluca and Cieri, Leandro},
      title   = {A Gauge-Inspired Coupled Fokker--Planck System for Multistate Stochastic Dynamics: Formalism and 1-D Numerical Implementation},
      year    = {2026}
    }
