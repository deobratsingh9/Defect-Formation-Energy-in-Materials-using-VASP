#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

# =========================
# JOURNAL STYLE
# =========================
plt.rcParams.update({
    "font.size": 14,
    "axes.labelsize": 16,
    "axes.titlesize": 16,
    "legend.fontsize": 12,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "lines.linewidth": 2.5,
    "figure.dpi": 150,
    "savefig.dpi": 600,
    "font.family": "DejaVu Sans"
})

# =========================
# READ DATA FILE
# =========================

# expects whitespace-separated file
data = np.genfromtxt(
    "data.dat",
    dtype=str,
    comments="#"
)

systems = data[:, 0]
energy = data[:, 1].astype(float)
fermi_ref = data[:, 2].astype(float)
vbm = data[:, 3].astype(float)
cbm = data[:, 4].astype(float)

# =========================
# CONSTANTS
# =========================

E_bulk = energy[0]      # first line = bulk
VBM_bulk = vbm[0]
CBM_bulk = cbm[0]
Eg = CBM_bulk - VBM_bulk

mu_C = -32.73462957 / 4.0

EF = np.linspace(0, Eg, 1000)

# =========================
# FORMATION ENERGY
# =========================

curves = {}
all_curves = []

for i in range(1, len(systems)):

    name = systems[i]
    Edef = energy[i]

    # charge extraction from label
    if "+" in name:
        q = int(name.split("+")[-1])
    elif "-" in name:
        q = -int(name.split("-")[-1])
    else:
        q = 0

    # formation energy (your same formula)
    Eform = Edef - E_bulk - mu_C + q * (VBM_bulk + EF)

    curves[name] = Eform
    all_curves.append(Eform)

all_curves = np.array(all_curves)

# shift for clean plot
shift = np.min(all_curves) - 0.5

# =========================
# PLOT
# =========================

fig, ax = plt.subplots(figsize=(8, 6))

ax.axhline(0, linestyle="--", color="black", linewidth=1.8)

colors = plt.cm.tab10(np.linspace(0, 1, len(curves)))

plot_curves = []

for i, (name, y) in enumerate(curves.items()):

    y_shifted = y - shift
    plot_curves.append(y_shifted)

    ax.plot(EF, y_shifted, color=colors[i], label=name)

plot_curves = np.array(plot_curves)

# envelope
envelope = np.min(plot_curves, axis=0)

ax.plot(
    EF,
    envelope,
    color="black",
    linewidth=3.5,
    label="Ground-state envelope"
)

# =========================
# TRANSITION LINES
# =========================

for i in range(len(EF) - 1):

    idx1 = np.argmin(plot_curves[:, i])
    idx2 = np.argmin(plot_curves[:, i + 1])

    if idx1 != idx2:
        ax.axvline(EF[i], linestyle=":", color="gray", linewidth=0.8, alpha=0.6)

# =========================
# LABELS
# =========================

ax.set_xlabel("Fermi Energy (eV)")
ax.set_ylabel("Formation Energy (eV)")
ax.set_title("Carbon Vacancy Formation Energy in SiC")

ax.set_xlim(0, Eg)
ax.set_ylim(-1, 8)

ax.text(0.02 * Eg, 7.2, "VBM")
ax.text(0.85 * Eg, 7.2, "CBM")

ax.grid(alpha=0.25)
ax.legend(frameon=False)

plt.tight_layout()

plt.savefig("VC_formation_energy.png", dpi=600, bbox_inches="tight")
#plt.savefig("VC_formation_energy.pdf", bbox_inches="tight")

plt.show()

# =========================
# PRINT INFO
# =========================

print("\n======================================")
print("Bulk SiC loaded from data.dat")
print("VBM =", VBM_bulk, "eV")
print("CBM =", CBM_bulk, "eV")
print("Band gap =", Eg, "eV")
print("mu_C =", mu_C, "eV")
print("Saved: VC_formation_energy.png")
print("======================================")
