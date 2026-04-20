from typing import TypedDict


class GraphState(TypedDict, total=False):
    bot_id: str
    persona: str
    topic: str
    search_query: str
    search_results: list[str]
    draft_post: str
    final_output: dict[str, str]
