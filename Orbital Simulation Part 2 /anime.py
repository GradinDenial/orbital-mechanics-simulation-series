import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from plotter import r_moon, omega_moon

def animate(solution, orbit_types):
    fig, ax = plt.subplots()

    colors = ['green', 'black', 'red', 'purple']
    n = int(len(solution.y) / 6)

    # --- Earth ---
    earth_radius = 6371e3 * 5
    earth = plt.Circle((0, 0), earth_radius, color='blue')
    ax.add_patch(earth)

    # --- Moon ---
    moon_radius = 1737e3 * 5
    moon = plt.Circle((0, 0), moon_radius, color='gray')
    ax.add_patch(moon)

    # Moon trail line
    moon_line, = ax.plot([], [], color='gray', linestyle='--', label="Moon Path")

    # --- Satellites ---
    lines = []
    sat_dots = []

    for i in range(n):
        # trail
        line, = ax.plot([], [], color=colors[i], label=orbit_types[i])
        lines.append(line)

        # moving dot
        dot, = ax.plot([], [], 'o', color=colors[i], markersize=6)
        sat_dots.append(dot)

    limit = 4e8
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.legend()

    t = solution.t

    # Precompute Moon trajectory for animation
    x_moon_all = r_moon * np.cos(omega_moon * t)
    y_moon_all = r_moon * np.sin(omega_moon * t)


    def update(frame):
        for i in range(n):
            x = solution.y[i*6 + 0]
            y = solution.y[i*6 + 1]

        # trail
            lines[i].set_data(x[:frame], y[:frame])

        # dot (current position)
            sat_dots[i].set_data([x[frame]], [y[frame]])

    # Moon
        x_moon = r_moon * np.cos(omega_moon * t[frame])
        y_moon = r_moon * np.sin(omega_moon * t[frame])
        moon.center = (x_moon, y_moon)

        moon_line.set_data(
            r_moon * np.cos(omega_moon * t[:frame]),
            r_moon * np.sin(omega_moon * t[:frame])
        )

        return lines + sat_dots + [moon, moon_line]

    ani = FuncAnimation(
        fig,
        update,
        frames=len(t),
        interval=10,
        blit=False
    )

    plt.title("Earth and its Satellites (Animated)")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)") 
    plt.show()
