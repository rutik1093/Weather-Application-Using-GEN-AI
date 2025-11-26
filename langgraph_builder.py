# app/langgraph_builder.py

from langgraph.graph import StateGraph, END
from typing import Optional, TypedDict

from .decision_node import decide_route
from .weather_node import fetch_weather, weather_to_text
from .pdf_rag import ingest_pdf, retrieve_for_query



class WorkflowState(TypedDict):
    query: str
    pdf_path: Optional[str]
    response: str     
    route: str        



def build_workflow():

    graph = StateGraph(WorkflowState)

 
    def start(state: WorkflowState):
        route = decide_route(state["query"])
        return {"route": route}

 
    def weather_node(state: WorkflowState):
        q = state["query"]

        import re
        m = re.search(r"in\s+([A-Za-z\s]+)", q)
        city = m.group(1).strip() if m else "London"

        w = fetch_weather(city)
        return {"response": weather_to_text(w)}

    def pdf_node(state: WorkflowState):
        pdf_path = state.get("pdf_path")

        if pdf_path:
            ingest_pdf(pdf_path)

        answer = retrieve_for_query(state["query"], k=4)

        return {"response": answer}


    graph.add_node("start", start)
    graph.add_node("weather", weather_node)
    graph.add_node("pdf", pdf_node)

  
    graph.set_entry_point("start")


    graph.add_conditional_edges(
        "start",
        lambda s: s["route"],
        {
            "weather": "weather",
            "pdf": "pdf"
        }
    )

    
    graph.add_edge("weather", END)
    graph.add_edge("pdf", END)

    return graph.compile()
