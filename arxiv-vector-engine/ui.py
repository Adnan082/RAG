import sys
import os
import streamlit as st

# ── Page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="COSMOS ARCHIVE",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Path setup ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from src.model import PhysicsEmbedder
from src.database import VectorVault

DATA_PATH = os.path.join(BASE_DIR, "data", "arxiv_data.csv")
DB_PATH   = os.path.join(BASE_DIR, "physics_db")

# ══════════════════════════════════════════════════════════════════════════════
#  CUSTOM CSS — Deep Space Scientific Lab Theme
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Base & Background ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #04080f;
    color: #c9d1d9;
    font-family: 'Courier New', monospace;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0e1a 0%, #060912 100%);
    border-right: 1px solid #1a2744;
}
[data-testid="stHeader"] { background: transparent; }

/* ── Header ── */
.cosmos-header {
    text-align: center;
    padding: 2rem 0 1rem 0;
    border-bottom: 1px solid #1a3a5c;
    margin-bottom: 1.5rem;
}
.cosmos-title {
    font-size: 2.6rem;
    font-weight: 900;
    letter-spacing: 0.18em;
    background: linear-gradient(90deg, #4fc3f7, #7c4dff, #00e5ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-transform: uppercase;
}
.cosmos-sub {
    color: #546e7a;
    font-size: 0.95rem;
    letter-spacing: 0.12em;
    margin-top: 0.3rem;
}

/* ── Search Bar ── */
.stTextInput > div > div > input {
    background: #0d1b2a !important;
    border: 1.5px solid #1a3a5c !important;
    border-radius: 8px !important;
    color: #e0f2fe !important;
    font-size: 1.05rem !important;
    padding: 0.75rem 1rem !important;
    caret-color: #4fc3f7;
}
.stTextInput > div > div > input:focus {
    border-color: #4fc3f7 !important;
    box-shadow: 0 0 0 2px rgba(79,195,247,0.18) !important;
}
.stTextInput > label {
    color: #546e7a !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em;
}

/* ── Result Card ── */
.result-card {
    background: linear-gradient(135deg, #0d1b2a 0%, #0a1628 100%);
    border: 1px solid #1a3a5c;
    border-left: 3px solid #4fc3f7;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.result-card:hover { border-left-color: #7c4dff; }
.card-rank {
    color: #546e7a;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}
.card-title {
    color: #e0f2fe;
    font-size: 1.05rem;
    font-weight: 700;
    line-height: 1.4;
    margin-bottom: 0.5rem;
}
.card-meta {
    color: #546e7a;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}
.score-badge {
    display: inline-block;
    background: rgba(79,195,247,0.12);
    border: 1px solid #4fc3f7;
    border-radius: 20px;
    color: #4fc3f7;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.15rem 0.7rem;
    letter-spacing: 0.08em;
}
.score-badge.high   { border-color: #00e676; color: #00e676; background: rgba(0,230,118,0.10); }
.score-badge.medium { border-color: #ffca28; color: #ffca28; background: rgba(255,202,40,0.10); }
.score-badge.low    { border-color: #ef5350; color: #ef5350; background: rgba(239,83,80,0.10); }
.tag-pill {
    display: inline-block;
    background: rgba(124,77,255,0.12);
    border: 1px solid #7c4dff;
    border-radius: 12px;
    color: #b39ddb;
    font-size: 0.7rem;
    padding: 0.1rem 0.55rem;
    margin: 0.1rem 0.15rem 0 0;
}

/* ── Sidebar Elements ── */
.sidebar-section {
    background: #0a1628;
    border: 1px solid #1a2744;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-bottom: 1rem;
}
.sidebar-title {
    color: #4fc3f7;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #1a2744;
    padding-bottom: 0.4rem;
}
.status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.25rem 0;
    font-size: 0.78rem;
}
.status-label { color: #546e7a; }
.status-value { color: #e0f2fe; font-weight: 600; }
.status-dot-green { color: #00e676; }
.status-dot-yellow { color: #ffca28; }

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid #1a3a5c !important;
    border-radius: 6px !important;
    color: #7ec8e3 !important;
    font-size: 0.78rem !important;
    padding: 0.3rem 0.8rem !important;
    letter-spacing: 0.05em;
    transition: all 0.2s;
}
.stButton > button:hover {
    border-color: #4fc3f7 !important;
    color: #e0f2fe !important;
    background: rgba(79,195,247,0.08) !important;
}

/* ── No results ── */
.no-results {
    text-align: center;
    padding: 3rem 1rem;
    color: #546e7a;
    border: 1px dashed #1a3a5c;
    border-radius: 10px;
}
.no-results-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }

/* ── Divider ── */
hr { border-color: #1a2744 !important; }

/* ── Selectbox / Slider ── */
[data-testid="stSlider"] > div { color: #546e7a; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  CACHED RESOURCES
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner="Initialising embedding model...")
def load_embedder():
    return PhysicsEmbedder()

@st.cache_resource(show_spinner="Connecting to vector database...")
def load_vault():
    return VectorVault(path=DB_PATH)


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def score_class(score: float) -> str:
    if score >= 0.75:  return "high"
    if score >= 0.50:  return "medium"
    return "low"

def score_label(score: float) -> str:
    pct = int(score * 100)
    if score >= 0.75:  return f"{pct}% Match"
    if score >= 0.50:  return f"{pct}% Match"
    return f"{pct}% Match"

def arxiv_search_url(title: str) -> str:
    import urllib.parse
    query = urllib.parse.quote_plus(title[:80])
    return f"https://arxiv.org/search/?query={query}&searchtype=all"

def parse_terms(raw: str) -> list:
    """Turn \"['cs.CV', 'cs.LG']\" into a list."""
    try:
        import ast
        return ast.literal_eval(raw)
    except Exception:
        return [t.strip().strip("'\"[]") for t in raw.split(",") if t.strip()]

def do_search(vault, embedder, query: str, n: int = 8):
    q_vec   = embedder.generate_vectors([query])
    results = vault.search_vault(q_vec, n_results=n)
    docs      = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    hits = []
    for doc, meta, dist in zip(docs, metadatas, distances):
        score = max(0.0, min(1.0, 1.0 - dist))   # cosine similarity approx
        hits.append({
            "title"    : meta.get("title", "Untitled"),
            "terms"    : parse_terms(meta.get("terms", "[]")),
            "score"    : score,
            "abstract" : doc,
        })
    return hits


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<p style="color:#4fc3f7;font-size:1.1rem;font-weight:800;'
                'letter-spacing:0.12em;text-transform:uppercase;">COSMOS ARCHIVE</p>',
                unsafe_allow_html=True)
    st.markdown("---")

    # ── System Status ──────────────────────────────────────────────────────
    vault   = load_vault()
    embedder = load_embedder()
    paper_count = vault.collection.count()

    st.markdown('<div class="sidebar-section">'
                '<div class="sidebar-title">System Status</div>'
                f'<div class="status-row">'
                f'  <span class="status-label">Vector DB</span>'
                f'  <span class="status-dot-green">&#9679;</span>'
                f'</div>'
                f'<div class="status-row">'
                f'  <span class="status-label">Embedding Model</span>'
                f'  <span class="status-dot-green">&#9679;</span>'
                f'</div>'
                f'<div class="status-row">'
                f'  <span class="status-label">Papers Indexed</span>'
                f'  <span class="status-value">{paper_count:,}</span>'
                f'</div>'
                f'<div class="status-row">'
                f'  <span class="status-label">Scraper Agent</span>'
                f'  <span class="status-dot-yellow">&#9679; Idle</span>'
                f'</div>'
                '</div>', unsafe_allow_html=True)

    # ── Trending Topics ─────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-title" style="margin-top:1rem;">Trending Topics</div>',
                unsafe_allow_html=True)

    trending = [
        "GWTC-4.0 gravitational wave catalog",
        "JWST Ice Giants atmosphere",
        "Dark Matter Scaffolding large scale structure",
        "Black hole merger ringdown",
        "Neutron star equation of state",
        "Exoplanet atmospheric transmission spectroscopy",
    ]
    for topic in trending:
        if st.button(topic, key=f"trend_{topic}"):
            st.session_state["query_input"] = topic

    st.markdown("---")

    # ── Filters ─────────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-title">Search Settings</div>',
                unsafe_allow_html=True)
    n_results = st.slider("Results to show", min_value=3, max_value=20, value=8, step=1)
    min_score = st.slider("Min similarity score", min_value=0.0, max_value=1.0,
                          value=0.0, step=0.05, format="%.2f")

    st.markdown("---")
    st.markdown('<p style="color:#1a3a5c;font-size:0.68rem;text-align:center;">'
                'COSMOS ARCHIVE v1.0<br>Semantic RAG Engine</p>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN AREA
# ══════════════════════════════════════════════════════════════════════════════

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cosmos-header">
  <div class="cosmos-title">COSMOS ARCHIVE</div>
  <div class="cosmos-sub">AI Research Intelligence &nbsp;|&nbsp;
  Semantic search across 50,000+ ArXiv papers</div>
</div>
""", unsafe_allow_html=True)

# ── Search Bar (form so Enter key works) ───────────────────────────────────
with st.form(key="search_form", border=False):
    query = st.text_input(
        label="NATURAL LANGUAGE QUERY",
        value=st.session_state.get("query_input", ""),
        placeholder='e.g.  "What are the latest findings from GWTC-4.0?"',
        key="search_box",
    )
    search_clicked = st.form_submit_button("Search", type="primary")

# When a trending topic button is clicked it sets query_input; rerun picks it up
if search_clicked and query:
    st.session_state["query_input"] = query
    st.session_state["active_query"] = query
elif not search_clicked and st.session_state.get("query_input", "") and \
        st.session_state.get("query_input") != st.session_state.get("active_query", ""):
    # Trending topic was clicked — auto-search it
    st.session_state["active_query"] = st.session_state["query_input"]

active_query = st.session_state.get("active_query", "")

st.markdown("")   # spacer

# ── Results ────────────────────────────────────────────────────────────────
if active_query:
    with st.spinner("Scanning the archive..."):
        hits = do_search(vault, embedder, active_query, n=n_results)

    # Apply min-score filter
    hits = [h for h in hits if h["score"] >= min_score]

    if not hits:
        st.markdown("""
        <div class="no-results">
          <div class="no-results-icon">&#x26A0;</div>
          <p>No results found above the similarity threshold.<br>
          Try lowering the minimum score or rephrasing your query.</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f'<p style="color:#546e7a;font-size:0.78rem;'
                    f'letter-spacing:0.08em;margin-bottom:1rem;">'
                    f'SHOWING {len(hits)} RESULTS FOR &nbsp;<span style="color:#4fc3f7;">'
                    f'"{active_query}"</span></p>', unsafe_allow_html=True)

        for i, hit in enumerate(hits, 1):
            title   = hit["title"]
            terms   = hit["terms"]
            score   = hit["score"]
            abstract = hit["abstract"]
            sc      = score_class(score)
            sl      = score_label(score)
            url     = arxiv_search_url(title)

            # Build tag pills HTML
            tags_html = "".join(
                f'<span class="tag-pill">{t}</span>' for t in terms[:6]
            )

            # Card HTML
            st.markdown(f"""
            <div class="result-card">
              <div class="card-rank">#{i:02d}</div>
              <div class="card-title">{title}</div>
              <div class="card-meta">
                ArXiv Preprint &nbsp;|&nbsp; {tags_html}
              </div>
              <span class="score-badge {sc}">{sl}</span>
            </div>
            """, unsafe_allow_html=True)

            # Abstract expander + PDF link (native Streamlit widgets)
            with st.expander("Abstract Preview"):
                st.markdown(f'<p style="color:#90a4ae;font-size:0.88rem;'
                            f'line-height:1.7;">{abstract}</p>',
                            unsafe_allow_html=True)
                st.markdown(f'<a href="{url}" target="_blank" style="'
                            f'color:#4fc3f7;font-size:0.8rem;'
                            f'text-decoration:none;border:1px solid #1a3a5c;'
                            f'padding:0.3rem 0.8rem;border-radius:5px;">'
                            f'Search on ArXiv &rarr;</a>',
                            unsafe_allow_html=True)

elif not query:
    st.markdown("""
    <div class="no-results" style="border-style:solid;margin-top:2rem;">
      <div class="no-results-icon">&#x2B50;</div>
      <p style="color:#4fc3f7;">Enter a query above or select a Trending Topic<br>
      to search the archive semantically.</p>
    </div>""", unsafe_allow_html=True)
