# from llama_index.core import Settings
# from llama_index.embeddings.openai import OpenAIEmbedding
# import chromadb
# from llama_index.vector_stores.chroma import ChromaVectorStore
# from llama_index.core import VectorStoreIndex, StorageContext
# from dotenv import load_dotenv
# import os
#
# # Load environment variables
# load_dotenv()
# groq_key = os.getenv("GROQ_API_KEY")
# print("DEBUG >>> GROQ_API_KEY =", groq_key)
#
# # ================================
# # 🔹 LlamaIndex Groq Integration
# # ================================
# from llama_index.llms.groq import Groq
#
# if groq_key:
#     print("✅ Using Groq with API key in LlamaIndex")
#     Settings.llm = Groq(
#         model="llama-3.1-8b-instant",  # lightweight Groq model
#         api_key=groq_key
#     )
# else:
#     raise RuntimeError("❌ GROQ_API_KEY not found. Please set it in your environment.")
#
# # ✅ Use lightweight embeddings (instead of HuggingFace/torch)
# Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
#
# # ✅ Chroma client
# chroma_client = chromadb.PersistentClient(path="chroma_db")
#
#
# def query_notes(question: str, class_name: str, subject: str, topic: str, k: int = 3):
#     try:
#         collection_name = f"{class_name}_{subject}_{topic}".lower().replace(" ", "_")
#         try:
#             collection = chroma_client.get_collection(name=collection_name)
#         except Exception:
#             return {"error": f"❌ Collection '{collection_name}' not found. Did you ingest notes first?"}
#
#         vector_store = ChromaVectorStore(chroma_collection=collection)
#         storage_context = StorageContext.from_defaults(vector_store=vector_store)
#         index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
#
#         query_engine = index.as_query_engine(llm=Settings.llm, similarity_top_k=k)
#         response = query_engine.query(question)
#
#         return {
#             "answer": str(response),
#             "sources": [str(n) for n in getattr(response, "source_nodes", [])]
#         }
#
#     except Exception as e:
#         return {"error": f"Query failed: {e}"}
import os
import chromadb
from dotenv import load_dotenv
from llama_index.core import Settings, StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.groq import Groq
from llama_index.embeddings.openai import OpenAIEmbedding  # ✅ lightweight embeddings

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise RuntimeError("❌ GROQ_API_KEY not found!")

# ✅ Set Groq LLM
Settings.llm = Groq(model="llama-3.1-8b-instant", api_key=groq_key)

# ✅ Use hosted embeddings (no torch, no huggingface, works with Groq key)
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
    api_key=groq_key
)

# ✅ Chroma client
db = chromadb.PersistentClient(path="./chroma_db")


def query_notes(question: str, class_name: str, subject: str, topic: str):
    """Query notes from Chroma collection using Groq LLM"""
    try:
        collection_name = f"{class_name}_{subject}_{topic}".replace(" ", "_").lower()

        # Load collection
        collection = db.get_or_create_collection(collection_name)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Load or create index
        index = VectorStoreIndex([], storage_context=storage_context)

        # Query with Groq LLM
        query_engine = index.as_query_engine()
        response = query_engine.query(question)

        print(f"❓ Question: {question}")
        print(f"💡 Answer: {response}")

        return {"status": "success", "answer": str(response)}

    except Exception as e:
        return {"status": "error", "message": str(e)}
