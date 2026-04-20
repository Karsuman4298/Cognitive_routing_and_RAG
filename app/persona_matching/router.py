from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import faiss

from app.config.settings import DEFAULT_ROUTING_THRESHOLD
from app.persona_matching.embeddings import encode_texts
from app.utils.logger import get_logger
from personas import PERSONAS

logger = get_logger("persona_router")

PERSONA_IDS = list(PERSONAS.keys())
PERSONA_TEXTS = [PERSONAS[persona_id] for persona_id in PERSONA_IDS]
PERSONA_EMBEDDINGS = encode_texts(PERSONA_TEXTS).astype("float32")

INDEX = faiss.IndexFlatIP(PERSONA_EMBEDDINGS.shape[1])
INDEX.add(PERSONA_EMBEDDINGS)


def route_post_to_bots(post_content: str, threshold: float = DEFAULT_ROUTING_THRESHOLD):
    """Return relevant bots as `(bot_id, cosine_similarity)` tuples."""
    post_embedding = encode_texts([post_content]).astype("float32")
    scores, indices = INDEX.search(post_embedding, k=len(PERSONA_IDS))

    matches = []
    logger.info("Routing post: %s", post_content)
    for score, idx in zip(scores[0], indices[0]):
        bot_id = PERSONA_IDS[idx]
        similarity = float(score)
        logger.info("Similarity score | %s | %.4f", bot_id, similarity)
        if similarity >= threshold:
            matches.append((bot_id, similarity))

    return matches


if __name__ == "__main__":
    sample_post = "OpenAI released a new AI model that can replace developers."
    print(route_post_to_bots(sample_post))
