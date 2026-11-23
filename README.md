
# AI Skill Dependency & Personalised Learning Path Generator

## Member 1: Skill Extraction and Skill Dependency Graph

### 1. Project Objective
To identify skills from career descriptions, standardise
skill concepts, identify evidence-supported skill
relationships, and construct a validated skill dependency
graph.

### 2. Member 1 Responsibilities
- Load and process ESCO and O*NET datasets.
- Preprocess career descriptions.
- Extract skills using NLP techniques.
- Match extracted skills to standardised skill concepts.
- Identify and classify skill relationships.
- Build a directed skill dependency graph.
- Validate and analyse the graph.
- Export results for Members 2 and 3.

### 3. Technologies
- Python 3.12
- Pandas and NumPy
- spaCy and NLTK
- Scikit-learn
- Sentence Transformers
- NetworkX
- Matplotlib and PyVis
- Pytest

### 4. Data Sources
- ESCO: https://esco.ec.europa.eu/en/use-esco/download
- O*NET: https://www.onetcenter.org/database.html

### 5. Project Structure
- config: application configuration
- datasets: raw and processed datasets
- src: implementation modules
- tests: automated tests
- outputs: generated results
- logs: execution logs
- docs: technical documentation

### 6. Setup
Create the virtual environment:

    py -3.12 -m venv .venv

Activate it on Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

Install project dependencies after requirements are prepared:

    pip install -r requirements.txt

### 7. Main Outputs
- Extracted skills
- Standardised skill concepts
- Skill relationship records
- Skill dependency graph
- Graph validation report
- Evaluation report

### 8. Graph Convention
An edge A -> B means skill A is a prerequisite
for learning skill B.

Only evidence-supported prerequisite relationships
should be treated as learning dependencies.

### 9. Project Status
Phase 1: Environment and project structure setup.
