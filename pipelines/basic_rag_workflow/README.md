# Basic RAG Workflow

A Retrieval-Augmented Generation pipeline that loads documents (web pages or PDFs), chunks them, creates embeddings, stores them in a FAISS vector database, and answers queries using retrieved context and a Groq LLM.

> **Environment setup:** See the [root README](../../README.md) for Python version requirements, venv creation, and dependency installation.

---

## How It Works

1. Web pages are loaded and split into pages
2. Pages are chunked using recursive character splitting
3. Chunks are embedded using HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
4. Embeddings are stored in a FAISS vector database at `storage/faiss_basic`
5. At query time, the top 5 most relevant chunks are retrieved
6. A Groq LLM generates a response using the retrieved context

---

## Knowledge Base

The vector database (`storage/faiss_basic`) contains **1,272 chunks** sourced from:

| Source | Content |
|--------|---------|
| Wikipedia — NFL | NFL history, structure, and overview |
| Wikipedia — 2024 NFL Season | Team records, standings, and season summary |
| Wikipedia — 2024-25 NFL Playoffs | Playoff bracket, results, and game summaries |
| Wikipedia — Super Bowl LIX | Eagles vs. Chiefs, final score, MVP, and highlights |

---

## Rebuilding the Vector Database

```bash
python -m pipelines.basic_rag_workflow.src.setup_vector_db
```

---

## Running the Pipeline

```bash
source .venv/bin/activate
python -m pipelines.basic_rag_workflow.src.rag_pipeline
```

---

## Sample Questions

```
Who won Super Bowl LIX?
What was the final score of Super Bowl LIX?
Who was the Super Bowl LIX MVP?
How did the Eagles perform in the 2024-25 playoffs?
What is the NFL's conference structure?
Which teams made the playoffs in the 2024 season?
```

---

## Pipeline Structure

```
pipelines/basic_rag_workflow/
├── src/
│   ├── config.py                 # Source URLs and configuration
│   ├── rag_pipeline.py           # Main pipeline — entry point
│   └── setup_vector_db.py        # Build FAISS index from configured URLs
└── storage/
    └── faiss_basic/              # Pre-built vector database
        ├── index.faiss
        └── index.pkl
```

**Shared utilities used:**
```
shared/utils/llm_utils.py         # LLM initialization
shared/utils/loader_utils.py      # Web document loading
shared/utils/chunking_utils.py    # Text splitting
shared/utils/vector_utils.py      # FAISS vector store
shared/utils/retrieval_utils.py   # Chunk retrieval and formatting
```

---

## Common Issues

**FAISS index not found**
Run `setup_vector_db.py` to build the index before querying.

**`ModuleNotFoundError: No module named 'shared'`**
Run `pip install -e .` from the project root with the venv activated.

**Slow first run**
HuggingFace downloads the embedding model on first use. Subsequent runs use the cached model.