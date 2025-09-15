
import subprocess
import os
from typing import List

class RepoManager:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

    def run_git_command(self, command: List[str]):
        """Runs a git command in the repository path."""
        return subprocess.run(["git"] + command, cwd=self.repo_path, capture_output=True, text=True)

    def init_repo(self):
        """Initializes a new Git repository."""
        self.run_git_command(["init"])

    def commit_files(self, files: List[str], message: str):
        """Commits a list of files to the repository."""
        for file in files:
            self.run_git_command(["add", file])
        self.run_git_command(["commit", "-m", message])

    def get_repo_tree(self) -> str:
        """Returns the repository tree."""
        return self.run_git_command(["ls-tree", "-r", "HEAD"]).stdout
