## 📂 Project Layout

[//]: # ()
[//]: # (ai-teaching-assistant/)

[//]: # (│)

[//]: # (├─ app.py                     # FastAPI entry &#40;routes -> services&#41;)

[//]: # (│)

[//]: # (├─ services/)

[//]: # (│   ├─ ingest_service.py       # ingestion logic &#40;chunks → Chroma&#41;)

[//]: # (│   └─ query_service.py        # retrieval + Ollama call)

[//]: # (│)

[//]: # (├─ scripts/)

[//]: # (│   ├─ ingest_teacher_file.py  # CLI ingest helper)

[//]: # (│   └─ query_chroma.py         # CLI query tester)

[//]: # (│)

[//]: # (├─ data/                      # teacher .txt notes &#40;uploaded or sample&#41;)

[//]: # (│   └─ thermodynamics.txt)

[//]: # (│)

[//]: # (├─ chroma_db/                 # auto-created ChromaDB storage)

[//]: # (│)

[//]: # (├─ templates/                 # Jinja2 HTML templates)

[//]: # (│   ├─ base.html)

[//]: # (│   ├─ teacher.html)

[//]: # (│   └─ student.html)

[//]: # (│)

[//]: # (├─ requirements.txt)

[//]: # (└─ venv/                      # local Python env &#40;ignored in git&#41;)


ai-teaching-assistant/
│
├─ backend/                      # all FastAPI code
│   ├─ app.py                     # FastAPI entry (routes -> services)
│   ├─ services/
│   │   ├─ ingest_service.py
│   │   └─ query_service.py
│   ├─ scripts/
│   │   ├─ ingest_teacher_file.py
│   │   └─ query_chroma.py
│   ├─ data/
│   │   └─ thermodynamics.txt
│   ├─ chroma_db/                # persistent ChromaDB
│   ├─ requirements.txt
│   └─ venv/
│
├─ frontend/                     # all React + Vite code
│   ├─ index.html
│   ├─ vite.config.ts
│   ├─ tsconfig.json
│   ├─ package.json
│   ├─ public/
│   └─ src/
│       ├─ App.tsx
│       ├─ Layout.tsx
│       ├─ TeacherUpload.tsx
│       ├─ StudentChat.tsx
│       └─ styles.css
│
└─ README.md


## Details 

1. **Separated concerns**

   * `services/` handles ingestion + querying (pure Python).
   * `scripts/` are CLI utilities (call services).
   * `app.py` only wires HTTP routes.

2. **Consistent naming**

   * `class_name_subject_topic` → Chroma collection format.
   * Predictable file-based chunk IDs.

3. **Better developer UX**

   * `/records` endpoint → peek stored docs quickly.
   * Student/Teacher templates wired for testing without frontend code.

4. **Git hygiene**

   * `venv/`, `chroma_db/`, `__pycache__/` ignored via `.gitignore`.


## 🧪 Postman Setup

Since FastAPI endpoints expect **form-data**, use these:

1. **POST /ingest** → Upload teacher notes

   * `class_name: Class10`
   * `subject: Physics`
   * `topic: Thermodynamics`
   * `file: <notes.txt>`

2. **GET /records** → Verify stored chunks

   * Params: `class_name=Class10&subject=Physics&topic=Thermodynamics`

3. **POST /ask** → Ask a student question

   * `class_name: Class10`
   * `subject: Physics`
   * `topic: Thermodynamics`
   * `question: What is the first law of thermodynamics?`
   * `k: 3`


## Run Setups
* git checkout -b feature/ai-ingest
* git add .
* git commit -m "Added ingest service"
* git push origin feature/ai-ingest
.\venv\Scripts\activate

