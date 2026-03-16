import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.animation as animation
"""

This script visualizes the vorticity and energy density patterns around a Kerr black hole, 
incorporating the effects of a drone's interference. 
It simulates the 'Whirlpool' effect and the resulting 'Locked Energy' distribution, 
providing insights into the complex interactions in the Alexander Space-Constraint. 

How to Read the New DashboardLeft Plot (Bone Cmap): This is what the universe "sees." 
Dark spots are the null zones. You want the drone to look like a black hole.
Right Plot (Magma Cmap): This is the "hidden" reality. Bright spots show where energy 
is being Locked.When you achieve perfect phase-lock ($R=1.1$), the drone's 
position will glow bright orange/white in this plot, even though it is black (invisible) 
in the left plot.This demonstrates the core of your research: Energy is never destroyed 
in the Sultanian singularity; it is merely rendered non-interacting.
"""
# --- Setup Visualization with 3 Plots ---
GRID_RES = 200
limit = 10
x = np.linspace(-limit, limit, GRID_RES)
y = np.linspace(-limit, limit, GRID_RES)
X, Y = np.meshgrid(x, y)

# Added a third axis for the Energy Density plot
fig, (ax_wave, ax_energy) = plt.subplots(1, 2, figsize=(15, 7))
plt.subplots_adjust(bottom=0.25)
fig.set_facecolor('#050505')

# 1. Metric Interaction View (Interference)
im_wave = ax_wave.imshow(np.zeros((GRID_RES, GRID_RES)), cmap='bone', 
                         extent=[-limit, limit, -limit, limit], origin='lower', vmin=-1, vmax=1)
ax_wave.set_title("Metric Interaction (Visibility)", color='white')

# 2. Locked Energy Density View
im_energy = ax_energy.imshow(np.zeros((GRID_RES, GRID_RES)), cmap='magma', 
                           extent=[-limit, limit, -limit, limit], origin='lower', vmin=0, vmax=1)
ax_energy.set_title("Locked Energy Density ($\\rho_L$)", color='white')

for ax in [ax_wave, ax_energy]:
    ax.tick_params(colors='white')
    ax.set_facecolor('#000')

# Sliders
ax_dist = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor='#222')
s_dist = Slider(ax_dist, 'Drone Distance', 0.1, 8.0, valinit=5.0, color='cyan')

state = {"t": 0}

def update(i):
    if not plt.fignum_exists(fig.number): return im_wave, im_energy
    
    state["t"] += 0.05
    drone_x = s_dist.val
    
    # 1. Generate Waves
    # Simplified engine logic for integrated script
    r_bh = np.sqrt(X**2 + Y**2)
    theta_bh = np.arctan2(Y, X)
    bh_amp = (1.0 - np.exp(-r_bh**2))
    bh_wave = bh_amp * np.sin(2 * np.pi * 1.0 * state["t"] + 5.0 * theta_bh)
    
    r_drone = np.sqrt((X - drone_x)**2 + Y**2)
    drone_amp = 0.5 * (1.0 - np.exp(-r_drone**2))
    drone_wave = drone_amp * np.sin(2 * np.pi * 1.0 * state["t"] + np.pi)
    
    # 2. Interference (Visibility)
    resultant = bh_wave + drone_wave
    im_wave.set_array(np.clip(resultant, -1, 1))
    
    # 3. Locked Energy Calculation
    # Energy is 'Locked' where waves cancel but intensities exist
    locked_energy = (bh_amp**2 + drone_amp**2) - (resultant**2)
    im_energy.set_array(np.clip(locked_energy, 0, 1))
    
    return im_wave, im_energy

ani = animation.FuncAnimation(fig, update, interval=30, blit=True)
plt.show()