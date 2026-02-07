# Walkthrough: Adaptive Relay Protection in Python

The project has been successfully migrated from MATLAB to Python. The new implementation replaces the Simulink model with a nodal analysis script and uses `matplotlib` for visualization.

## Changes Made

### Core Logic
- [relay_parameters.py](file:///home/abhay/.gemini/antigravity/brain/3e2dc557-7e04-413f-b050-2c9b620e897c/relay_parameters.py): Ported IEC standard constants.
- [adaptive_logic.py](file:///home/abhay/.gemini/antigravity/brain/3e2dc557-7e04-413f-b050-2c9b620e897c/adaptive_logic.py): Implemented the adaptive calculation for $Is$ and $TMS$.
- [system_model.py](file:///home/abhay/.gemini/antigravity/brain/3e2dc557-7e04-413f-b050-2c9b620e897c/system_model.py): Created a 4-bus fault current calculator.

### Simulation and Visualization
### Documentation and Reporting
- [run_simulation.py](file:///home/abhay/.gemini/antigravity/brain/3e2dc557-7e04-413f-b050-2c9b620e897c/run_simulation.py): Master script that executes research scenarios and generates plots.
- [main.tex](file:///home/abhay/.gemini/antigravity/brain/3e2dc557-7e04-413f-b050-2c9b620e897c/main.tex): A comprehensive 3+ page IEEE conference report documenting the theoretical background of IBRs, nodal mathematics, and a detailed line-by-line analysis of the Python implementation.

## Results

### Relay Settings Comparison
The simulation compares relay settings with and without IBR contribution:

| Parameter | Fixed (IBR OFF) | Adaptive (IBR ON) |
| :--- | :--- | :--- |
| Pickup Current ($Is$) | 1000.00 A | 1040.00 A |
| Time Multiplier ($TMS$) | 0.0701 | 0.0605 |

### Time-Current Characteristic (TCC)
The following plot shows the coordination curve. The adaptive curve (blue) is slightly faster and adjusted for the higher fault current level when the IBR is active.

![TCC Curve Comparison](/home/abhay/.gemini/antigravity/brain/3e2dc557-7e04-413f-b050-2c9b620e897c/relay_tcc_comparison.png)

## Verification
- Standard IEC formulas verified with `numpy`.
- Adaptive logic correctly adjusts $Is$ based on `ibr_active` flag.
- Visualization confirms log-log TCC behavior.
