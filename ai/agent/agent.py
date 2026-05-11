import anthropic
from config.settings import settings
from ai.rag.retriever import Retriever
from ai.agent.prompts import SYSTEM_PROMPT
from ai.mcp_conf.notion_client import NotionMCPClient
from ai.agent.tools import NOTION_TOOLS

class Agent:
    def __init__(self, retriever: Retriever, notion: NotionMCPClient):
        self._retriever = retriever
        self._notion = notion
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    async def _execute_call(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "create_notion_page":
            return await self._notion.create_page(
                title=tool_input["title"],
                content=tool_input["content"],
                parent_id=tool_input["parent_id"]
            )
        elif tool_name == "search_notion":
            return await self._notion.search(query=tool_input["query"])
        return "Инструмент не найден"

    async def chat(self, user_message: str) -> str:
        chunks = self._retriever.retrieve(user_message, top_k=50)
        rag_context = '\n\n'.join(
            f"[{c['title']}]\n{c['text']}" for c in chunks
        )
    
        augmented_message = f"""Контекст из Notion (RAG):
    ---
    {rag_context}
    ---
    
    Вопрос пользователя: {user_message}
    """
        
        messages=[{'role': 'user', 'content': augmented_message}]

        while True:
            response = self._client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=5000,
                system=SYSTEM_PROMPT,
                tools=NOTION_TOOLS,
                messages=messages
            )

            if response.stop_reason == "end_turn":
                return response.content[0].text
            
            if response.stop_reason == "tool_use":
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = await self._execute_call(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        })
                
                messages.append({
                    "role": "user",
                    "content": tool_results
                })