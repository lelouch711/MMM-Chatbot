
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

from rag.ingest import load_and_embed_data
from rag.retreiver import get_retriever
from tools.increase_total_spend import increase_total_spend
from tools.reallocate_spend import reallocate_spend

import pandas as pd

def create_agent(data_path):

    docs, vectorstore = load_and_embed_data(data_path)
    retriever = get_retriever(vectorstore)


    df = pd.read_excel(data_path)

    """def increase_tool_func(channel, sub_channel, pct_change):
        changes = {(channel, sub_channel): float(pct_change)}
        df_res = increase_total_spend(df, changes)
        return str(df_res[df_res['Channel'] == channel])"""


    """def reallocate_tool_func(channel, sub_channel, alloc_frac):
        allocations = {(channel, sub_channel): float(alloc_frac)}
        df_res = reallocate_spend(df, allocations)
        return str(df_res[df_res['Channel'] == channel])  # Simplified"""

    def reallocate_tool_func(input_str):
       parts = [x.strip() for x in input_str.split(",")]
       if len(parts) == 2:
          channel, alloc_frac = parts
          sub_channel = None
       elif len(parts) == 3:
          channel, sub_channel, alloc_frac = parts
          sub_channel = sub_channel if sub_channel else None
       else:
          return "Error: Please provide input as 'channel,sub_channel,allocation_fraction' (comma separated). Example: TV,National,0.5 or TV,,0.4"
       try:
           alloc_frac = float(alloc_frac)
       except ValueError:
           return "Error: Could not parse the allocation fraction."
       allocations = {(channel, sub_channel): alloc_frac}
       df_res = reallocate_spend(df, allocations)
       mask = (df_res['Channel'] == channel)
       if sub_channel is not None:
          mask &= (df_res['Sub-Channel'] == sub_channel)
       return str(df_res[mask])

    def increase_tool_func(input_str):
      parts = [x.strip() for x in input_str.split(",")]
      if len(parts) == 2:
          channel, pct_change = parts
          sub_channel = None
      elif len(parts) == 3:
          channel, sub_channel, pct_change = parts
          sub_channel = sub_channel if sub_channel else None
      else:
          return "Error: Please provide input as 'channel,sub_channel,percentage_change' (comma separated). Example: TV,National,10 or TV,,10"
      try:
          pct_change = float(pct_change)
      except ValueError:
          return "Error: Could not parse the percentage change."
      changes = {(channel, sub_channel): pct_change}
      df_res = increase_total_spend(df, changes)

      mask = (df_res['Channel'] == channel)
      if sub_channel is not None:
          mask &= (df_res['Sub-Channel'] == sub_channel)
      return str(df_res[mask])



    increase_tool = Tool(
        name="increase_total_spend",
        func=increase_tool_func,
        description=("Increase total spend for a channel/sub-channel by a percentage. "
                     "Input as a comma-separated string: channel,sub_channel,percentage_change. "
                     "Example: 'TV,National,10' or 'TV,,10'"

        )
    )
    reallocate_tool = Tool(
        name="reallocate_spend",
        func=reallocate_tool_func,
        description=("Reallocate spend to a channel/sub-channel as a fraction of total budget. "
                     "Input as: channel,sub_channel,allocation_fraction. "
                     "Example: 'TV,National,0.5' or 'TV,,0.4'"
                     )
    )


    llm = Ollama(model="mistral", base_url="http://localhost:11434")


    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


    agent = initialize_agent(
        tools=[increase_tool, reallocate_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent, qa_chain,
