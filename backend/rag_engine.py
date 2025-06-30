from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings

def create_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_vector_store(chunks):
    documents = [Document(page_content=chunk) for chunk in chunks]
    if os.path.exists("vector_store/index.faiss"):
        db = FAISS.load_local("vector_store", embeddings=create_embeddings(),allow_dangerous_deserialization=True)
        db.add_documents(documents)
    else:
        db = FAISS.from_documents(documents, embedding=create_embeddings())
    db.save_local("vector_store")
def load_vector_store():
    embedding = create_embeddings()
    return FAISS.load_local("vector_store", embeddings=embedding,allow_dangerous_deserialization=True)


#spliting the text into chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_text(text)


# now use groq llm 

from langchain_groq import ChatGroq
from langchain.chains.question_answering import load_qa_chain
import os
#loading my api key
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.environ['GROQ_API_KEY']


def get_groq_llm():
    return ChatGroq(
        groq_api_key=groq_api_key, 
        model_name="llama-3.3-70b-versatile"
    )

def answer_question(vector_store, query):
    docs = vector_store.similarity_search(query)
    llm = get_groq_llm()
    chain = load_qa_chain(llm, chain_type="stuff")
    return chain.run(input_documents=docs, question=query)
