
import src.main as pipeline


def test_pipeline_calls_all_stages_in_order(monkeypatch):
    called = []

    stage_names = [
        "validate_all_datasets",
        "clean_all_datasets",
        "extract_skills",
        "standardise_skills",
        "match_skills",
        "prepare_match_review_safely",
        "extract_relationships",
        "validate_prerequisites",
        "validate_problem_solving_review",
        "build_dependency_graph",
        "evaluate_dependency_graph",
    ]

    for name in stage_names:
        monkeypatch.setattr(
            pipeline,
            name,
            lambda name=name: called.append(name),
        )

    pipeline.run_project()

    assert called == stage_names
