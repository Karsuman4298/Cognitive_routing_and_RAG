from pathlib import Path
import sys
from functools import lru_cache
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from app.config.settings import EMBEDDING_MODEL_ID, ENV_FILE

load_dotenv(ENV_FILE)


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL_ID)


def encode_texts(texts: Iterable[str]) -> np.ndarray:
    model = get_embedding_model()
    embeddings = model.encode(list(texts), convert_to_numpy=True)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.clip(norms, a_min=1e-12, a_max=None)
    return embeddings / norms


def get_embedding(text: str) -> np.ndarray:
    return encode_texts([text])[0]
