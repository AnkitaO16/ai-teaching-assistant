import os
import chromadb
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from utils.collections import make_collection_name  # ✅ helper for consistent naming

load_dotenv()

# ✅ Global embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# ✅ Chroma Cloud client
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
CHROMA_TENANT = os.getenv("CHROMA_TENANT")
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")

db = chromadb.CloudClient(
    api_key=CHROMA_API_KEY,
    tenant=CHROMA_TENANT,
    database=CHROMA_DATABASE,
)


def ingest_text_file(file_path: str, class_name: str, subject: str, topic: str) -> dict:
    """Ingest a teacher's text file into a Chroma Cloud collection."""
    try:
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        collection_name = make_collection_name(class_name, subject, topic)

        collection = db.get_or_create_collection(collection_name)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        VectorStoreIndex.from_documents(documents, storage_context=storage_context)

        return {"status": "success", "collection": collection_name, "docs": len(documents)}

    except Exception as e:
        return {"status": "error", "message": str(e)}
