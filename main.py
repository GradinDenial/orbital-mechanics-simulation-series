import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Earth's gravitational parameter (m^3/s^2)
mu = 3.986e14

def state_derivative(t, state):
    x, y, z, vx, vy, vz = state
    
    r = np.sqrt(x**2 + y**2 + z**2)
    
    ax = -mu * x / r**3
    ay = -mu * y / r**3
    az = -mu * z / r**3
    
    return [vx, vy, vz, ax, ay, az]

# Initial conditions (example: low Earth orbit)
r0 = 7000e3  # 7000 km from Earth's center
v0 = 7500    # m/s approximate orbital velocity

initial_state = [r0, 0, 0, 0, v0, 0]

# Time span (seconds)
t_span = (0, 5800)
t_eval = np.linspace(*t_span, 10000)

# Solve ODE
solution = solve_ivp(
    state_derivative,
    t_span,
    initial_state,
    t_eval=t_eval,
    method='DOP853',
    rtol=1e-13,
    atol=1e-14,
    max_step=1.0 # Critical for accurate interpolation
)   

# Extract position
x = solution.y[0]
y = solution.y[1]
z = solution.y[2]

# Plot orbit
plt.figure()
plt.plot(x, y)
plt.scatter(0, 0, label="Earth")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.axis("equal")
plt.title("Satellite Orbit")
plt.legend()
plt.show()

# Compute radius and velocity magnitude
r = np.sqrt(x**2 + y**2 + z**2)
vx = solution.y[3]
vy = solution.y[4]
vz = solution.y[5]
v = np.sqrt(vx**2 + vy**2 + vz**2)

# Specific mechanical energy
energy = 0.5 * v**2 - mu / r

# Create one figure with two plots
plt.figure()

# Orbit plot
plt.subplot(2,1,1)
plt.plot(x, y, label="Orbit")
plt.scatter(0, 0, color='orange', label="Earth")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.axis("equal")
plt.title("Orbit")
plt.legend()
plt.grid()


# Energy plot
plt.subplot(2,1,2)
plt.plot(t_eval, energy) # Use t_eval, not solution.t
plt.xlabel("Time (s)")
plt.ylabel("Energy (J/kg)")
plt.title("Energy Conservation")
plt.grid()   

plt.tight_layout()
plt.show()