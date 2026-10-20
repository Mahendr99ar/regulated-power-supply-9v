"""
Plot the ngspice waveforms of the 9 V supply (last 40 ms = two mains cycles).

Run from the repo folder after the simulation:
    ngspice -b simulation/psu_9v.cir
    python3 simulation/plot_waveform.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
with open(os.path.join(HERE, "waveform.txt")) as f:
    for line in f:
        parts = line.split()
        try:
            rows.append([float(x) for x in parts])
        except ValueError:
            continue                      # skip any header line

t_end = rows[-1][0]
rows = [r for r in rows if r[0] >= t_end - 0.04]
t = [(r[0] - (t_end - 0.04)) * 1000 for r in rows]
sec = [abs(r[1]) for r in rows]
vin = [r[2] for r in rows]
vout = [r[3] for r in rows]

fig, ax = plt.subplots(figsize=(9, 4.6))
ax.plot(t, sec, color="#9AA0A6", lw=1.2, ls="--", label="|Transformer secondary|")
ax.plot(t, vin, color="#2A2E33", lw=2, label="Filter capacitor (regulator input)")
ax.plot(t, vout, color="#D4A017", lw=2.4, label="LM7809 output")
ax.axhline(11, color="#C0392B", ls=":", lw=1.4, label="11 V: minimum for regulation")
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Voltage (V)")
ax.set_title("ngspice: 2200 µF filter, 500 mA load")
ax.set_ylim(0, 19)
ax.grid(alpha=0.3)
ax.legend(loc="lower right", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "waveform.png"), dpi=130)
print("wrote simulation/waveform.png")
