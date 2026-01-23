from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import Tool


def load_hr_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory="./vector_db",
        embedding_function=embeddings
    )

    return vectordb.as_retriever(search_kwargs={"k": 4})


def create_hr_rag_tool():
    retriever = load_hr_retriever()

    def search_hr_policy(query: str) -> str:
        docs = retriever.invoke(query)
        if not docs:
            return "No relevant HR policy found."

        return "\n\n".join([doc.page_content for doc in docs])

    return Tool(
        name="hr_policy_search",
        func=search_hr_policy,
        description="Search and retrieve answers from HR policy documents"
    )
