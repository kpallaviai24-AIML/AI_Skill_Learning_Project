
import pandas as pd

from src.matching.standardise_skills import (
    normalise_name,
    standardise_esco,
    standardise_onet,
)


def test_normalise_name():
    assert normalise_name("  DATA   ANALYSIS ") == "data analysis"


def test_standardise_esco():
    df = pd.DataFrame({
        "source_skill_id": ["esco-1"],
        "skill_name": ["Python"],
        "aliases": ["Python programming"],
        "skill_type": ["skill"],
        "reuse_level": ["cross-sector"],
        "description": ["Programming language"],
    })

    result = standardise_esco(df)

    assert len(result) == 1
    assert result.loc[0, "source"] == "ESCO"
    assert result.loc[0, "skill_name"] == "Python"


def test_standardise_onet_removes_duplicate_catalogue_entries():
    df = pd.DataFrame({
        "Element ID": ["2.A.1", "2.A.1", "2.B.1"],
        "Element Name": [
            "Active Listening",
            "Active Listening",
            "Mathematics",
        ],
        "skill_category": [
            "essential_skills",
            "essential_skills",
            "transferable_skills",
        ],
    })

    result = standardise_onet(df)

    assert len(result) == 2
    assert result["skill_name"].nunique() == 2
    assert set(result["source"]) == {"O*NET"}
