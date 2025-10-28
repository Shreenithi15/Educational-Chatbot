# Simple LLM service wrapper. Replace the `generate_reply` implementation
# with an actual call to OpenAI or another LLM if you have API access.

from typing import List
import asyncio

async def generate_reply(messages: List[dict], user_message: str, topic: str | None = None) -> str:
    """
    messages: list of {role: "user"|"assistant", "content": "..."}
    For now, we return a rule-based reply. Replace this with HTTP call to an LLM.
    """
    # Tiny rule-based fallback:
    # If user asks about a quiz, return helpful instructions
    text = user_message.lower()
    if "explain" in text or "what is" in text:
        return "Here's a short explanation: " + " ".join(user_message.split()[:50])
    if "quiz" in text:
        return "I can generate a small quiz. Send GET /quiz?topic=your_topic to get started."
    # else echo style:
    return f"I heard you say: '{user_message}'. Ask me to explain a topic, request a quiz, or ask a question."

# Example sync wrapper if you need to call from sync code
def generate_reply_sync(*args, **kwargs):
    return asyncio.run(generate_reply(*args, **kwargs))
