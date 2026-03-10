import re
import spacy
from neo4j import GraphDatabase
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# -----------------------------
# Load NLP model
# -----------------------------
nlp = spacy.load("en_core_web_sm")


# -----------------------------
# Neo4j connection
# -----------------------------
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "12345678"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


# -----------------------------
# Load FAISS documents
# -----------------------------
INDEX_PATH = "../data/faiss_index"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = FAISS.load_local(
    INDEX_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)

documents = list(vector_store.docstore._dict.values())


# -----------------------------
# Maritime keywords
# -----------------------------
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


# -----------------------------
# Clean entity
# -----------------------------
def clean_entity(text):

    text = text.strip()

    if re.match(r"^[0-9\.\s]+$", text):
        return None

    if len(text) < 3:
        return None

    if len(text) > 50:
        return None

    return text


# -----------------------------
# Extract entities
# -----------------------------
def extract_entities(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        cleaned = clean_entity(ent.text)

        if cleaned:
            entities.append(cleaned)

    text_lower = text.lower()

    for term in MARITIME_TERMS:

        if term.lower() in text_lower:
            entities.append(term)

    return list(set(entities))


# -----------------------------
# Create relation
# -----------------------------
def create_relation(tx, source, target):

    query = """
    MERGE (a:Entity {name:$source})
    MERGE (b:Entity {name:$target})
    MERGE (a)-[:RELATED_TO]->(b)
    """

    tx.run(query, source=source, target=target)


# -----------------------------
# Clear graph
# -----------------------------
def clear_graph():

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


# -----------------------------
# Build graph from documents
# -----------------------------
def build_graph():

    print("Building knowledge graph from documents...")

    with driver.session() as session:

        for doc in documents:

            text = doc.page_content[:2000]

            entities = extract_entities(text)

            if len(entities) < 2:
                continue

            for i in range(len(entities)):
                for j in range(i + 1, len(entities)):

                    session.execute_write(
                        create_relation,
                        entities[i],
                        entities[j]
                    )

    print("Knowledge graph created successfully")


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":

    clear_graph()

    build_graph()