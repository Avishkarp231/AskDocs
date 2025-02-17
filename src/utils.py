CHROMA_PATH = "chroma"
DATA_PATH = "data"

PROMPT_TEMPLATE = """
You are a helpful assistant. Maintain the context of the conversation and answer the user's question based only on the following context:

{context}

---

Conversation so far:
{history}

User's Question: {question}
"""