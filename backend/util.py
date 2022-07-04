from pathlib import Path


def get_project_root() -> Path:
    parent_path = str(Path(__file__).parent.parent)

    return parent_path
