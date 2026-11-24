
import pandas as pd

from src import main as pipeline


def test_existing_manual_decisions_are_preserved(
    tmp_path, monkeypatch
):
    candidates_file = tmp_path / "candidates.csv"
    review_file = tmp_path / "review.csv"

    candidates = pd.DataFrame({
        "onet_skill_id": ["O1", "O2"],
        "onet_skill_name": ["Python", "Mathematics"],
        "esco_skill_id": ["E1", "E2"],
        "esco_skill_name": ["Python programming", "Mathematics"],
        "similarity_score": [0.95, 0.90],
        "review_status": ["needs_manual_review", "needs_manual_review"],
    })

    candidates.to_csv(candidates_file, index=False)

    existing = pd.DataFrame({
        "onet_skill_id": ["O1"],
        "onet_skill_name": ["Python"],
        "esco_skill_id": ["E1"],
        "esco_skill_name": ["Python programming"],
        "similarity_score": [0.95],
        "review_status": ["needs_manual_review"],
        "decision": ["approved"],
        "review_notes": ["Manually verified"],
    })

    existing.to_csv(review_file, index=False)

    monkeypatch.setattr(
        pipeline, "MATCH_CANDIDATES", candidates_file
    )
    monkeypatch.setattr(
        pipeline, "MATCH_REVIEW", review_file
    )

    pipeline.prepare_match_review_safely()

    result = pd.read_csv(review_file)

    approved = result[result["onet_skill_id"] == "O1"].iloc[0]
    new_record = result[result["onet_skill_id"] == "O2"].iloc[0]

    assert approved["decision"] == "approved"
    assert approved["review_notes"] == "Manually verified"
    assert new_record["decision"] == "needs_review"
    assert len(result) == 2
