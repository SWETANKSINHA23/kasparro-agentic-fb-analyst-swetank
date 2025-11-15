"""Utility module for file system operations."""

import os


def ensure_reports_directory() -> str:
    """
    Create and return the path to the reports directory.
    
    Output: Absolute path to the reports folder.
    """
    # Resolve path relative to project root
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    reports_dir = os.path.join(project_root, 'reports')
    
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir

# refactor later

# refactor later

# TODO: check this

# note: important

# note: important

# note: important
