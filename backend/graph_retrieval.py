from neo4j import GraphDatabase
import spacy
import re

# =========================
# LOAD NLP MODEL
# =========================

nlp = spacy.load("en_core_web_sm")

# Maritime domain keywords
MARITIME_TERMS = [
    "SOLAS",
    "IMO",
    "AIS",
    "IALA",
    "VTS",
    "IMDG",
    "IAMSAR",
    "Navigation Safety",
    "Maritime Safety"
]

# =========================
# NEO4J CONNECTION
# =========================

URI = "bolt://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "12345678"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


# =========================
# QUERY ENTITY EXTRACTION
# =========================

def extract_query_entities(query):

    doc = nlp(query)

    entities = [ent.text.strip() for ent in doc.ents]

    # also detect uppercase maritime terms
    words = query.split()

    for w in words:

        if w.upper() in MARITIME_TERMS:
            entities.append(w.upper())

    return list(set(entities))


# =========================
# GRAPH RETRIEVAL
# =========================

def get_related_entities(entity):

    cypher = """
    MATCH (a:Entity)-[:RELATED_TO]-(b:Entity)
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

def expand_query(query):

    entities = extract_query_entities(query)

    expanded = []

    for entity in entities:

        related = get_related_entities(entity)

        expanded.extend(related)

    if expanded:
        query = query + " " + " ".join(expanded)

    return query