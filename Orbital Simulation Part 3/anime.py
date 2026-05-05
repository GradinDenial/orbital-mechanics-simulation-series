import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from dynamics import mu, r_moon, omega_moon

inclinations = [0, 45, 90, 135]
COLORS = ['#00cfff', '#ff4fff', '#39ff14', '#ff9900']

def animate(solution, orbit_types):
    fig = plt.figure(figsize=(10, 8))
    ax  = fig.add_subplot(111, projection='3d')

    # --- Space theme ---
    fig.patch.set_facecolor('#000010')
    ax.set_facecolor('#000010')
    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
        pane.fill = False
        pane.set_edgecolor('#111133')
    ax.grid(True, color='#111133', linewidth=0.5)
    ax.tick_params(colors='#aaaacc', labelsize=7)
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.label.set_color('#aaaacc')

    # --- Stars ---
    rng = np.random.default_rng(42)
    limit = 4e8
    xs = rng.uniform(-limit, limit, 300)
    ys = rng.uniform(-limit, limit, 300)
    zs = rng.uniform(-limit, limit, 300)
    ax.scatter(xs, ys, zs, s=0.3, c='white', alpha=0.4, depthshade=False)

    # --- Earth sphere (static) ---
    earth_radius = 6371e3 * 5
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
    ex = earth_radius * np.cos(u) * np.sin(v)
    ey = earth_radius * np.sin(u) * np.sin(v)
    ez = earth_radius * np.cos(v)
    ax.plot_surface(ex, ey, ez, color='#1a6fff', alpha=0.85, linewidth=0)

    # --- Moon orbital plane reference disc (static, faint) ---
    theta = np.linspace(0, 2 * np.pi, 200)
    x_ring = r_moon * np.cos(theta)
    y_ring = r_moon * np.sin(theta)
    z_ring = np.zeros_like(theta)
    ax.plot(x_ring, y_ring, z_ring,
            color='#aaaaaa', linewidth=0.8, linestyle='--', alpha=0.4)

    # Pre-compute Moon positions for every frame
    t = solution.t
    moon_x_all = r_moon * np.cos(omega_moon * t)
    moon_y_all = r_moon * np.sin(omega_moon * t)

    n = int(len(solution.y) / 6)

    # --- Satellite trails + glow + dots ---
    trails, glows, dots = [], [], []
    for i in range(n):
        label = f"{orbit_types[i]} ({inclinations[i]}°)"
        glow,  = ax.plot([], [], [], color=COLORS[i], linewidth=4,  alpha=0.12)
        trail, = ax.plot([], [], [], color=COLORS[i], linewidth=1,  alpha=0.9, label=label)
        dot,   = ax.plot([], [], [], 'o', color=COLORS[i], markersize=5)
        glows.append(glow)
        trails.append(trail)
        dots.append(dot)

    # --- Moon: accumulated trail + current dot ---
    moon_trail_glow, = ax.plot([], [], [], color='#dddddd', linewidth=3, alpha=0.12)
    moon_trail,      = ax.plot([], [], [], color='#dddddd', linewidth=1.2, alpha=0.85, label='Moon')
    moon_dot,        = ax.plot([], [], [], 'o', color='white', markersize=7)

    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)
    ax.set_xlabel("X (m)", labelpad=8)
    ax.set_ylabel("Y (m)", labelpad=8)
    ax.set_zlabel("Z (m)", labelpad=8)
    ax.set_title("3D Orbital Animation — Earth, Moon, and Satellites",
                 color='white', fontsize=12, pad=14)
    ax.legend(fontsize=7, loc='upper left',
              facecolor='#000020', edgecolor='#333355', labelcolor='white')

    def update(frame):
        # Update satellites
        for i in range(n):
            x = solution.y[i*6 + 0]
            y = solution.y[i*6 + 1]
            z = solution.y[i*6 + 2]
            for artist in [trails[i], glows[i]]:
                artist.set_data(x[:frame], y[:frame])
                artist.set_3d_properties(z[:frame])
            dots[i].set_data([x[frame]], [y[frame]])
            dots[i].set_3d_properties([z[frame]])

        # Update Moon trail (accumulated path up to current frame)
        mx = moon_x_all[:frame]
        my = moon_y_all[:frame]
        mz = np.zeros(frame)
        for artist in [moon_trail, moon_trail_glow]:
            artist.set_data(mx, my)
            artist.set_3d_properties(mz)

        # Moon current position dot
        moon_dot.set_data([moon_x_all[frame]], [moon_y_all[frame]])
        moon_dot.set_3d_properties([0])

        return trails + glows + dots + [moon_trail, moon_trail_glow, moon_dot]

    ani = FuncAnimation(fig, update, frames=len(t), interval=10, blit=False)
    plt.show()
