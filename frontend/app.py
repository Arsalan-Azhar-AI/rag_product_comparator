import streamlit as st
import requests

st.title("AI RAG Product Assistant")

backend = "http://localhost:8000"

st.header("Upload PDF")
pdf = st.file_uploader("Upload a PDF file")
if pdf and st.button("Upload"):
    res = requests.post(f"{backend}/upload-pdf/", files={"file": pdf})
    st.success(res.json()["message"])

st.header("Scrape Website")
url = st.text_input("Enter product URL")
if st.button("Scrape URL"):
    if url.strip() == "":
        st.warning("Please enter a URL before scraping.")
    else:
        res = requests.post(f"{backend}/scrape-url/", data={"url": url})
        if res.status_code == 200:
            st.success(res.json()["message"])
        else:
            st.error(f"Failed to scrape. Status: {res.status_code}")

st.header("Ask a Question")
query = st.text_input("Your question")
if st.button("Ask"):
    res = requests.post(f"{backend}/ask/", data={"query": query})
    st.write(res.text) 
    st.write(res.json()["answer"])


st.header("Compare Products")
url1 = st.text_input("Product URL 1")
url2 = st.text_input("Product URL 2")
if st.button("Compare"):
    res = requests.post(f"{backend}/compare/", data={"url1": url1, "url2": url2})
    st.write(res.json()["comparison"])



st.header("Compare Products from Single URL")
url_single = st.text_input("Single URL (with 2 products)")
prompt = st.text_input("Comparison Prompt (e.g., 'Compare AirPods Max and AirPods 4')")
if st.button("Compare from Single URL"):
    if url_single and prompt:
        res = requests.post(
            f"{backend}/compare-products-from-url/",
            data={"url": url_single, "prompt": prompt}
        )
        try:
            st.write(res.json()["comparison"])
        except Exception:
            st.error("Error: Could not get LLM comparison.")
    else:
        st.warning("Please enter both URL and comparison prompt.")