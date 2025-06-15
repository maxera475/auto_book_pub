# vector_store.py
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import datetime

# Initialize ChromaDB client and collection
chroma_client = chromadb.Client()
embedding_func = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = chroma_client.get_or_create_collection(
    name="chapter_versions",
    embedding_function=embedding_func
)

def add_version(chapter_name, text, metadata):
    version_id = metadata.get("version_id", datetime.datetime.now().isoformat())
    doc_id = f"{chapter_name}_{version_id}"
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[doc_id]
    )

def search_versions(query_text, top_k=3):
    results = collection.query(query_texts=[query_text], n_results=top_k)
    return {
        "matches": [
            {
                "text": doc,
                "score": score,
                "metadata": meta
            }
            for doc, score, meta in zip(results["documents"][0], results["distances"][0], results["metadatas"][0])
        ]
    }
