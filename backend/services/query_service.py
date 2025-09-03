from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
print("DEBUG >>> GROQ_API_KEY =", groq_key)

# ================================
# 🔹 Direct test: Groq official SDK
# ================================
try:
    from groq import Groq as GroqSDK
    client = GroqSDK(api_key=groq_key)
    resp = client.chat.completions.create(
        # ✅ Updated to new model
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Hello from direct Groq SDK"}]
    )
    print("✅ Direct Groq SDK works:", resp.choices[0].message.content)
except Exception as e:
    print("❌ Direct Groq SDK failed:", e)

# ================================
# 🔹 LlamaIndex Groq Integration
# ================================
from llama_index.llms.groq import Groq
from llama_index.llms.ollama import Ollama

if groq_key:
    print("✅ Using Groq with API key in LlamaIndex")
    Settings.llm = Groq(
        # ✅ Updated to new model
        model="llama-3.1-8b-instant",
        api_key=groq_key
    )
else:
    print("⚠️ GROQ_API_KEY not found, falling back to local Ollama")
    Settings.llm = Ollama(
        model="llama3.1:8b",
        request_timeout=60.0,
        base_url="http://127.0.0.1:11434"
    )

# ✅ Configure embeddings (lightweight, stays local)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# ✅ Chroma client
chroma_client = chromadb.PersistentClient(path="chroma_db")


def query_notes(question: str, class_name: str, subject: str, topic: str, k: int = 3):
    try:
        collection_name = f"{class_name}_{subject}_{topic}".lower().replace(" ", "_")
        try:
            collection = chroma_client.get_collection(name=collection_name)
        except Exception:
            return {"error": f"❌ Collection '{collection_name}' not found. Did you ingest notes first?"}

        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

        query_engine = index.as_query_engine(llm=Settings.llm, similarity_top_k=k)
        response = query_engine.query(question)

        return {
            "answer": str(response),
            "sources": [str(n) for n in getattr(response, "source_nodes", [])]
        }

    except Exception as e:
        return {"error": f"Query failed: {e}"}
