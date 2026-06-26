from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings


SYSTEM_PROMPT = (
    "你是一个有帮助的AI助手。基于提供的知识库上下文回答用户的问题。"
    "如果上下文信息不足，请如实说明。"
    "请用用户提问的语言来回答。"
)


class Generator:
    def __init__(self):
        self.llm = self._create_llm()

    def _create_llm(self):
        provider = settings.llm_provider.lower()

        if provider == "mimo":
            return ChatOpenAI(
                model=settings.mimo_model,
                openai_api_key=settings.mimo_api_key,
                openai_api_base=settings.mimo_base_url,
                temperature=0.7,
            )
        elif provider == "ollama":
            return ChatOpenAI(
                model=settings.ollama_model,
                openai_api_key="ollama",
                openai_api_base=f"{settings.ollama_base_url}/v1",
                temperature=0.7,
            )
        else:
            return ChatOpenAI(
                model=settings.openai_model,
                openai_api_key=settings.openai_api_key,
                openai_api_base=settings.openai_base_url,
                temperature=0.7,
            )

    def generate(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        context = "\n\n---\n\n".join(
            doc["document"] for doc in context_docs
        )

        user_message = (
            f"以下是知识库中的相关内容：\n{context}\n\n"
            f"用户问题：{query}"
        )

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ]

        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"AI 回答生成失败：{str(e)}"


generator = Generator()
