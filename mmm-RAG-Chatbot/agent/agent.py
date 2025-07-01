
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

from rag.ingest import load_and_embed_data
from rag.retreiver import get_retriever
from tools.increase_total_spend import increase_total_spend
from tools.reallocate_spend import reallocate_spend
from tools.parse_natural_language import parse_natural_language
import pandas as pd
import re

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

    def increase_tool_func(user_query):
    # Clean input, accept e.g. TV,,10 or TV,,10%
      parts = [x.strip().replace("%", "") for x in user_query.split(",")]
      channel = parts[0]
      sub_channel = parts[1] if len(parts) > 1 and parts[1] else None

      try:
          pct_change = float(parts[2])
      except (IndexError, ValueError):
          return "Error: Could not extract a percentage value. Please use the format Channel,Sub-Channel,Percentage"

      changes = {(channel, sub_channel): pct_change}
      summary_df, _ = increase_total_spend(df, changes)   # UNPACK HERE

      if summary_df.empty:
          return "No matching rows found for your input."

    # Pretty output
      output_lines = []
      for _, row in summary_df.iterrows():
          output_lines.append(
              f"--- Simulation Result ---\n"
              f"Channel: {row['Channel']}, Sub-Channel: {row['Sub-Channel'] or 'All'}\n"
              f"Original Spend: {row['Original Spend']:.2f}, New Spend: {row['New Spend']:.2f}\n"
              f"Original Sales: {row['Original Sales']:.2f}, New Sales: {row['New Sales']:.2f}\n"
              f"Original ROI: {row['Original ROI']:.2f}, New ROI: {row['New ROI']:.2f}\n"
              f"Spend Change (%): {row['Spend Change (%)']}\n"
        )
      return "\n".join(output_lines)






    parse_tool = Tool(
        name="parse_natural_language",
        func=parse_natural_language,
        description=(
            "Use this tool to convert conversational user input into the correct argument format for other tools. "
            "For example, if the user says 'Increase TV National by 10%' or 'Allocate 40% to TV', "
            "this tool will output 'TV,National,10' or 'TV,,0.4' respectively."
        )
    )



    increase_tool = Tool(
        name="increase_total_spend",
        func=increase_tool_func,
        description=(
            "Increase total spend for a channel/sub-channel by a percentage. "
                     "Input as a comma-separated string: channel,sub_channel,percentage_change. "
                     "Example: 'TV,National,10' or 'TV,,10'"
                     "Use this tool when the user asks about increasing marketing spend on a channel. "
                     "The user may ask: 'Increase TV spend by 10%' or 'What if we boost Digital by 20%?' "
                     "Extract the channel (e.g., TV), sub-channel (if present), and percentage change from their question. "
                     "Call this tool with: channel,sub_channel,percentage_change (e.g., TV,National,10 or TV,,10)."
            "Return the new ROI and the new Spend if the input from the user is of the form TV,,10"


        )
    )
    reallocate_tool = Tool(
        name="reallocate_spend",
        func=reallocate_tool_func,
        description=("Reallocate spend to a channel/sub-channel as a fraction of total budget. "
                     "Input as: channel,sub_channel,allocation_fraction. "
                     "Example: 'TV,National,0.5' or 'TV,,0.4'"
                     "Use this tool when the user wants to reallocate part of the total marketing budget to a channel or sub-channel."
                     "\nThe user may say things like:"
                     "\n- 'Allocate 40% of budget to TV'"
                     "\n- 'Reallocate 30% of budget to Digital National'"
                     "\n- 'Put 50% into TV National'"
                     "\n\nExtract the channel, sub-channel (if given), and the fraction (e.g. 0.3 for 30%)."
                     "\n\nCall this tool with:"
                     "\n   channel,sub_channel,allocation_fraction"
                     "\nExamples:"
                     "\n   TV,,0.4          # TV channel, 40% of total budget"
                     "\n   Digital,National,0.3   # Digital National, 30% of budget"
                     )
    )
    qa_tool = Tool(
        name="rag_qa",
        func=lambda q: qa_chain({"query": q})["result"],
        description=(
            "Answer questions by retrieving relevant context from the marketing mix model data. "
            "Use this tool when the user asks for facts or analysis based on the uploaded data, such as 'What is the ROI for TV in 2023?' or 'Which channel had the highest spend?'."
        )
    )



    llm = Ollama(model="llama3", base_url="http://localhost:11434")


    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


    agent = initialize_agent(
        tools=[increase_tool, reallocate_tool,parse_tool,qa_tool],
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )

    return agent, qa_chain,
