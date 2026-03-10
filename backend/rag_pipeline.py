import os
import re

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder
from transformers import pipeline

from neo4j import GraphDatabase
import spacy
from spacy.pipeline import EntityRuler


# =========================
# CONFIG
# =========================

INDEX_PATH = "../data/faiss_index"


# =========================
# LAZY MODEL LOADING
# =========================

embedding_model = None
reranker = None
generator = None


def load_models():
    global embedding_model, reranker, generator

    if embedding_model is None:

        print("Loading embedding model...")
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Loading reranker...")
        reranker = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        print("Loading generator...")
        generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_new_tokens=120
        )


# =========================
# GRAPH CONFIG
# =========================

URI = os.getenv("NEO4J_URI", "neo4j://127.0.0.1:7687")
USERNAME = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "12345678")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


# =========================
# NLP MODEL
# =========================

print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")


# Maritime domain entities
MARITIME_TERMS = [
    "SOLAS",
    "IALA",
    "IMO",
    "AtoN",
    "VTS",
    "AIS",
    "IALA VTS",
    "Navigation Aid",
    "Maritime Safety",
    "Ship Safety",
    "Vessel Traffic Service"
]


ruler = nlp.add_pipe("entity_ruler", before="ner")

patterns = []

for term in MARITIME_TERMS:
    patterns.append({
        "label": "MARITIME",
        "pattern": term
    })

ruler.add_patterns(patterns)


# =========================
# GLOBAL OBJECTS
# =========================

vector_store = None
documents = None
bm25 = None


# =========================
# QUERY PREPROCESSING
# =========================

def preprocess_query(query):

    query = query.lower()
    query = re.sub(r"[^\w\s]", "", query)

    return query


# =========================
# ENTITY EXTRACTION
# =========================

def extract_query_entities(query):

    doc = nlp(query)

    entities = [ent.text.strip() for ent in doc.ents]

    words = query.split()

    for w in words:
        if w.isupper() and len(w) > 2:
            entities.append(w)

    return list(set(entities))


# =========================
# GRAPH RETRIEVAL
# =========================

def get_related_entities(entity):

    cypher = """
    MATCH (a:Entity)-[r]->(b)
    WHERE toLower(a.name) CONTAINS toLower($name)
    RETURN b.name AS related
    LIMIT 10
    """

    with driver.session() as session:

        result = session.run(cypher, name=entity)

        return [record["related"] for record in result]


# =========================
# QUERY EXPANSION
# =========================

def expand_query_with_graph(query):

    entities = extract_query_entities(query)

    expanded_terms = []

    for entity in entities:

        related = get_related_entities(entity)

        expanded_terms.extend(related)

    if expanded_terms:

        query = query + " " + " ".join(expanded_terms)

    return query


# =========================
# LOAD DOCUMENTS
# =========================

def load_documents():

    global vector_store, documents, bm25

    load_models()

    print("Loading FAISS index...")

    vector_store = FAISS.load_local(
        INDEX_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    documents = list(vector_store.docstore._dict.values())

    corpus = [doc.page_content for doc in documents]

    tokenized = [doc.split() for doc in corpus]

    bm25 = BM25Okapi(tokenized)

    print("Index loaded. Documents:", len(documents))


# =========================
# HYBRID RETRIEVAL
# =========================

def retrieve(query, top_k=5):

    load_models()

    query = preprocess_query(query)

    query = expand_query_with_graph(query)

    tokenized_query = query.split()

    bm25_scores = bm25.get_scores(tokenized_query)

    bm25_ids = sorted(
        range(len(bm25_scores)),
        key=lambda i: bm25_scores[i],
        reverse=True
    )[:top_k * 3]

    bm25_docs = [documents[i] for i in bm25_ids]

    dense_docs = vector_store.similarity_search(
        query,
        k=top_k * 3
    )

    candidates = bm25_docs + dense_docs

    unique = []
    seen = set()

    for doc in candidates:

        text = doc.page_content

        if text not in seen:

            seen.add(text)
            unique.append(doc)

    pairs = [(query, d.page_content) for d in unique]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(scores, unique),
        key=lambda x: x[0],
        reverse=True
    )

    results = ranked[:top_k]

    contexts = []

    for rank, (score, doc) in enumerate(results):

        contexts.append({
            "rank": rank + 1,
            "source": os.path.basename(doc.metadata.get("source", "")),
            "page": doc.metadata.get("page", ""),
            "score": float(score),
            "text": doc.page_content
        })

    return contexts


# =========================
# ANSWER GENERATION
# =========================

def generate_answer(question, contexts):

    load_models()

    contexts = contexts[:3]

    context_text = "\n\n".join(
        [c["text"][:800] for c in contexts]
    )

    prompt = f"""
You are an expert maritime regulations assistant.

Use the context below to answer the question.

Rules:
- Provide a clear definition
- Use 1–2 sentences
- Do NOT copy the context text
- Summarize the meaning

Context:
{context_text}

Question:
{question}

Answer:
"""

    output = generator(prompt)

    return output[0]["generated_text"]