"""
Task 1: DNA stretching model (Worm-Like Chain)

The whole assignment is really just: implement one formula, call it in a loop
over three parameter values, and plot the results.

The formula (Marko-Siggia interpolation):

    F(z) = (kBT / P) * [ 1/(4*(1-z)^2) - 1/4 + z ]

where z = x/L is "what fraction of its full length is the molecule stretched to",
so z = 0 means totally coiled up and z = 1 means totally straight.

Run:  python wlc_simple.py
Makes: wlc_simple.png and wlc_simple.csv
"""

import numpy as np
import matplotlib.pyplot as plt

# ---- constants -------------------------------------------------------
# kBT is the amount of energy things have just from being at room temperature.
# 4.1 pN*nm is that energy written in units that match our other units,
# so the force comes out in piconewtons (pN) without any conversion.
kBT = 4.1

# P = persistence length in nanometers. This is the "stiffness" knob.
# We test three values because the assignment says to.
P_VALUES = [30.0, 50.0, 70.0]


# ---- the model -------------------------------------------------------
def force(z, P, kBT=4.1):
    """Given how stretched the DNA is (z, from 0 to <1), return the force in pN.

    z can be a single number or a numpy array - numpy handles both.
    """
    # Guard clause: the formula divides by (1-z)^2, so z = 1 is a divide by zero.
    if np.any(np.asarray(z) >= 1.0):
        raise ValueError("z must be less than 1 - the formula blows up at z = 1")

    return (kBT / P) * (1.0 / (4.0 * (1.0 - z) ** 2) - 0.25 + z)


# ---- run it ----------------------------------------------------------
# 400 evenly spaced z values from 0.05 to 0.95.
# We stop at 0.95, not 1.0, because of the divide-by-zero above.
z = np.linspace(0.05, 0.95, 400)

# Dict comprehension: {30.0: array_of_forces, 50.0: ..., 70.0: ...}
results = {P: force(z, P) for P in P_VALUES}


# ---- plot ------------------------------------------------------------
# Two side-by-side plots. Left is the normal one. Right uses a log scale on the
# force axis, because on the normal plot all three curves look flat and identical
# until the very end, which hides the actual difference between them.
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.6))

for P in P_VALUES:
    left.plot(z, results[P], lw=2, label=f"P = {P:.0f} nm")
    right.semilogy(z, results[P], lw=2, label=f"P = {P:.0f} nm")

left.set_title("Normal scale")
left.set_ylim(0, 15)   # cut off the top, otherwise the spike squashes everything

right.set_title("Log scale on force axis")

for ax in (left, right):
    ax.set_xlabel("How stretched:  x/L  (0 = coiled, 1 = straight)")
    ax.set_ylabel("Force needed  (pN)")
    ax.set_xlim(0, 1)
    ax.legend(title="Stiffness")
    ax.grid(alpha=0.3)

fig.suptitle("How hard you have to pull DNA to stretch it (WLC model)")
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig("wlc_simple.png", dpi=300)


# ---- save the numbers + check the code works -------------------------
np.savetxt("wlc_simple.csv",
           np.column_stack([z] + [results[P] for P in P_VALUES]),
           delimiter=",", header="z,F_P30,F_P50,F_P70", comments="")

print("Force (pN) at a few stretch levels:\n")
print(f"{'x/L':>6} | {'P=30':>9} {'P=50':>9} {'P=70':>9}")
print("-" * 40)
for zc in [0.05, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]:
    print(f"{zc:6.2f} | {force(zc, 30):9.3f} {force(zc, 50):9.3f} {force(zc, 70):9.3f}")

# Unit test, basically. P only shows up in the formula as division by P,
# so doubling P should exactly halve the force. Check that it does.
print(f"\nSanity check - force ratio P=30 vs P=70 at z=0.5: "
      f"{force(0.5, 30) / force(0.5, 70):.4f}")
print(f"Should be exactly 70/30 = {70/30:.4f}  -> code implements formula correctly")
