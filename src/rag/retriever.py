from rag.vectorstore import load_vectorstore, vectorstore_exists
from rag.build_pipeline import build_full_pipeline  


def get_db():
    """
    Load the vector DB if it exists.
    If missing, build it automatically from source documents.
    """
    if vectorstore_exists():
        print("✅ Existing vector store found. Loading it...")
        return load_vectorstore()

    print("⚠️ Vector store not found. Building it now...")
    return build_full_pipeline()


def retrieve_context(query, k=8):
    """
    Retrieve the most relevant documents from the vector database.

    Args:
        query (str): User's question.
        k (int): Number of document chunks to retrieve.

    Returns:
        str: Combined context from retrieved documents.
    """
    db = get_db()

    docs = db.max_marginal_relevance_search(
        query=query,
        k=k,
        fetch_k=20
    )

    if not docs:
        return "No relevant information found."

    context = []

    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "Unknown Source")

        context.append(
            f"""
===== DOCUMENT {i} =====
Source: {source}

{doc.page_content}
"""
        )

    return "\n".join(context)