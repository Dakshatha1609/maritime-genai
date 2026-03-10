import time
import spacy

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from neo4j import GraphDatabase

from rag_pipeline import load_documents, retrieve, generate_answer


# =========================
# APP
# =========================

app = FastAPI(title="Maritime GenAI RAG API")


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# NEO4J
# =========================

URI = "bolt://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "12345678"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


# =========================
# NLP MODEL
# =========================

nlp = spacy.load("en_core_web_sm")

MARITIME_TERMS = [
    "SOLAS",
    "IMO",
    "AIS",
    "IALA",
    "VTS",
    "IAMSAR",
    "IMDG",
    "Maritime Safety",
    "Navigation Safety"
]


# =========================
# REQUEST MODEL
# =========================

class Query(BaseModel):
    question: str
    top_k: int = 5


# =========================
# STARTUP
# =========================

@app.on_event("startup")
def startup():

    load_documents()

    print("RAG system ready")


# =========================
# CHAT
# =========================

@app.post("/chat")
def chat(query: Query):

    start = time.time()

    contexts = retrieve(query.question, query.top_k)

    answer = generate_answer(query.question, contexts)

    latency = round((time.time() - start) * 1000, 2)

    return {
        "question": query.question,
        "answer": answer,
        "latency_ms": latency,
        "contexts": contexts
    }


# =========================
# GRAPH QUERY
# =========================

def fetch_graph(entity):

    cypher = """
    MATCH (a:Entity)-[:RELATED_TO]-(b:Entity)
    WHERE toLower(a.name) CONTAINS toLower($entity)
       OR toLower(b.name) CONTAINS toLower($entity)
    RETURN a.name AS source, b.name AS target
    LIMIT 50
    """

    nodes = set()
    links = []

    with driver.session() as session:

        result = session.run(cypher, entity=entity)

        for record in result:

            src = record["source"]
            tgt = record["target"]

            nodes.add(src)
            nodes.add(tgt)

            links.append({
                "source": src,
                "target": tgt
            })

    return {
        "nodes": [{"id": n} for n in nodes],
        "links": links
    }


# =========================
# GRAPH API
# =========================

@app.get("/graph")
def graph(query: str):

    doc = nlp(query)

    entities = [ent.text for ent in doc.ents]

    query_upper = query.upper()

    for term in MARITIME_TERMS:

        if term in query_upper:
            entities.append(term)

    if not entities:
        words = query.replace("?", "").split()
        entities.append(words[-1])

    entity = entities[0]

    return fetch_graph(entity)