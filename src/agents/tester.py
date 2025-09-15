
import os
from typing import Any, Dict, Optional

from src.agents.base_agent import BaseAgent
from src.sandbox.sandbox_runner import SandboxRunner


class TesterAgent(BaseAgent):
    def __init__(self, sandbox_runner: Optional[SandboxRunner] = None, **kwargs):
        super().__init__(**kwargs)
        self.sandbox_runner = sandbox_runner or SandboxRunner()

    def reason(self, prompt: str, context=None) -> Dict[str, Any]:
        self.logger.info("Reasoning about testing", prompt=prompt)
        return {"action": "run_tests", "prompt": prompt}

    def act(self, action: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("Running tests in sandbox")

        project_path = "generated_project"
        test_dir = os.path.join(project_path, "tests")
        os.makedirs(test_dir, exist_ok=True)

        # Create a simple test file
        with open(os.path.join(test_dir, "test_main.py"), "w") as f:
            f.write("import pytest\n\ndef test_hello_world():\n    assert True\n")

        # Create a Dockerfile
        with open(os.path.join(project_path, "Dockerfile"), "w") as f:
            f.write("FROM python:3.9-slim\n")
            f.write("WORKDIR /app\n")
            f.write("COPY . .\n")
            f.write("RUN pip install pytest\n")
            f.write("CMD [\"pytest\"]\n")

        if self.sandbox_runner:
            exit_code, logs = self.sandbox_runner.run_in_sandbox(os.path.abspath(project_path), "pytest")
            self.logger.info("Sandbox run finished", exit_code=exit_code, logs=logs)
            return {"status": "completed", "test_results": {"exit_code": exit_code, "logs": logs}}
        else:
            return {"status": "failed", "error": "SandboxRunner not configured"}
