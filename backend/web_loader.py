from langchain_community.document_loaders import WebBaseLoader

def load_website_content(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    return "\n".join([doc.page_content for doc in docs])
