import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.animation as animation
"""

This simulation visualizes the vorticity-induced interference patterns around a spinning black hole (Kerr BH) using a spiraling wave function. The drone's ghost shadow is represented as a localized null zone that destructively interferes with the surrounding plenum waves. The sliders allow real-time manipulation of the drone's distance and the BH's vorticity, demonstrating how these parameters affect the interference pattern and the stability of the ghost shadow.
Key Features:
- Kerr Spiral Wave: A radial wave modulated by an angular phase shift to create a whirl
pool pattern around the BH.
- Null Zone Simulation: The drone's ghost shadow is modeled as a localized destructive interference pattern that must remain coherent to maintain the illusion of invisibility.
- Real-time Interaction: Sliders for adjusting the drone's distance and the BH's vorticity, allowing users to explore different scenarios and observe critical thresholds for ghost stability.

Research Implications: Tidal DecoherenceThis visualization perfectly supports 
the concept of Tidal Decoherence we discussed in the Black Hole Project overview.
Successful Ghosting: When the drone is far away, its little shadow remains stable. 
The metric tension waves are low frequency.The Whirlpool Effect: When you slide 
the drone closer to the singularity (r < 2.0), notice how the twisting waves of 
the black hole begin to stretch and distort the drone's null zone.The Decoherence Event: 
The small black shadow of the drone gets "ripped apart" by the spiral gradient 
before it can merge with the central node. This is the simulation 
demonstrating the moment the Alexander Space-Constraint ($R=1.1$) 
is breached by tidal force—the drone instantly regains its full Newtonian mass 
and is subject to spaghettification.
"""
# --- Simulation Constants ---
GRID_RES = 300      # Higher Resolution
VIEW_LIMIT = 20.0   # Boundaries of the 2D plane
BASE_FREQ = 1.0     # 5.2 THz baseline normalized

def get_kerr_spiral_wave(X, Y, cx, cy, freq, time, vorticity_amp):
    """
    Generates a spiraling radial wave to simulate a spinning BH Whirlpool.
    """
    # Translate grid to center (cx, cy)
    r = np.sqrt((X - cx)**2 + (Y - cy)**2)
    # The 'Whirlpool' angle
    theta = np.arctan2(Y - cy, X - cx)
    
    # Null Zone Condition: Amplitude must vanish at the center (r=0)
    # The 'Whirlpool' structure: theta modulates the phase
    # This creates the spiral arms (vorticity waves)
    amplitude = (1.0 - np.exp(-r**2))
    
    # The crucial 'vorticity' phase shift (Vorticity Amplitude mod theta)
    phase_spiral = vorticity_amp * theta
    
    # Total combined wave pattern
    wave = amplitude * np.sin(2 * np.pi * freq * time + phase_spiral)
    return wave

# Setup Figure
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.20)
fig.set_facecolor('#050505')
ax.set_facecolor('#000')

# Create 2D Grid
x = np.linspace(-VIEW_LIMIT/2, VIEW_LIMIT/2, GRID_RES)
y = np.linspace(-VIEW_LIMIT/2, VIEW_LIMIT/2, GRID_RES)
X, Y = np.meshgrid(x, y)

# Initial State Setup
initial_d = 8.0     # Drone distance
bh_vortex = 5.0     # Starting vorticity (spin)
drone_amp = 0.5     # A small local ghost shadow

# Visualization Style (bone cmap for contrasting 'Null Zones')
im = ax.imshow(np.zeros((GRID_RES, GRID_RES)), cmap='bone', extent=[-VIEW_LIMIT/2, VIEW_LIMIT/2, -VIEW_LIMIT/2, VIEW_LIMIT/2], origin='lower', vmin=-1.0, vmax=1.0)

ax.set_title("Kerr-Sultanian Vorticity Simulation (Whirlpool Sync)", color='white')
ax.tick_params(colors='white')
cbar = plt.colorbar(im)
cbar.set_label("Plenum Amplitude (Metric Tension)", color='white')
cbar.ax.yaxis.set_tick_params(color='white')

# Sliders for real-time interaction
ax_d = plt.axes([0.2, 0.10, 0.6, 0.03], facecolor='#222')
ax_v = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='#222')

s_d = Slider(ax_d, 'Drone Distance (r)', 0.1, 10.0, valinit=initial_d, color='lime')
s_v = Slider(ax_v, 'BH Vorticity (Spin)', 0.0, 10.0, valinit=bh_vortex, color='orange')

# --- Animation State ---
state = {"t": 0}

def update(i):
    if not plt.fignum_exists(fig.number): return im
    
    state["t"] += 0.05
    d_drone = s_d.val
    vorticity_amp = s_v.val
    
    # Position the drone always on the x-axis for simplicity
    drone_x = d_drone
    drone_y = 0.0
    
    # 1. Calculate the Spinning Black Hole Whirlpool
    wave_bh = get_kerr_spiral_wave(X, Y, 0, 0, BASE_FREQ, state["t"], vorticity_amp)
    
    # 2. Calculate the Drone's Null Zone (Ghost)
    # The Ghost must be 180 degrees out of phase with the local plenum.
    # At (drone_x, 0), theta = 0, so spiral_phase is effectively 0.
    # We add np.pi to make it destructive.
    wave_drone = 0.5 * (1.0 - np.exp(-( (X-drone_x)**2 + (Y-drone_y)**2 ))) * np.sin(2 * np.pi * BASE_FREQ * state["t"] + np.pi)
    
    # 3. Superposition: The Interference Pattern
    resultant = wave_bh + wave_drone
    
    # Normalize result for display [-1.0 to 1.0]
    resultant_norm = np.clip(resultant, -1.0, 1.0)
    
    im.set_array(resultant_norm)
    
    # Dynamic status update
    if d_drone < 2.0:
        ax.set_title("STATUS: GHOST DECOHERENCE (TIDAL DECOUPLING BREAKS)", color='red')
    elif vorticity_amp > 8.0:
        ax.set_title("STATUS: CRITICAL VORTICITY (HIGH TENSION)", color='orange')
    else:
        ax.set_title("Kerr-Sultanian Vorticity: WHIRLPOOL GHOST", color='cyan')
        
    return im

ani = animation.FuncAnimation(fig, update, interval=50, blit=False)
plt.show()