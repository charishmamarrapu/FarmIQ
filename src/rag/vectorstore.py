import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

EMBED_MODEL = "all-MiniLM-L6-v2"

# Project root: FarmIQ/
# current file = src/rag/vectorstore.py
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

VECTORSTORE_DIR = os.path.join(PROJECT_ROOT, "vectorstore")


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)


def build_vectorstore(chunks, persist_path=VECTORSTORE_DIR):
    print("⏳ Building vector store... this may take a few minutes")
    embeddings = get_embeddings()

    os.makedirs(persist_path, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_path
    )
    vectorstore.persist()
    print(f"✅ Vector store saved to {persist_path}")
    return vectorstore


def vectorstore_exists(persist_path=VECTORSTORE_DIR):
    if not os.path.exists(persist_path):
        return False

    contents = os.listdir(persist_path)
    return len(contents) > 0


def load_vectorstore(persist_path=VECTORSTORE_DIR):
    embeddings = get_embeddings()
    os.makedirs(persist_path, exist_ok=True)

    return Chroma(
        persist_directory=persist_path,
        embedding_function=embeddings
    )