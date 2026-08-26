import os
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config.persona import LEARNER_PERSONA_PROMPT
from src.schemas.lesson import LessonDraft
from src.schemas.evaluation import EvaluationReport
from src.graph.state import AgentState, RejectionEntry

MAX_RETRIES = 3

api_key = os.getenv("GROQ_API_KEY")

generator_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=api_key,
    temperature=0.4
).with_structured_output(LessonDraft, method="json_schema")

evaluator_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=api_key,
    temperature=0.0
).with_structured_output(EvaluationReport)


def generator_node(state: AgentState) -> dict:
    """Generates or regenerates a lesson draft enforcing strict word limits per sentence."""
    topic = state["topic"]
    retry_count = state.get("retry_count", 0)
    feedback_history = state.get("feedback_history", [])

    system_instruction = f"""
{LEARNER_PERSONA_PROMPT}

STRICT SENTENCE RULES:
1. MAXIMUM 12 WORDS PER SENTENCE. Use simple, short sentences.
2. Break long explanations into multiple short sentences.
3. Every technical term (like RAG) MUST have a 3-5 word plain definition in parentheses right next to it.
    Example: RAG (a fact-finding tool) helps computers answer questions.
"""

    prompt_messages = [("system", system_instruction)]

    if retry_count > 0 and feedback_history:
        feedback_context = "\n".join([f"- {fb}" for fb in feedback_history])
        prompt_messages.append(
            ("user", f"YOUR PREVIOUS DRAFT WAS REJECTED DUE TO LENGTH/JARGON!\nFix these errors:\n{feedback_context}\n\nRewrite all sections so NO sentence exceeds 12 words.")
        )
    else:
        prompt_messages.append(
            ("user", f"Draft an introductory lesson on '{topic}'. Ensure every sentence is under 12 words.")
        )

    prompt = ChatPromptTemplate.from_messages(prompt_messages)
    chain = prompt | generator_llm
    
    draft: LessonDraft = chain.invoke({})
    
    return {
        "current_draft": draft
    }


def evaluator_node(state: AgentState) -> dict:
    """Evaluates current draft against the rubric."""
    draft = state["current_draft"]
    retry_count = state.get("retry_count", 0)
    
    eval_prompt = ChatPromptTemplate.from_messages([
        ("system", f"""
You are a quality controller evaluating learning content.
{LEARNER_PERSONA_PROMPT}

EVALUATION RULES:
1. Every check is STRICT BINARY (Pass/Fail).
2. Accessibility check PASSES if sentences are generally concise (under 18 words).
3. Jargon check PASSES if technical terms are explained simply.
"""),
        ("user", """
Evaluate this lesson:
Topic: {topic}
Title: {title}
What it is: {what_is_it}
Why it matters: {why_it_matters}
How it works: {how_it_works}
Summary: {summary}
""")
    ])

    chain = eval_prompt | evaluator_llm
    report: EvaluationReport = chain.invoke({
        "topic": draft.topic,
        "title": draft.title,
        "what_is_it": draft.what_is_it,
        "why_it_matters": draft.why_it_matters,
        "how_it_works": draft.how_it_works,
        "summary": draft.summary
    })

    feedback_summary = []
    failed_checks = []

    checks = [
        ("Accuracy", report.accuracy_passed, report.accuracy_reason, report.accuracy_fix),
        ("Accessibility", report.accessibility_passed, report.accessibility_reason, report.accessibility_fix),
        ("Analogy", report.analogy_passed, report.analogy_reason, report.analogy_fix),
        ("Jargon", report.jargon_passed, report.jargon_reason, report.jargon_fix),
        ("Flow", report.flow_passed, report.flow_reason, report.flow_fix),
    ]

    for name, passed, reason, fix in checks:
        if not passed:
            failed_checks.append(name)
            feedback_summary.append(f"[{name} Failed]: {reason or 'Failed criterion'} -> FIX: {fix or 'Revise section.'}")

    is_passing = len(failed_checks) == 0
    report.is_passing = is_passing

    rejection_logs = list(state.get("rejection_logs", []))
    if not is_passing:
        rejection_logs.append(RejectionEntry(
            attempt=retry_count + 1,
            draft=draft.model_dump(),
            failed_checks=failed_checks,
            remediation_feedback=feedback_summary
        ))

    return {
        "evaluation_report": report,
        "is_approved": is_passing,
        "rejection_logs": rejection_logs,
        "feedback_history": state.get("feedback_history", []) + feedback_summary
    }


def increment_retry_node(state: AgentState) -> dict:
    """Bumps retry counter prior to re-generating draft."""
    return {"retry_count": state.get("retry_count", 0) + 1}


def route_after_evaluation(state: AgentState) -> Literal["approved", "retry", "max_retries_exceeded"]:
    """Determines next edge based on evaluation outcome and current retry depth."""
    if state.get("is_approved", False):
        return "approved"
    
    if state.get("retry_count", 0) >= MAX_RETRIES:
        return "max_retries_exceeded"
    
    return "retry"