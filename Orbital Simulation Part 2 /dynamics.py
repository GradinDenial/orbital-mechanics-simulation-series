import numpy as np

# Earth's gravitational parameter = GM = 3.986e14 m^3/s^2
mu = 3.986e14

# Function to compute the state derivatives ie. the time derivatives of position and velocity for each satellite at every instance of time. This function will be called by the propagator to compute the satellite trajectories.
def state_derivative(t, state):
    derivatives = []

 # Number of bodies 3 dimenstions (x, y, z) and 3 velocity components (vx, vy, vz) for each satellite
    n = int(len(state) / 6)

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

# Append the derivatives of position and velocity to the list
        derivatives.extend([vx, vy, vz, ax, ay, az])

    return derivatives
