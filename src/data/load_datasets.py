
from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ESCO_DIR = PROJECT_ROOT / "datasets" / "raw" / "esco"
ONET_DIR = PROJECT_ROOT / "datasets" / "raw" / "onet"


def find_file(folder, filename):
    """Find a dataset file, including inside extracted subfolders."""
    matches = [
        path for path in folder.rglob("*")
        if path.is_file() and path.name.lower() == filename.lower()
    ]

    if not matches:
        raise FileNotFoundError(
            f"{filename} not found inside {folder}"
        )

    if len(matches) > 1:
        raise ValueError(
            f"Multiple copies of {filename} found: {matches}"
        )

    return matches[0]


def load_esco_data():
    """Load the main ESCO CSV datasets."""
    return {
        "skills": pd.read_csv(
            find_file(ESCO_DIR, "skills_en.csv"),
            low_memory=False
        ),
        "occupations": pd.read_csv(
            find_file(ESCO_DIR, "occupations_en.csv"),
            low_memory=False
        ),
        "occupation_skill_relations": pd.read_csv(
            find_file(ESCO_DIR, "occupationSkillRelations_en.csv"),
            low_memory=False
        ),
        "skill_skill_relations": pd.read_csv(
            find_file(ESCO_DIR, "skillSkillRelations_en.csv"),
            low_memory=False
        ),
    }


def load_onet_data():
    """Load the main O*NET Excel datasets."""
    return {
        "occupations": pd.read_excel(
            find_file(ONET_DIR, "Occupation Data.xlsx")
        ),
        "essential_skills": pd.read_excel(
            find_file(ONET_DIR, "Essential Skills.xlsx")
        ),
        "transferable_skills": pd.read_excel(
            find_file(ONET_DIR, "Transferable Skills.xlsx")
        ),
    }


def load_all_datasets():
    """Load both ESCO and O*NET datasets."""
    return {
        "esco": load_esco_data(),
        "onet": load_onet_data(),
    }
