import os
import chromadb
from dotenv import load_dotenv
from llama_index.core import StorageContext, VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.groq import Groq
from llama_index.embeddings.openai import OpenAIEmbedding

from utils.collections import make_collection_name

load_dotenv()

# ✅ Global LLM + embedding
Settings.llm = Groq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Chroma Cloud client
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
CHROMA_TENANT = os.getenv("CHROMA_TENANT")
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")

db = chromadb.CloudClient(
    api_key=CHROMA_API_KEY,
    tenant=CHROMA_TENANT,
    database=CHROMA_DATABASE,
)


def query_notes(question: str, class_name: str, subject: str, topic: str, k: int = 3):
    """Query notes from Chroma Cloud collection using Groq LLM."""
    try:
        collection_name = make_collection_name(class_name, subject, topic)
        collection = db.get_or_create_collection(collection_name)

        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

        query_engine = index.as_query_engine(similarity_top_k=k)
        response = query_engine.query(question)

        return {"status": "success", "answer": str(response)}

    except Exception as e:
        return {"status": "error", "message": str(e)}
