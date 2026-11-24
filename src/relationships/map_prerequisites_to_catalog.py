
from pathlib import Path
from difflib import SequenceMatcher
import pandas as pd
import re

ROOT = Path(__file__).resolve().parents[2]

RELATIONSHIP_FILE = (
    ROOT / "outputs" / "relationships"
    / "prerequisite_relationships.csv"
)

CATALOG_FILE = (
    ROOT / "outputs" / "standardised"
    / "standardised_skills.csv"
)

OUTPUT_FILE = (
    ROOT / "outputs" / "standardised"
    / "prerequisite_skill_mapping_review.csv"
)


def normalise(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def main():
    relationships = pd.read_csv(RELATIONSHIP_FILE)
    catalog = pd.read_csv(CATALOG_FILE)

    required = [
        "skill_name",
        "source",
        "source_skill_id",
        "normalised_name",
    ]

    for column in required:
        if column not in catalog.columns:
            raise ValueError(f"Missing catalogue column: {column}")

    concepts = pd.unique(
        pd.concat([
            relationships["prerequisite_skill"],
            relationships["dependent_skill"],
        ]).dropna()
    )

    results = []

    for concept in concepts:
        target = normalise(concept)

        catalog_copy = catalog.copy()
        catalog_copy["score"] = catalog_copy[
            "normalised_name"
        ].fillna("").apply(
            lambda name: SequenceMatcher(
                None, target, str(name)
            ).ratio()
        )

        top_matches = catalog_copy.nlargest(5, "score")

        for _, row in top_matches.iterrows():
            results.append({
                "research_skill": concept,
                "catalog_skill_name": row["skill_name"],
                "catalog_source": row["source"],
                "catalog_skill_id": row["source_skill_id"],
                "similarity_score": round(row["score"], 4),
                "mapping_decision": "needs_review",
                "review_notes": "",
            })

    result_df = pd.DataFrame(results)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    result_df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("Mapping candidates generated:", len(result_df))
    print("Research competencies:", len(concepts))
    print("Output:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
