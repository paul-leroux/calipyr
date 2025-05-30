from pathlib import Path
import pandas as pd
from calipyr.processing import load_triaxial_test


def main():
    # Get absolute path to the root directory
    root_dir = Path(__file__).resolve().parent.parent
    data_dir = root_dir / "data"

    xlsx_files = list(data_dir.glob("*.xlsx"))
    print("Files found in data/:", [f.name for f in xlsx_files])

    if not xlsx_files:
        print("No Excel files found in 'data/'")
        return

    test_file = xlsx_files[0]
    print(f"Loading test: {test_file.name}")
    df = load_triaxial_test(test_file)

    print("\nTest Info:")
    print("Test ID:", df['test_id'].iloc[0])
    print("Test Type:", df['test_type'].iloc[0])
    print("Phases:", df['phase'].unique())

    print("\nPreview of standardised data:")
    print(df.head())

    # Save to outputs/
    output_path = root_dir / "outputs" / f"{test_file.stem}_standardised.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
