from pathlib import Path
import os
import sys
from functools import lru_cache
from typing import Iterable

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from app.config.settings import ENV_FILE

load_dotenv(ENV_FILE)

EMBEDDING_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL_ID)


def normalize_embeddings(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms = np.clip(norms, a_min=1e-12, a_max=None)
    return vectors / norms


def encode_texts(texts: Iterable[str]) -> np.ndarray:
    model = get_embedding_model()
    cleaned_texts = [text.strip() for text in texts]
    embeddings = model.encode(
        cleaned_texts,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    return normalize_embeddings(embeddings).astype("float32")


def get_embedding(text: str) -> np.ndarray:
    return encode_texts([text])[0]
