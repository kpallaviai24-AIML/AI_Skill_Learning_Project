
from pathlib import Path

import networkx as nx
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

VALID_STATUSES = {
    "approved",
    "needs_review",
    "rejected",
}


def validate_file(file_path):
    """Validate prerequisite relationship data."""

    df = pd.read_csv(file_path)

    print("Total relationships:", len(df))

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df.empty:
        print("No prerequisite relationships added yet.")
        return {
            "total_relationships": 0,
            "incomplete_rows": 0,
            "duplicate_relationships": 0,
            "self_loops": 0,
            "invalid_review_statuses": 0,
            "has_cycles": False,
            "valid": True,
        }

    # Normalise required text fields for reliable validation.
    for column in REQUIRED_COLUMNS:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    incomplete = df[REQUIRED_COLUMNS].isna().any(axis=1)

    complete_edges = df.dropna(
        subset=["prerequisite_skill", "dependent_skill"]
    ).copy()

    # Compare skill names without case sensitivity.
    complete_edges["_source_key"] = (
        complete_edges["prerequisite_skill"].str.casefold()
    )
    complete_edges["_target_key"] = (
        complete_edges["dependent_skill"].str.casefold()
    )

    duplicate_edges = complete_edges.duplicated(
        subset=["_source_key", "_target_key"],
        keep=False,
    )

    self_loops = (
        complete_edges["_source_key"]
        == complete_edges["_target_key"]
    )

    invalid_status = ~df["review_status"].str.lower().isin(
        VALID_STATUSES
    )

    # Check cycles using approved, complete relationships only.
    approved = df[
        (df["review_status"].str.lower() == "approved")
        & df["prerequisite_skill"].notna()
        & df["dependent_skill"].notna()
    ]

    graph = nx.DiGraph()

    for _, row in approved.iterrows():
        graph.add_edge(
            row["prerequisite_skill"].casefold(),
            row["dependent_skill"].casefold(),
        )

    has_cycles = not nx.is_directed_acyclic_graph(graph)

    report = {
        "total_relationships": len(df),
        "incomplete_rows": int(incomplete.sum()),
        "duplicate_relationships": int(duplicate_edges.sum()),
        "self_loops": int(self_loops.sum()),
        "invalid_review_statuses": int(invalid_status.sum()),
        "has_cycles": has_cycles,
    }

    report["valid"] = (
        report["incomplete_rows"] == 0
        and report["duplicate_relationships"] == 0
        and report["self_loops"] == 0
        and report["invalid_review_statuses"] == 0
        and not has_cycles
    )

    print("Incomplete rows:", report["incomplete_rows"])
    print(
        "Duplicate relationships:",
        report["duplicate_relationships"],
    )
    print("Self-loops:", report["self_loops"])
    print(
        "Invalid review statuses:",
        report["invalid_review_statuses"],
    )
    print("Has cycles:", report["has_cycles"])

    return report


def main():
    report = validate_file(FILE)

    if not report["valid"]:
        print("\nPrerequisite validation FAILED.")
        raise ValueError(
            "Invalid prerequisite relationships detected. "
            "Please correct the data before building the graph."
        )

    print("\nPrerequisite validation completed successfully.")
    return report


if __name__ == "__main__":
    main()
