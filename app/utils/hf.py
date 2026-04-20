import re


def _extract_section(prompt: str, label: str) -> str:
    pattern = rf"{re.escape(label)}:\n(.*?)(?:\n\n[A-Z][^\n]*:|$)"
    match = re.search(pattern, prompt, re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def generate_text(prompt: str, max_new_tokens: int = 160) -> str:
    if "Return strict JSON only with keys: bot_id, topic, post_content." in prompt:
        persona = _extract_section(prompt, "Persona")
        topic = _extract_section(prompt, "Topic") or "AI"
        context = _extract_section(prompt, "Retrieved context")
        sentence_one = f"{topic} is exactly where this persona wants to press the argument."
        context_line = context.splitlines()[0].lstrip("- ").strip() if context else "The supporting evidence is already moving in that direction."
        sentence_two = context_line if context_line.endswith(".") else f"{context_line}."
        return '{"bot_id": "bot_A", "topic": "%s", "post_content": "%s %s"}' % (
            topic.replace('"', ""),
            sentence_one.replace('"', ""),
            sentence_two.replace('"', ""),
        )

    if "Choose one concise topic this persona would post about." in prompt:
        persona = _extract_section(prompt, "Persona").lower()
        if any(word in persona for word in ["market", "roi", "interest", "trading"]):
            return "Markets"
        if any(word in persona for word in ["privacy", "monopol", "social media", "nature"]):
            return "Privacy"
        return "AI"

    if "You are a debater AI with a fixed persona." in prompt or "Rewrite the draft reply" in prompt:
        parent_post = _extract_section(prompt, "Parent post")
        history = _extract_section(prompt, "Conversation history")
        if "electric vehicle" in parent_post.lower() or "batter" in parent_post.lower():
            return (
                "I'm not backing off a weak claim. Modern EV batteries routinely retain strong capacity well past 100,000 miles, "
                "and your own argument ignores the real-world data already reflected in this discussion."
            )
        return (
            "That argument still falls apart under scrutiny. The evidence already on the table is stronger than the rhetoric, "
            "so the serious move here is to answer the facts instead of trying to redirect the conversation."
        )

    return "AI"
