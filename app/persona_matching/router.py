from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import faiss

from app.persona_matching.embeddings import EMBEDDING_MODEL_ID, encode_texts
from personas import PERSONAS

PERSONA_IDS = list(PERSONAS.keys())
PERSONA_TEXTS = [PERSONAS[persona_id] for persona_id in PERSONA_IDS]
PERSONA_EMBEDDINGS = encode_texts(PERSONA_TEXTS)

INDEX = faiss.IndexFlatIP(PERSONA_EMBEDDINGS.shape[1])
INDEX.add(PERSONA_EMBEDDINGS)


def route_post_to_bots(post_content: str, threshold: float = 0.3):
    post_text = " ".join(post_content.strip().split())
    post_embedding = encode_texts([post_text])
    scores, indices = INDEX.search(post_embedding, k=len(PERSONA_IDS))

    print(f"Embedding model used: {EMBEDDING_MODEL_ID}")

    matches = []
    for score, idx in zip(scores[0], indices[0]):
        bot_id = PERSONA_IDS[idx]
        similarity = float(score)
        print(f"Similarity score | {bot_id} | {similarity:.4f}")
        if similarity >= threshold:
            matches.append((bot_id, similarity))

    print(f"Filtered bots (threshold={threshold}): {matches}")
    return matches


if __name__ == "__main__":
    sample_post = "OpenAI released a new AI model that can replace developers."
    print(route_post_to_bots(sample_post))
