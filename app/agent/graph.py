from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict, total=False):
    query: str
    sources: list
    response: str

def build_graph(rag):
    def retrieve(state):
        return {"sources": rag.search(state["query"])}

    def generate(state):
        sources = state.get("sources", [])
        if not sources:
            answer = "I could not find that information in the connected knowledge base."
        else:
            answer = f"Based on the knowledge base: {sources[0]['text'][:700]} (Source: {sources[0]['source']})"
        return {"response": answer}

    g = StateGraph(State)
    g.add_node("retrieve", retrieve)
    g.add_node("generate", generate)
    g.add_edge(START, "retrieve")
    g.add_edge("retrieve", "generate")
    g.add_edge("generate", END)
    return g.compile()
