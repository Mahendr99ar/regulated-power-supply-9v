"""
Design calculator for a 230 V AC -> 9 V DC linear power supply
(step-down transformer + bridge rectifier + capacitor filter + LM7809).

Run:  python3 design/psu_design.py
"""
import math

V_SECONDARY_RMS = 12.0     # transformer secondary (230 V : 12 V)
F_MAINS = 50.0             # Hz (India)
V_DIODE = 0.9              # 1N4007 forward drop at ~0.5 A
I_LOAD = 0.5               # A, maximum load current
V_OUT = 9.0                # LM7809 output
V_DROPOUT = 2.0            # LM7809 dropout (datasheet, worst case)
E_SERIES = [1000, 1500, 2200, 3300, 4700]  # common electrolytic values (uF)

v_peak = V_SECONDARY_RMS * math.sqrt(2)
v_dc_peak = v_peak - 2 * V_DIODE               # two diodes conduct in a bridge
v_in_min = V_OUT + V_DROPOUT                   # regulator needs at least this
ripple_allowed = v_dc_peak - v_in_min
f_ripple = 2 * F_MAINS                         # full-wave ripple frequency

c_min_uF = I_LOAD / (f_ripple * ripple_allowed) * 1e6
c_used_uF = next(c for c in E_SERIES if c >= 1.5 * c_min_uF)   # 50 % margin
ripple_used = I_LOAD / (f_ripple * c_used_uF * 1e-6)
p_reg = (v_dc_peak - ripple_used / 2 - V_OUT) * I_LOAD

print(f"Secondary peak voltage      : {v_peak:.2f} V")
print(f"Peak after bridge (2 diodes): {v_dc_peak:.2f} V")
print(f"Minimum regulator input     : {v_in_min:.2f} V")
print(f"Ripple allowed              : {ripple_allowed:.2f} V p-p")
print(f"Minimum filter capacitor    : {c_min_uF:.0f} uF  (C = I / (2 f dV))")
print(f"Capacitor chosen            : {c_used_uF} uF / 25 V")
print(f"Ripple with chosen capacitor: {ripple_used:.2f} V p-p")
print(f"Regulator dissipation       : {p_reg:.2f} W at {I_LOAD} A -> use a heat sink")
print(f"Capacitor voltage rating    : >= {1.5 * v_peak:.0f} V recommended -> 25 V part")
