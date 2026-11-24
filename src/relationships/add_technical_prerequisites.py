
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

FILE = (
    ROOT / "outputs" / "relationships"
    / "prerequisite_relationships.csv"
)

SOURCE = (
    "U.S. Department of Energy, DOE-HDBK-1003-96, "
    "Appendix E, Section E.2, page E-5. "
    "https://www.energy.gov/sites/default/files/2026-04/DOE-HDBK-1003-96.pdf"
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
            "Identify equipment types, drawing symbols, purpose and use",
        "dependent_skill":
            "Identify equipment parts and explain operating principles",
        "evidence_source": SOURCE,
        "evidence_description":
            "DOE Appendix E.2 Module B explicitly builds on Module A. "
            "Module A covers equipment types, drawing symbols and purpose; "
            "Module B adds equipment parts and operating principles.",
        "confidence":
            "high - explicit curriculum progression; rotating equipment context",
        "review_status": "needs_review",
    },
    {
        "prerequisite_skill":
            "Identify equipment parts and explain operating principles",
        "dependent_skill":
            "Recognise abnormal equipment performance and probable causes during troubleshooting",
        "evidence_source": SOURCE,
        "evidence_description":
            "DOE Appendix E.2 Module C explicitly builds on Modules A and B "
            "and adds recognition of normal and abnormal performance "
            "indications and probable causes during troubleshooting.",
        "confidence":
            "high - explicit curriculum progression; rotating equipment context",
        "review_status": "needs_review",
    },
]


def main():
    FILE.parent.mkdir(parents=True, exist_ok=True)

    if FILE.exists():
        df = pd.read_csv(FILE)
    else:
        df = pd.DataFrame(columns=COLUMNS)

    for column in COLUMNS:
        if column not in df.columns:
            df[column] = ""

    df = df[COLUMNS]

    proposed = pd.DataFrame(PROPOSED_RELATIONSHIPS)

    df = pd.concat([df, proposed], ignore_index=True)

    # Avoid adding the same evidence-backed edge more than once
    df = df.drop_duplicates(
        subset=[
            "prerequisite_skill",
            "dependent_skill",
            "evidence_source",
        ],
        keep="first",
    )

    df.to_csv(FILE, index=False, encoding="utf-8-sig")

    print("Technical prerequisite research completed.")
    print("Total relationships:", len(df))
    print("New proposals have review_status = needs_review")
    print("Saved to:", FILE)


if __name__ == "__main__":
    main()
