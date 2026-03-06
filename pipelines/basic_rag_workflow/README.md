# Basic RAG Workflow

A Retrieval-Augmented Generation pipeline that loads documents (PDF or web pages), chunks them, creates embeddings, stores them in a FAISS vector database, and answers queries using retrieved context and a Groq LLM.

> **Environment setup:** See the [root README](../../README.md) for Python version requirements, venv creation, and dependency installation.

---

## How It Works

1. Documents (PDFs or URLs) are loaded and split into pages
2. Pages are chunked using recursive character splitting
3. Chunks are embedded using HuggingFace sentence transformers
4. Embeddings are stored in a FAISS vector database at `storage/faiss_basic`
5. At query time, the top 5 most relevant chunks are retrieved
6. A Groq LLM generates a response using the retrieved context

---

## Pre-loaded Documents

The default database (`storage/faiss_basic`) contains:

| Document | Content |
|----------|---------|
| IBM Agentic AI Article | Concepts, definitions, and use cases of agentic AI |
| NASA ISS Page | International Space Station information and missions |
| Attention Is All You Need | Transformer architecture, multi-head attention, positional encoding |

---

## Setting Up the Vector Database

Build the database before running:

```bash
python -m pipelines.basic_rag_workflow.src.setup_multi_docs
```

For a single document:

```bash
python -m pipelines.basic_rag_workflow.src.setup_vector_db
```

---

## Running the Pipeline

```bash
source .venv/bin/activate
cd /path/to/agentic_ai_portfolio
python -m pipelines.basic_rag_workflow.src.rag_pipeline
```

---

## Sample Questions

```
What is agentic AI?
How does agentic AI differ from traditional AI?
Tell me about the International Space Station
What is the attention mechanism in transformers?
Explain multi-head attention
What is scaled dot-product attention?
```

---

## Pipeline Structure

```
pipelines/basic_rag_workflow/
├── src/
│   ├── rag_pipeline.py           # Main pipeline — entry point
│   ├── setup_vector_db.py        # Build FAISS index from single document
│   └── setup_multi_docs.py       # Build FAISS index from multiple documents
└── storage/
    └── faiss_basic/              # Pre-built vector database
        ├── index.faiss
        └── index.pkl
```

**Shared utilities used:**

```
shared/utils/llm_utils.py         # LLM initialization, DEFAULT_MODEL
shared/utils/loader_utils.py      # PDF and web document loading
shared/utils/chunking_utils.py    # Text splitting
shared/utils/vector_utils.py      # FAISS vector store
shared/utils/retrieval_utils.py   # Chunk retrieval and formatting
```

---

## Common Issues

**FAISS index not found**
Run `setup_multi_docs.py` to build the index before querying.

**`ModuleNotFoundError: No module named 'shared'`**
Run `pip install -e .` from the project root with the venv activated.

**Slow first run**
HuggingFace downloads the embedding model on first use. Subsequent runs use the cached model.