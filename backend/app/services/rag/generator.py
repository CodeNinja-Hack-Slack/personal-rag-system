from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings


SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer the user's question based on the provided context. "
    "If the context does not contain enough information, say so honestly. "
    "Always answer in the same language as the user's question."
)


class Generator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            openai_api_key=settings.openai_api_key,
            temperature=0,
        )

    def generate(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        context = "\n\n---\n\n".join(
            doc["document"] for doc in context_docs
        )

        user_message = (
            f"Context:\n{context}\n\n"
            f"Question: {query}"
        )

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ]

        response = self.llm.invoke(messages)
        return response.content


generator = Generator()
