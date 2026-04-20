import json
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

from app.content_engine.state import GraphState
from app.content_engine.tool import mock_search
from app.utils.hf import generate_text

DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

TOPIC_PROMPT = """
You are helping a persona-driven content engine.
Persona:
{persona}

Choose one concise topic this persona would post about.
Do not repeat the input. Return only the answer.
""".strip()

WRITE_PROMPT = """
You are writing a short social post for a fixed persona.
Persona:
{persona}

Topic:
{topic}

Retrieved context:
{context}

Return strict JSON only with keys: bot_id, topic, post_content.
Do not include any extra keys.
Do not use nested JSON.
The post_content must be 2 short sentences.
Do not repeat the input. Return only the answer.
""".strip()


def _debug(message: str) -> None:
    if DEBUG_MODE:
        print(message)


def _invoke_llm(prompt: str) -> str:
    try:
        response = generate_text(prompt, max_new_tokens=128)
        if isinstance(response, str):
            return response.strip()
        content = getattr(response, "content", None)
        if isinstance(content, str):
            return content.strip()
        return str(response).strip()
    except Exception as exc:
        _debug(f"[Phase 2] LLM error: {exc}")
        return ""


def _repair_output(raw_output: str, state: GraphState) -> dict[str, str]:
    fallback = {
        "bot_id": state["bot_id"],
        "topic": state["topic"],
        "post_content": (
            f"{state['topic']} is exactly where this persona wants to press the argument. "
            f"{state['search_results'][0]}"
        ),
    }

    try:
        parsed = json.loads(raw_output)
        repaired = {
            "bot_id": str(parsed.get("bot_id", state["bot_id"])),
            "topic": str(parsed.get("topic", state["topic"])),
            "post_content": str(parsed.get("post_content", fallback["post_content"])),
        }
    except Exception:
        repaired = fallback

    repaired["bot_id"] = state["bot_id"]
    repaired["topic"] = repaired["topic"].strip() or state["topic"]
    repaired["post_content"] = repaired["post_content"].strip() or fallback["post_content"]
    return repaired


def decide_node(state: GraphState) -> GraphState:
    _debug("[Phase 2] decide_node start")
    topic = _invoke_llm(TOPIC_PROMPT.format(persona=state["persona"])) or "AI"
    _debug("[Phase 2] decide_node done")
    return {
        **state,
        "topic": topic,
        "search_query": topic,
    }


def search_node(state: GraphState) -> GraphState:
    _debug("[Phase 2] search_node start")
    results = mock_search(state["search_query"])
    _debug("[Phase 2] search_node done")
    return {
        **state,
        "search_results": results,
    }


def write_node(state: GraphState) -> GraphState:
    _debug("[Phase 2] write_node start")
    context = "\n".join(f"- {item}" for item in state["search_results"])
    raw_output = _invoke_llm(
        WRITE_PROMPT.format(
            persona=state["persona"],
            topic=state["topic"],
            context=context,
        )
    )
    final_output = _repair_output(raw_output, state)
    _debug("[Phase 2] write_node done")
    return {"final_output": final_output}
