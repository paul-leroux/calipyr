#C:\Users\Python\Projects\calipyr\scripts\import_TX_data.py
#''' Make a general script(s)/function(s) to import CIU, CID and Dmin CID triaxial data from Excel files with multiple
#sheets.'''
# import prerequisites
# look in directory C:\Users\Python\Projects\calipyr\data and its subdirectories for Excel files (.xlsx)
# there should be subdirectories for different materials tested. in this case it will be "Leslie TSF Fine Overflow Mix"
# and "Leslie TSF Underflow Mix". As an example the Leslie TSF Fine Overflow Mix material will have a file named
# TRXD-CSL-V25-04-125-CRD (REV 4).xlsx containing the following sheets:
# Directory
# Sample Data
# TX1-CIU-150kPa-Consolidation
# TX1-CIU-150kPa-Shear
# TX3-CIU-300kPa-Consolidation
# TX3-CIU-300kPa-Shear
# TX4-CID-300kPa-Consolidation
# TX4-CID-300kPa-Shear
# TX5-CID-600kPa-Consolidation
# TX5-CID-600kPa-Shear
# TX6-CIU-600kPa-Consolidation
# TX6-CIU-600kPa-Shear
# TX6-DMIN-CID-50kPa-Consolidation
# TX6-DMIN-CID-50kPa-Shear
# TX7-DMIN-CID-75kPa-Consolidation
# TX7-DMIN-CID-75kPa-Shear
# TX8-CIU-300kPa-Consolidation
# TX8-CIU-300kPa-Shear
#
# The Underflow file is called "TRXD-Elikhulu TSF-V25-03-104.xlsx" in this case and has less tests but generally the
# same structure
# the sheets will generally follow that pattern but there may be mistakes due to human input error. The Direcotry and
# Sample Data sheets can be ignored for now.
# The consolidation and shear phases for each separate test should be read into dataframes to be accessed later.
# C:\Users\Python\Projects\calipyr\scripts\import_TX_data.py

"""
Import CIU, CID and DMIN CID triaxial data from Excel files with multiple sheets.

This script searches recursively in the data directory for Excel files (.xlsx),
ignores metadata sheets, and loads valid triaxial test phases (Consolidation and Shear)
into structured dictionaries for further processing.

Author: Paul le Roux
Date: 2025-06-04
"""

import os
import re
import pandas as pd
from pathlib import Path

# Constants
DATA_ROOT = Path(r"C:\Users\Python\Projects\calipyr\data")
VALID_PHASES = ["Consolidation", "Shear"]
IGNORE_SHEETS = {"Directory", "Sample Data"}
VALID_EXT = ".xlsx"

# Regex pattern for identifying test sheets, e.g. "TX1-CIU-150kPa-Consolidation"
# Updated regex pattern: allows "Consol" or "Consolidation" or spacing issues
SHEET_PATTERN = re.compile(
    r"^(TX\d+)-(CIU|CID|DMIN-CID)-(\d+)kPa[-\s]+(Consol(idation)?|Shear)\s*$",
    re.IGNORECASE
)

def find_excel_files(root: Path) -> list[Path]:
    """Recursively find all .xlsx files under the given root directory."""
    return [p for p in root.rglob(f"*{VALID_EXT}") if p.is_file()]

