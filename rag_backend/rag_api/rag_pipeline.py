import os
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import pipeline

# Base project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

VECTOR_PATH = os.path.join(BASE_DIR, "vector_store")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_length=200
)


def create_vector_db(pdf_path):

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    db = FAISS.from_documents(docs, embedding_model)

    db.save_local(VECTOR_PATH)


def load_vector_db():

    db = FAISS.load_local(
        VECTOR_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    return db


def ask_question(query):

    db = load_vector_db()

    docs = db.similarity_search(query, k=4)

    context = " ".join([doc.page_content for doc in docs])

    context = re.sub(r"\s+", " ", context)

    prompt = f"""
    You are an AI assistant that answers questions using the document context.

    Context:
    {context}

    Question:
    {query}

    Answer clearly based only on the document.
    If the answer is not present, say:
    "I could not find the answer in the document."
    """

    result = generator(prompt)

    return result[0]["generated_text"]