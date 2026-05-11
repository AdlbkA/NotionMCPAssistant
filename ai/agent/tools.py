NOTION_TOOLS = [
    {
        "name": "create_notion_page",
        "description": "Создать новую страницу в Notion. Используй когда пользователь просит создать заметку, страницу или запись.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Заголовок страницы"
                },
                "content": {
                    "type": "string",
                    "description": "Содержимое страницы"
                },
                "parent_id": {
                    "type": "string",
                    "description": "ID родительской страницы в Notion"
                }
            },
            "required": ["title", "content", "parent_id"]
        }
    },
    {
        "name": "search_notion",
        "description": "Поиск по Notion если RAG-контекст недостаточен или нужна актуальная информация.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Поисковый запрос"
                }
            },
            "required": ["query"]
        }
    }
]