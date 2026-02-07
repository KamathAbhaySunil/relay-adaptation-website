"""
Adaptive Relay Logic for Microgrid Protection.
Recalculates relay settings based on IBR contribution and fault scenarios.
"""

def calculate_adaptive_settings(ibr_active, i_load, i_fault, curve, target_time):
    """
    Calculates the optimal Pickup Current (Is) and Time Multiplier Setting (TMS).
    
    Args:
        ibr_active: Boolean, true if IBR is connected.
        i_load: Maximum expected load current (A).
        i_fault: Minimum expected fault current (A).
        curve: IEC_Curve object (k, alpha).
        target_time: Desired operating time (s).
        
    Returns:
        tuple: (Is, TMS)
    """
    # 1. Calculate Pickup Current (Is)
    if ibr_active:
        # If IBR is on, we might tighten or loosen safety factors.
        # For this model, we slightly increase the margin for load.
        is_pickup = 1.3 * i_load
    else:
        is_pickup = 1.25 * i_load
        
    # Ensure sensitivity: Is must be less than fault current
    if is_pickup > 0.8 * i_fault:
        is_pickup = 0.5 * i_fault
        
    # 2. Calculate TMS
    # Operating time formula: t = TMS * (k / ((I/Is)^alpha - 1))
    # => TMS = t / (k / ((I/Is)^alpha - 1))
    
    psm = i_fault / is_pickup  # Plug Setting Multiplier
    
    if psm <= 1:
        tms = 0.1  # Minimum default if sensitivity is lost
    else:
        tms = target_time / (curve.k / (pow(psm, curve.alpha) - 1))
        
    # Constrain TMS within typical relay ranges (0.05 to 1.1)
    tms = max(0.05, min(1.1, tms))
    
    return is_pickup, tms
