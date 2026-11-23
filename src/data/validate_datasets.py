
import json
from pathlib import Path

from src.data.load_datasets import load_all_datasets


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = PROJECT_ROOT / "outputs" / "evaluation" / "data_quality_report.json"


def validate_dataframe(df):
    """Generate basic data quality information for a dataset."""

    missing_values = df.isnull().sum()
    missing_values = {
        str(column): int(count)
        for column, count in missing_values.items()
        if count > 0
    }

    return {
        "rows": int(df.shape[0]),
        "columns_count": int(df.shape[1]),
        "column_names": [str(col) for col in df.columns],
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": missing_values,
        "completely_empty_columns": [
            str(col) for col in df.columns if df[col].isnull().all()
        ],
    }


def validate_all_datasets():
    """Validate all loaded ESCO and O*NET tables."""

    datasets = load_all_datasets()
    report = {}

    for group, tables in datasets.items():
        report[group] = {}

        for name, df in tables.items():
            report[group][name] = validate_dataframe(df)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print("DATASET VALIDATION COMPLETED")
    print("=" * 45)

    for group, tables in report.items():
        for name, details in tables.items():
            print(f"\n{group}/{name}")
            print(f"Rows: {details['rows']}")
            print(f"Columns: {details['columns_count']}")
            print(f"Duplicate rows: {details['duplicate_rows']}")
            print(f"Columns with missing values: {len(details['missing_values'])}")

    print(f"\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    validate_all_datasets()
