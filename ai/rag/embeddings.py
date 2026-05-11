from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def get_embed_model():
    return HuggingFaceEmbedding(
        model_name="paraphrase-multilingual-MiniLM-L12-v2"
    )