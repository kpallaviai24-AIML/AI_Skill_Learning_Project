from pathlib import Path
import pandas as pd
import re

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = PROJECT_ROOT / "outputs" / "extracted"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "standardised"


def normalise_name(name):
    """Create a consistent matching key without changing the original name."""
    if pd.isna(name):
        return ""
    name = str(name).casefold().strip()
    name = re.sub(r"\s+", " ", name)
    return name


def standardise_esco(df):
    result = pd.DataFrame({
        "source": "ESCO",
        "source_skill_id": df["source_skill_id"],
        "skill_name": df["skill_name"],
        "aliases": df["aliases"],
        "skill_type": df["skill_type"],
        "category": df["reuse_level"],
        "description": df["description"],
    })
    return result


def standardise_onet(df):
    # O*NET has separate Importance and Level rows.
    # Keep one catalogue entry per skill and category, not one per scale row.
    unique = df.drop_duplicates(
        subset=["Element ID", "Element Name", "skill_category"]
    )

    result = pd.DataFrame({
        "source": "O*NET",
        "source_skill_id": unique["Element ID"],
        "skill_name": unique["Element Name"],
        "aliases": "",
        "skill_type": "",
        "category": unique["skill_category"],
        "description": "",
    })
    return result


def main():
    esco = pd.read_csv(INPUT_DIR / "esco_extracted_skills.csv")
    onet = pd.read_csv(INPUT_DIR / "onet_extracted_skills.csv")

    esco_standard = standardise_esco(esco)
    onet_standard = standardise_onet(onet)

    combined = pd.concat(
        [esco_standard, onet_standard],
        ignore_index=True
    )

    combined["normalised_name"] = combined["skill_name"].apply(
        normalise_name
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "standardised_skills.csv"
    combined.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("ESCO catalogue entries:", len(esco_standard))
    print("O*NET catalogue entries:", len(onet_standard))
    print("Combined catalogue entries:", len(combined))
    print("Saved to:", output_path)


if __name__ == "__main__":
    main()