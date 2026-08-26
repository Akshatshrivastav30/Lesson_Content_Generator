from typing import TypedDict, List, Dict, Any, Optional

class RejectionEntry(TypedDict):
    attempt: int
    draft: Dict[str, Any]
    failed_checks: List[str]
    remediation_feedback: List[str]

class AgentState(TypedDict):
    topic: str
    current_draft: Optional[Any]
    evaluation_report: Optional[Any]
    is_approved: bool
    retry_count: int
    feedback_history: List[str]
    rejection_logs: List[RejectionEntry]