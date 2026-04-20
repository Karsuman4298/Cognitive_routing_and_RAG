from app.utils.logger import get_logger

logger = get_logger("mock_search")

MOCK_SEARCH_INDEX = {
    "ai": [
        "Open-source models are lowering the cost of experimentation.",
        "Teams adopting retrieval pipelines are improving reliability and auditability.",
        "Regulation pressure is pushing AI builders toward transparent deployment practices.",
    ],
    "markets": [
        "Rate-sensitive sectors are reacting quickly to inflation guidance.",
        "Algorithmic strategies are concentrating around liquidity and volatility signals.",
        "Investors are pricing risk more carefully after sharp macro surprises.",
    ],
    "privacy": [
        "Consumers are pushing back on platforms that over-collect personal data.",
        "Regulators are increasing scrutiny on targeted advertising and surveillance tooling.",
        "Privacy-focused products are differentiating through trust and simplicity.",
    ],
}


def mock_search(topic: str) -> list[str]:
    lowered = topic.lower()
    if "market" in lowered or "roi" in lowered or "interest" in lowered:
        key = "markets"
    elif "privacy" in lowered or "monopoly" in lowered or "social" in lowered:
        key = "privacy"
    else:
        key = "ai"

    logger.info("Mock search query: %s", topic)
    return MOCK_SEARCH_INDEX[key]
