# COSMOS ARCHIVE — ArXiv Semantic Search Engine

A fully local RAG (Retrieval-Augmented Generation) pipeline for semantic search over 50,000+ ArXiv physics papers. No API keys. No internet required at query time. Everything runs on your machine.

---

## Screenshot

<!-- Add screenshot: save your Streamlit screenshot as screenshots/demo.png -->
> Run the app, take a screenshot, save it to `screenshots/demo.png` and it will appear here.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                        INDEXING (once)                       │
│                                                              │
│  arxiv_data.csv  ──►  title + abstract  ──►  Embedder       │
│                                               │              │
│                                               ▼              │
│                                         384-dim vector       │
│                                               │              │
│                                               ▼              │
│                                     ChromaDB  (physics_db/)  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       SEARCH (every query)                   │
│                                                              │
│  "black hole merger"  ──►  Embedder  ──►  384-dim vector    │
│                                               │              │
│                                               ▼              │
│                              Cosine Similarity Search        │
│                              (ChromaDB ANN lookup)           │
│                                               │              │
│                                               ▼              │
│                              Top N papers ranked by score    │
└─────────────────────────────────────────────────────────────┘
```

The model understands **meaning**, not keywords.
- `"black hole merger"` and `"gravitational wave collision"` → close in vector space → similar results
- `"black hole merger"` and `"plant biology"` → far apart → no overlap

---

## Key Numbers

| Metric | Value |
|---|---|
| Papers indexed | 50,000+ |
| Vector dimensions | **384** |
| Embedding model | `all-MiniLM-L6-v2` (ONNX, runs locally) |
| Indexing batch size | 512 papers per batch |
| Vector DB | ChromaDB (persistent local storage) |
| Similarity metric | Cosine similarity |
| Score range | 0.0 (no match) → 1.0 (perfect match) |
| Score: High match | ≥ 0.75 (green badge) |
| Score: Medium match | ≥ 0.50 (yellow badge) |
| Score: Low match | < 0.50 (red badge) |

---

## Tech Stack

| Component | Tool |
|---|---|
| Embeddings | `sentence-transformers` — `all-MiniLM-L6-v2` via ChromaDB ONNX runtime |
| Vector Database | `chromadb` — local persistent ANN storage |
| Data processing | `pandas` |
| Web UI | `streamlit` |
| Language | Python 3.10+ |

---

## Project Structure

```
RAG/
├── README.md
├── .gitignore
├── screenshots/
│   └── demo.png                  # UI screenshot
└── arxiv-vector-engine/
    ├── ui.py                     # Streamlit web app  ← main entry point
    ├── main.py                   # CLI version
    ├── app.py                    # Environment sanity check
    ├── requirements.txt          # Dependencies
    ├── src/
    │   ├── model.py              # PhysicsEmbedder — text → 384-dim vectors
    │   └── database.py           # VectorVault — ChromaDB read/write wrapper
    └── data/
        └── arxiv_data.csv        # Dataset (not in repo — see below)
```

---

## Dataset

The CSV must be placed at `arxiv-vector-engine/data/arxiv_data.csv` and have these columns:

| Column | Description | Example |
|---|---|---|
| `titles` | Paper title | `"Observation of Gravitational Waves from..."` |
| `summaries` | Abstract text | `"We report the observation of..."` |
| `terms` | ArXiv category tags | `"['gr-qc', 'astro-ph.HE']"` |

Source: [ArXiv Dataset on Kaggle](https://www.kaggle.com/datasets/Cornell-University/arxiv)

---

## Setup

### 1. Clone

```bash
git clone https://github.com/Adnan082/RAG.git
cd RAG
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Mac / Linux:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r arxiv-vector-engine/requirements.txt
```

### 4. Add the dataset

Place `arxiv_data.csv` in `arxiv-vector-engine/data/`.

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

## First Launch

On first run, the engine indexes all 50,000+ papers into ChromaDB:

```
Loading data from arxiv_data.csv ...
Total papers to index: 50000
[512/50000]  Embedding batch ...
[1024/50000] Embedding batch ...
...
[OK] All 50000 papers indexed.
```

This takes **3–10 minutes** depending on your machine. The database is saved to `physics_db/` and subsequent launches are instant.

---

## UI Features

| Feature | Detail |
|---|---|
| Natural language search | Understands meaning, not just keywords |
| Trending topics | One-click quick searches for popular physics topics |
| Results count | Adjustable 3 – 20 results via sidebar slider |
| Score filter | Filter out results below a minimum similarity score |
| Abstract preview | Expandable abstract for each result |
| ArXiv link | Direct search link to the paper on arxiv.org |
| Score badges | Color-coded: green ≥75%, yellow ≥50%, red <50% |
| Theme | Dark space-themed "COSMOS ARCHIVE" design |

---

## License

Apache 2.0
