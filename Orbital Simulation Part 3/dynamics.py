import numpy as np

# Earth's gravitational parameter = GM = 3.986e14 m^3/s^2
mu = 3.986e14

# Moon's gravitational parameter = GM_moon
mu_moon = 4.9048e12  # m^3/s^2

# Moon orbital parameters (centralised here so all modules can import)
r_moon = 3844e5          # mean Earth-Moon distance (m)
T_moon = 27.3 * 24 * 3600  # orbital period (s)
omega_moon = 2 * np.pi / T_moon  # angular velocity (rad/s)

def moon_position(t):
    """Returns the Moon's (x, y, z) position at time t (circular orbit in x-y plane)."""
    x_m = r_moon * np.cos(omega_moon * t)
    y_m = r_moon * np.sin(omega_moon * t)
    z_m = 0.0
    return x_m, y_m, z_m


# Function to compute the state derivatives ie. the time derivatives of position and velocity for each satellite at every instance of time. This function will be called by the propagator to compute the satellite trajectories.
def state_derivative(t, state):
    derivatives = []

    # Number of bodies 3 dimenstions (x, y, z) and 3 velocity components (vx, vy, vz) for each satellite
    n = int(len(state) / 6)

    # Moon position at current time
    x_m, y_m, z_m = moon_position(t)

    #compute the derivatives for each satellite
    for i in range(n):
        x = state[i*6 + 0]
        y = state[i*6 + 1]
        z = state[i*6 + 2]
        vx = state[i*6 + 3]
        vy = state[i*6 + 4]
        vz = state[i*6 + 5]

        #Compute the distance from Earth to the satellite 
        r = np.sqrt(x**2 + y**2 + z**2)  

        # acceleration due to gravity decays with the cube of the distance, and is directed towards Earth
        ax = -mu * x / r**3
        ay = -mu * y / r**3
        az = -mu * z / r**3

        # Moon gravity
        # Vector from satellite to Moon
        dx = x_m - x
        dy = y_m - y
        dz = z_m - z
        r_sat_moon = np.sqrt(dx**2 + dy**2 + dz**2)
 
        ax += mu_moon * dx / r_sat_moon**3
        ay += mu_moon * dy / r_sat_moon**3
        az += mu_moon * dz / r_sat_moon**3

        # Append the derivatives of position and velocity to the list
        derivatives.extend([vx, vy, vz, ax, ay, az])

    return derivatives
