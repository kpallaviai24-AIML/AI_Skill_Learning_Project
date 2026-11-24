
import pandas as pd

from src.extraction.extract_skills import (
    extract_esco_skills,
    extract_onet_skills,
)


def test_extract_esco_skills():
    df = pd.DataFrame({
        "conceptUri": ["esco-1"],
        "preferredLabel": ["Python"],
        "altLabels": ["Python programming"],
        "skillType": ["skill"],
        "reuseLevel": ["cross-sector"],
        "description": ["Programming language"],
    })

    result = extract_esco_skills({"skills": df})

    assert len(result) == 1
    assert result.loc[0, "skill_name"] == "Python"
    assert result.loc[0, "source"] == "ESCO"
    assert result.loc[0, "source_skill_id"] == "esco-1"


def test_extract_onet_skills():
    sample = pd.DataFrame({
        "Element ID": ["2.A.1.a"],
        "Element Name": ["Active Listening"],
        "Scale ID": ["IM"],
        "Scale Name": ["Importance"],
        "Data Value": [4.5],
        "O*NET-SOC Code": ["15-1252.00"],
    })

    result = extract_onet_skills({
        "essential_skills": sample,
        "transferable_skills": sample,
    })

    assert len(result) == 2
    assert set(result["source"]) == {"O*NET"}
    assert set(result["Element Name"]) == {"Active Listening"}

