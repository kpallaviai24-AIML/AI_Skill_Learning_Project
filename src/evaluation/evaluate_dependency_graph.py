
import json
from pathlib import Path

import networkx as nx
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

GRAPH_FILE = ROOT / "outputs" / "graphs" / "skill_dependency_graph.graphml"
PREREQUISITES_FILE = ROOT / "outputs" / "relationships" / "prerequisite_relationships.csv"
PROBLEM_SOLVING_FILE = ROOT / "outputs" / "relationships" / "problem_solving_review.csv"
MATCH_REVIEW_FILE = ROOT / "outputs" / "standardised" / "skill_match_review.csv"

REPORT_FILE = ROOT / "outputs" / "evaluation" / "dependency_graph_evaluation.json"


def review_counts(file_path, column):
    if not file_path.exists():
        return {"file_missing": True}

    data = pd.read_csv(file_path)

    if column not in data.columns:
        return {"column_missing": True}

    return {
        str(key): int(value)
        for key, value in data[column].value_counts(dropna=False).items()
    }


def evaluate_dependency_graph():
    if not GRAPH_FILE.exists():
        raise FileNotFoundError(f"Graph file not found: {GRAPH_FILE}")

    graph = nx.read_graphml(GRAPH_FILE)

    is_dag = nx.is_directed_acyclic_graph(graph)

    sources = sorted(
        node for node in graph
        if graph.in_degree(node) == 0
    )

    sinks = sorted(
        node for node in graph
        if graph.out_degree(node) == 0
    )

    isolated_nodes = sorted(
        node for node in graph
        if graph.degree(node) == 0
    )

    weak_components = list(nx.weakly_connected_components(graph))

    topological_order = (
        list(nx.topological_sort(graph)) if is_dag else []
    )

    report = {
        "graph_summary": {
            "total_nodes": graph.number_of_nodes(),
            "total_edges": graph.number_of_edges(),
            "graph_density": round(nx.density(graph), 4),
            "is_directed": graph.is_directed(),
            "is_directed_acyclic_graph": is_dag,
            "has_cycles": not is_dag,
            "weakly_connected_components": len(weak_components),
            "isolated_nodes": isolated_nodes,
            "source_nodes": sources,
            "sink_nodes": sinks,
            "topological_order": topological_order,
        },
        "review_summary": {
            "prerequisite_relationships": review_counts(
                PREREQUISITES_FILE, "review_status"
            ),
            "problem_solving_proposals": review_counts(
                PROBLEM_SOLVING_FILE, "review_status"
            ),
            "skill_match_decisions": review_counts(
                MATCH_REVIEW_FILE, "decision"
            ),
        },
        "evaluation_notes": [
            "Only approved prerequisite relationships are expected in the graph.",
            "A DAG check confirms structural consistency, not educational correctness.",
            "The current graph is a small proof of concept based on rotating-equipment training.",
            "Pending proposals require expert review before they can be used as graph edges.",
        ],
    }

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_FILE.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print("DEPENDENCY GRAPH EVALUATION COMPLETED")
    print(json.dumps(report, indent=4, ensure_ascii=False))
    print(f"\nReport saved to: {REPORT_FILE}")

    return report


if __name__ == "__main__":
    evaluate_dependency_graph()
