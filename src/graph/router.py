from typing import Literal
from src.graph.state import AgentState


def route_evaluation(state: AgentState) -> Literal["approved", "retry", "max_retries_exceeded"]:
    """Determines next node based on evaluation state and retry limit."""
    is_approved = state.get("is_approved", False)
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 2)

    if is_approved:
        return "approved"
    elif retry_count >= max_retries:
        return "max_retries_exceeded"
    else:
        return "retry"