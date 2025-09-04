# # import os
# # import chromadb
# # from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
# # from llama_index.vector_stores.chroma import ChromaVectorStore
# # from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# #
# # # ✅ set global embedding model
# # Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
# #
# #
# # def ingest_text_file(file_path: str, class_name: str, subject: str, topic: str) -> dict:
# #     """
# #     Ingest a teacher's text file into Chroma collection
# #     Collection name format: class_subject_topic
# #     """
# #     try:
# #         # load file into LlamaIndex docs
# #         documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
# #
# #         # prepare collection (class + subject + topic)
# #         collection_name = f"{class_name}_{subject}_{topic}".replace(" ", "_").lower()
# #
# #         db = chromadb.PersistentClient(path="./chroma_db")
# #         collection = db.get_or_create_collection(collection_name)
# #
# #         # wrap in LlamaIndex
# #         vector_store = ChromaVectorStore(chroma_collection=collection)
# #         storage_context = StorageContext.from_defaults(vector_store=vector_store)
# #
# #         # build index and insert
# #         index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
# #
# #         return {
# #             "status": "success",
# #             "collection": collection_name,
# #             "docs": len(documents)
# #         }
# #
# #     except Exception as e:
# #         return {"status": "error", "message": str(e)}
# import os
# import chromadb
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
# from llama_index.vector_stores.chroma import ChromaVectorStore
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
#
# from utils.collections import make_collection_name  # ✅ new helper
#
# # ✅ set global embedding model
# Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
#
#
# def ingest_text_file(file_path: str, class_name: str, subject: str, topic: str) -> dict:
#     """
#     Ingest a teacher's text file into Chroma collection.
#     Collection name format is standardized via make_collection_name().
#     """
#     try:
#         # load file into LlamaIndex docs
#         documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
#
#         # ✅ unified collection name
#         collection_name = make_collection_name(class_name, subject, topic)
#
#         db = chromadb.PersistentClient(path="./chroma_db")
#         collection = db.get_or_create_collection(collection_name)
#
#         # wrap in LlamaIndex
#         vector_store = ChromaVectorStore(chroma_collection=collection)
#         storage_context = StorageContext.from_defaults(vector_store=vector_store)
#
#         # build index and insert docs
#         index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
#
#         return {
#             "status": "success",
#             "collection": collection_name,
#             "docs": len(documents)
#         }
#
#     except Exception as e:
#         return {"status": "error", "message": str(e)}
import os
import chromadb
from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding  # ✅ lightweight embeddings
from llama_index.llms.groq import Groq  # ✅ Groq LLM

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise RuntimeError("❌ GROQ_API_KEY not found!")

# ✅ Use Groq for LLM
Settings.llm = Groq(model="llama-3.1-8b-instant", api_key=groq_key)

# ✅ Use hosted embeddings (no torch / huggingface needed)
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
    api_key=groq_key   # 🔑 pass Groq key here
)

# ✅ Persistent Chroma client
db = chromadb.PersistentClient(path="./chroma_db")


def ingest_text_file(file_path: str, class_name: str, subject: str, topic: str):
    """Ingest teacher notes into Chroma collection (Groq only)."""
    try:
        # 1. Load file into docs
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

        # 2. Standardize collection name
        collection_name = f"{class_name}_{subject}_{topic}".replace(" ", "_").lower()

        # 3. Get/create collection
        collection = db.get_or_create_collection(collection_name)

        # 4. Wrap in LlamaIndex VectorStore
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # 5. Build index and insert docs
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

        print(f"✅ Ingested {len(documents)} docs into collection '{collection_name}'")
        return {"status": "success", "collection": collection_name, "docs": len(documents)}

    except Exception as e:
        return {"status": "error", "message": str(e)}
