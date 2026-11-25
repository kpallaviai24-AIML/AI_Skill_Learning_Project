
# AI Skill Dependency & Personalised Learning Path Generator

## Member 1: Skill Extraction and Skill Dependency Graph

### 1. Project Objective

The project aims to identify and standardise skill concepts from established skill databases, investigate evidence-supported relationships between skills, and construct a directed skill dependency graph.

Member 1 is responsible for the skill extraction, standardisation, relationship preparation, and dependency graph stages. The resulting outputs are intended to support the work of the other project members.

### 2. Member 1 Responsibilities

- Load and validate ESCO and O*NET datasets.
- Clean and preprocess source data.
- Extract skill records from the selected datasets.
- Standardise skill names and catalogue entries.
- Generate potential cross-dataset skill matches for review.
- Prepare skill relationship records.
- Research and document potential prerequisite relationships.
- Require review before proposed prerequisite relationships are approved.
- Build a directed skill dependency graph using approved relationships.
- Validate and export graph results.

### 3. Technologies

- Python 3.12
- Pandas
- OpenPyXL
- NetworkX
- Pytest

### 4. Data Sources

- ESCO: https://esco.ec.europa.eu/en/use-esco/download
- O*NET: https://www.onetcenter.org/database.html

The current implementation uses selected ESCO skill, occupation, and relationship tables, along with O*NET occupation, Essential Skills, and Transferable Skills tables.

### 5. Project Structure

- `config/` - configuration files
- `datasets/raw/` - downloaded source datasets
- `datasets/processed/` - cleaned datasets
- `src/data/` - data loading and validation
- `src/preprocessing/` - data cleaning
- `src/extraction/` - skill extraction
- `src/matching/` - skill standardisation and matching
- `src/relationships/` - relationship preparation and validation
- `src/graph/` - dependency graph construction
- `src/evaluation/` - evaluation-related modules
- `src/integration/` - integration-related modules
- `tests/` - automated tests
- `outputs/` - generated results
- `docs/` - project documentation
- `logs/` - execution logs

### 6. Environment Setup

Create a virtual environment:

    py -3.12 -m venv .venv

Activate it in Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

Install project and development dependencies:

    python -m pip install -r requirements-dev.txt

### 7. Dataset Setup

Download the ESCO and O*NET datasets from the official sources listed above.

Place the extracted files in the corresponding folders under:

    datasets/raw/esco/
    datasets/raw/onet/

The input filenames and folder structure must match the paths expected by the data-loading modules.

Raw datasets and generated outputs are not included in the Git repository. Each developer must obtain the source datasets separately.

### 8. Running the Project

From the project root, activate the virtual environment and run:

    python run.py

The main pipeline performs dataset validation, cleaning, skill extraction, standardisation, candidate matching, relationship validation, and graph construction.

### 9. Testing

Run all automated tests:

    python -m pytest -v

The tests cover data cleaning, skill extraction, standardisation, prerequisite validation, graph construction, preservation of manual matching decisions, and pipeline stage ordering.

### 10. Main Outputs

Generated outputs include:

- Extracted skill records
- Standardised skill catalogue
- Potential skill match candidates
- Skill match review file
- ESCO skill relationship records
- Prerequisite relationship review records
- GraphML and JSON dependency graph files
- Graph validation report
- Data quality report

Generated files are stored under the relevant subfolders in `outputs/`.

### 11. Dependency Graph Convention

A directed edge:

    A -> B

means that skill A is treated as a prerequisite for learning skill B.

Only relationships with an approved review status are included in the dependency graph.

Related-skill associations, occupational relevance, textbook chapter order, and process workflow order must not automatically be interpreted as universal learning prerequisites.

### 12. Current Implementation Status and Limitations

The current implementation is a working proof of concept for Member 1.

- The current approved dependency graph contains a small number of evidence-backed relationships from a rotating-equipment training example.
- Additional analytical and problem-solving relationships are maintained separately or marked for review.
- Potential ESCO–O*NET matches require manual verification.
- The current graph is not a comprehensive prerequisite graph across all occupations or skill domains.
- The integration test verifies pipeline stage ordering using mocked functions; it is not a complete end-to-end test of every dataset operation.
- Evaluation and integration modules may be expanded as the project develops.

Proposed relationships must be reviewed before approval and inclusion in the graph.
s











Hi everyone,

I have completed the Member 1 implementation for our project, **AI Skill Dependency & Personalised Learning Path Generator**.

The following modules are ready:
- Skill extraction from ESCO and O*NET datasets
- Skill standardisation
- Cross-source skill matching
- Prerequisite relationship preparation and validation
- Dependency graph construction
- Graph evaluation

All 26 tests are passing, and the latest code has been pushed to GitHub.

**GitHub repository:**  
https://github.com/kpallaviai24-AIML/AI_Skill_Learning_Project

I have also prepared `Member1_Handover.zip`, which contains the generated datasets, standardised skill catalogue, matching files, prerequisite relationships, dependency graph, evaluation reports and documentation.

**Member 2:** Please use `standardised_skills.csv` and the dependency graph outputs as the starting point for learner profiling and skill-gap analysis.

**Member 3:** Please coordinate with Member 2 and use the learner skill-gap output to develop the personalised learning path generation module.

Important: Skill matches and prerequisite relationships marked `needs_review` are not approved. The current graph contains only approved relationships.

Please review the handover files and let me know if you need clarification about the data formats or integration.
