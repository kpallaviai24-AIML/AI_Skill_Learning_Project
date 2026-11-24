
import pandas as pd
import pytest

from src.relationships import validate_prerequisites


def create_test_data():
    return pd.DataFrame({
        "prerequisite_skill": ["Basic Mathematics"],
        "dependent_skill": ["Statistics"],
        "evidence_source": ["Test source"],
        "evidence_description": ["Test evidence"],
        "confidence": ["high"],
        "review_status": ["approved"],
    })


def run_validation(tmp_path, monkeypatch, df):
    test_file = tmp_path / "prerequisites.csv"
    df.to_csv(test_file, index=False)

    monkeypatch.setattr(
        validate_prerequisites,
        "FILE",
        test_file,
    )

    return validate_prerequisites.main()


def test_valid_relationships_pass(tmp_path, monkeypatch, capsys):
    report = run_validation(
        tmp_path, monkeypatch, create_test_data()
    )

    output = capsys.readouterr().out

    assert "Total relationships: 1" in output
    assert report["valid"] is True
    assert report["incomplete_rows"] == 0
    assert report["duplicate_relationships"] == 0
    assert report["self_loops"] == 0
    assert report["invalid_review_statuses"] == 0
    assert report["has_cycles"] is False


def test_incomplete_rows_are_rejected(tmp_path, monkeypatch):
    df = create_test_data()
    df.loc[0, "evidence_source"] = ""

    with pytest.raises(ValueError, match="Invalid prerequisite"):
        run_validation(tmp_path, monkeypatch, df)


def test_duplicate_relationships_are_rejected(tmp_path, monkeypatch):
    df = pd.concat(
        [create_test_data(), create_test_data()],
        ignore_index=True,
    )

    with pytest.raises(ValueError, match="Invalid prerequisite"):
        run_validation(tmp_path, monkeypatch, df)


def test_self_loops_are_rejected(tmp_path, monkeypatch):
    df = create_test_data()
    df.loc[0, "dependent_skill"] = "Basic Mathematics"

    with pytest.raises(ValueError, match="Invalid prerequisite"):
        run_validation(tmp_path, monkeypatch, df)


def test_invalid_review_status_is_rejected(tmp_path, monkeypatch):
    df = create_test_data()
    df.loc[0, "review_status"] = "pending"

    with pytest.raises(ValueError, match="Invalid prerequisite"):
        run_validation(tmp_path, monkeypatch, df)


def test_approved_cycles_are_rejected(tmp_path, monkeypatch):
    df = create_test_data()

    second = {
        "prerequisite_skill": "Statistics",
        "dependent_skill": "Basic Mathematics",
        "evidence_source": "Test source",
        "evidence_description": "Reverse relationship",
        "confidence": "high",
        "review_status": "approved",
    }

    df = pd.concat(
        [df, pd.DataFrame([second])],
        ignore_index=True,
    )

    with pytest.raises(ValueError, match="Invalid prerequisite"):
        run_validation(tmp_path, monkeypatch, df)


def test_missing_columns_are_rejected(tmp_path, monkeypatch):
    df = pd.DataFrame({
        "prerequisite_skill": ["Basic Mathematics"],
        "dependent_skill": ["Statistics"],
    })

    with pytest.raises(ValueError, match="Missing required columns"):
        run_validation(tmp_path, monkeypatch, df)


def test_empty_file_with_required_columns_is_valid(
    tmp_path, monkeypatch
):
    df = pd.DataFrame(columns=[
        "prerequisite_skill",
        "dependent_skill",
        "evidence_source",
        "evidence_description",
        "confidence",
        "review_status",
    ])

    report = run_validation(tmp_path, monkeypatch, df)

    assert report["valid"] is True
    assert report["total_relationships"] == 0
