import time
from typing import Optional, Tuple
from langchain_community.chat_models import ChatTongyi
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from src.settings import settings
from src.utils.logger import logger


QWEN_MODELS = {"qwen-max", "qwen-plus", "qwen-turbo", "qwen-long", "qwen-max-longcontext"}


class LLMClient:
    def _get_llm(self, model_name: str) -> BaseChatModel:
        if model_name in QWEN_MODELS:
            return ChatTongyi(
                model=model_name,
                temperature=0.7,
                top_p=0.8,
                api_key=settings.DASHSCOPE_API_KEY,
                streaming=True,
            )
        else:
            return ChatOpenAI(
                model=model_name,
                temperature=0.7,
                top_p=0.8,
                api_key=settings.DEEPSEEK_API_KEY,
                base_url=settings.DEEPSEEK_BASE_URL,
                streaming=True,
            )

    def generate_response_with_metrics(
        self, prompt: str, model_name: Optional[str] = None
    ) -> Tuple[str, float, float]:
        model = model_name or settings.LLM_MODEL
        llm = self._get_llm(model)

        start_time = time.time()
        first_token_time = None
        content = ""

        try:
            messages = [
                SystemMessage(content="You are a helpful RAG assistant."),
                HumanMessage(content=prompt),
            ]
            for chunk in llm.stream(messages):
                if first_token_time is None:
                    first_token_time = time.time()
                content += chunk.content

            end_time = time.time()
            first_token_latency = (
                (first_token_time - start_time) if first_token_time else 0.0
            )
            total_latency = end_time - start_time
            return content, first_token_latency, total_latency
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return f"Error generating response: {str(e)}", 0.0, 0.0

    def generate_response(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> str:
        model = model_name or settings.LLM_MODEL
        llm = self._get_llm(model)

        if system_prompt:
            prompt = f"""{system_prompt}

上下文：
{context}

问题：{query}

要求：
1. 基于上下文回答
2. 输出符合指令要求
"""
            return self.generate_custom_response(prompt, model_name=model)

        prompt = f"""基于以下上下文信息，回答问题。

上下文：
{context}

问题：{query}

要求：
1. 基于上下文回答，不添加外部知识
2. 如上下文无相关信息，明确说明"根据提供的信息无法回答"
3. 引用相关段落编号
4. 保持回答准确、简洁

回答："""
        return self.generate_custom_response(prompt, model_name=model)

    def generate_general_response(
        self, query: str, context: str = "", model_name: Optional[str] = None
    ) -> str:
        model = model_name or settings.LLM_MODEL

        prompt = f"""You are a helpful assistant.

{context}

User Question: {query}

Answer:"""
        return self.generate_custom_response(prompt, model_name=model)

    def generate_custom_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> str:
        model = model_name or settings.LLM_MODEL
        llm = self._get_llm(model)

        try:
            sys_msg = (
                system_prompt if system_prompt else "You are a helpful RAG assistant."
            )
            messages = [
                SystemMessage(content=sys_msg),
                HumanMessage(content=prompt),
            ]
            response = llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return f"Error generating response: {str(e)}"
