from langgraph.graph import StateGraph, END
from src.graph.state import AgentState
from src.graph.nodes import (
    generator_node,
    evaluator_node,
    increment_retry_node,
    route_after_evaluation,
    MAX_RETRIES,
)

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("generator", generator_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("increment_retry", increment_retry_node)

    workflow.set_entry_point("generator")
    workflow.add_edge("generator", "evaluator")

    workflow.add_conditional_edges(
        "evaluator",
        route_after_evaluation,
        {
            "approved": END,
            "retry": "increment_retry",
            "max_retries_exceeded": END,
        },
    )

    workflow.add_edge("increment_retry", "generator")

    return workflow.compile()


if __name__ == "__main__":
    app = build_graph()

    topic_input = "Introduction to RAG (Retrieval-Augmented Generation)"
    print(f"\n🚀 Starting Self-Evaluating Agent Pipeline for Topic: '{topic_input}'\n")

    initial_state: AgentState = {
        "topic": topic_input,
        "current_draft": None,
        "evaluation_report": None,
        "is_approved": False,
        "retry_count": 0,
        "feedback_history": [],
        "rejection_logs": [],
    }

    final_state = app.invoke(initial_state)

    if final_state.get("is_approved"):
        print("╭" + "─" * 54 + " Status " + "─" * 55 + "╮")
        print("│ ✅ LESSON APPROVED BY EVALUATOR" + " " * 86 + "│")
        print("╰" + "─" * 117 + "╯")

        draft = final_state["current_draft"]
        print("╭" + "─" * 45 + " Final Lesson Draft Output " + "─" * 45 + "╮\n")
        print(f" Title: {draft.title}\n")
        print(f" 1. What is it?\n {draft.what_is_it}\n")
        print(f" 2. Why it matters?\n {draft.why_it_matters}\n")
        print(f" 3. How it works?\n {draft.how_it_works}\n")
        print(f" Summary:\n {draft.summary}\n")
        print("╰" + "─" * 117 + "╯\n")
    else:
        print("╭" + "─" * 54 + " Status " + "─" * 55 + "╮")
        print(f"│ ⚠️ PIPELINE TERMINATED: Max retries ({MAX_RETRIES}) reached without full approval." + " " * 36 + "│")
        print("╰" + "─" * 117 + "╯\n")

    rejection_logs = final_state.get("rejection_logs", [])
    if rejection_logs:
        print("📋 REJECTION LOG (Audit Trail):")
        for log in rejection_logs:
            print(f"\nAttempt #{log['attempt']} Failed Checks: {', '.join(log['failed_checks'])}")
            for feedback in log["remediation_feedback"]:
                print(f"  • {feedback}")