# COSMOS ARCHIVE — ArXiv Semantic Search Engine

A local RAG (Retrieval-Augmented Generation) vector search engine that lets you search 50,000+ ArXiv physics papers using natural language — no API keys, no internet required at query time.

---

## Demo

> Query: *"What are the latest findings from gravitational wave detections?"*

Returns the most semantically similar papers ranked by cosine similarity, with abstracts and ArXiv links.

---

## How It Works

```
Your Query (text)
      ↓
Embed with all-MiniLM-L6-v2  (runs locally via ONNX)
      ↓
384-dimensional vector
      ↓
ChromaDB cosine similarity search
      ↓
Top N matching papers ranked by score
```

The model understands meaning, not just keywords. "black hole merger" and "gravitational wave collision" return similar results because they are semantically close in vector space.

---

## Tech Stack

| Component | Library |
|---|---|
| Embeddings | `sentence-transformers` / ChromaDB ONNX `all-MiniLM-L6-v2` |
| Vector Database | `chromadb` (local persistent storage) |
| Data Processing | `pandas` |
| Web UI | `streamlit` |

---

## Project Structure

```
arxiv-vector-engine/
├── ui.py              # Streamlit web app (main entry point)
├── main.py            # CLI version
├── app.py             # Environment sanity check
├── requirements.txt   # Dependencies
├── src/
│   ├── model.py       # PhysicsEmbedder — text → vectors
│   └── database.py    # VectorVault — ChromaDB wrapper
└── data/
    └── arxiv_data.csv # Dataset (not included — see below)
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Adnan082/RAG.git
cd RAG
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r arxiv-vector-engine/requirements.txt
```

### 4. Add the dataset

Place `arxiv_data.csv` inside `arxiv-vector-engine/data/`.

The CSV must have these columns:

| Column | Description |
|---|---|
| `titles` | Paper title |
| `summaries` | Abstract text |
| `terms` | ArXiv category tags e.g. `['cs.LG', 'cs.CV']` |

> Dataset source: [ArXiv Dataset on Kaggle](https://www.kaggle.com/datasets/Cornell-University/arxiv)

---

## Run

### Web UI (recommended)

```bash
streamlit run arxiv-vector-engine/ui.py
```

Opens at `http://localhost:8501`

### CLI

```bash
python arxiv-vector-engine/main.py
```

---

## First Run

On first launch, the engine indexes all papers from the CSV into ChromaDB (stored in `physics_db/`). This takes a few minutes depending on dataset size. Subsequent runs skip indexing and load instantly.

---

## Features

- Natural language semantic search
- Dark space-themed UI ("COSMOS ARCHIVE")
- Trending topic quick-search buttons
- Adjustable result count (3–20)
- Minimum similarity score filter
- Per-result abstract preview
- Direct ArXiv search links
- Color-coded similarity badges (green / yellow / red)

---

## License

MIT
