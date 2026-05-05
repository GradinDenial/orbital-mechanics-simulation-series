import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from dynamics import mu, r_moon, omega_moon

inclinations = [0, 45, 90, 135]
COLORS = ['#00cfff', '#ff4fff', '#39ff14', '#ff9900']

def _apply_space_theme(fig, ax):
    fig.patch.set_facecolor('#000010')
    ax.set_facecolor('#000010')
    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
        pane.fill = False
        pane.set_edgecolor('#111133')
    ax.grid(True, color='#111133', linewidth=0.5)
    ax.tick_params(colors='#aaaacc', labelsize=7)
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.label.set_color('#aaaacc')

def _draw_stars(ax, n_stars=300, limit=4e8):
    rng = np.random.default_rng(42)
    xs = rng.uniform(-limit, limit, n_stars)
    ys = rng.uniform(-limit, limit, n_stars)
    zs = rng.uniform(-limit, limit, n_stars)
    ax.scatter(xs, ys, zs, s=0.3, c='white', alpha=0.4, depthshade=False)

def _earth_sphere(ax, radius):
    u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:25j]
    x = radius * np.cos(u) * np.sin(v)
    y = radius * np.sin(u) * np.sin(v)
    z = radius * np.cos(v)
    ax.plot_surface(x, y, z, color='#1a6fff', alpha=0.85, zorder=2, linewidth=0)

def _moon_sphere(ax, cx, cy, cz, radius):
    u, v = np.mgrid[0:2*np.pi:25j, 0:np.pi:15j]
    x = radius * np.cos(u) * np.sin(v) + cx
    y = radius * np.sin(u) * np.sin(v) + cy
    z = radius * np.cos(v) + cz
    ax.plot_surface(x, y, z, color='#aaaaaa', alpha=0.8, zorder=2, linewidth=0)

def _draw_moon_orbital_plane(ax):
    """Draw a faint filled disc to show the Moon orbits in the x-y plane."""
    theta = np.linspace(0, 2 * np.pi, 200)
    # Draw the orbit ring prominently
    x_ring = r_moon * np.cos(theta)
    y_ring = r_moon * np.sin(theta)
    z_ring = np.zeros_like(theta)
    ax.plot(x_ring, y_ring, z_ring, color='#aaaaaa', linewidth=1.2,
            alpha=0.7, linestyle='--', label="Moon's Orbit")

    # Draw a faint equatorial plane disc so z=0 is visually obvious
    r_vals = np.linspace(0, r_moon, 30)
    R, T = np.meshgrid(r_vals, theta)
    Xp = R * np.cos(T)
    Yp = R * np.sin(T)
    Zp = np.zeros_like(Xp)
    ax.plot_surface(Xp, Yp, Zp, color='#334466', alpha=0.08, linewidth=0)


def plot_orbits(solution, orbit_types):
    fig = plt.figure(figsize=(10, 8))
    ax  = fig.add_subplot(111, projection='3d')
    _apply_space_theme(fig, ax)
    _draw_stars(ax)

    t = solution.t
    # Pre-compute full Moon trajectory
    x_moon = r_moon * np.cos(omega_moon * t)
    y_moon = r_moon * np.sin(omega_moon * t)
    z_moon = np.zeros_like(t)

    # Satellite orbits
    n = int(len(solution.y) / 6)
    for i in range(n):
        x = solution.y[i*6 + 0]
        y = solution.y[i*6 + 1]
        z = solution.y[i*6 + 2]
        label = f"{orbit_types[i]} ({inclinations[i]}°)"
        ax.plot(x, y, z, color=COLORS[i], linewidth=3, alpha=0.15)   # glow
        ax.plot(x, y, z, color=COLORS[i], linewidth=1, alpha=0.9, label=label)

    # Earth
    _earth_sphere(ax, 6371e3 * 5)

    # Moon orbital plane + ring (shows z=0 context clearly)
    _draw_moon_orbital_plane(ax)

    # Moon sphere at final position so you can see where it ended up
    _moon_sphere(ax, x_moon[-1], y_moon[-1], 0, 1737e3 * 5)

    # Moon trail — full 30-day path as a bright line
    ax.plot(x_moon, y_moon, z_moon,
            color='#dddddd', linewidth=1.5, alpha=0.85, zorder=5)

    # Moon start marker
    ax.scatter([x_moon[0]], [y_moon[0]], [0],
               color='white', s=20, zorder=6, label='Moon (start)')

    limit = 4e8
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)
    ax.set_xlabel("X (m)", labelpad=8)
    ax.set_ylabel("Y (m)", labelpad=8)
    ax.set_zlabel("Z (m)", labelpad=8)
    ax.set_title("3D Orbital Simulation — Earth, Moon, and Satellites",
                 color='white', fontsize=13, pad=14)
    ax.legend(fontsize=8, loc='upper left',
              facecolor='#000020', edgecolor='#333355', labelcolor='white')
    plt.tight_layout()
    plt.show()


def plot_energy(solution, orbit_types):
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#000010')
    ax.set_facecolor('#000010')
    ax.tick_params(colors='#aaaacc')
    ax.xaxis.label.set_color('#aaaacc')
    ax.yaxis.label.set_color('#aaaacc')
    ax.title.set_color('white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333355')
    ax.grid(color='#111133', linewidth=0.6)

    n = int(len(solution.y) / 6)
    for i in range(n):
        x  = solution.y[i*6 + 0]
        y  = solution.y[i*6 + 1]
        z  = solution.y[i*6 + 2]
        vx = solution.y[i*6 + 3]
        vy = solution.y[i*6 + 4]
        vz = solution.y[i*6 + 5]
        r  = np.sqrt(x**2 + y**2 + z**2)
        v  = np.sqrt(vx**2 + vy**2 + vz**2)
        energy = 0.5 * v**2 - mu / r
        label  = f"{orbit_types[i]} ({inclinations[i]}°)"
        ax.plot(solution.t / 86400, energy, color=COLORS[i], label=label,
                linewidth=1.4, alpha=0.9)
        ax.plot(solution.t / 86400, energy, color=COLORS[i], linewidth=4, alpha=0.12)

    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Specific Energy (J/kg)")
    ax.set_title("Orbital Energy vs Time")
    ax.legend(fontsize=9, facecolor='#000020',
              edgecolor='#333355', labelcolor='white')
    plt.tight_layout()
    plt.show()
