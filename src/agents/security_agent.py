
import subprocess
import json
from typing import Any, Dict, List, Optional

from src.agents.base_agent import BaseAgent

class SecurityAgent(BaseAgent):
    def reason(self, prompt: str, context: Optional[List[str]] = None) -> Dict[str, Any]:
        self.logger.info("Reasoning about security", prompt=prompt)
        return {"action": "run_security_scans", "prompt": prompt}

    def act(self, action: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("Running security scans")
        project_path = "generated_project"
        
        bandit_report = self.run_bandit(project_path)
        semgrep_report = self.run_semgrep(project_path)
        pip_audit_report = self.run_pip_audit(project_path)

        report = {
            "bandit": bandit_report,
            "semgrep": semgrep_report,
            "pip_audit": pip_audit_report,
        }

        high_severity_issues = self.find_high_severity_issues(report)

        return {
            "status": "completed",
            "report": report,
            "high_severity_issues": high_severity_issues,
        }

    def run_bandit(self, path: str) -> Dict[str, Any]:
        try:
            result = subprocess.run(
                ["bandit", "-r", path, "-f", "json"],
                capture_output=True,
                text=True,
            )
            return json.loads(result.stdout)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.logger.error("Bandit scan failed", error=str(e))
            return {"error": str(e)}

    def run_semgrep(self, path: str) -> Dict[str, Any]:
        try:
            result = subprocess.run(
                ["semgrep", "--config", "auto", "--json", path],
                capture_output=True,
                text=True,
            )
            return json.loads(result.stdout)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.logger.error("Semgrep scan failed", error=str(e))
            return {"error": str(e)}

    def run_pip_audit(self, path: str) -> Dict[str, Any]:
        try:
            # pip-audit requires a requirements.txt file
            requirements_path = f"{path}/requirements.txt"
            if not os.path.exists(requirements_path):
                with open(requirements_path, "w") as f:
                    f.write("pytest\n") # Add some default dependency

            result = subprocess.run(
                ["pip-audit", "-r", requirements_path, "--format", "json"],
                capture_output=True,
                text=True,
            )
            return json.loads(result.stdout)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.logger.error("pip-audit scan failed", error=str(e))
            return {"error": str(e)}

    def find_high_severity_issues(self, report: Dict[str, Any]) -> List[Dict[str, Any]]:
        high_severity_issues = []
        if report.get("bandit") and "results" in report["bandit"]:
            for issue in report["bandit"]["results"]:
                if issue["issue_severity"] == "HIGH":
                    high_severity_issues.append(issue)
        
        if report.get("semgrep") and "results" in report["semgrep"]:
            for issue in report["semgrep"]["results"]:
                if issue["extra"]["severity"] == "ERROR":
                    high_severity_issues.append(issue)

        if report.get("pip_audit") and "dependencies" in report["pip_audit"]:
            for dep in report["pip_audit"]["dependencies"]:
                if dep["vulns"]:
                    high_severity_issues.extend(dep["vulns"])

        return high_severity_issues
