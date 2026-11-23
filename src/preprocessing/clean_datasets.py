
from pathlib import Path
import pandas as pd

from src.data.load_datasets import load_all_datasets


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "datasets" / "processed"


def clean_dataframe(df):
    """Clean whitespace while preserving original records and missing values."""

    cleaned = df.copy()

    for column in cleaned.columns:
        if pd.api.types.is_string_dtype(cleaned[column].dtype):
            cleaned[column] = cleaned[column].map(
                lambda value: value.strip()
                if isinstance(value, str)
                else value
            )

            cleaned[column] = cleaned[column].replace("", pd.NA)

    return cleaned


def clean_all_datasets():
    """Clean and save all ESCO and O*NET datasets."""

    datasets = load_all_datasets()

    for group, tables in datasets.items():
        output_folder = OUTPUT_DIR / group
        output_folder.mkdir(parents=True, exist_ok=True)

        for name, df in tables.items():
            cleaned_df = clean_dataframe(df)

            output_path = output_folder / f"{name}.csv"

            cleaned_df.to_csv(
                output_path,
                index=False,
                encoding="utf-8-sig"
            )

            print(
                f"{group}/{name}: "
                f"{len(df)} original rows -> "
                f"{len(cleaned_df)} cleaned rows"
            )

    print("\nDATASET CLEANING COMPLETED")


if __name__ == "__main__":
    clean_all_datasets()
