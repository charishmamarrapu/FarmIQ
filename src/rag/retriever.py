from rag.vectorstore import load_vectorstore

# Load the vector database only once
db = load_vectorstore()


def retrieve_context(query, k=8):
    """
    Retrieve the most relevant documents from the vector database.

    Args:
        query (str): User's question.
        k (int): Number of document chunks to retrieve.

    Returns:
        str: Combined context from retrieved documents.
    """

    # Use Max Marginal Relevance to avoid duplicate chunks
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