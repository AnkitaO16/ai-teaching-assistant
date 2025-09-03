# import os
# from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
# from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
#
# from services.ingest_service import ingest_text_file
# from services.query_service import query_notes as answer_question
# import chromadb
#
# app = FastAPI()
#
# # ✅ Enable CORS for frontend (if served separately during dev)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # tighten later
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# os.makedirs("data", exist_ok=True)
# os.makedirs("chroma_db", exist_ok=True)
#
# chroma_client = chromadb.PersistentClient(path="chroma_db")
#
# # ✅ Serve React static build
# frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
# app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
#
# @app.get("/")
# async def serve_index():
#     return FileResponse(os.path.join(frontend_dist, "index.html"))
#
# # -------------------
# # API ROUTES
# # -------------------
#
# @app.post("/ingest")
# async def ingest(
#     class_name: str = Form(...),
#     subject: str = Form(...),
#     topic: str = Form(...),
#     file: UploadFile = File(...)
# ):
#     if not file.filename.lower().endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Only .pdf allowed")
#
#     save_path = os.path.join("data", file.filename)
#     with open(save_path, "wb") as f:
#         f.write(await file.read())
#
#     res = ingest_text_file(save_path, class_name, subject, topic)
#     return JSONResponse(res)
#
#
# @app.get("/records")
# async def get_records(class_name: str, subject: str, topic: str):
#     try:
#         collection_name = f"{class_name}_{subject}_{topic}".lower().replace(" ", "_")
#         collection = chroma_client.get_collection(name=collection_name)
#         results = collection.peek()
#
#         return {
#             "status": "success",
#             "collection": collection_name,
#             "count": len(results.get("ids", [])),
#             "ids": results.get("ids", []),
#             "documents": results.get("documents", []),
#             "metadatas": results.get("metadatas", []),
#         }
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=f"Collection not found: {e}")
#
#
# @app.post("/ask")
# async def ask(
#     class_name: str = Form(...),
#     subject: str = Form(...),
#     topic: str = Form(...),
#     question: str = Form(...),
#     k: int = Form(3)
# ):
#     try:
#         res = answer_question(question, class_name, subject, topic, k=int(k))
#         if "error" in res:
#             raise HTTPException(status_code=400, detail=res["error"])
#         return JSONResponse(content=res)
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from services.ingest_service import ingest_text_file
from services.query_service import query_notes as answer_question
import chromadb

app = FastAPI()

# ✅ Enable CORS for frontend (during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # you can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Ensure data dirs exist
os.makedirs("data", exist_ok=True)
os.makedirs("chroma_db", exist_ok=True)

# ✅ Init ChromaDB client
chroma_client = chromadb.PersistentClient(path="chroma_db")

# ✅ Serve React frontend build
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(frontend_dist, "assets")),
    name="assets"
)

@app.get("/")
async def serve_index():
    """Serve React index.html"""
    return FileResponse(os.path.join(frontend_dist, "index.html"))

# -------------------
# API ROUTES
# -------------------

@app.post("/ingest")
async def ingest(
    class_name: str = Form(...),
    subject: str = Form(...),
    topic: str = Form(...),
    file: UploadFile = File(...)
):
    """Upload and ingest a PDF file into ChromaDB"""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf files allowed")

    save_path = os.path.join("data", file.filename)
    with open(save_path, "wb") as f:
        f.write(await file.read())

    res = ingest_text_file(save_path, class_name, subject, topic)
    return JSONResponse(res)


@app.get("/records")
async def get_records(class_name: str, subject: str, topic: str):
    """Peek into an existing collection"""
    try:
        collection_name = f"{class_name}_{subject}_{topic}".replace(" ", "_").lower()
        collection = chroma_client.get_collection(name=collection_name)
        results = collection.peek()

        return {
            "status": "success",
            "collection": collection_name,
            "count": len(results.get("ids", [])),
            "ids": results.get("ids", []),
            "documents": results.get("documents", []),
            "metadatas": results.get("metadatas", []),
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Collection not found: {e}")


@app.post("/ask")
async def ask(
    class_name: str = Form(...),
    subject: str = Form(...),
    topic: str = Form(...),
    question: str = Form(...),
    k: int = Form(3)
):
    """Ask a question over stored notes"""
    try:
        res = answer_question(question, class_name, subject, topic, k=int(k))
        if "error" in res:
            raise HTTPException(status_code=400, detail=res["error"])
        return JSONResponse(content=res)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
