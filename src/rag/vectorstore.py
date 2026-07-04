import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

EMBED_MODEL = "all-MiniLM-L6-v2"

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "farmiq-index")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")

# Global cache
_embeddings = None
_vectorstore = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        print("🔹 Loading embedding model once...")
        _embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        print("✅ Embedding model loaded")
    return _embeddings


def get_pinecone_client():
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is missing in .env")
    return Pinecone(api_key=PINECONE_API_KEY)


def ensure_index():
    pc = get_pinecone_client()
    existing = pc.list_indexes().names()

    if PINECONE_INDEX_NAME not in existing:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=PINECONE_CLOUD,
                region=PINECONE_REGION
            )
        )
        print(f"✅ Created Pinecone index: {PINECONE_INDEX_NAME}")
    else:
        print(f"✅ Pinecone index already exists: {PINECONE_INDEX_NAME}")


def build_vectorstore(chunks, batch_size=100):
    ensure_index()
    embeddings = get_embeddings()

    total = len(chunks)
    print(f"📦 Uploading {total} chunks to Pinecone in batches of {batch_size}...")

    first_batch = chunks[:batch_size]
    vectorstore = PineconeVectorStore.from_documents(
        documents=first_batch,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME
    )
    print(f"✅ Uploaded batch 1: {len(first_batch)} / {total}")

    for start in range(batch_size, total, batch_size):
        end = min(start + batch_size, total)
        batch = chunks[start:end]
        vectorstore.add_documents(batch)
        print(f"✅ Uploaded batch {start // batch_size + 1}: {end} / {total}")

    print("🎉 All chunks uploaded to Pinecone successfully.")
    return vectorstore


def load_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        ensure_index()
        embeddings = get_embeddings()
        _vectorstore = PineconeVectorStore(
            index_name=PINECONE_INDEX_NAME,
            embedding=embeddings
        )
    return _vectorstore