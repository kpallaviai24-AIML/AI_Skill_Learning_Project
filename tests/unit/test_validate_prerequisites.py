
import pandas as pd

from src.relationships import validate_prerequisites


def test_validate_prerequisites_reports_valid_relationships(
    tmp_path, monkeypatch, capsys
):
    test_file = tmp_path / "prerequisites.csv"

    df = pd.DataFrame({
        "prerequisite_skill": ["Basic Mathematics"],
        "dependent_skill": ["Statistics"],
        "evidence_source": ["Test source"],
        "evidence_description": ["Test evidence"],
        "confidence": ["high"],
        "review_status": ["approved"],
    })

    df.to_csv(test_file, index=False)

    monkeypatch.setattr(
        validate_prerequisites,
        "FILE",
        test_file,
    )

    validate_prerequisites.main()

    output = capsys.readouterr().out

    assert "Total relationships: 1" in output
    assert "Incomplete rows: 0" in output
    assert "Duplicate relationships: 0" in output
    assert "Self-loops: 0" in output
    assert "Invalid review statuses: 0" in output
