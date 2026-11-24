from pathlib import Path
import networkx as nx
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "outputs" / "relationships" / "problem_solving_review.csv"

REQUIRED = [
    "prerequisite_skill",
    "dependent_skill",
    "evidence_source",
    "evidence_description",
    "confidence",
    "review_status",
    "review_notes",
]

def main():
    if not INPUT.exists():
        raise FileNotFoundError(INPUT)

    df = pd.read_csv(INPUT)

    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    incomplete = df[REQUIRED[:6]].isna().any(axis=1).sum()
    duplicates = df.duplicated(
        ["prerequisite_skill", "dependent_skill"]
    ).sum()

    self_loops = (
        df["prerequisite_skill"].astype(str).str.strip()
        == df["dependent_skill"].astype(str).str.strip()
    ).sum()

    invalid = (~df["review_status"].isin(
        ["needs_review", "approved", "rejected"]
    )).sum()

    graph = nx.DiGraph()
    for _, row in df.iterrows():
        graph.add_edge(
            str(row["prerequisite_skill"]).strip(),
            str(row["dependent_skill"]).strip()
        )

    cycles = not nx.is_directed_acyclic_graph(graph)

    print("PROBLEM-SOLVING REVIEW VALIDATION")
    print("Total proposals:", len(df))
    print("Incomplete rows:", incomplete)
    print("Duplicate relationships:", duplicates)
    print("Self-loops:", self_loops)
    print("Invalid review statuses:", invalid)
    print("Has cycles:", cycles)
    print("\nReview status counts:")
    print(df["review_status"].value_counts().to_string())

    if incomplete or duplicates or self_loops or invalid or cycles:
        raise SystemExit("Validation failed.")

    print("\nValidation completed successfully.")

if __name__ == "__main__":
    main()
