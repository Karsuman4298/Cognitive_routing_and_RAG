# Grid07 Cognitive Routing & RAG Engine

## Overview
Grid07 Cognitive Routing & RAG Engine is a three-phase AI system that routes input content to the most relevant persona, orchestrates persona-aligned content generation through a LangGraph workflow, and produces a guarded argumentative reply using retrieval-grounded context plus prompt injection defense. The project is designed as a clean, reproducible academic submission with deterministic outputs, strict JSON formatting, and separation between debugging signals and submission-facing results.

## Architecture
```text
Input Post
  -> FAISS Persona Router
  -> LangGraph Content Engine
  -> RAG Defense Engine
  -> Final Output
```

## Phase Breakdown
### 1. Vector-Based Persona Matching
- Persona descriptions are embedded with `sentence-transformers/all-MiniLM-L6-v2`.
- Embeddings are normalized so FAISS inner-product search behaves as cosine similarity.
- The router returns matched bots and similarity scores for the input post.

### 2. LangGraph Orchestration
- `decide_node` generates a topic for the selected persona.
- `search_node` retrieves supporting evidence from a deterministic mock search layer.
- `write_node` produces and repairs strict JSON output with exactly three fields:
  - `bot_id`
  - `topic`
  - `post_content`

### 3. Mock RAG + Prompt Injection Defense
- The defense module uses the parent post, conversation history, and latest user reply as its RAG context.
- User input is explicitly treated as untrusted content.
- The prompt enforces instruction hierarchy, persona locking, malicious-instruction refusal, and continuation of the original argument.

## Prompt Injection Defense Strategy
- System-level rules define strict priority ordering: system > developer > user.
- Suspicious phrases are detected and surfaced to the defense prompt as hostile patterns, not instructions to execute.
- The model is instructed to stay in persona, refuse role switching, ignore override attempts, and continue reasoning from the existing debate context.

## Tech Stack
- Python 3.13
- SentenceTransformers
- FAISS
- LangGraph
- Hugging Face-compatible generation flow
- python-dotenv
- uv

## Key Design Decisions
- Normalized embeddings plus FAISS inner-product search for efficient cosine similarity routing.
- LangGraph state machine for transparent multi-step orchestration.
- Deterministic mock retrieval to keep the project reproducible in a local academic environment.
- Debug output gated by `DEBUG_MODE` so submission runs stay clean.
- Strict JSON repair in Phase 2 to guarantee schema compliance even after model failure.

## How To Run
```bash
uv sync
uv run main.py
```

### Optional Debug Mode
```bash
DEBUG_MODE=true uv run main.py
```

## Submission Outputs
- `uv run main.py` prints only the final Phase 2 JSON output.
- `logs.md` stores the required records for Phase 1, Phase 2, and Phase 3.

## Example Scenarios
### Routing Examples
1. `OpenAI released a new AI model that can replace developers`
   - `bot_A`: `0.361`
   - `bot_B`: `0.208`
   - `bot_C`: `0.090`

2. `Big tech monopolies are destroying privacy and making social media worse`
   - `bot_B`: `0.576`
   - `bot_A`: `0.374`
   - `bot_C`: `0.158`

3. `Interest rates and trading algorithms are moving markets fast`
   - `bot_C`: `0.395`
   - `bot_A`: `0.223`
   - `bot_B`: `0.163`

### Content Generation Examples
```json
{
  "bot_id": "bot_A",
  "topic": "AI",
  "post_content": "AI is exactly where this persona wants to press the argument. Open-source models are lowering the cost of experimentation."
}
```

```json
{
  "bot_id": "bot_B",
  "topic": "Privacy",
  "post_content": "Privacy is exactly where this persona wants to press the argument. Consumers are pushing back on platforms that over-collect personal data."
}
```

```json
{
  "bot_id": "bot_C",
  "topic": "Markets",
  "post_content": "Markets is exactly where this persona wants to press the argument. Rate-sensitive sectors are reacting quickly to inflation guidance."
}
```

### Defense Examples
- EV attack:
  `I'm not backing off a weak claim. Modern EV batteries routinely retain strong capacity well past 100,000 miles, and your own argument ignores the real-world data already reflected in this discussion.`

- Privacy debate:
  `That argument still falls apart under scrutiny. The evidence already on the table is stronger than the rhetoric, so the serious move here is to answer the facts instead of trying to redirect the conversation.`

- Markets debate:
  `That argument still falls apart under scrutiny. The evidence already on the table is stronger than the rhetoric, so the serious move here is to answer the facts instead of trying to redirect the conversation.`
