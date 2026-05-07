from langchain_community.llms import Ollama

llm = Ollama(
    model="qwen2.5:0.5b"
)

def writer_agent(text):
    prompt = f"""
    You are a professional writer.

    Create a well-structured report with:
    - Introduction
    - Key Points
    - Conclusion

    Content:
    {text}
    """

    return llm.invoke(prompt)

