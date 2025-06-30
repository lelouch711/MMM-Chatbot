from agent.agent import create_agent

if __name__ == "__main__":
    data_path = "data/MMM Dummy Data.xlsx"
    agent, qa_chain = create_agent(data_path)
    print("MMM Agent Ready. Type your question (type 'exit' to quit):")
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            break

        # Simple logic: Use retrieval QA for data Qs, tools for simulation Qs
        if "increase" in query.lower() or "reallocate" in query.lower():
            result = agent.run(query)
        else:
            result = qa_chain({"query": query})["result"]
        print("\nAgent:", result)
