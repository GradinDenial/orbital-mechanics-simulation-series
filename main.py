import numpy as np
from dynamics import state_derivative, mu
from propagator import propagate
from analysis import analyze_orbits
from plotter import plot_orbits, plot_energy
print("STARTING SIM")

r0 = 2300e5  # Initial distance from Earth in meters (7500 km)

v_c = np.sqrt(mu / r0)  # Circular orbit velocity
v_e = np.sqrt(2 * mu / r0)  # Escape velocity

# Initial states: [x, y, z, vx, vy, vz]
sat1 = [r0, 0, 0, 0, 0.8 * v_c, 0]   # elliptical
sat2 = [r0, 0, 0, 0, v_c, 0]         # circular
sat3 = [r0, 0, 0, 0, v_e, 0]         # parabolic
sat4 = [r0, 0, 0, 0, 1.2 * v_e, 0]   # hyperbolic

# Combine into one flat list
initial_state = sat1 + sat2 + sat3 + sat4

t_span = (0, 30 * 24 * 3600)  # Simulate for 30 days
t_eval = np.linspace(*t_span, 1000)

solution = propagate(state_derivative, initial_state, t_span, t_eval)

##################################################################################

orbit_types = analyze_orbits(solution)

plot_orbits(solution, orbit_types)
plot_energy(solution, orbit_types)


# Print perigee/apogee (min/max radius during sim)
n = int(len(solution.y) / 6)
for i in range(n):
    x = solution.y[i*6 + 0]
    y = solution.y[i*6 + 1]
    r = np.sqrt(x**2 + y**2)
    r_min = np.min(r)
    r_max = np.max(r)
    print(f"Satellite {i+1}:")
    print(f"  Perigee (min radius): {r_min/1000:.1f} km")
    print(f"  Apogee  (max radius): {r_max/1000:.1f} km")

from anime import animate
animate(solution, orbit_types)

print("SIM DONE")   