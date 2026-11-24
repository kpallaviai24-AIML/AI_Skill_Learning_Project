
from pathlib import Path
import json
import pandas as pd
import networkx as nx

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    ROOT / "outputs" / "relationships"
    / "prerequisite_relationships.csv"
)

OUTPUT_DIR = ROOT / "outputs" / "graphs"

REQUIRED_COLUMNS = [
    "prerequisite_skill",
    "dependent_skill",
    "evidence_source",
    "evidence_description",
    "confidence",
    "review_status",
]


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_FILE)

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Only evidence-reviewed and approved relationships
    approved = df[
        df["review_status"].astype(str).str.lower() == "approved"
    ].copy()

    # Remove incomplete relationships
    approved = approved.dropna(
        subset=["prerequisite_skill", "dependent_skill"]
    )

    graph = nx.DiGraph()

    for _, row in approved.iterrows():
        prerequisite = str(row["prerequisite_skill"]).strip()
        dependent = str(row["dependent_skill"]).strip()

        if not prerequisite or not dependent:
            continue

        if prerequisite == dependent:
            print("Skipping self-loop:", prerequisite)
            continue

        graph.add_node(prerequisite)
        graph.add_node(dependent)

        graph.add_edge(
            prerequisite,
            dependent,
            evidence_source=str(row["evidence_source"]),
            evidence_description=str(row["evidence_description"]),
            confidence=str(row["confidence"]),
        )

    # Save GraphML
    nx.write_graphml(
        graph,
        OUTPUT_DIR / "skill_dependency_graph.graphml"
    )

    # Save JSON
    graph_data = {
        "nodes": [
            {"id": node}
            for node in graph.nodes()
        ],
        "edges": [
            {
                "source": source,
                "target": target,
                **attributes,
            }
            for source, target, attributes
            in graph.edges(data=True)
        ],
    }

    with open(
        OUTPUT_DIR / "skill_dependency_graph.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(graph_data, file, indent=4)

    # Check whether the graph is a DAG
    is_dag = nx.is_directed_acyclic_graph(graph)

    report = {
        "total_nodes": graph.number_of_nodes(),
        "total_edges": graph.number_of_edges(),
        "approved_relationships_used": len(approved),
        "is_directed_acyclic_graph": is_dag,
        "has_cycles": not is_dag,
    }

    if is_dag and graph.number_of_nodes() > 0:
        report["topological_order"] = list(
            nx.topological_sort(graph)
        )

    with open(
        OUTPUT_DIR / "graph_validation_report.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(report, file, indent=4)

    print("\nDEPENDENCY GRAPH BUILD COMPLETED")
    print("Nodes:", graph.number_of_nodes())
    print("Edges:", graph.number_of_edges())
    print("Is DAG:", is_dag)
    print("Output directory:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
