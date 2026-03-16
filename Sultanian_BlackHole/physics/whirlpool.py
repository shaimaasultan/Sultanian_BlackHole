import numpy as np

class WhirlpoolEngine:
    def __init__(self, spin=5.0):
        self.spin = spin
        self.base_freq = 1.0

    def generate_vorticity_field(self, X, Y, t):
        """Generates the spiral wave pattern of the plenum."""
        r = np.sqrt(X**2 + Y**2)
        theta = np.arctan2(Y, X)
        
        # The 'Null Zone' damping (amplitude vanishes at r=0)
        amplitude = (1.0 - np.exp(-r**2))
        
        # Spiral phase: The 'Whirlpool' logic
        # Frequency increases toward center to simulate vorticity
        spiral_phase = self.spin * theta
        
        wave = amplitude * np.sin(2 * np.pi * self.base_freq * t + spiral_phase)
        return wave

    def get_drone_wave(self, X, Y, dx, dy, t):
        """Generates the local destructive interference wave for the drone."""
        r_drone = np.sqrt((X - dx)**2 + (Y - dy)**2)
        # 180-degree phase shift for cancellation
        drone_wave = 0.5 * (1.0 - np.exp(-r_drone**2)) * np.sin(2 * np.pi * self.base_freq * t + np.pi)
        return drone_wave