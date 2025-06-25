def get_retriever(vectorstore, k=3):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever
