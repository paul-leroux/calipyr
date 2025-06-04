# main.py
import pandas as pd
import matplotlib.pyplot as plt
from config import params
from simulation import NorSandTriaxialSimulation
import numpy as np

# Modify for undrained triaxial test
params["undrained"] = True

# Run the simulation
sim = NorSandTriaxialSimulation(params)
results = sim.run()
df = pd.DataFrame(results)

# Add ln(p') column
df["ln_p"] = np.log(df["p"].where(df["p"] > 0))

# Save to CSV
output_csv = "norsand_undrained_results.csv"
df.to_csv(output_csv, index=False)
print(f"Results saved to {output_csv}")

# Plot q vs ε1
plt.figure()
plt.plot(df["eps1"], df["q"])
plt.xlabel("Axial Strain ε₁ (m/m)")
plt.ylabel("Deviatoric Stress q (kPa)")
plt.title("Undrained: q vs ε₁")
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot p vs εv
plt.figure()
plt.plot(df["epsV"], df["p"])
plt.xlabel("Volumetric Strain εᵥ (m/m)")
plt.ylabel("Mean Effective Stress p' (kPa)")
plt.title("Undrained: p' vs εᵥ")
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot q vs p with CSL
plt.figure()
plt.plot(df["p"], df["q"], label="Stress Path")
p_range = np.linspace(df["p"].min(), df["p"].max(), 200)
csl_q = params["Mc"] * p_range
plt.plot(p_range, csl_q, '--', label="CSL: q = Mc·p'")
plt.xlabel("Mean Effective Stress p' (kPa)")
plt.ylabel("Deviatoric Stress q (kPa)")
plt.title("Undrained: Stress Path (q vs p') with CSL")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot log scale p' vs e with CSL
plt.figure()
plt.plot(df["p"], df["e"], label="Compression Path")
ec_csl = params["N"] - params["lambda"] * np.log(df["p"].where(df["p"] > 0))
plt.plot(df["p"], ec_csl, '--', label="CSL: e = N - λ·ln(p')")
plt.xscale("log")
plt.xlabel("Mean Effective Stress p' (kPa) [log scale]")
plt.ylabel("Void Ratio e (-)")
plt.title("Undrained: log-scaled p' vs e with CSL")
plt.legend()
plt.grid(True, which="both")
plt.tight_layout()
plt.show()

# Plot pore pressure vs strain
plt.figure()
plt.plot(df["eps1"], df["pore_pressure"])
plt.xlabel("Axial Strain ε₁ (m/m)")
plt.ylabel("Pore Pressure u (kPa)")
plt.title("Undrained: Pore Pressure vs ε₁")
plt.grid(True)
plt.tight_layout()
plt.show()
