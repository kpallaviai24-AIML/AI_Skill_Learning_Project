
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

FILE = (
    ROOT / "outputs" / "relationships"
    / "prerequisite_relationships.csv"
)

SOURCE = (
    "OpenStax, Introductory Statistics 2e, "
    "Preface and chapter sequence. "
    "https://openstax.org/books/introductory-statistics-2e/pages/preface"
)

COLUMNS = [
    "prerequisite_skill",
    "dependent_skill",
    "evidence_source",
    "evidence_description",
    "confidence",
    "review_status",
]

PROPOSED_RELATIONSHIPS = [
    {
        "prerequisite_skill":
            "Collect and understand sampling data",
        "dependent_skill":
            "Summarise data using descriptive statistics",
        "evidence_source": SOURCE,
        "evidence_description":
            "OpenStax presents Sampling and Data in Chapter 1 "
            "followed by Descriptive Statistics in Chapter 2.",
        "confidence":
            "moderate - textbook sequence; not a universal prerequisite",
        "review_status": "needs_review",
    },
    {
        "prerequisite_skill":
            "Understand probability concepts",
        "dependent_skill":
            "Work with random variables and probability distributions",
        "evidence_source": SOURCE,
        "evidence_description":
            "OpenStax presents Probability Topics in Chapter 3 "
            "before Discrete and Continuous Random Variables "
            "in Chapters 4 and 5.",
        "confidence":
            "moderate - textbook sequence; not a universal prerequisite",
        "review_status": "needs_review",
    },
    {
        "prerequisite_skill":
            "Understand probability distributions",
        "dependent_skill":
            "Apply the normal distribution",
        "evidence_source": SOURCE,
        "evidence_description":
            "OpenStax presents discrete and continuous random "
            "variables before the Normal Distribution in Chapter 6.",
        "confidence":
            "moderate - textbook sequence; not a universal prerequisite",
        "review_status": "needs_review",
    },
    {
        "prerequisite_skill":
            "Understand the normal distribution",
        "dependent_skill":
            "Apply the central limit theorem",
        "evidence_source": SOURCE,
        "evidence_description":
            "OpenStax presents the Normal Distribution in Chapter 6 "
            "before the Central Limit Theorem in Chapter 7.",
        "confidence":
            "moderate - textbook sequence; not a universal prerequisite",
        "review_status": "needs_review",
    },
    {
        "prerequisite_skill":
            "Understand sampling distributions and the central limit theorem",
        "dependent_skill":
            "Construct confidence intervals",
        "evidence_source": SOURCE,
        "evidence_description":
            "OpenStax presents the Central Limit Theorem in Chapter 7 "
            "before Confidence Intervals in Chapter 8.",
        "confidence":
            "moderate - textbook sequence; not a universal prerequisite",
        "review_status": "needs_review",
    },
    {
        "prerequisite_skill":
            "Understand confidence intervals and sampling distributions",
        "dependent_skill":
            "Perform hypothesis testing",
        "evidence_source": SOURCE,
        "evidence_description":
            "OpenStax presents Confidence Intervals in Chapter 8 "
            "before Hypothesis Testing in Chapters 9 and 10.",
        "confidence":
            "moderate - textbook sequence; not a universal prerequisite",
        "review_status": "needs_review",
    },
]


def main():
    if FILE.exists():
        df = pd.read_csv(FILE)
    else:
        df = pd.DataFrame(columns=COLUMNS)

    for column in COLUMNS:
        if column not in df.columns:
            df[column] = ""

    df = df[COLUMNS]

    proposed = pd.DataFrame(PROPOSED_RELATIONSHIPS)

    combined = pd.concat(
        [df, proposed],
        ignore_index=True
    )

    combined = combined.drop_duplicates(
        subset=[
            "prerequisite_skill",
            "dependent_skill",
            "evidence_source",
        ],
        keep="first",
    )

    combined.to_csv(
        FILE,
        index=False,
        encoding="utf-8-sig",
    )

    print("Analytical prerequisite proposals added.")
    print("Total relationships:", len(combined))
    print("New proposals:", len(PROPOSED_RELATIONSHIPS))
    print("All new proposals remain needs_review.")
    print("Saved to:", FILE)


if __name__ == "__main__":
    main()
