import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.animation as animation

# --- Physics of the Whirlpool ---
def get_vorticity(r, bh_spin):
    """Vorticity increases as r decreases toward the cancellation node."""
    return bh_spin / (r**2)

# --- Interactive Dashboard ---
fig, (ax_wave, ax_sync) = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(bottom=0.25)
fig.set_facecolor('#050505')

# Wave View: Visualizing the Whirlpool vs Vessel
t = np.linspace(0, 1, 500)
ax_wave.set_facecolor('#000')
line_bh, = ax_wave.plot(t, np.zeros(500), 'w--', alpha=0.3, label="BH Whirlpool")
line_drone, = ax_wave.plot(t, np.zeros(500), 'm', alpha=0.6, label="Drone Phase")
line_res, = ax_wave.plot(t, np.zeros(500), 'c', linewidth=2, label="Locked Energy")

ax_wave.set_ylim(-2.5, 2.5)
ax_wave.legend(loc='upper right')

# Sync Bar
ax_sync.set_facecolor('#111')
bar = ax_sync.bar(["Energy Locking (Ghosting)"], [0], color='cyan')
ax_sync.set_ylim(0, 1.0)

# Sliders
ax_r = plt.axes([0.2, 0.15, 0.6, 0.03], facecolor='#222')
ax_sync_ctrl = plt.axes([0.2, 0.10, 0.6, 0.03], facecolor='#222')
ax_spin = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='#222')

s_r = Slider(ax_r, 'Radius (r)', 1.05, 10.0, valinit=5.0, color='white')
s_sync = Slider(ax_sync_ctrl, 'Phase Sync', 0.0, 2*np.pi, valinit=0.0, color='cyan')
s_spin = Slider(ax_spin, 'BH Spin', 1.0, 10.0, valinit=5.0, color='orange')

def update(i):
    if not plt.fignum_exists(fig.number): return line_bh, line_drone, line_res, bar
    
    r = s_r.val
    spin = s_spin.val
    sync_input = s_sync.val
    
    vorticity = get_vorticity(r, spin)
    
    # Calculate Waves
    bh_wave = np.sin(2 * np.pi * vorticity * (t + i*0.01))
    # Vessel tries to match R=1.1 cancellation
    drone_wave = np.sin(2 * np.pi * vorticity * (t + i*0.01) + sync_input + np.pi)
    
    resultant = bh_wave + drone_wave
    
    # Update Lines
    line_bh.set_ydata(bh_wave)
    line_drone.set_ydata(drone_wave)
    line_res.set_ydata(resultant)
    
    # Calculate how much energy is 'locked' (cancellation success)
    lock_factor = 1.0 - (np.sqrt(np.mean(resultant**2)) / 1.414)
    bar[0].set_height(max(lock_factor, 0))
    
    if lock_factor > 0.95:
        ax_sync.set_title("STATUS: ENERGY LOCKED / GHOSTED", color='cyan')
        bar[0].set_color('cyan')
    else:
        ax_sync.set_title("STATUS: DECOHERENCE / VISIBLE", color='red')
        bar[0].set_color('red')
        
    return line_bh, line_drone, line_res, bar

ani = animation.FuncAnimation(fig, update, interval=30, blit=False)
plt.show()