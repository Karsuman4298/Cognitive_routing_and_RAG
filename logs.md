Phase 1:
- input post: OpenAI released a new AI model that can replace developers
- matched bots + scores:
- bot_A: 0.361

Phase 2:
{
  "bot_id": "bot_A",
  "topic": "AI",
  "post_content": "AI is exactly where this persona wants to press the argument. Open-source models are lowering the cost of experimentation."
}

Phase 3:
- parent post: Electric Vehicles are a complete scam. Batteries degrade in 3 years.
- conversation context: Bot: That is statistically false. Modern EV batteries retain 90% capacity after 100,000 miles.
- final defense reply: I'm not backing off a weak claim. Modern EV batteries routinely retain strong capacity well past 100,000 miles, and your own argument ignores the real-world data already reflected in this discussion.

Additional Test Cases:
- Routing Case 1: OpenAI released a new AI model that can replace developers
- Output: [('bot_A', 0.3610004782676697)]

- Routing Case 2: Big tech monopolies are destroying privacy and making social media worse
- Output: [('bot_B', 0.576358437538147), ('bot_A', 0.3741467297077179)]

- Routing Case 3: Interest rates and trading algorithms are moving markets fast
- Output: [('bot_C', 0.3951506018638611)]

- Content Case bot_A:
{
  "bot_id": "bot_A",
  "topic": "AI",
  "post_content": "AI is exactly where this persona wants to press the argument. Open-source models are lowering the cost of experimentation."
}

- Content Case bot_B:
{
  "bot_id": "bot_B",
  "topic": "Privacy",
  "post_content": "Privacy is exactly where this persona wants to press the argument. Consumers are pushing back on platforms that over-collect personal data."
}

- Content Case bot_C:
{
  "bot_id": "bot_C",
  "topic": "Markets",
  "post_content": "Markets is exactly where this persona wants to press the argument. Rate-sensitive sectors are reacting quickly to inflation guidance."
}

- Defense Case EV attack:
I'm not backing off a weak claim. Modern EV batteries routinely retain strong capacity well past 100,000 miles, and your own argument ignores the real-world data already reflected in this discussion.

- Defense Case Privacy debate:
That argument still falls apart under scrutiny. The evidence already on the table is stronger than the rhetoric, so the serious move here is to answer the facts instead of trying to redirect the conversation.

- Defense Case Markets debate:
That argument still falls apart under scrutiny. The evidence already on the table is stronger than the rhetoric, so the serious move here is to answer the facts instead of trying to redirect the conversation.
