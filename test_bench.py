"""
Test Bench for Relay Protection System.
Evaluates corner cases and records performance.
"""

import numpy as np
import csv
from adaptive_logic import calculate_adaptive_settings
from ml_model import RelayMLP
from relay_parameters import STANDARD_INVERSE

def run_test_bench():
    # Load ML weights
    weights = np.load("relay_mlp_weights.npz")
    W1, b1, W2, b2 = weights['W1'], weights['b1'], weights['W2'], weights['b2']
    X_mean, X_std = weights['X_mean'], weights['X_std']
    y_mean, y_std = weights['y_mean'], weights['y_std']
    
    def ml_predict(features):
        X = (np.array([features]) - X_mean) / X_std
        z1 = np.dot(X, W1) + b1
        a1 = np.maximum(0, z1)
        z2 = np.dot(a1, W2) + b2
        pred = z2 * y_std + y_mean
        return pred[0]

    # Corner Cases: [i_load, i_grid, i_ibr, ibr_active, name]
    corner_cases = [
        [1100, 2500, 500, 1, "Extreme Load + Weak Grid"],
        [400, 1500, 1200, 1, "Islanding (Low Grid Fault)"],
        [100, 7000, 100, 0, "No Load + Strong Grid"],
        [200, 3000, 1500, 1, "High IBR Contribution"],
        [1200, 2000, 200, 0, "Overload (No IBR)"]
    ]
    
    results = []
    print(f"{'Scenario':<25} | {'Analytical (Is/TMS)':<25} | {'ML (Is/TMS)':<25}")
    print("-" * 80)
    
    for case in corner_cases:
        i_load, i_grid, i_ibr, ibr_active, name = case
        i_fault = i_grid + (i_ibr if ibr_active else 0)
        
        # Analytical
        is_a, tms_a = calculate_adaptive_settings(ibr_active, i_load, i_fault, STANDARD_INVERSE, 0.25 if ibr_active else 0.3)
        
        # ML
        pred = ml_predict([i_load, i_grid, i_ibr, ibr_active])
        is_m, tms_m = pred[0], pred[1]
        
        results.append({
            "scenario": name,
            "is_analytical": is_a,
            "tms_analytical": tms_a,
            "is_ml": is_m,
            "tms_ml": tms_m,
            "diff_is": abs(is_a - is_m),
            "diff_tms": abs(tms_a - tms_m)
        })
        
        print(f"{name:<25} | {is_a:>8.1f}/{tms_a:.4f} | {is_m:>8.1f}/{tms_m:.4f}")

    # Save results
    with open("test_results.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print("\nResults saved to test_results.csv")

if __name__ == "__main__":
    run_test_bench()
