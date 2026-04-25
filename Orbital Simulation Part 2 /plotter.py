import matplotlib.pyplot as plt
import numpy as np
from dynamics import mu

# Moon parameters
r_moon = 3844e5        # distance from Earth (m)
T_moon = 27.3 * 24 * 3600  # orbital period (s)
omega_moon = 2 * np.pi / T_moon

# Plot orbits with legend labels
def plot_orbits(solution, orbit_types):
    plt.figure()
    colors = ['green', 'black', 'red', 'purple']

# Plot Moon's orbit    
    t = solution.t
    x_moon = r_moon * np.cos(omega_moon * t)
    y_moon = r_moon * np.sin(omega_moon * t)

#satellite orbits
    n = int(len(solution.y) / 6)
    for i in range(n):
        x = solution.y[i*6 + 0]
        y = solution.y[i*6 + 1]
        vx = solution.y[i*6 + 3]
        vy = solution.y[i*6 + 4]
        plt.plot(x, y, color=colors[i], label=orbit_types[i])

    earth_radius = 6371e3 * 5   # scaled up for visibility
    earth = plt.Circle((0, 0), earth_radius, color='blue', label="Earth")
    plt.gca().add_patch(earth)

    moon_radius = 1737e3 * 5   # scaled up for visibility
    moon = plt.Circle((x_moon[0], y_moon[0]), moon_radius, color='gray', label="Moon")
    plt.gca().add_patch(moon)   

    plt.scatter(0, 0, color='green', label="Earth")
    plt.plot(x_moon, y_moon, color='gray', label="Moon's Orbit")
    plt.axis("equal")
    plt.title("Earth and its Satellites (Automatically Labeled Orbits)")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.legend()
    plt.grid(True)
    limit = 4e8
    plt.xlim(-limit, limit)
    plt.ylim(-limit, limit)
    plt.show()

# Energy plot
def plot_energy(solution, orbit_types):
    plt.figure()
    colors = ['blue', 'black', 'red', 'purple']
    n = int(len(solution.y) / 6)
    for i in range(n):
        x = solution.y[i*6 + 0]
        y = solution.y[i*6 + 1]
        vx = solution.y[i*6 + 3]
        vy = solution.y[i*6 + 4]

        r = np.sqrt(x**2 + y**2)
        v = np.sqrt(vx**2 + vy**2)
        energy = 0.5 * v**2 - mu / r
        plt.plot(solution.t, energy, color=colors[i], label=orbit_types[i])

    plt.xlabel("Time (s)")
    plt.ylabel("Specific Energy (J/kg)")
    plt.title("Energy vs Time")
    plt.legend()
    plt.grid()
    plt.show()

