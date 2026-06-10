from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

EMBED_MODEL = "all-MiniLM-L6-v2"

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def build_vectorstore(chunks, persist_path="vectorstore/"):
    print("⏳ Building vector store... this may take a few minutes")
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_path
    )
    vectorstore.persist()
    print(f"✅ Vector store saved to {persist_path}")
    return vectorstore

def load_vectorstore(persist_path="vectorstore/"):
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=persist_path,
        embedding_function=embeddings
    )