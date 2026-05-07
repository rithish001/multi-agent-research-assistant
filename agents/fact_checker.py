from langchain_community.llms import Ollama

llm = Ollama(
    model="qwen2.5:0.5b"
)

def fact_checker_agent(text):
    prompt = f"""
    You are a fact-checker.
    Verify the following content and highlight any incorrect or doubtful claims:

    {text}
    """

    return llm.invoke(prompt)