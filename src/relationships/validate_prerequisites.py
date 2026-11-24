
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

FILE = (
    ROOT / "outputs" / "relationships"
    / "prerequisite_relationships.csv"
)

REQUIRED_COLUMNS = [
    "prerequisite_skill",
    "dependent_skill",
    "evidence_source",
    "evidence_description",
    "confidence",
    "review_status",
]


def main():
    df = pd.read_csv(FILE)

    print("Total relationships:", len(df))

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        print("Missing columns:", missing_columns)
        return

    if df.empty:
        print("No prerequisite relationships added yet.")
        print("This is expected at this stage.")
        return

    required_fields = [
        "prerequisite_skill",
        "dependent_skill",
        "evidence_source",
        "evidence_description",
        "confidence",
        "review_status",
    ]

    incomplete = df[required_fields].isna().any(axis=1)

    print("Incomplete rows:", int(incomplete.sum()))

    duplicate_edges = df.duplicated(
        subset=["prerequisite_skill", "dependent_skill"]
    )

    print("Duplicate relationships:", int(duplicate_edges.sum()))

    self_loops = (
        df["prerequisite_skill"].astype(str).str.strip()
        == df["dependent_skill"].astype(str).str.strip()
    )

    print("Self-loops:", int(self_loops.sum()))

    valid_statuses = ["approved", "needs_review", "rejected"]

    invalid_status = ~df["review_status"].astype(str).str.lower().isin(
        valid_statuses
    )

    print("Invalid review statuses:", int(invalid_status.sum()))

    print("\nValidation completed.")


if __name__ == "__main__":
    main()

