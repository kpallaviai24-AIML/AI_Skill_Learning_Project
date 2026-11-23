from pathlib import Path
from difflib import SequenceMatcher
import pandas as pd
import re

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT / "outputs" / "standardised"
    / "standardised_skills.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "standardised"


def normalise(text):
    if pd.isna(text):
        return ""
    text = str(text).casefold().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def get_esco_labels(row):
    """Return the ESCO preferred name and its alternative labels."""
    labels = [normalise(row["skill_name"])]

    aliases = row["aliases"]
    if pd.notna(aliases):
        labels.extend(
            normalise(alias)
            for alias in str(aliases).splitlines()
        )

    return {label for label in labels if label}


def main():
    df = pd.read_csv(INPUT_FILE)

    esco = df[df["source"] == "ESCO"].copy()
    onet = df[df["source"] == "O*NET"].copy()

    esco["match_labels"] = esco.apply(get_esco_labels, axis=1)
    onet["normalised_name"] = onet["skill_name"].apply(normalise)

    candidates = []

    for _, onet_row in onet.iterrows():
        onet_name = onet_row["normalised_name"]

        if not onet_name:
            continue

        for _, esco_row in esco.iterrows():
            labels = esco_row["match_labels"]

            if not labels:
                continue

            best_score = max(
                SequenceMatcher(None, onet_name, label).ratio()
                for label in labels
            )

            if best_score >= 0.85:
                candidates.append({
                    "onet_skill_id": onet_row["source_skill_id"],
                    "onet_skill_name": onet_row["skill_name"],
                    "esco_skill_id": esco_row["source_skill_id"],
                    "esco_skill_name": esco_row["skill_name"],
                    "similarity_score": round(best_score, 4),
                    "review_status": "needs_manual_review"
                })

    result = pd.DataFrame(candidates)

    if not result.empty:
        result = result.sort_values(
            by=["similarity_score", "onet_skill_name"],
            ascending=[False, True]
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "skill_match_candidates.csv"
    result.to_csv(output_file, index=False, encoding="utf-8-sig")

    print("O*NET skills checked:", len(onet))
    print("ESCO skills checked:", len(esco))
    print("Potential matches found:", len(result))
    print("Saved to:", output_file)


if __name__ == "__main__":
    main()