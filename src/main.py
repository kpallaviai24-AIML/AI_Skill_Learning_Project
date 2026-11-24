
from pathlib import Path
import pandas as pd

from src.data.validate_datasets import validate_all_datasets
from src.preprocessing.clean_datasets import clean_all_datasets
from src.extraction.extract_skills import main as extract_skills
from src.matching.standardise_skills import main as standardise_skills
from src.matching.match_skills import main as match_skills
from src.relationships.extract_relationships import main as extract_relationships
from src.relationships.validate_prerequisites import main as validate_prerequisites
from src.relationships.validate_problem_solving_review import (
    main as validate_problem_solving_review,
)
from src.graph.build_dependency_graph import main as build_dependency_graph
from src.evaluation.evaluate_dependency_graph import (
    evaluate_dependency_graph,
)


ROOT = Path(__file__).resolve().parent.parent

MATCH_CANDIDATES = (
    ROOT / "outputs" / "standardised" / "skill_match_candidates.csv"
)
MATCH_REVIEW = (
    ROOT / "outputs" / "standardised" / "skill_match_review.csv"
)


def prepare_match_review_safely():
    """Create a review file without overwriting existing human decisions."""

    if not MATCH_CANDIDATES.exists():
        raise FileNotFoundError(MATCH_CANDIDATES)

    candidates = pd.read_csv(MATCH_CANDIDATES)

    if MATCH_REVIEW.exists():
        existing = pd.read_csv(MATCH_REVIEW)

        if "decision" not in existing.columns:
            existing["decision"] = "needs_review"

        if "review_notes" not in existing.columns:
            existing["review_notes"] = ""

        keys = [
            "onet_skill_id",
            "esco_skill_id",
        ]

        if all(key in existing.columns for key in keys):
            existing_keys = set(
                zip(existing["onet_skill_id"], existing["esco_skill_id"])
            )

            new_rows = candidates[
                ~candidates.set_index(keys).index.isin(existing_keys)
            ].copy()

            if not new_rows.empty:
                new_rows["decision"] = "needs_review"
                new_rows["review_notes"] = ""
                existing = pd.concat(
                    [existing, new_rows],
                    ignore_index=True,
                )

        existing.to_csv(
            MATCH_REVIEW,
            index=False,
            encoding="utf-8-sig",
        )

        print("Existing skill-match review decisions preserved.")
        print("Review records:", len(existing))

    else:
        candidates["decision"] = "needs_review"
        candidates["review_notes"] = ""

        candidates.to_csv(
            MATCH_REVIEW,
            index=False,
            encoding="utf-8-sig",
        )

        print("New skill-match review file created.")
        print("Review records:", len(candidates))


def run_project():
    print("=" * 60)
    print("AI SKILL DEPENDENCY & PERSONALISED LEARNING PATH")
    print("MEMBER 1: SKILL EXTRACTION AND DEPENDENCY GRAPH")
    print("=" * 60)
    print("Project root:", ROOT)

    stages = [
        ("1. Validate raw datasets", validate_all_datasets),
        ("2. Clean datasets", clean_all_datasets),
        ("3. Extract skills", extract_skills),
        ("4. Standardise skills", standardise_skills),
        ("5. Generate skill-match candidates", match_skills),
        ("6. Prepare skill-match review safely", prepare_match_review_safely),
        ("7. Extract ESCO relationships", extract_relationships),
        ("8. Validate prerequisite relationships", validate_prerequisites),
        (
            "9. Validate problem-solving review",
            validate_problem_solving_review,
        ),
        ("10. Build dependency graph", build_dependency_graph),
        ("11. Evaluate dependency graph", evaluate_dependency_graph),
    ]

    for stage_name, stage_function in stages:
        print("\n" + "-" * 60)
        print(stage_name)
        print("-" * 60)
        stage_function()

    print("\n" + "=" * 60)
    print("MEMBER 1 PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    run_project()
