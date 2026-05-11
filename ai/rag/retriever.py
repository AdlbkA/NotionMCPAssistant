import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from config.settings import settings
from ai.rag.embeddings import get_embed_model

class Retriever:

    def __init__(self):
        self._embed_model = get_embed_model()
        client = chromadb.PersistentClient(path=settings.chroma_path)
        collection = client.get_or_create_collection('notion_docs')
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self._index = VectorStoreIndex.from_vector_store(
            vector_store,
            storage_context=storage_context,
            embed_model=self._embed_model
        )


    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        retriever = self._index.as_retriever(similarity_top_k=top_k)
        nodes = retriever.retrieve(query)

        return [
            {
                'text': n.text,
                'score': n.score,
                'title': n.metadata.get('title', ''),
                'notion_id': n.metadata.get('notion_id', '')
            }
            for n in nodes
        ]

