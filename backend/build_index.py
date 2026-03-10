import os
import re
from pathlib import Path

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from graph_builder import build_graph_from_chunks


# =========================
# PATHS
# =========================

PDF_PATH = "../data/pdfs"
INDEX_PATH = "../data/faiss_index"


# =========================
# EMBEDDING MODEL
# =========================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================
# TEXT CLEANING
# =========================

def clean_text(text):
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# =========================
# LOAD DOCUMENTS
# =========================

print("Loading PDFs...")

loader = PyPDFDirectoryLoader(PDF_PATH)
docs = loader.load()

print("Total PDF pages:", len(docs))


# =========================
# SPLIT DOCUMENTS
# =========================

print("Splitting documents...")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=100
)

documents = splitter.split_documents(docs)


# =========================
# CLEAN CHUNKS
# =========================

cleaned_docs = []

for doc in documents:

    text = clean_text(doc.page_content)

    if len(text) > 50:
        doc.page_content = text
        cleaned_docs.append(doc)

print("Total chunks:", len(cleaned_docs))


# =========================
# BUILD FAISS INDEX
# =========================

print("Creating embeddings and FAISS index...")

vector_store = FAISS.from_documents(
    cleaned_docs,
    embedding_model
)

Path(INDEX_PATH).mkdir(parents=True, exist_ok=True)

vector_store.save_local(INDEX_PATH)

print("FAISS index built and saved.")


# =========================
# BUILD KNOWLEDGE GRAPH
# =========================

print("Building knowledge graph...")

build_graph_from_chunks(cleaned_docs)

print("Knowledge graph created.")