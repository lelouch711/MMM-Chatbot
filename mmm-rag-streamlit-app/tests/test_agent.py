from agent.agent import create_agent
import streamlit as st

# Initialize the agent
data_path = "data/MMM Dummy Data.xlsx"
agent, qa_chain = create_agent(data_path)

# Streamlit UI
st.title("MMM RAG Chatbot")
st.write("Ask your questions below:")

# User input
user_input = st.text_input("You:", "")

if st.button("Submit"):
    if user_input.lower() in ["exit", "quit"]:
        st.write("Exiting the chatbot.")
    else:
        # Simple logic: Use retrieval QA for data Qs, tools for simulation Qs
        if "increase" in user_input.lower() or "reallocate" in user_input.lower():
            result = agent.run(user_input)
        else:
            result = qa_chain({"query": user_input})["result"]
        st.write("Agent:", result)