
import pandas as pd

from src.matching.match_skills import (
    calculate_similarity,
    generate_candidates,
    normalise,
)


def test_normalise_skill_name():
    assert normalise("  Active   Listening! ") == "active listening"


def test_exact_match_has_score_one():
    assert calculate_similarity(
        "mathematics", "mathematics"
    ) == 1.0


def test_scoped_skill_has_lower_similarity():
    score = calculate_similarity(
        "operations monitoring",
        "monitor operations in the leather industry",
    )

    assert score < 0.85


def test_exact_alias_is_detected():
    df = pd.DataFrame([
        {
            "source": "O*NET",
            "source_skill_id": "ONET-1",
            "skill_name": "Equipment Maintenance",
            "aliases": "",
        },
        {
            "source": "ESCO",
            "source_skill_id": "ESCO-1",
            "skill_name": "maintain equipment",
            "aliases": "Equipment Maintenance",
        },
    ])

    result = generate_candidates(df)

    assert len(result) == 1
    assert result.iloc[0]["match_type"] == "exact_alias"
    assert result.iloc[0]["similarity_score"] == 1.0
    assert result.iloc[0]["review_status"] == "needs_manual_review"


def test_duplicate_candidate_pairs_are_removed():
    df = pd.DataFrame([
        {
            "source": "O*NET",
            "source_skill_id": "ONET-1",
            "skill_name": "Mathematics",
            "aliases": "",
        },
        {
            "source": "ESCO",
            "source_skill_id": "ESCO-1",
            "skill_name": "Mathematics",
            "aliases": "",
        },
        {
            "source": "ESCO",
            "source_skill_id": "ESCO-1",
            "skill_name": "Mathematics",
            "aliases": "",
        },
    ])

    result = generate_candidates(df)

    assert len(result) == 1
    assert result.iloc[0]["esco_skill_id"] == "ESCO-1"
