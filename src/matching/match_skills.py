
from pathlib import Path
from difflib import SequenceMatcher
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT / "outputs" / "standardised"
    / "standardised_skills.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "standardised"

MATCH_THRESHOLD = 0.85


def normalise(text):
    """Normalise text for skill-name comparison."""
    if pd.isna(text):
        return ""

    text = str(text).casefold()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def get_esco_labels(row):
    """Return preferred ESCO label and alternative labels."""
    labels = []

    preferred = normalise(row["skill_name"])

    if preferred:
        labels.append((preferred, "preferred_label"))

    aliases = row.get("aliases", "")

    if pd.notna(aliases):
        for alias in str(aliases).splitlines():
            alias = normalise(alias)

            if alias:
                labels.append((alias, "alias"))

    # Remove duplicate labels while preserving their order.
    return list(dict.fromkeys(labels))


def calculate_similarity(first, second):
    """Combine character similarity and token Jaccard similarity."""
    if not first or not second:
        return 0.0

    if first == second:
        return 1.0

    character_score = SequenceMatcher(
        None, first, second
    ).ratio()

    first_tokens = set(first.split())
    second_tokens = set(second.split())

    union = first_tokens | second_tokens

    token_score = (
        len(first_tokens & second_tokens) / len(union)
        if union else 0.0
    )

    return (0.65 * character_score) + (0.35 * token_score)


def find_best_match(onet_name, esco_labels):
    """Find the best matching ESCO label for one O*NET skill."""
    best_score = 0.0
    best_label = ""
    best_type = ""

    for label, label_type in esco_labels:
        score = calculate_similarity(onet_name, label)

        if score > best_score:
            best_score = score
            best_label = label
            best_type = label_type

        if score == 1.0 and label_type == "preferred_label":
            break

    if best_score == 1.0:
        match_type = f"exact_{best_type}"
    else:
        match_type = f"fuzzy_{best_type}" if best_type else ""

    return best_score, best_label, match_type


def generate_candidates(df, threshold=MATCH_THRESHOLD):
    """Generate unique O*NET-to-ESCO candidate pairs."""
    esco = df[df["source"] == "ESCO"].copy()
    onet = df[df["source"] == "O*NET"].copy()

    esco_records = []

    for _, row in esco.iterrows():
        labels = get_esco_labels(row)

        if labels:
            esco_records.append((row, labels))

    candidates = {}

    for _, onet_row in onet.iterrows():
        onet_name = normalise(onet_row["skill_name"])

        if not onet_name:
            continue

        for esco_row, labels in esco_records:
            score, matched_label, match_type = find_best_match(
                onet_name, labels
            )

            if score < threshold:
                continue

            onet_id = str(onet_row["source_skill_id"])
            esco_id = str(esco_row["source_skill_id"])

            key = (onet_id, esco_id)

            candidate = {
                "onet_skill_id": onet_row["source_skill_id"],
                "onet_skill_name": onet_row["skill_name"],
                "esco_skill_id": esco_row["source_skill_id"],
                "esco_skill_name": esco_row["skill_name"],
                "matched_label": matched_label,
                "similarity_score": round(score, 4),
                "match_type": match_type,
                "review_status": "needs_manual_review",
            }

            # Keep only the strongest candidate for each ID pair.
            if (
                key not in candidates
                or score > candidates[key]["similarity_score"]
            ):
                candidates[key] = candidate

    result = pd.DataFrame(list(candidates.values()))

    if not result.empty:
        result = result.sort_values(
            by=["similarity_score", "onet_skill_name"],
            ascending=[False, True],
        ).reset_index(drop=True)

    return result


def main():
    df = pd.read_csv(INPUT_FILE)

    required_columns = {
        "source",
        "source_skill_id",
        "skill_name",
        "aliases",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    result = generate_candidates(df)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "skill_match_candidates.csv"

    result.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig",
    )

    print("O*NET skills checked:", (df["source"] == "O*NET").sum())
    print("ESCO skills checked:", (df["source"] == "ESCO").sum())
    print("Potential matches found:", len(result))
    print("All candidates require manual review.")
    print("Saved to:", output_file)


if __name__ == "__main__":
    main()
