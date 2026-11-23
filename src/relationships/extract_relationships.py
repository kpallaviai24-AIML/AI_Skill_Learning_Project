from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "datasets" / "processed" / "esco"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "relationships"


def main():
    skills = pd.read_csv(DATA_DIR / "skills.csv")
    relations = pd.read_csv(DATA_DIR / "skill_skill_relations.csv")

    # Build a lookup from each ESCO skill URI to its preferred name.
    skill_lookup = (
        skills[["conceptUri", "preferredLabel"]]
        .drop_duplicates(subset=["conceptUri"])
        .set_index("conceptUri")["preferredLabel"]
    )

    result = relations.copy()

    result["original_skill_name"] = result["originalSkillUri"].map(
        skill_lookup
    )
    result["related_skill_name"] = result["relatedSkillUri"].map(
        skill_lookup
    )

    result["source"] = "ESCO"
    result["relationship_kind"] = "related_skill"
    result["is_learning_prerequisite"] = False

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "esco_skill_relationships.csv"
    result.to_csv(output_file, index=False, encoding="utf-8-sig")

    print("ESCO relationships extracted:", len(result))
    print(
        "Relationships with both skill names:",
        result[
            result["original_skill_name"].notna()
            & result["related_skill_name"].notna()
        ].shape[0]
    )
    print("Saved to:", output_file)


if __name__ == "__main__":
    main()