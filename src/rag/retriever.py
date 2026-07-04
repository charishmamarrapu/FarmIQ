from rag.vectorstore import load_vectorstore

db = None


def get_db():
    global db
    if db is None:
        db = load_vectorstore()
    return db


def retrieve_context(query, k=8):
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