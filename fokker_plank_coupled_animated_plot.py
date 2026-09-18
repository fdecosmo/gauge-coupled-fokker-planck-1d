"""
Animation and Visualization Script for Fokker-Planck Coupled Solver
==================================================================
Imports the numerical solver module and generates an interactive Matplotlib animation.

"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from fokker_planck_coupled_solver_1D import run_simulation


def build_animation():
    """Runs the simulation and launches the interactive animation window."""
    # Execute numerical core with history enabled and logging disabled
    results = run_simulation(save_history=True, verbose=False)

    x_vals = results['x_vals']
    Ps_init = results['Ps_init']
    storia_ps = results['STORIA_Ps']
    dt = results['dt']
    t_final = results['t_final']
    N_dist = results['N_dist']

    colors = ['blue', 'green', 'red', 'purple', 'orange'][:N_dist]
    labels = [f"P{i+1}" for i in range(N_dist)]

    fig, ax = plt.subplots(figsize=(10, 6))
    lines = []

    # Initial profiles reference (dashed lines)
    for i in range(N_dist):
        ax.plot(x_vals, Ps_init[i], '--', color=colors[i], alpha=0.3, label=f"{labels[i]} Initial (t=0)")
        line, = ax.plot([], [], color=colors[i], lw=2, label=f"{labels[i]} Real-time")
        lines.append(line)

    ax.set_title("Density Evolution with Full Gauge Couplings $g$ and $g^2$ (Inverted Splitting)", fontsize=13)
    ax.set_xlabel("x")
    ax.set_ylabel("Probability Density")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.05, 0.6)
    ax.legend(loc="upper right")

    time_text = ax.text(0.05, 0.92, '', transform=ax.transAxes, fontsize=11, fontweight='bold')

    # Subsampling frames for smooth animation playback (1 frame every 10 iterations)
    passo_frame = 10
    indici_frame = list(range(0, len(storia_ps), passo_frame))
    if indici_frame[-1] != len(storia_ps) - 1:
        indici_frame.append(len(storia_ps) - 1)

    def init_anim():
        for line in lines:
            line.set_data([], [])
        time_text.set_text('')
        return lines + [time_text]

    def update(frame_idx):
        stato_corrente = storia_ps[frame_idx]
        for i, line in enumerate(lines):
            line.set_data(x_vals, stato_corrente[i])

        tempo_corrente = frame_idx * dt
        time_text.set_text(f"Time: {tempo_corrente:.4f} s / {t_final} s (Step: {frame_idx})")
        return lines + [time_text]

    anim = FuncAnimation(
        fig,
        update,
        frames=indici_frame,
        init_func=init_anim,
        blit=True,
        interval=30
    )

    plt.show()


if __name__ == "__main__":
    build_animation()
