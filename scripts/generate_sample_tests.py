import pandas as pd
from pathlib import Path


def create_sample_excel(test_id: str, test_type: str, out_dir: Path):
    # Consolidation phase
    df_consol = pd.DataFrame({
        "Axial Displacement (mm)": [0.0, 0.5, 1.0],
        "Vol Offset (cm³)": [0.0, 0.2, 0.4],
        "Time (s)": [0, 60, 120]
    })

    # Shear metadata (4 lines to skip)
    metadata = ["Test data", "Sample details", "Lab: CaliPyr", "Generated for testing"]

    # Shear phase – vary columns depending on type
    if test_type == "CIU":
        df_shear = pd.DataFrame({
            "σ3' (kPa)": [100, 100, 100],
            "σ1' (kPa)": [150, 180, 200],
            "Deviator Stress q (kPa)": [50, 80, 100],
            "Mean Effective stress p (kPa)": [116.7, 120, 133.3],
            "Induced PWP": [10, 15, 20],
            "Axial strain ɛa %": [0.1, 0.5, 1.0],
            "e": [0.8, 0.79, 0.78],
            "φ'": [30, 31, 32]
        })
    else:  # CID or DMIN CID
        df_shear = pd.DataFrame({
            "Mean Effective Stress p (kPa)": [100, 110, 120],
            "Deviator Stress q (kPa)": [0, 30, 60],
            "Axial Strain ɛa %": [0.0, 0.5, 1.0],
            "Vol Strain %": [0.0, 0.2, 0.4],
            "e": [0.7, 0.69, 0.68],
            "φ'": [32, 33, 34]
        })

    # Save to Excel
    outfile = out_dir / f"{test_id}.xlsx"
    with pd.ExcelWriter(outfile, engine="openpyxl") as writer:
        df_consol.to_excel(writer, sheet_name=f"{test_id}-Consolidation", index=False)
        # Add metadata + header + data manually
        sheet = writer.book.create_sheet(title=f"{test_id}-Shear")
        for i, line in enumerate(metadata, start=1):
            sheet.cell(row=i, column=1).value = line
        for j, col in enumerate(df_shear.columns, start=1):
            sheet.cell(row=5, column=j).value = col
        for i, row in enumerate(df_shear.values, start=6):
            for j, value in enumerate(row, start=1):
                sheet.cell(row=i, column=j).value = value

    print(f"Created: {outfile.name}")


def main():
    #out_dir = Path("data")
    out_dir = Path(__file__).resolve().parent.parent / "data"
    out_dir.mkdir(exist_ok=True)

    create_sample_excel("TX1-CIU-150kPa", "CIU", out_dir)
    create_sample_excel("TX2-CID-150kPa", "CID", out_dir)
    create_sample_excel("TX3-DMIN-CID-150kPa", "DMIN CID", out_dir)


if __name__ == "__main__":
    main()
