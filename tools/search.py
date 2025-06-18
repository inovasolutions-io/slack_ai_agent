from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import pathlib
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_community.document_loaders.text import TextLoader
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()


def get_vectorstore() -> Chroma:
    """Check if vector store exists and initialize if needed."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore_path = pathlib.Path("./chroma_langchain_db")
    if not vectorstore_path.exists() or not any(vectorstore_path.iterdir()):
        initialize_rag()
    return Chroma(
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db",
    )


def initialize_rag():
    """Initialize the RAG system by creating and populating the vector store."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    documents = []
    docs_dir = "./docs"
    if os.path.exists(docs_dir):
        for filename in os.listdir(docs_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(docs_dir, filename)
                loader = TextLoader(file_path)
                loaded_docs = loader.load()
                texts = text_splitter.split_documents(loaded_docs)
                documents.extend(texts)

    uuids = [str(uuid4()) for _ in range(len(documents))]
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./chroma_langchain_db",
        ids=uuids,
    )
    return vectorstore
