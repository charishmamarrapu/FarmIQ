import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

EMBED_MODEL = "all-MiniLM-L6-v2"

# FarmIQ project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Absolute vectorstore path
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")


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
    """
    Check whether a usable Chroma vectorstore already exists.
    """
    if not os.path.exists(persist_path):
        return False

    # Chroma usually creates files like chroma.sqlite3 and index folders
    contents = os.listdir(persist_path)
    return len(contents) > 0


def load_vectorstore(persist_path=VECTORSTORE_DIR):
    embeddings = get_embeddings()
    os.makedirs(persist_path, exist_ok=True)

    return Chroma(
        persist_directory=persist_path,
        embedding_function=embeddings
    )