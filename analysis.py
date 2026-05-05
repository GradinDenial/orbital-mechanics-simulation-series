import numpy as np
from dynamics import mu 

def analyze_orbits(solution):
    orbit_types = []
    n = int(len(solution.y) / 6)
    for i in range(n):
        x = solution.y[i*6 + 0]
        y = solution.y[i*6 + 1]
        vx = solution.y[i*6 + 3]
        vy = solution.y[i*6 + 4]

        r = np.sqrt(x**2 + y**2)
        v = np.sqrt(vx**2 + vy**2)
        energy = 0.5 * v**2 - mu / r
        avg_energy = np.mean(energy)

        if np.isclose(avg_energy, 0, atol=1e5):
            orbit_type = "Parabolic"
        elif avg_energy < 0:
            orbit_type = "Elliptical"
        else:
            orbit_type = "Hyperbolic"
    
        orbit_types.append(orbit_type)
    return orbit_types
