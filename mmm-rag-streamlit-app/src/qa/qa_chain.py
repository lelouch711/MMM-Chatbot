from agent.agent import create_agent

def load_qa_chain(data_path):
    agent, qa_chain = create_agent(data_path)
    return agent, qa_chain

def get_answer(agent, qa_chain, query):
    if "increase" in query.lower() or "reallocate" in query.lower():
        return agent.run(query)
    else:
        return qa_chain({"query": query})["result"]