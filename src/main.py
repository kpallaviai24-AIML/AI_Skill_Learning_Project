from pathlib import Path


def run_project():
    project_root = Path(__file__).resolve().parent.parent

    print("=" * 50)
    print("AI SKILL DEPENDENCY & PERSONALISED LEARNING PATH")
    print("Member 1: Skill Extraction and Dependency Graph")
    print("=" * 50)

    print(f"Project root: {project_root}")
    print("Project initialisation successful.")


if __name__ == "__main__":
    run_project()