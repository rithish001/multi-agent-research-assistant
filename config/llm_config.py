#Here instead of writing and making calls in every step or node or (researcher, summarizer, fact_checker, writer)
#we are writing all in this config files

from langchain_community.llms import Ollama

def get_llm(model_name: str = "qwen2.5:0.5b", temperature: float=0.7):
    return Ollama(
        model=model_name,
        temperature=temperature
    )



