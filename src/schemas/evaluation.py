from pydantic import BaseModel, Field
from typing import Optional

class EvaluationReport(BaseModel):
    is_passing: bool = Field(description="Set to True ONLY if ALL checks pass.")

    # Flattened Rubric Checks
    accuracy_passed: bool = Field(description="True if accurate, False otherwise.")
    accuracy_reason: Optional[str] = Field(default=None, description="Reason if accuracy failed.")
    accuracy_fix: Optional[str] = Field(default=None, description="Actionable fix if accuracy failed.")

    accessibility_passed: bool = Field(description="True if sentences are 12-15 words max and simple.")
    accessibility_reason: Optional[str] = Field(default=None, description="Reason if accessibility failed.")
    accessibility_fix: Optional[str] = Field(default=None, description="Actionable fix if accessibility failed.")

    analogy_passed: bool = Field(description="True if everyday analogy is used.")
    analogy_reason: Optional[str] = Field(default=None, description="Reason if analogy failed.")
    analogy_fix: Optional[str] = Field(default=None, description="Actionable fix if analogy failed.")

    jargon_passed: bool = Field(description="True if no unexplained technical jargon.")
    jargon_reason: Optional[str] = Field(default=None, description="Reason if jargon failed.")
    jargon_fix: Optional[str] = Field(default=None, description="Actionable fix if jargon failed.")

    flow_passed: bool = Field(description="True if logical structure and progression hold.")
    flow_reason: Optional[str] = Field(default=None, description="Reason if flow failed.")
    flow_fix: Optional[str] = Field(default=None, description="Actionable fix if flow failed.")