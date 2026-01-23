from mcp_server import load_docs

try:
    docs = load_docs()
    print(f"Successfully loaded {len(docs)} documents")
    for i, doc in enumerate(docs):
        print(f"\nDocument {i+1}:")
        print(f"  Title: {doc.metadata.get('title', 'Unknown')}")
        print(f"  Content length: {len(doc.page_content)} chars")
        print(f"  First 200 chars: {doc.page_content[:200]}")
except Exception as e:
    print(f"Error loading docs: {e}")