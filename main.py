
import asyncio
import threading
import time
import uvicorn

from src.logging_setup import setup_logging
from src.rag.indexer import Indexer
from src.rag.retriever import Retriever
from src.orchestrator.orchestrator import Orchestrator
from src.repo_manager.repo_manager import RepoManager
from src.sandbox.sandbox_runner import SandboxRunner
from src.review_api import app as review_app

def run_review_api():
    uvicorn.run(review_app, host="0.0.0.0", port=8000)

def main():
    """Main function to demonstrate the RAG-powered agentic code generator."""
    setup_logging()

    # 1. Start the review API in a background thread
    review_thread = threading.Thread(target=run_review_api, daemon=True)
    review_thread.start()
    time.sleep(2) # Give the server time to start

    # 2. Index some documents
    indexer = Indexer()
    documents = [
        "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.",
        "Prefect is a workflow orchestration tool that allows you to build, run, and monitor data pipelines at scale.",
        "Structlog is a powerful and flexible logging library for Python that helps you produce structured, machine-readable logs."
    ]
    indexer.index_documents(documents)

    # 3. Create a retriever
    retriever = Retriever()

    # 4. Create a repo manager
    repo_manager = RepoManager(repo_path="generated_project")

    # 5. Create a sandbox runner
    sandbox_runner = SandboxRunner()

    # 6. Define the project manifest
    project_manifest = {
        "name": "ComplexWebApp",
        "tasks": [
            {
                "name": "generate_api",
                "agent": "CodeGenAgent",
                "description": "Generate the FastAPI backend.",
                "context_query": "How to create a FastAPI backend?",
                "retries": 2,
            },
            {
                "name": "generate_frontend",
                "agent": "CodeGenAgent",
                "description": "Generate the React frontend.",
                "context_query": "How to create a React frontend?",
            },
            {
                "name": "security_scan_api",
                "agent": "SecurityAgent",
                "description": "Scan the API for vulnerabilities.",
                "dependencies": ["generate_api"],
            },
            {
                "name": "test_api",
                "agent": "TesterAgent",
                "description": "Test the API.",
                "dependencies": ["generate_api"],
            },
            {
                "name": "test_frontend",
                "agent": "TesterAgent",
                "description": "Test the frontend.",
                "dependencies": ["generate_frontend"],
            },
            {
                "name": "integration_test",
                "agent": "TesterAgent",
                "description": "Run integration tests.",
                "dependencies": ["test_api", "test_frontend"],
            },
            {
                "name": "generate_deployment",
                "agent": "DeploymentAgent",
                "description": "Generate deployment files.",
                "dependencies": ["integration_test"],
            },
        ]
    }

    # 7. Run the orchestrator with the generated manifest
    orchestrator = Orchestrator(retriever=retriever, repo_manager=repo_manager, sandbox_runner=sandbox_runner)
    asyncio.run(orchestrator.execute_dag(project_manifest))

    # 8. Show the repo tree
    print("\nGenerated project repository tree:")
    print(repo_manager.get_repo_tree())

if __name__ == "__main__":
    main()
