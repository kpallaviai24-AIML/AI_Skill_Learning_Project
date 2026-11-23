from pathlib import Path
import pandas as pd

from src.data.load_datasets import load_all_datasets

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "extracted"


def extract_esco_skills(esco_data):
    skills = esco_data["skills"].copy()

    extracted = skills[
        ["conceptUri", "preferredLabel", "altLabels",
         "skillType", "reuseLevel", "description"]
    ].copy()

    extracted["source"] = "ESCO"
    extracted = extracted.rename(columns={
        "conceptUri": "source_skill_id",
        "preferredLabel": "skill_name",
        "altLabels": "aliases",
        "skillType": "skill_type",
        "reuseLevel": "reuse_level"
    })

    return extracted


def extract_onet_skills(onet_data):
    frames = []

    for dataset_name in ["essential_skills", "transferable_skills"]:
        df = onet_data[dataset_name].copy()

        extracted = df[
            ["Element ID", "Element Name", "Scale ID",
             "Scale Name", "Data Value", "O*NET-SOC Code"]
        ].copy()

        extracted["source"] = "O*NET"
        extracted["skill_category"] = dataset_name

        frames.append(extracted)

    return pd.concat(frames, ignore_index=True)


def main():
    datasets = load_all_datasets()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    esco_skills = extract_esco_skills(datasets["esco"])
    onet_skills = extract_onet_skills(datasets["onet"])

    esco_skills.to_csv(
        OUTPUT_DIR / "esco_extracted_skills.csv",
        index=False,
        encoding="utf-8-sig"
    )

    onet_skills.to_csv(
        OUTPUT_DIR / "onet_extracted_skills.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("ESCO extracted records:", len(esco_skills))
    print("O*NET extracted records:", len(onet_skills))
    print("Skill extraction completed successfully.")


if __name__ == "__main__":
    main()