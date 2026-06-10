import sys, os
sys.path.append(os.path.dirname(__file__))
from vectorstore import load_vectorstore

def test_retrieval():
    print("Loading vector store...")
    vs = load_vectorstore()

    test_queries = [
        "Best crop to grow in Guntur district Kharif season",
        "Fertilizer recommendation for paddy cultivation",
        "Yellow leaves on tomato plant disease treatment",
        "Current price of paddy in Krishna district mandi",
        "Impact of heavy rainfall on cotton crop",
        "PM-KISAN scheme eligibility for small farmers",
        "Pest control for rice crop in AP",
    ]

    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        results = vs.similarity_search(query, k=2)
        for i, doc in enumerate(results):
            print(f"  Result {i+1}: {doc.page_content[:200]}")
            print(f"  Source: {doc.metadata.get('source', 'N/A')}")

if __name__ == "__main__":
    test_retrieval()