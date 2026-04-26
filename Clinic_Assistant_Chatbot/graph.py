from langgraph.graph import StateGraph, END, START
from state import GraphState

from agents.intake_agent import intake_agent
from agents.extractor_agent import extractor_agent
from agents.report_generator_agent import report_agent


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("IntakeAgent", intake_agent)
    graph.add_node("ExtractorAgent", extractor_agent)
    graph.add_node("ReportGenerator", report_agent)

    graph.add_edge(START, "IntakeAgent")
    graph.add_edge("IntakeAgent", "ExtractorAgent")
    graph.add_edge("ExtractorAgent", "ReportGenerator")
    graph.add_edge("ReportGenerator", END)

    return graph.compile()


compiled_graph = build_graph()
