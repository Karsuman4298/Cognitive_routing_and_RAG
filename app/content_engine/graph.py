from langgraph.graph import END, StateGraph

from app.content_engine.node import decide_node, search_node, write_node
from app.content_engine.state import GraphState

builder = StateGraph(GraphState)
builder.add_node("decide", decide_node)
builder.add_node("search", search_node)
builder.add_node("write", write_node)

builder.set_entry_point("decide")
builder.add_edge("decide", "search")
builder.add_edge("search", "write")
builder.add_edge("write", END)

graph = builder.compile()


def generate_post(bot_id: str, persona: str) -> dict[str, str]:
    state = graph.invoke({"bot_id": bot_id, "persona": persona})
    final_output = state.get("final_output", {})
    return {
        "bot_id": str(final_output.get("bot_id", bot_id)),
        "topic": str(final_output.get("topic", "AI")),
        "post_content": str(final_output.get("post_content", "")),
    }
