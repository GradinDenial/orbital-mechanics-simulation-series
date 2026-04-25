# orbital-mechanics-simulation-series
Numerical simulation of a satellite orbiting Earth using Newtonian gravity and SciPy ODE solvers (Part of an orbital mechanics series).
#Download each part folder respectively and assess yourself the progression as well as changing some bits of code to personalise your simulation with the Earth and its different satellites in orbit!

## Overview
This project is a series of numerical simulations of a satellite/s orbiting Earth under Newtonian gravity.

It solves the two-body problem using `solve_ivp` from SciPy.

## Features
- Newtonian gravitational model
- Numerical integration (DOP853 solver)
- 2D orbit visualization
- Energy conservation analysis
- 3D Orbit visualization
- N body problem
- Moon gravity effect??


## Output
- Satellite orbit around Earth
- Specific mechanical energy over time
- Orbital Animation
- Different forms of orbit and Moon orbit

## Tech Stack
- Python
- NumPy
- SciPy
- Matplotlib

## Note
This is Part 1 of a larger orbital mechanics simulation series, part 2 will later include:
- multiple orbital regimes
- improved visuals and animation
- Moon trajectory
-improved simulation structure


# Orbital Mechanics Simulation — Part 1

![Orbit Energy Plot](orbit_energy_plot.png)
Can see the path a Satellite takes at r away frome Earth
Can Prove the sim with Energy plot staying Constant in that Orbital Field

# Orbital Mechanics Simulation — Part 2

Now we can see at distance r from Earth 4 kinds of orbit as well as compute the closest and furthest part of the Satellites' orbit from Earth (Perigee & Apogee respectively.)
We can also visualize the path of the Moon.
Download the folder and change the value of r0 in main.py to see compute different paths

![Orbital Paths Animation](orbitalpaths-gif.gif)
![Energy V Time](energyplot.png)
![Orbital Paths Plot](orbitalpaths.png)
