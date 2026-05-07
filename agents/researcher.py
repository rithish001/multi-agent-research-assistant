from config.llm_config import get_llm
from tools.search_tool import search_web

llm = get_llm()


def researcher_agent(query):
    search_results = search_web(query)

    prompt = f"""
    You are Research assistant. 
    Use the following web results to answer:{search_results}
    Question: {query}

    Extract useful insights clearly.
    """

    return llm.invoke(prompt)




