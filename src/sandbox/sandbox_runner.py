
import docker
from typing import Tuple

class SandboxRunner:
    def __init__(self):
        self.client = docker.from_env()

    def run_in_sandbox(self, project_path: str, command: str) -> Tuple[int, str]:
        """Runs a command in a Docker container.

        Args:
            project_path: The path to the project to be mounted in the container.
            command: The command to run in the container.

        Returns:
            A tuple of (exit_code, logs).
        """
        try:
            container = self.client.containers.run(
                image="python:3.9-slim",
                command=command,
                volumes={project_path: {"bind": "/app", "mode": "rw"}},
                working_dir="/app",
                detach=True,
                mem_limit="128m",
                cpu_shares=128,
            )
            result = container.wait()
            logs = container.logs().decode("utf-8")
            container.remove()
            return result["StatusCode"], logs
        except docker.errors.ImageNotFound:
            print("Pulling python:3.9-slim image...")
            self.client.images.pull("python:3.9-slim")
            return self.run_in_sandbox(project_path, command)
        except Exception as e:
            return -1, str(e)
