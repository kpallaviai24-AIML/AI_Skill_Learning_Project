
import json
import pandas as pd
import networkx as nx

from src.graph import build_dependency_graph


def test_graph_uses_only_approved_relationships(
    tmp_path, monkeypatch
):
    input_file = tmp_path / "prerequisites.csv"
    output_dir = tmp_path / "graphs"

    df = pd.DataFrame({
        "prerequisite_skill": [
            "Basic Mathematics",
            "Statistics",
        ],
        "dependent_skill": [
            "Statistics",
            "Data Analysis",
        ],
        "evidence_source": [
            "Test source",
            "Test source",
        ],
        "evidence_description": [
            "Approved evidence",
            "Pending evidence",
        ],
        "confidence": ["high", "medium"],
        "review_status": ["approved", "needs_review"],
    })

    df.to_csv(input_file, index=False)

    monkeypatch.setattr(
        build_dependency_graph,
        "INPUT_FILE",
        input_file,
    )
    monkeypatch.setattr(
        build_dependency_graph,
        "OUTPUT_DIR",
        output_dir,
    )

    build_dependency_graph.main()

    graph_file = output_dir / "skill_dependency_graph.graphml"
    json_file = output_dir / "skill_dependency_graph.json"
    report_file = output_dir / "graph_validation_report.json"

    assert graph_file.exists()
    assert json_file.exists()
    assert report_file.exists()

    graph = nx.read_graphml(graph_file)

    assert graph.number_of_nodes() == 2
    assert graph.number_of_edges() == 1
    assert nx.is_directed_acyclic_graph(graph)

    with open(json_file, encoding="utf-8") as file:
        graph_data = json.load(file)

    assert len(graph_data["nodes"]) == 2
    assert len(graph_data["edges"]) == 1

    with open(report_file, encoding="utf-8") as file:
        report = json.load(file)

    assert report["is_directed_acyclic_graph"] is True
    assert report["approved_relationships_used"] == 1
