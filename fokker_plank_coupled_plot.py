"""
Final State Plotting Script for Fokker-Planck Coupled Solver
===========================================================
Imports the numerical solver module and generates a static plot comparing
the initial states (t=0) and final density distributions (t=t_final).
"""

import matplotlib.pyplot as plt
from fokker_planck_coupled_solver_1D import run_simulation


def plot_final_state():
    """Runs the simulation and renders a static figure of the final probability distributions."""
    # Execute numerical core without history tracking for optimal computational performance
    results = run_simulation(save_history=False, verbose=False)

    x_vals = results['x_vals']
    Ps_init = results['Ps_init']
    Ps_final = results['Ps_final']
    t_final = results['t_final']
    N_dist = results['N_dist']

    colors = ['blue', 'green', 'red', 'purple', 'orange'][:N_dist]
    labels = [f"P{i+1}" for i in range(N_dist)]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot initial states (dashed lines) and final states (solid lines)
    for i in range(N_dist):
        ax.plot(x_vals, Ps_init[i], '--', color=colors[i], alpha=0.4, linewidth=1.5, label=f"{labels[i]} Initial ($t=0$)")
        ax.plot(x_vals, Ps_final[i], '-', color=colors[i], linewidth=2.0, label=f"{labels[i]} Final ($t={t_final}$s)")

    # Figure aesthetics and formatting for manuscript publication
    ax.set_title("Probability Density Distributions: Initial vs Final State", fontsize=13, fontweight='bold')
    ax.set_xlabel("Spatial coordinate $x$", fontsize=11)
    ax.set_ylabel("Probability Density $P(x)$", fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.05, 0.6)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_final_state()