def load_test_sheets(filepath: Path) -> dict:
    """
    Load valid test sheets from an Excel file.
    Returns a nested dictionary:
    {
        'TX1-CIU-150kPa': {
            'Consolidation': pd.DataFrame,
            'Shear': pd.DataFrame
        },
        ...
    }
    """
    xls = pd.ExcelFile(filepath)
    test_data = {}

    for sheet in xls.sheet_names:
        if sheet in IGNORE_SHEETS:
            continue

        match = SHEET_PATTERN.match(sheet)
        if not match:
            print(f"Skipping unrecognised sheet: {sheet} in file: {filepath.name}")
            continue

        test_id = f"{match.group(1)}-{match.group(2)}-{match.group(3)}kPa"
        raw_phase = match.group(4).strip().lower()

        if raw_phase.startswith("consol"):
            phase = "Consolidation"
        elif raw_phase == "shear":
            phase = "Shear"
        else:
            print(f"Unrecognised phase label: {raw_phase} in sheet: {sheet}")
            continue

        try:
            raw_preview = xls.parse(sheet, nrows=10, header=None)

            header_row_idx = None
            for idx, row in raw_preview.iterrows():
                joined = ",".join(str(x) for x in row if pd.notna(x)).lower()
                if any(kw in joined for kw in ["axial", "stress", "strain", "time", "mean effective", "deviator"]):
                    header_row_idx = idx
                    break

            if header_row_idx is None:
                print(f"  Could not detect header row in sheet {sheet} (file: {filepath.name})")
                continue

            # Load using detected header
            df = xls.parse(sheet, header=header_row_idx)

            df.dropna(how='all', inplace=True)  # drop completely empty rows
            if test_id not in test_data:
                test_data[test_id] = {}
            test_data[test_id][phase] = df
        except Exception as e:
            print(f"Error reading sheet {sheet} in {filepath.name}: {e}")

    return test_data

def import_all_tests(data_root: Path) -> dict:
    """
    Scan all Excel files and load valid triaxial test data.
    Returns a nested dictionary:
    {
        'Material Name': {
            'TX1-CIU-150kPa': {
                'Consolidation': pd.DataFrame,
                'Shear': pd.DataFrame
            },
            ...
        },
        ...
    }
    """
    results = {}

    for file in find_excel_files(data_root):
        material_name = file.parent.name
        print(f"Processing file: {file.name} (Material: {material_name})")

        test_sheets = load_test_sheets(file)

        if material_name not in results:
            results[material_name] = {}

        results[material_name].update(test_sheets)

    return results

if __name__ == "__main__":
    imported_data = import_all_tests(DATA_ROOT)

    # Example: print out loaded test IDs per material
    for material, tests in imported_data.items():
        print(f"\nMaterial: {material}")
        for test_id in tests:
            print(f"  Loaded test: {test_id} with phases: {list(tests[test_id].keys())}")

print("\n=== Test Import Summary ===")
for material, tests in imported_data.items():
    print(f"\nMaterial: {material}")
    for test_id, phases in tests.items():
        phase_summary = []
        for phase in ["Consolidation", "Shear"]:
            if phase in phases:
                df = phases[phase]
                nrows, ncols = df.shape
                phase_summary.append(f"{phase} ({nrows} rows, {ncols} cols)")
            else:
                phase_summary.append(f"{phase} [MISSING]")
        print(f"  {test_id:<30} -->  {', '.join(phase_summary)}")

# # Optional: limit to 1 test per material to avoid too many plots
# for material, tests in imported_data.items():
#     for test_id, phases in tests.items():
#         print(f"\nPlotting test: {test_id} ({material})")
#         for phase, df in phases.items():
#             plt.figure()
#             df_numeric = df.select_dtypes(include="number")  # Only plot numeric columns
#             if not df_numeric.empty:
#                 df_numeric.plot(title=f"{test_id} - {phase}")
#                 plt.xlabel("Row index")
#                 plt.ylabel("Values")
#                 plt.grid(True)
#                 plt.tight_layout()
#             else:
#                 print(f"  Skipping {phase}: no numeric data")
#         break  # comment this line if you want to plot all tests per material
#
# plt.show()

EXPORT_DIR = Path("C:/Users/Python/Projects/calipyr/_import_preview")
EXPORT_DIR.mkdir(exist_ok=True)

for material, tests in imported_data.items():
    for test_id, phases in tests.items():
        for phase, df in phases.items():
            outname = f"{test_id}_{phase}.csv"
            outfile = EXPORT_DIR / outname
            df.to_csv(outfile, index=False)

import pickle

EXPORT_PATH = Path("C:/Users/Python/Projects/calipyr/_cache/imported_triaxials.pkl")
EXPORT_PATH.parent.mkdir(exist_ok=True)  # create _cache dir if needed

with open(EXPORT_PATH, "wb") as f:
    pickle.dump(imported_data, f)

print(f"\nData cached to: {EXPORT_PATH}")