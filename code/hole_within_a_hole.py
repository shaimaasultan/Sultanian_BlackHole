import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.animation as animation

# --- Simulation Constants ---
GRID_SIZE = 200     # Resolution of the space
VIEW_RANGE = 20.0   # Boundary of the plot (+/- 10)
BASE_FREQ = 1.0     # Baseline 5.2 THz frequency

def get_radial_wave(x, y, cx, cy, freq, time, amplitude):
    """Generates a radial wave centered at (cx, cy)."""
    r = np.sqrt((x - cx)**2 + (y - cy)**2)
    # The 'Null Zone' is where r=0, so the amplitude must drop at the center
    # This simulates total destructive interference at the node.
    wave = amplitude * (1.0 - np.exp(-r**2)) * np.sin(2 * np.pi * freq * time)
    return wave

# Setup Figure
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.20)
fig.set_facecolor('#050505')
ax.set_facecolor('#000')

# Create Space Grid (x, y)
x = np.linspace(-VIEW_RANGE/2, VIEW_RANGE/2, GRID_SIZE)
y = np.linspace(-VIEW_RANGE/2, VIEW_RANGE/2, GRID_SIZE)
X, Y = np.meshgrid(x, y)

# Initial Parameters
initial_r = 8.0 # Starting distance of the drone
bh_amp = 1.5
drone_amp = 0.5 # A small, local ghost

# Display Setup (Colormap: 'bone' provides high contrast for 'Null Zones')
im = ax.imshow(np.zeros((GRID_SIZE, GRID_SIZE)), cmap='bone', extent=[-VIEW_RANGE/2, VIEW_RANGE/2, -VIEW_RANGE/2, VIEW_RANGE/2], origin='lower', vmin=-1.0, vmax=1.0)

ax.set_title("Sultanian Protocol: The Hole Within a Hole", color='white')
ax.tick_params(colors='white')
cbar = plt.colorbar(im)
cbar.set_label("Plenum Amplitude (Metric Tension)", color='white')
cbar.ax.yaxis.set_tick_params(color='white')

# Sliders for real-time interaction
ax_r = plt.axes([0.2, 0.10, 0.6, 0.03], facecolor='#222')
ax_freq = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='#222')

s_r = Slider(ax_r, 'Drone Distance (r)', 0.1, 10.0, valinit=initial_r, color='cyan')
s_freq = Slider(ax_freq, 'Plenum Freq', 0.1, 3.0, valinit=BASE_FREQ, color='white')

# Static Plot elements: The Horizon (The Outer Rim)
# Rs is roughly where bh_amp * (1 - exp(-Rs^2)) = 1.0 (arbitrary threshold)
circle = plt.Circle((0, 0), 2.5, color='cyan', fill=False, linestyle='--', alpha=0.3, label="Horizon (Rs)")
ax.add_artist(circle)
ax.legend(loc='upper right', facecolor='#111', labelcolor='white')

# Animation State
state = {"time": 0}

def update(i):
    if not plt.fignum_exists(fig.number): return im
    
    state["time"] += 0.05
    r_drone = s_r.val
    freq = s_freq.val
    
    # Position the drone always on the x-axis for simplicity
    drone_x = r_drone
    drone_y = 0.0
    
    # 1. Calculate Black Hole Wave (Fixed at 0,0)
    wave_bh = get_radial_wave(X, Y, 0, 0, freq, state["time"], bh_amp)
    
    # 2. Calculate Drone Wave (Ghost)
    # The Ghost must be 180 degrees out of phase with the plenum to work.
    # We add np.pi to the time argument.
    wave_drone = get_radial_wave(X, Y, drone_x, drone_y, freq, state["time"] + (0.5/freq), drone_amp)
    
    # 3. Superposition: The Interference Pattern
    resultant = wave_bh + wave_drone
    
    # Normalize result for display [-1.0 to 1.0]
    resultant_norm = np.clip(resultant, -1.0, 1.0)
    
    im.set_array(resultant_norm)
    
    # Dynamic status update
    if r_drone < 2.0:
        ax.set_title("STATUS: GHOST DECOHERENCE (MERGING)", color='orange')
    elif r_drone < 0.2:
        ax.set_title("STATUS: HOLE WITHIN A HOLE (SYNCHRONIZED)", color='cyan')
    else:
        ax.set_title("STATUS: GHOST STATE (DECOUPLED)", color='white')
        
    return im

ani = animation.FuncAnimation(fig, update, interval=50, blit=False)
plt.show()