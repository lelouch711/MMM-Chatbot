from agent.tools import create_tools
from qa.qa_chain import create_qa_chain

class MMMAgent:
    def __init__(self, data_path):
        self.tools = create_tools()
        self.qa_chain = create_qa_chain(data_path)

    def run(self, query):
        if "increase" in query.lower() or "reallocate" in query.lower():
            return self._run_tool(query)
        else:
            return self._run_qa_chain(query)

    def _run_tool(self, query):
        # Logic to run the appropriate tool based on the query
        for tool in self.tools:
            if tool.can_handle(query):
                return tool.execute(query)
        return "No suitable tool found for the query."

    def _run_qa_chain(self, query):
        result = self.qa_chain({"query": query})
        return result["result"] if "result" in result else "No answer found."