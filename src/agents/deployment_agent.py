import os
from typing import Any, Dict, Optional, List

from src.agents.base_agent import BaseAgent

class DeploymentAgent(BaseAgent):
    def reason(self, prompt: str, context: Optional[List[str]] = None) -> Dict[str, Any]:
        self.logger.info("Reasoning about deployment", prompt=prompt)
        return {"action": "generate_deployment_files", "prompt": prompt}

    def act(self, action: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("Generating deployment files")
        project_path = "generated_project"

        self.generate_dockerfile(project_path)
        self.generate_kubernetes_manifest(project_path)
        self.generate_github_workflow(project_path)

        return {"status": "completed", "files": [f"{project_path}/Dockerfile", f"{project_path}/deployment.yaml", f"{project_path}/.github/workflows/ci.yaml"]}

    def generate_dockerfile(self, project_path: str):
        dockerfile_path = os.path.join(project_path, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write("FROM python:3.9-slim\n")
            f.write("WORKDIR /app\n")
            f.write("COPY . .\n")
            f.write("RUN pip install -r requirements.txt\n")
            f.write("CMD [\"python\", \"main.py\"]\n")

    def generate_kubernetes_manifest(self, project_path: str):
        k8s_path = os.path.join(project_path, "deployment.yaml")
        with open(k8s_path, "w") as f:
            f.write("apiVersion: apps/v1\n")
            f.write("kind: Deployment\n")
            f.write("metadata:\n")
            f.write("  name: my-app\n")
            f.write("spec:\n")
            f.write("  replicas: 1\n")
            f.write("  selector:\n")
            f.write("    matchLabels:\n")
            f.write("      app: my-app\n")
            f.write("  template:\n")
            f.write("    metadata:\n")
            f.write("      labels:\n")
            f.write("        app: my-app\n")
            f.write("    spec:\n")
            f.write("      containers:\n")
            f.write("      - name: my-app\n")
            f.write("        image: my-app:latest\n")
            f.write("        ports:\n")
            f.write("        - containerPort: 80\n")

    def generate_github_workflow(self, project_path: str):
        workflow_dir = os.path.join(project_path, ".github", "workflows")
        os.makedirs(workflow_dir, exist_ok=True)
        workflow_path = os.path.join(workflow_dir, "ci.yaml")
        with open(workflow_path, "w") as f:
            f.write("name: CI\n")
            f.write("on: [push]\n")
            f.write("jobs:\n")
            f.write("  build:\n")
            f.write("    runs-on: ubuntu-latest\n")
            f.write("    steps:\n")
            f.write("    - uses: actions/checkout@v2\n")
            f.write("    - name: Set up Python 3.9\n")
            f.write("      uses: actions/setup-python@v2\n")
            f.write("      with:\n")
            f.write("        python-version: 3.9\n")
            f.write("    - name: Install dependencies\n")
            f.write("      run: pip install -r requirements.txt\n")
            f.write("    - name: Run tests\n")
            f.write("      run: pytest\n")
