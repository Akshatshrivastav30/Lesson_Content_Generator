from langgraph.graph import StateGraph, START, END
from src.graph.state import AgentState
from src.graph.nodes import generator_node, evaluator_node, increment_retry_node
from src.graph.router import route_evaluation


def build_agent_pipeline():
    """Builds and compiles the Self-Evaluating Content Generation LangGraph."""
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("generate_lesson", generator_node)
    workflow.add_node("evaluate_lesson", evaluator_node)
    workflow.add_node("increment_retry", increment_retry_node)

    # Edge Connections
    workflow.add_edge(START, "generate_lesson")
    workflow.add_edge("generate_lesson", "evaluate_lesson")

    # Conditional Routing Edge
    workflow.add_conditional_edges(
        "evaluate_lesson",
        route_evaluation,
        {
            "approved": END,
            "retry": "increment_retry",
            "max_retries_exceeded": END
        }
    )

    # Loop edge: increment retry count then route back to generator
    workflow.add_edge("increment_retry", "generate_lesson")

    return workflow.compile()