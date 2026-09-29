from langgraph.graph import END, START, StateGraph

from app.ai.nodes import (
    extract_complaint,
    check_completeness,
    classify_complaint,
    assess_risk,
    generate_summary,
    detect_duplicate_complaints,
)

from app.ai.state import ComplaintState


def build_complaint_graph():
    workflow = StateGraph(ComplaintState)

    # Add AI nodes
    workflow.add_node(
        "extract_complaint",
        extract_complaint
    )

    workflow.add_node(
        "check_completeness",
        check_completeness
    )

    workflow.add_node(
        "classify_complaint",
        classify_complaint
    )

    workflow.add_node(
        "assess_risk",
        assess_risk
    )

    workflow.add_node(
        "generate_summary",
        generate_summary
    )

    workflow.add_node(
        "detect_duplicate_complaints",
        detect_duplicate_complaints
    )

    # Define workflow
    workflow.add_edge(
        START,
        "extract_complaint"
    )

    workflow.add_edge(
        "extract_complaint",
        "check_completeness"
    )

    workflow.add_edge(
        "check_completeness",
        "classify_complaint"
    )

    workflow.add_edge(
        "classify_complaint",
        "assess_risk"
    )

    workflow.add_edge(
        "assess_risk",
        "generate_summary"
    )

    workflow.add_edge(
        "generate_summary",
        "detect_duplicate_complaints"
    )

    workflow.add_edge(
        "detect_duplicate_complaints",
        END
    )

    return workflow.compile()


complaint_graph = build_complaint_graph()