import pandas as pd
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS

def load_and_embed_data(csv_path):
    """
    Loads the MMM output CSV, converts each row to a text doc, embeds, and returns docs + vectorstore.
    """
    df = pd.read_excel(csv_path)
    docs = []
    for _, row in df.iterrows():
    
        doc = ", ".join([f"{col}: {row[col]}" for col in df.columns])
        docs.append(doc)

    embedding = OllamaEmbeddings(model="mistral", base_url="http://localhost:11434")
    vectorstore = FAISS.from_texts(docs, embedding)
    return docs, vectorstore
