import numpy as np

class EventHorizonSolver:
    def __init__(self, R_margin=1.1):
        self.R = R_margin
        self.Rs = 1.0  # Normalized Schwarzschild Radius

    def calculate_required_psi(self, r, phi_ext):
        """
        Step-14 Logic: Calculates the internal phase (Psi) needed 
        to maintain the Alexander Space-Constraint.
        """
        if r <= self.Rs:
            # Beyond the horizon, the potential is locked
            return -self.R * -1.0 
        
        # Psi must mirror the external potential to maintain the 'Ghost'
        return -(self.R * phi_ext)

    def get_tidal_tension(self, r):
        """Calculates the metric gradient (Tidal Force) acting on the vessel."""
        if r <= self.Rs: return 100.0 # Extreme tension
        return 1.0 / (r**3) # Standard tidal decay