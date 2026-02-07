"""
Data Generator for Relay Setting ML Model.
Generates synthetic network scenarios and computes analytical labels.
"""

import numpy as np
import csv
from adaptive_logic import calculate_adaptive_settings
from relay_parameters import STANDARD_INVERSE

def generate_data(num_samples=2000):
    data = []
    
    for _ in range(num_samples):
        i_load = np.random.uniform(200, 1200)
        i_grid = np.random.uniform(2000, 8000)
        i_ibr = np.random.uniform(300, 1500)
        ibr_active = np.random.choice([True, False])
        
        i_fault = i_grid + (i_ibr if ibr_active else 0)
        
        is_pickup, tms = calculate_adaptive_settings(
            ibr_active=ibr_active,
            i_load=i_load,
            i_fault=i_fault,
            curve=STANDARD_INVERSE,
            target_time=0.25 if ibr_active else 0.3
        )
        
        data.append([
            i_load, i_grid, i_ibr, int(ibr_active), i_fault, is_pickup, tms
        ])
        
    with open("relay_training_data.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["i_load", "i_grid", "i_ibr_potential", "ibr_active", "i_fault", "is_pickup_target", "tms_target"])
        writer.writerows(data)
    
    print(f"Generated {num_samples} samples and saved to relay_training_data.csv")

if __name__ == "__main__":
    generate_data()
