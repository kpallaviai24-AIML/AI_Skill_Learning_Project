
import pandas as pd

from src.preprocessing.clean_datasets import clean_dataframe


def test_clean_dataframe_removes_extra_whitespace():
    df = pd.DataFrame({
        "skill_name": ["  Python  ", "Data Analysis "]
    })

    result = clean_dataframe(df)

    assert result["skill_name"].tolist() == [
        "Python",
        "Data Analysis",
    ]


def test_clean_dataframe_converts_empty_strings_to_missing():
    df = pd.DataFrame({
        "skill_name": ["Python", "", "   "]
    })

    result = clean_dataframe(df)

    assert pd.isna(result.loc[1, "skill_name"])
    assert pd.isna(result.loc[2, "skill_name"])


def test_clean_dataframe_preserves_row_count():
    df = pd.DataFrame({
        "skill_name": ["Python", "", "Java"]
    })

    result = clean_dataframe(df)

    assert len(result) == len(df)
