import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def trim_query(query: str, max_length: int = 350):
    # Remove extra whitespace
    query = " ".join(query.split())

    # Trim safely
    if len(query) > max_length:
        query = query[:max_length]

    return query

def search_web(query):

    try:
        safe_query = trim_query(query)

        response = client.search(
            query=safe_query,
            search_depth="advanced"
        )

        results = []

        for r in response["results"]:
            results.append(
                f"Title: {r.get('title')}\n"
                f"URL: {r.get('url')}\n"
                f"Content: {r.get('content')}\n"
            )

        return "\n".join(results[:3])

    except Exception as e:
        return f"Search failed: {str(e)}"

