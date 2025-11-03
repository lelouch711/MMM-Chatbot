from streamlit import st

def chat_ui(agent, qa_chain):
    st.title("MMM RAG Chatbot")
    st.write("Ask your questions below:")

    user_input = st.text_input("You:", "")
    
    if st.button("Send"):
        if user_input.lower() in ["exit", "quit"]:
            st.write("Exiting the chat.")
        else:
            if "increase" in user_input.lower() or "reallocate" in user_input.lower():
                result = agent.run(user_input)
            else:
                result = qa_chain({"query": user_input})["result"]
            st.write("Agent:", result)