from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

EMBEDDING_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
GENERATION_MODEL_ID = "google/flan-t5-base"
DEFAULT_ROUTING_THRESHOLD = 0.30
MAX_GENERATION_TOKENS = 160
