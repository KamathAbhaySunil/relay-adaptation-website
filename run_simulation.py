"""
Adaptive Relay Coordination Simulation Study.
Runs scenarios and visualizes results.
"""

import numpy as np
import matplotlib.pyplot as plt
from relay_parameters import STANDARD_INVERSE
from adaptive_logic import calculate_adaptive_settings
from system_model import SystemModel

def run_study():
    model = SystemModel()
    params = model.get_system_parameters()
    
    # 1. Define Scenarios
    # Scenario A: Fixed Settings (Calculated for IBR Off)
    is_fixed, tms_fixed = calculate_adaptive_settings(
        ibr_active=False,
        i_load=params["i_load_max"],
        i_fault=params["i_grid_fault"],
        curve=STANDARD_INVERSE,
        target_time=0.3
    )
    
    # Scenario B: Adaptive Settings (Recalculated for IBR On)
    is_adaptive, tms_adaptive = calculate_adaptive_settings(
        ibr_active=True,
        i_load=params["i_load_max"],
        i_fault=params["i_grid_fault"] + params["i_ibr_fault"],
        curve=STANDARD_INVERSE,
        target_time=0.25  # Slightly faster for adaptive
    )
    
    print("--- RELAY SETTINGS COMPARISON ---")
    print(f"Fixed (IBR OFF)   : Is = {is_fixed:.2f} A, TMS = {tms_fixed:.4f}")
    print(f"Adaptive (IBR ON) : Is = {is_adaptive:.2f} A, TMS = {tms_adaptive:.4f}")
    
    # 2. Plot TCC Curves
    i_range = np.linspace(1.1 * min(is_fixed, is_adaptive), 6000, 200)
    
    def calc_time(i, i_s, tms, curve):
        psm = i / i_s
        # Avoid division by zero if PSM <= 1
        with np.errstate(divide='ignore', invalid='ignore'):
            t = tms * (curve.k / (np.power(psm, curve.alpha) - 1))
        return t

    t_fixed = calc_time(i_range, is_fixed, tms_fixed, STANDARD_INVERSE)
    t_adaptive = calc_time(i_range, is_adaptive, tms_adaptive, STANDARD_INVERSE)
    
    plt.figure(figsize=(10, 6))
    plt.loglog(i_range, t_fixed, 'r--', label='Fixed Settings (IBR OFF base)', linewidth=2)
    plt.loglog(i_range, t_adaptive, 'b-', label='Adaptive Settings (IBR ON active)', linewidth=2)
    
    # Mark Fault Levels
    plt.axvline(x=params["i_grid_fault"], color='k', linestyle=':', label='Fault (Grid Only)')
    plt.axvline(x=params["i_grid_fault"] + params["i_ibr_fault"], color='g', linestyle=':', label='Fault (Grid+IBR)')
    
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.xlabel('Current (A)')
    plt.ylabel('Operating Time (s)')
    plt.title('TCC Curve Comparison: Fixed vs Adaptive Protection')
    plt.legend()
    
    output_path = "relay_tcc_comparison.png"
    plt.savefig(output_path)
    print(f"\nSimulation complete. Plot saved as {output_path}")

if __name__ == "__main__":
    run_study()
