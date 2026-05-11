import chromadb
from llama_index.core import Document, VectorStoreIndex
from ai.rag.retriever import Retriever


class Indexer:

    def __init__(self, retriever: Retriever):
        self._retriever = retriever
        

    def index_documents(self, pages: list[dict]) -> VectorStoreIndex:
        """
        pages - список словарей:
        [{'id': 'abc', 'title': 'Title', 'content': 'Text'}]
        """

        documents = [
            Document(
                text=p['content'],
                metadata={'notion_id': p['id'], 'title': p['title']},
                id_=p['id']
            )
            for p in pages
        ]
        for doc in documents:
            self._retriever._index.insert(doc)
        