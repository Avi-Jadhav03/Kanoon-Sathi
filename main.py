from langgraph.graph import StateGraph, END
from state import LegalAuditState
from agents import (
    type_identifier,
    meaning_extractor,
    law_fetcher,
    cross_checker,
    hallucination_guard,
    report_generator
)

# Build the graph
graph = StateGraph(LegalAuditState)

# Add all nodes
graph.add_node("type_identifier", type_identifier)
graph.add_node("meaning_extractor", meaning_extractor)
graph.add_node("law_fetcher", law_fetcher)
graph.add_node("cross_checker", cross_checker)
graph.add_node("hallucination_guard", hallucination_guard)
graph.add_node("report_generator", report_generator)

# Add normal edges
graph.set_entry_point("type_identifier")
graph.add_edge("type_identifier", "meaning_extractor")
graph.add_edge("meaning_extractor", "law_fetcher")
graph.add_edge("law_fetcher", "cross_checker")
graph.add_edge("cross_checker", "hallucination_guard")

# Add conditional edge for hallucination guard loop
def route_guard(state: LegalAuditState):
    if state["guard_verdict"] == "pass":
        return "report_generator"
    elif state["retry_count"] >= 3:
        # Safety limit - stop infinite loop
        return "report_generator"
    else:
        return "law_fetcher"

graph.add_conditional_edges(
    "hallucination_guard",
    route_guard,
    {
        "report_generator": "report_generator",
        "law_fetcher": "law_fetcher"
    }
)

graph.add_edge("report_generator", END)

# Compile the graph
app = graph.compile()

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader('rent_agreement.pdf')
pages = loader.load()
raw_text = " ".join([page.page_content for page in pages])




initial_state = {
    "raw_document": raw_text,
    "document_type": "",
    "extracted_clauses": [],
    "retrieved_laws": [],
    "analyst_findings": [],
    "guard_verdict": "",
    "retry_count": 0,
    "retry_query": "",
    "final_report": ""
}

# Run the pipeline
result = app.invoke(initial_state)

print("\n========== FINAL AUDIT REPORT ==========")
print(result["final_report"])
print("========================================")