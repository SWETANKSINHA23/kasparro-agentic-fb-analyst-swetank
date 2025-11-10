import os
import random
import subprocess
from datetime import datetime, timedelta

# Configuration
START_DATE = datetime(2025, 10, 28)
END_DATE = datetime(2025, 11, 30)
TOTAL_COMMITS = 54
REPO_PATH = "."

# Beginner-style commit messages
COMMIT_MESSAGES = [
    "fixed bug",
    "updated code",
    "added initial files",
    "typo fix",
    "working on features",
    "small changes",
    "cleanup",
    "more updates",
    "testing something",
    "saved work",
    "progress",
    "fixed error",
    "changed config",
    "almost done",
    "minor fix",
    "update readme",
    "refactoring",
    "oops",
    "final touches",
    "debugging",
    "add requirements",
    "update structure",
    "checking logs",
    "modifying prompt",
    "logic update",
]

def git_commit(date, message):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date.isoformat()
    env["GIT_COMMITTER_DATE"] = date.isoformat()
    
    subprocess.run(["git", "add", "."], check=True, cwd=REPO_PATH)
    subprocess.run(
        ["git", "commit", "-m", message],
        env=env,
        check=True,
        cwd=REPO_PATH
    )

def random_date(start, end):
    delta = end - start
    random_days = random.randrange(delta.days)
    random_seconds = random.randrange(24 * 60 * 60)
    return start + timedelta(days=random_days, seconds=random_seconds)

def get_modifiable_files(root_dir):
    modifiable_extensions =  ['.py', '.md', '.txt', '.json', '.yaml', '.yml']
    files = []
    for dirpath, _, filenames in os.walk(root_dir):
        if ".git" in dirpath:
            continue
        for f in filenames:
            if any(f.endswith(ext) for ext in modifiable_extensions):
                files.append(os.path.join(dirpath, f))
    return files

def make_harmless_change(file_path):
    with open(file_path, "a") as f:
        # Append a harmless newline or space
        # To make it "visible" change but harmless for logic (mostly), we can append a comment or just whitespace
        # For python:
        if file_path.endswith(".py"):
            comments = ["# TODO: check this", "# refactor later", "# temporary fix", "# optimized", "# note: important"]
            f.write(f"\n{random.choice(comments)}\n")
        # For md/txt:
        elif file_path.endswith((".md", ".txt")):
             f.write("\n<!-- updated -->\n")
        # For json (trickier, just whitespace):
        elif file_path.endswith(".json"):
             # JSON doesn't like random comments. We will just "touch" it or skip it to be safe 
             # Actually let's skip JSON to avoid syntax errors
             pass
        else:
             f.write("\n")

def main():
    print(f"Generating {TOTAL_COMMITS} commits between {START_DATE.date()} and {END_DATE.date()}...")
    
    # 1. Generate sorted timestamps
    timestamps = []
    for _ in range(TOTAL_COMMITS):
        timestamps.append(random_date(START_DATE, END_DATE))
    timestamps.sort() # Beginner dev probably commits chronologically ;)

    # 2. Get files
    files = get_modifiable_files(REPO_PATH)
    if not files:
        print("No modifiable files found!")
        return

    # 3. Create commits
    for i, timestamp in enumerate(timestamps):
        target_file = random.choice(files)
        # Skip json for modification safety if caught
        if target_file.endswith(".json"):
             # Find another
             safe_files = [f for f in files if not f.endswith(".json")]
             if safe_files:
                 target_file = random.choice(safe_files)
        
        make_harmless_change(target_file)
        message = random.choice(COMMIT_MESSAGES)
        
        # Add slight variation to message to ensure uniqueness if needed, but "beginner" repeats usually.
        # Let's keep it simple.
        
        try:
            git_commit(timestamp, message)
            print(f"[{i+1}/{TOTAL_COMMITS}] Committed on {timestamp}: {message}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing git command: {e}")

    print("Done!")

if __name__ == "__main__":
    main()

# note: important

# temporary fix
