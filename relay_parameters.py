"""
IDMT Relay Parameters and Constants.
Provides standard IEC and IEEE curves for relay coordination.
"""

from dataclasses import dataclass

@dataclass
class IEC_Curve:
    k: float
    alpha: float

# IEC Standard Curves
STANDARD_INVERSE = IEC_Curve(k=0.14, alpha=0.02)
VERY_INVERSE = IEC_Curve(k=13.5, alpha=1.0)
EXTREMELY_INVERSE = IEC_Curve(k=80.0, alpha=2.0)

# CTI (Coordination Time Interval) - Target margin between primary and backup
CTI_TARGET = 0.3  # seconds

# Default Multipliers
PICKUP_SAFETY_FACTOR = 1.25  # Is = 1.25 * I_load_max
FAULT_SENSITIVITY_FACTOR = 0.5  # Is <= 0.5 * I_fault_min
