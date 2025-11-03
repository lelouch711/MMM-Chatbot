from agent.agent import create_agent
import streamlit as st

def main():
    st.title("MMM RAG Chatbot")
    st.write("Ask your questions below:")

    data_path = "data/MMM Dummy Data.xlsx"
    agent, qa_chain = create_agent(data_path)

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

if __name__ == "__main__":
    main()