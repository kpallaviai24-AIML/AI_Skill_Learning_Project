
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

FILE = (
    ROOT / "outputs" / "relationships"
    / "prerequisite_relationships.csv"
)

COLUMNS = [
    "prerequisite_skill",
    "dependent_skill",
    "evidence_source",
    "evidence_description",
    "confidence",
    "review_status",
]


def main():
    FILE.parent.mkdir(parents=True, exist_ok=True)

    if FILE.exists():
        df = pd.read_csv(FILE)
    else:
        df = pd.DataFrame(columns=COLUMNS)

    for column in COLUMNS:
        if column not in df.columns:
            df[column] = ""

    df = df[COLUMNS]
    df.to_csv(FILE, index=False, encoding="utf-8-sig")

    print("Prerequisite evidence file is ready.")
    print("Columns:", df.columns.tolist())
    print("Existing relationships:", len(df))
    print("File:", FILE)


if __name__ == "__main__":
    main()
