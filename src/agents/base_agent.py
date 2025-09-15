
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List

import structlog

from src.rag.retriever import Retriever


class BaseAgent(ABC):
    def __init__(self, retriever: Optional[Retriever] = None):
        self.logger = structlog.get_logger(self.__class__.__name__)
        self.retriever = retriever

    @abstractmethod
    def reason(self, prompt: str, context: Optional[List[str]] = None) -> Dict[str, Any]:
        """Reason about the prompt and decide on a course of action."""
        pass

    @abstractmethod
    def act(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the action and return the result."""
        pass

    def run(self, prompt: str, context_query: Optional[str] = None) -> Dict[str, Any]:
        """Run the agent's reason-act loop."""
        try:
            self.logger.info("Starting agent run", prompt=prompt)
            context = None
            if self.retriever and context_query:
                context = self.retriever.retrieve_context(context_query)
                self.logger.info("Retrieved context", context=context)
            
            action = self.reason(prompt, context=context)
            result = self.act(action)
            self.logger.info("Agent run completed", result=result)
            return result
        except Exception as e:
            self.logger.error("Agent run failed", error=str(e))
            return {"status": "failed", "error": str(e)}
