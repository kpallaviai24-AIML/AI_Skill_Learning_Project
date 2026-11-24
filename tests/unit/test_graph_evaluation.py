
import json

import networkx as nx
import pandas as pd

from src.evaluation import evaluate_dependency_graph as evaluation


def test_evaluate_dependency_graph_generates_report(tmp_path, monkeypatch):
    graph_file = tmp_path / "test_graph.graphml"
    prerequisite_file = tmp_path / "prerequisites.csv"
    problem_solving_file = tmp_path / "problem_solving.csv"
    match_file = tmp_path / "matches.csv"
    report_file = tmp_path / "evaluation.json"

    graph = nx.DiGraph()
    graph.add_edge("Basic skill", "Advanced skill")
    nx.write_graphml(graph, graph_file)

    pd.DataFrame({
        "review_status": ["approved", "needs_review"]
    }).to_csv(prerequisite_file, index=False)

    pd.DataFrame({
        "review_status": ["needs_review"]
    }).to_csv(problem_solving_file, index=False)

    pd.DataFrame({
        "decision": ["needs_review", "approved"]
    }).to_csv(match_file, index=False)

    monkeypatch.setattr(evaluation, "GRAPH_FILE", graph_file)
    monkeypatch.setattr(evaluation, "PREREQUISITES_FILE", prerequisite_file)
    monkeypatch.setattr(evaluation, "PROBLEM_SOLVING_FILE", problem_solving_file)
    monkeypatch.setattr(evaluation, "MATCH_REVIEW_FILE", match_file)
    monkeypatch.setattr(evaluation, "REPORT_FILE", report_file)

    report = evaluation.evaluate_dependency_graph()

    assert report_file.exists()

    saved_report = json.loads(report_file.read_text(encoding="utf-8"))

    assert saved_report == report
    assert report["graph_summary"]["total_nodes"] == 2
    assert report["graph_summary"]["total_edges"] == 1
    assert report["graph_summary"]["is_directed_acyclic_graph"] is True
    assert report["graph_summary"]["has_cycles"] is False
    assert report["review_summary"]["prerequisite_relationships"]["approved"] == 1


def test_evaluate_dependency_graph_detects_cycles(tmp_path, monkeypatch):
    graph_file = tmp_path / "cyclic_graph.graphml"
    report_file = tmp_path / "evaluation.json"

    graph = nx.DiGraph()
    graph.add_edges_from([
        ("Skill A", "Skill B"),
        ("Skill B", "Skill A"),
    ])

    nx.write_graphml(graph, graph_file)

    monkeypatch.setattr(evaluation, "GRAPH_FILE", graph_file)
    monkeypatch.setattr(evaluation, "REPORT_FILE", report_file)

    report = evaluation.evaluate_dependency_graph()

    assert report["graph_summary"]["is_directed_acyclic_graph"] is False
    assert report["graph_summary"]["has_cycles"] is True
    assert report["graph_summary"]["topological_order"] == []
