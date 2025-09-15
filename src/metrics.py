
from prometheus_client import Counter, Histogram

TASK_COUNTER = Counter("agentic_code_generator_tasks_total", "Total number of tasks", ["agent_name", "status"])
TASK_DURATION = Histogram("agentic_code_generator_task_duration_seconds", "Duration of tasks", ["agent_name"])
