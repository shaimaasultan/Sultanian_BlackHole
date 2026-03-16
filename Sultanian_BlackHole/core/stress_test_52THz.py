import numpy as np
import matplotlib.pyplot as plt

# --- Sultanian Constants ---
F_CPU = 5.2e12          # 5.2 Terahertz
TAU = 1.0 / F_CPU       # Clock cycle in seconds
R_MARGIN = 1.1          # The Alexander Space-Constraint
TOLERANCE = 1e-6        # Threshold for "Metric Leakage"
C = 299792458           # Speed of Light (m/s)
RS = 1000.0             # Schwarzschild Radius of the BH (meters)

def get_phi(r):
    """Calculates the Schwarzschild potential at radius r."""
    # Normalized gravitational potential
    return - (RS / r)

def run_stress_test(velocity_pct=0.1):
    """
    Measures at what distance the 5.2 THz clock fails to 
    update the counter-phase fast enough.
    """
    v = velocity_pct * C  # Vessel velocity as % of light
    
    # Range of distances to test (from 10x Rs down to the Horizon)
    distances = np.linspace(RS * 5, RS * 1.0001, 10000)
    failure_r = None
    errors = []

    for r in distances:
        # Potential at current time
        phi_now = get_phi(r)
        
        # Potential at next clock cycle (r moves by v*tau)
        r_next = r - (v * TAU) 
        phi_next = get_phi(r_next)
        
        # The Delta the Governor must 'swallow' in one cycle
        delta_phi = abs(phi_next - phi_now)
        errors.append(delta_phi)
        
        if delta_phi > TOLERANCE and failure_r is None:
            failure_r = r

    return distances, errors, failure_r

# --- Execution & Visualization ---
v_level = 0.5 # 50% Speed of Light
dist, err, fail_point = run_stress_test(v_level)

plt.figure(figsize=(10, 6), facecolor='#050505')
ax = plt.gca()
ax.set_facecolor('#000')

plt.plot(dist, err, color='cyan', label="Delta Phi per Cycle")
plt.axhline(y=TOLERANCE, color='red', linestyle='--', label="5.2 THz Limit")

if fail_point:
    plt.axvline(x=fail_point, color='orange', linestyle=':', label=f"Failure at r={fail_point:.2f}m")
    print(f"CRITICAL FAILURE: Ghost state collapses at {fail_point:.2f} meters.")
    print(f"Proximity to Horizon: {((fail_point/RS)-1)*100:.4f}% above Rs.")

plt.title(f"Sultanian Stress Test: 5.2 THz Governor at {v_level*100}% c", color='white')
plt.xlabel("Distance from Singularity (m)", color='white')
plt.ylabel("Potential Change per Clock Cycle", color='white')
plt.yscale('log')
plt.tick_params(colors='white')
plt.legend()
plt.grid(alpha=0.2)
plt.show()