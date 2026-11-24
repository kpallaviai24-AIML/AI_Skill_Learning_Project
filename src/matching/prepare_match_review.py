
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT / "outputs" / "standardised" / "skill_match_candidates.csv"
OUTPUT_FILE = ROOT / "outputs" / "standardised" / "skill_match_review.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    df["decision"] = "needs_review"
    df["review_notes"] = ""

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("Candidates prepared for review:", len(df))
    print("Review file:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
