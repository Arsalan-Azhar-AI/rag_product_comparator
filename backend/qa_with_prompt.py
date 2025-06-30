from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Load API key from .env
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.environ['GROQ_API_KEY']

def compare_from_page_with_llm(web_text, user_prompt):
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are a helpful assistant. Given the following webpage text:

        {context}

        Answer the user's question below:
        {question}

        Provide a clear, side-by-side comparison if multiple products are mentioned.
        """
    )

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile" 
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain.run({"context": web_text, "question": user_prompt})
