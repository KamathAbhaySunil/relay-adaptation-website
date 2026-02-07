"""
Simplified 4-Bus System Model.
Calculates fault currents based on grid and IBR contributions.
"""

class SystemModel:
    def __init__(self, v_nom=11000):
        self.v_nom = v_nom  # Nominal Voltage (V)
        self.i_grid_fault_max = 5000  # Max fault current from grid (A)
        self.i_ibr_max = 500  # Max fault contribution from IBR (A)
        self.i_load_max = 800  # Max load current (A)

    def get_fault_current(self, ibr_active):
        """Returns total fault current at the protected bus."""
        if ibr_active:
            # Total fault current is contribution from Grid + IBR
            return self.i_grid_fault_max + self.i_ibr_max
        else:
            # Only Grid contribution
            return self.i_grid_fault_max

    def get_system_parameters(self):
        return {
            "v_nom": self.v_nom,
            "i_load_max": self.i_load_max,
            "i_grid_fault": self.i_grid_fault_max,
            "i_ibr_fault": self.i_ibr_max
        }
