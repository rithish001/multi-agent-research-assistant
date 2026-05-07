from langgraph.graph import StateGraph

from agents.researcher import researcher_agent
from agents.summarizer import summarizer_agent
from agents.fact_checker import fact_checker_agent
from agents.writer import writer_agent

from memory.vector_store import store_memory, retrieve_memory
from tools.search_tool import search_web   # ✅ NEW

# -------------------------------
# STATE DEFINITION
# -------------------------------
class AgentState(dict):
    """
    Expected keys:
    - query: str
    - research: str
    - summary: str
    - checked: str
    - final: str
    """
    pass

# NODES

def researcher_node(state: AgentState):
    query = state["query"]

    # ✅ Retrieve past memory
    past_memory = retrieve_memory(query)

    # ✅ Web search (REAL TOOL USAGE)
    web_results = search_web(query)

    # ✅ Combine all context
    combined_input = f"""
    You are a research agent.

    User Question:
    {query}

    Relevant Past Memory:
    {past_memory}

    Web Search Results:
    {web_results}

    Task:
    - Extract useful, factual, and relevant information
    - Ignore noise
    - Structure the output clearly
    """

    research_output = researcher_agent(combined_input)

    return {**state, "research": research_output}


def summarizer_node(state: AgentState):
    research = state["research"]

    summary = summarizer_agent(f"""
    Summarize the following research clearly and concisely:

    {research}
    """)

    return {**state, "summary": summary}


def fact_checker_node(state: AgentState):
    summary = state["summary"]
    query = state["query"]

    # ✅ Optional: re-check using web (stronger validation)
    verification_data = search_web(query)

    checked = fact_checker_agent(f"""
    You are a fact-checking agent.

    Summary:
    {summary}

    External Data:
    {verification_data}

    Task:
    - Verify factual correctness
    - Highlight any inconsistencies
    - If unsure, say "uncertain"
    """)

    return {**state, "checked": checked}


def writer_node(state: AgentState):
    checked = state["checked"]
    query = state["query"]

    final_output = writer_agent(f"""
    Generate a well-structured final answer for the user.

    Question:
    {query}

    Verified Content:
    {checked}

    Requirements:
    - Clear explanation
    - Structured format
    - Include key points
    """)

    # ✅ Store memory
    store_memory(query, final_output)

    return {**state, "final": final_output}


# GRAPH BUILDING


graph = StateGraph(AgentState)

graph.add_node("researcher", researcher_node)
graph.add_node("summarizer", summarizer_node)
graph.add_node("fact_checker", fact_checker_node)
graph.add_node("writer", writer_node)

graph.set_entry_point("researcher")

graph.add_edge("researcher", "summarizer")
graph.add_edge("summarizer", "fact_checker")
graph.add_edge("fact_checker", "writer")

# Compile graph
app = graph.compile()
