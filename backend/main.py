from fastapi import FastAPI, UploadFile, Form
import os
from backend import pdf_loader, web_loader, rag_engine, compare
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile):
    file_path = f"data/uploaded/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    text = pdf_loader.load_pdf_text(file_path)
    chunks = rag_engine.split_text(text)
    rag_engine.create_vector_store(chunks)
    return {"message": "PDF uploaded and indexed"}

@app.post("/scrape-url/")
async def scrape_url(url: str = Form(...)):
    text = web_loader.load_website_content(url)
    chunks = rag_engine.split_text(text)
    rag_engine.create_vector_store(chunks)
    return {"message": "Website content scraped and indexed"}

@app.post("/ask/")
async def ask_question(query: str = Form(...)):
    db = rag_engine.load_vector_store()
    answer = rag_engine.answer_question(db, query)
    return {"answer": answer}

@app.post("/compare/")
async def compare_urls(url1: str = Form(...), url2: str = Form(...)):
    text1 = web_loader.load_website_content(url1)
    text2 = web_loader.load_website_content(url2)
    comparison = compare.compare_products(text1, text2)
    return {"comparison": comparison}

@app.post("/compare-products-from-url/")
async def compare_products_from_url(url: str = Form(...), prompt: str = Form(...)):
    from backend.web_loader import load_website_content
    from backend.qa_with_prompt import compare_from_page_with_llm

    text = load_website_content(url)
    answer = compare_from_page_with_llm(text, prompt)
    return {"comparison": answer}
