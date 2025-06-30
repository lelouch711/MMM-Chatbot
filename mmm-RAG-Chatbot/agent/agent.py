
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

from rag.ingest import load_and_embed_data
from rag.retriever import get_retriever
from tools.simulation_tools import increase_total_spend, reallocate_spend

import pandas as pd

def create_agent(data_path):

    docs, vectorstore = load_and_embed_data(data_path)
    retriever = get_retriever(vectorstore)


    df = pd.read_excel(data_path)

    def increase_tool_func(channel, sub_channel, pct_change):
        changes = {(channel, sub_channel): float(pct_change)}
        df_res = increase_total_spend(df, changes)
        return str(df_res[df_res['Channel'] == channel])


    def reallocate_tool_func(channel, sub_channel, alloc_frac):
        allocations = {(channel, sub_channel): float(alloc_frac)}
        df_res = reallocate_spend(df, allocations)
        return str(df_res[df_res['Channel'] == channel])  # Simplified


    increase_tool = Tool(
        name="increase_total_spend",
        func=increase_tool_func,
        description="Increase total spend for a channel/sub-channel by a percentage. Args: channel, sub_channel, pct_change"
    )
    reallocate_tool = Tool(
        name="reallocate_spend",
        func=reallocate_tool_func,
        description="Reallocate spend across channels/sub-channels as a fraction of the total budget. Args: channel, sub_channel, alloc_frac"
    )


    llm = Ollama(model="mistral", base_url="http://localhost:11434")


    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


    agent = initialize_agent(
        tools=[increase_tool, reallocate_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent, qa_chain
