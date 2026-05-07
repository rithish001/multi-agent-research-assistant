from langchain_community.llms import Ollama

llm = Ollama(
    model="qwen2.5:0.5b"
)

def summarizer_agent(text):
    prompt = f"""
    You are a summarizer.
    Convert the following into concise points:

    {text}
    """

    return llm.invoke(prompt)

