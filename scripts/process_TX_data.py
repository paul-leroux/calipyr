# process_TX_data.py

"""
Load cached triaxial test data from pickle file and prepare for processing.

Author: Paul le Roux
Date: 2025-06-04
"""

import pickle
from pathlib import Path
import pandas as pd

# Path to cached .pkl file
CACHE_FILE = Path(r"C:\Users\Python\Projects\calipyr\_cache\imported_triaxials.pkl")


def load_cached_triaxial_data(cache_path: Path) -> dict:
    """Load the triaxial test data dictionary from a .pkl file."""
    if not cache_path.exists():
        raise FileNotFoundError(f"Cached file not found: {cache_path}")

    with open(cache_path, "rb") as f:
        data = pickle.load(f)

    print(f"Loaded triaxial data from cache: {cache_path}")
    return data


if __name__ == "__main__":
    imported_data = load_cached_triaxial_data(CACHE_FILE)

    # Example usage
    for material, tests in imported_data.items():
        print(f"\nMaterial: {material}")
        for test_id, phases in tests.items():
            loaded_phases = list(phases.keys())
            print(f"  {test_id} → {loaded_phases}")








import matplotlib.pyplot as plt

# Plot stress paths and state paths for each material
for material, tests in imported_data.items():
    print(f"\nProcessing material: {material}")

    plt.figure()
    for test_id, phases in tests.items():
        if "Shear" not in phases:
            print(f"  Skipping {test_id}: missing shear phase")
            continue

        df = phases["Shear"]

        # Fuzzy column access
        colmap = {col.lower(): col for col in df.columns}
        try:
            p_col = next(colmap[k] for k in colmap if "mean" in k and "p" in k)
            q_col = next(colmap[k] for k in colmap if "deviator" in k or "q" in k)
        except StopIteration:
            print(f"  Skipping {test_id}: missing p' or q column")
            continue

        plt.plot(df[p_col], df[q_col], label=test_id)

    plt.xlabel("Mean effective stress, p' [kPa]")
    plt.ylabel("Deviator stress, q [kPa]")
    plt.title(f"Stress paths for {material}")
    plt.xlim(left=0)
    plt.ylim(bottom=0.45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Now plot e–log(p') state paths
    plt.figure()
    for test_id, phases in tests.items():
        if "Shear" not in phases:
            continue

        df = phases["Shear"]
        colmap = {col.lower(): col for col in df.columns}
        try:
            p_col = next(colmap[k] for k in colmap if "mean" in k and "p" in k)
            e_col = next(colmap[k] for k in colmap if k.strip().startswith("e"))
        except StopIteration:
            print(f"  Skipping {test_id}: missing p' or e column")
            continue

        plt.plot(df[p_col], df[e_col], label=test_id)

    plt.xlabel("Mean effective stress, p' [kPa]")
    plt.xscale("log")
    plt.ylabel("Void ratio, e [–]")
    plt.title(f"State paths for {material}")
    plt.grid(True)
    plt.xlim(left=10)  # log scale: must be > 0
    plt.ylim(bottom=0.45)  # allow auto top limit
    plt.ylim(top=1.0)
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure()
    for test_id, phases in tests.items():
        if "Shear" not in phases:
            continue

        df = phases["Shear"]
        colmap = {col.lower(): col for col in df.columns}
        try:
            p_col = next(colmap[k] for k in colmap if "mean" in k and "p" in k)
            q_col = next(colmap[k] for k in colmap if "deviator" in k or "q" in k)
        except StopIteration:
            print(f"Skipping {test_id}: missing p' or q column")
            continue

        # Compute q / p' safely
        df["q_over_p"] = (df[q_col] / df[p_col]).replace([float("inf"), -float("inf")], pd.NA)

        # Then: plot q/p' vs axial strain for this material
        try:
            strain_col = next(colmap[k] for k in colmap if "axial" in k and "strain" in k)
        except StopIteration:
            print(f"Skipping {test_id}: missing axial strain column")
            continue

        if "q_over_p" not in df.columns:
            continue

        plt.plot(df[strain_col], df["q_over_p"], label=test_id)

    # outside loop
    plt.xlabel("Axial strain [%]")
    plt.ylabel("Stress ratio q / p'")
    plt.title(f"Stress ratio vs Axial strain – {material}")
    plt.grid(True)
    plt.xlim(left=0)
    plt.ylim(bottom=0, top=1.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

    import pickle

    SAVE_DIR = Path("C:/Users/Python/Projects/calipyr/_figures_pickled")
    SAVE_DIR.mkdir(parents=True, exist_ok=True)


import matplotlib.pyplot as plt
import pickle
from pathlib import Path

# Directory to store figure pickles
SAVE_DIR = Path(r"C:\Users\Python\Projects\calipyr\_figures_pickled")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

stored_figures = {}

# Loop over each material and plot + store its figure
for material, tests in imported_data.items():
    fig, ax = plt.subplots()

    for test_id, phases in tests.items():
        if "Shear" not in phases:
            continue

        df = phases["Shear"]
        colmap = {col.lower(): col for col in df.columns}
        try:
            p_col = next(colmap[k] for k in colmap if "mean" in k and "p" in k)
            q_col = next(colmap[k] for k in colmap if "deviator" in k or "q" in k)
        except StopIteration:
            continue

        ax.plot(df[p_col], df[q_col], label=test_id)

    ax.set_title(f"Stress paths – {material}")
    ax.set_xlabel("Mean effective stress, p' [kPa]")
    ax.set_ylabel("Deviator stress, q [kPa]")
    ax.grid(True)
    ax.legend()
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    fig.tight_layout()

    # Save to memory
    stored_figures[f"{material}_stress_path"] = fig

    # Save to file
    with open(SAVE_DIR / f"{material}_stress_path.pkl", "wb") as f:
        pickle.dump(fig, f)

    plt.close(fig)

# import matplotlib.pyplot as plt
# from pathlib import Path
# # Directory containing saved figure .pkl files
# SAVE_DIR = Path(r"C:\Users\Python\Projects\calipyr\_figures_pickled")
# # Loop through all .pkl files in the folder
# for fig_path in SAVE_DIR.glob("*.pkl"):
#     print(f"Loading: {fig_path.name}")
#     with open(fig_path, "rb") as f:
#         fig = pickle.load(f)
#     # Attach the figure to pyplot and refresh its canvas
#     plt.figure(fig.number)
#     fig.canvas.draw()
#     plt.show()
