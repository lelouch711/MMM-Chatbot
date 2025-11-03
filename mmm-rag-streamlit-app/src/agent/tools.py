from agent.agent import create_agent

def get_tools():
    data_path = "data/MMM Dummy Data.xlsx"
    agent, qa_chain = create_agent(data_path)
    return agent, qa_chain

agent, qa_chain = get_tools()