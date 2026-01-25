from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def load_db_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory="./vector_db",
        embedding_function=embeddings
    )

    return vectordb.as_retriever(search_kwargs={"k": 4})


def search_vector_db(query: str) -> str:
    """Get relevant data for IT and Finance"""
    retriever = load_db_retriever()
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant IT or Finance data found."

    return "\n\n".join([doc.page_content for doc in docs])
